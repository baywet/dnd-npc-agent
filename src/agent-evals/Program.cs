using Azure.AI.Projects;
using Azure.Identity;
using DotNetEnv;
using OpenAI.Evals;
#pragma warning disable OPENAI001
using System.ClientModel;
using System.ClientModel.Primitives;
using System.Text.Json;

// Load environment variables from .env file
Env.TraversePath().Load();

var projectEndpoint = new Uri(Environment.GetEnvironmentVariable("FOUNDRY_PROJECT_ENDPOINT")
    ?? throw new InvalidOperationException("FOUNDRY_PROJECT_ENDPOINT environment variable is not set."));

var deploymentName = Environment.GetEnvironmentVariable("AZURE_AI_MODEL_DEPLOYMENT_NAME")
    ?? throw new InvalidOperationException("AZURE_AI_MODEL_DEPLOYMENT_NAME not set");

var agentName = Environment.GetEnvironmentVariable("AGENT_LOCAL_TOOLS_NAME")
    ?? throw new InvalidOperationException("AGENT_LOCAL_TOOLS_NAME not set");

var agentVersion = Environment.GetEnvironmentVariable("AGENT_LOCAL_TOOLS_VERSION");

var datasetPath = Path.Combine(AppContext.BaseDirectory, "datasets", "character_sheet_requirement.jsonl");

Console.WriteLine("=== D&D NPC Agent Evaluation ===\n");
Console.WriteLine($"Project: {projectEndpoint}");
Console.WriteLine($"Deployment (for evaluators): {deploymentName}");
Console.WriteLine($"Agent: {agentName}{(string.IsNullOrEmpty(agentVersion) ? "" : $" (version {agentVersion})")}");
Console.WriteLine($"Dataset: {datasetPath}\n");

// Initialize Foundry client
var credential = new DefaultAzureCredential();
var projectClient = new AIProjectClient(projectEndpoint, credential);

// Get OpenAI evaluation client through ProjectOpenAIClient
var oaiClient = projectClient.ProjectOpenAIClient;
var evaluationClient = oaiClient.GetEvaluationClient();

// Load dataset
Console.WriteLine("Loading dataset...");
var testData = LoadDataset(datasetPath);
Console.WriteLine($"Loaded {testData.Count} test cases\n");

// Define testing criteria for task completion and task adherence
object[] testingCriteria =
[
    new
    {
        type = "azure_ai_evaluator",
        name = "task_completion",
        evaluator_name = "builtin.task_completion",
        initialization_parameters = new { deployment_name = deploymentName },
        data_mapping = new { query = "{{item.query}}", response = "{{sample.output_text}}" }
    },
    new
    {
        type = "azure_ai_evaluator",
        name = "task_adherence",
        evaluator_name = "builtin.task_adherence",
        initialization_parameters = new { deployment_name = deploymentName },
        data_mapping = new { query = "{{item.query}}", response = "{{sample.output_text}}" }
    }
];

// Define data source config
object dataSourceConfig = new
{
    type = "custom",
    item_schema = new
    {
        type = "object",
        properties = new
        {
            query = new { type = "string" }
        },
        required = new[] { "query" }
    },
    include_sample_schema = true
};

// Step 1: Find an existing evaluation by name, or create a new one
const string evaluationDisplayName = "Character Sheet Requirement Evaluation";
Console.WriteLine($"Looking up existing evaluation '{evaluationDisplayName}'...");

var evaluationId = await FindEvaluationIdByNameAsync(evaluationClient, evaluationDisplayName);

if (evaluationId is not null)
{
    Console.WriteLine($"✓ Reusing existing evaluation (id: {evaluationId})\n");
}
else
{
    Console.WriteLine("No existing evaluation found, creating a new one...");
    var evaluationCreatePayload = BinaryData.FromObjectAsJson(new
    {
        name = evaluationDisplayName,
        data_source_config = dataSourceConfig,
        testing_criteria = testingCriteria
    });

    using var evaluationCreateContent = BinaryContent.Create(evaluationCreatePayload);
    ClientResult evaluationResult = await evaluationClient.CreateEvaluationAsync(evaluationCreateContent);

    var evaluationJson = JsonDocument.Parse(evaluationResult.GetRawResponse().Content.ToString());
    evaluationId = evaluationJson.RootElement.GetProperty("id").GetString()!;
    Console.WriteLine($"✓ Evaluation created (id: {evaluationId})\n");
}

// Step 2: Create the evaluation run with the dataset
Console.WriteLine($"Creating evaluation run with {testData.Count} test cases...");

var runDataItems = testData
    .Select(tc => new { item = new { query = tc.Query } })
    .ToArray();

var runCreatePayload = BinaryData.FromObjectAsJson(new
{
    name = $"character-sheet-run-{DateTime.UtcNow:yyyyMMddHHmmss}",
    data_source = new
    {
        type = "azure_ai_target_completions",
        source = new
        {
            type = "file_content",
            content = runDataItems
        },
        input_messages = new
        {
            type = "template",
            template = new object[]
            {
                new
                {
                    type = "message",
                    role = "user",
                    content = new { type = "input_text", text = "{{item.query}}" }
                }
            }
        },
        target = string.IsNullOrEmpty(agentVersion)
            ? (object)new { type = "azure_ai_agent", name = agentName }
            : new { type = "azure_ai_agent", name = agentName, version = agentVersion }
    }
});

using var runCreateContent = BinaryContent.Create(runCreatePayload);
ClientResult runResult = await evaluationClient.CreateEvaluationRunAsync(evaluationId, runCreateContent);

var runJson = JsonDocument.Parse(runResult.GetRawResponse().Content.ToString());
var runId = runJson.RootElement.GetProperty("id").GetString()!;
var runStatus = runJson.RootElement.GetProperty("status").GetString();
var reportUrl = runJson.RootElement.TryGetProperty("report_url", out var ru) ? ru.GetString() : null;

Console.WriteLine($"✓ Evaluation run created (id: {runId}, status: {runStatus})");
if (!string.IsNullOrEmpty(reportUrl))
{
    Console.WriteLine($"  Report: {reportUrl}");
}
Console.WriteLine();

// Step 3: Poll for completion
Console.WriteLine("Polling for completion...");
var terminalStatuses = new[] { "completed", "failed", "canceled" };
while (!terminalStatuses.Contains(runStatus, StringComparer.OrdinalIgnoreCase))
{
    await Task.Delay(TimeSpan.FromSeconds(15));
    ClientResult statusResult = await evaluationClient.GetEvaluationRunAsync(evaluationId, runId, options: null);
    var statusJson = JsonDocument.Parse(statusResult.GetRawResponse().Content.ToString());
    runStatus = statusJson.RootElement.GetProperty("status").GetString();
    Console.WriteLine($"  Status: {runStatus} (at {DateTime.Now:HH:mm:ss})");
}

Console.WriteLine($"\n✓ Evaluation finished with status: {runStatus}");
if (!string.IsNullOrEmpty(reportUrl))
{
    Console.WriteLine($"  View results: {reportUrl}");
}

static async Task<string?> FindEvaluationIdByNameAsync(EvaluationClient client, string name)
{
    string? after = null;
    while (true)
    {
        ClientResult page = await client.GetEvaluationsAsync(
            limit: 100,
            orderBy: "created_at",
            order: "asc",
            after: after,
            options: null);

        var pageJson = JsonDocument.Parse(page.GetRawResponse().Content.ToString());
        var root = pageJson.RootElement;

        if (root.TryGetProperty("data", out var data))
        {
            foreach (var item in data.EnumerateArray())
            {
                if (item.TryGetProperty("name", out var nameProp)
                    && string.Equals(nameProp.GetString(), name, StringComparison.Ordinal))
                {
                    return item.GetProperty("id").GetString();
                }
            }
        }

        var hasMore = root.TryGetProperty("has_more", out var hm) && hm.GetBoolean();
        if (!hasMore) return null;

        after = root.TryGetProperty("last_id", out var lastId) ? lastId.GetString() : null;
        if (string.IsNullOrEmpty(after)) return null;
    }
}

static List<TestCase> LoadDataset(string path)
{
    var testCases = new List<TestCase>();

    if (!File.Exists(path))
    {
        throw new FileNotFoundException($"Dataset not found: {path}");
    }

    foreach (var line in File.ReadLines(path))
    {
        if (string.IsNullOrWhiteSpace(line))
            continue;

        var doc = JsonDocument.Parse(line);
        var query = doc.RootElement.GetProperty("query").GetString() ?? "";
        var response = doc.RootElement.GetProperty("response").GetString() ?? "";
        testCases.Add(new TestCase { Query = query, Response = response });
    }

    return testCases;
}

record TestCase
{
    public string Query { get; set; } = "";
    public string Response { get; set; } = "";
}
