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

var judgeDeploymentName = Environment.GetEnvironmentVariable("AZURE_AI_MODEL_DEPLOYMENT_NAME")
    ?? throw new InvalidOperationException("AZURE_AI_MODEL_DEPLOYMENT_NAME not set");

var baseModelName = Environment.GetEnvironmentVariable("BASE_MODEL_DEPLOYMENT_NAME")
    ?? throw new InvalidOperationException("BASE_MODEL_DEPLOYMENT_NAME not set");

var fineTunedModelName = Environment.GetEnvironmentVariable("FINE_TUNED_MODEL_DEPLOYMENT_NAME")
    ?? throw new InvalidOperationException("FINE_TUNED_MODEL_DEPLOYMENT_NAME not set");

var datasetPath = Path.Combine(AppContext.BaseDirectory, "datasets", "dnd_npc_data_test.jsonl");

Console.WriteLine("=== D&D NPC Model Evaluation ===\n");
Console.WriteLine($"Project: {projectEndpoint}");
Console.WriteLine($"Judge deployment (for evaluators): {judgeDeploymentName}");
Console.WriteLine($"Base model: {baseModelName}");
Console.WriteLine($"Fine-tuned model: {fineTunedModelName}");
Console.WriteLine($"Dataset: {datasetPath}\n");

var credential = new DefaultAzureCredential();
var projectClient = new AIProjectClient(projectEndpoint, credential);

var oaiClient = projectClient.ProjectOpenAIClient;
var evaluationClient = oaiClient.GetEvaluationClient();

Console.WriteLine("Loading dataset...");
var testData = LoadDataset(datasetPath);
Console.WriteLine($"Loaded {testData.Count} test cases\n");

// Compare each model's response against the preferred ground-truth answer using
// LLM-based semantic similarity, plus task adherence on the user's query.
object[] testingCriteria =
[
    new
    {
        type = "azure_ai_evaluator",
        name = "similarity",
        evaluator_name = "builtin.similarity",
        initialization_parameters = new { deployment_name = judgeDeploymentName },
        data_mapping = new
        {
            query = "{{item.query}}",
            response = "{{sample.output_text}}",
            ground_truth = "{{item.ground_truth}}"
        }
    },
    new
    {
        type = "azure_ai_evaluator",
        name = "task_adherence",
        evaluator_name = "builtin.task_adherence",
        initialization_parameters = new { deployment_name = judgeDeploymentName },
        data_mapping = new { query = "{{item.query}}", response = "{{sample.output_text}}" }
    }
];

object dataSourceConfig = new
{
    type = "custom",
    item_schema = new
    {
        type = "object",
        properties = new
        {
            query = new { type = "string" },
            ground_truth = new { type = "string" }
        },
        required = new[] { "query", "ground_truth" }
    },
    include_sample_schema = true
};

const string evaluationDisplayName = "D&D NPC Model Evaluation";
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

var runDataItems = testData
    .Select(tc => new { item = new { query = tc.Query, ground_truth = tc.GroundTruth } })
    .ToArray();

await CreateAndPollRunAsync(evaluationClient, evaluationId, "base", baseModelName, runDataItems);
await CreateAndPollRunAsync(evaluationClient, evaluationId, "fine-tuned", fineTunedModelName, runDataItems);

Console.WriteLine("\n✓ All model evaluation runs finished.");

static async Task CreateAndPollRunAsync(
    EvaluationClient client,
    string evaluationId,
    string label,
    string modelName,
    object runDataItems)
{
    Console.WriteLine($"Creating evaluation run for '{label}' model ({modelName})...");

    var runCreatePayload = BinaryData.FromObjectAsJson(new
    {
        name = $"model-eval-{label}-{DateTime.UtcNow:yyyyMMddHHmmss}",
        data_source = new
        {
            type = "completions",
            model = modelName,
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
                        role = "system",
                        content = new { type = "input_text", text = "You are a helpful assistant." }
                    },
                    new
                    {
                        type = "message",
                        role = "user",
                        content = new { type = "input_text", text = "{{item.query}}" }
                    }
                }
            }
        }
    });

    using var runCreateContent = BinaryContent.Create(runCreatePayload);
    ClientResult runResult = await client.CreateEvaluationRunAsync(evaluationId, runCreateContent);

    var runJson = JsonDocument.Parse(runResult.GetRawResponse().Content.ToString());
    var runId = runJson.RootElement.GetProperty("id").GetString()!;
    var runStatus = runJson.RootElement.GetProperty("status").GetString();
    var reportUrl = runJson.RootElement.TryGetProperty("report_url", out var ru) ? ru.GetString() : null;

    Console.WriteLine($"✓ Run created for '{label}' (id: {runId}, status: {runStatus})");
    if (!string.IsNullOrEmpty(reportUrl))
    {
        Console.WriteLine($"  Report: {reportUrl}");
    }

    var terminalStatuses = new[] { "completed", "failed", "canceled" };
    while (!terminalStatuses.Contains(runStatus, StringComparer.OrdinalIgnoreCase))
    {
        await Task.Delay(TimeSpan.FromSeconds(15));
        ClientResult statusResult = await client.GetEvaluationRunAsync(evaluationId, runId, options: null);
        var statusJson = JsonDocument.Parse(statusResult.GetRawResponse().Content.ToString());
        runStatus = statusJson.RootElement.GetProperty("status").GetString();
        Console.WriteLine($"  [{label}] Status: {runStatus} (at {DateTime.Now:HH:mm:ss})");
    }

    Console.WriteLine($"✓ Run for '{label}' finished with status: {runStatus}\n");
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

        using var doc = JsonDocument.Parse(line);
        var root = doc.RootElement;

        // Extract the last user message from input.messages as the query.
        string query = "";
        if (root.TryGetProperty("input", out var input)
            && input.TryGetProperty("messages", out var messages))
        {
            foreach (var msg in messages.EnumerateArray())
            {
                if (msg.TryGetProperty("role", out var role)
                    && role.GetString() == "user"
                    && msg.TryGetProperty("content", out var content))
                {
                    query = content.GetString() ?? "";
                }
            }
        }

        // Use the first preferred_output assistant message as ground truth.
        string groundTruth = "";
        if (root.TryGetProperty("preferred_output", out var preferred)
            && preferred.ValueKind == JsonValueKind.Array
            && preferred.GetArrayLength() > 0)
        {
            var first = preferred[0];
            if (first.TryGetProperty("content", out var gt))
            {
                groundTruth = gt.GetString() ?? "";
            }
        }

        if (!string.IsNullOrEmpty(query) && !string.IsNullOrEmpty(groundTruth))
        {
            testCases.Add(new TestCase { Query = query, GroundTruth = groundTruth });
        }
    }

    return testCases;
}

record TestCase
{
    public string Query { get; set; } = "";
    public string GroundTruth { get; set; } = "";
}
