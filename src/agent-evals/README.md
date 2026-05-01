# D&D NPC Agent Evaluations

Console application for running programmatic evaluations on the D&D NPC Agent using the Azure AI Foundry SDK.

## Setup

### Prerequisites

- .NET 10.0 SDK
- Azure subscription with AI Foundry project
- Agent deployed in AI Foundry

### Environment Variables

Create a `.env` file in the project root or set these environment variables:

```bash
AZURE_FOUNDRY_PROJECT_CONNECTION_STRING=<your-connection-string>
DEPLOYMENT_NAME=<your-deployment-name>
DATASET_PATH=../../agent-eval-datasets/character_sheet_requirement.jsonl
```

**Getting your connection string:**

1. Go to Azure AI Foundry portal
2. Navigate to your project
3. Find the project connection string in Settings/Project Info

**Deployment name:**
The name of your deployed model (e.g., `gpt-4`, `gpt-4-turbo`)

## Running Evaluations

### Basic Run

```bash
dotnet run --project src/agent-evals
```

### With Environment Variables

```bash
export AZURE_FOUNDRY_PROJECT_CONNECTION_STRING="<connection-string>"
export DEPLOYMENT_NAME="gpt-4"
dotnet run --project src/agent-evals
```

### From Solution

```bash
dotnet run --project src/agent-evals/agent-evals.csproj
```

## How It Works

1. **Loads Dataset**: Reads the JSONL evaluation dataset (90 test cases for character sheet requirement)
2. **Initializes Client**: Connects to Azure AI Foundry using the provided credentials
3. **Configures Evaluators**: Sets up two evaluators:
   - **Task Completion**: Did the agent complete the task?
   - **Task Adherence**: Did the agent follow instructions?
4. **Prepares Data**: Formats evaluation data with proper mappings
5. **Outputs Configuration**: Shows the evaluation configuration ready to run

## Dataset Format

The evaluation dataset (`character_sheet_requirement.jsonl`) contains one JSON object per line:

```json
{"query": "...", "response": "..."}
```

- **query**: User input/question to the agent
- **response**: Expected agent behavior or response

## Evaluation Configuration

The app generates configuration for Azure AI Foundry evaluators with:

```json
{
  "type": "azure_ai_evaluator",
  "name": "task_completion",
  "evaluator_name": "builtin.task_completion",
  "initialization_parameters": {
    "deployment_name": "gpt-4"
  },
  "data_mapping": {
    "query": "{{item.query}}",
    "response": "{{item.response}}"
  }
}
```

## Troubleshooting

### Environment variables not loading

- Ensure `.env` file is in the project root (not in src/agent-evals)
- Use absolute paths or run from the project root

### Connection string errors

- Verify your Azure Foundry project exists
- Check that your credentials have access to the project
- Ensure you're authenticated with `az login`

### Dataset not found

- Check that the JSONL file exists at the specified path
- Use absolute paths if relative paths don't work
- Verify the file has proper JSONL format (one JSON object per line)

## Next Steps

1. Configure the evaluation in Azure AI Foundry UI
2. Target your deployed agent for evaluation
3. Run the evaluation and monitor results in the portal
4. Review Pass/Fail metrics for each test case

## References

- [Azure AI Foundry Agent Evaluators](https://learn.microsoft.com/en-us/azure/foundry/concepts/evaluation-evaluators/agent-evaluators)
- [Azure AI Projects SDK](https://learn.microsoft.com/en-us/python/api/azure-ai-projects/)
