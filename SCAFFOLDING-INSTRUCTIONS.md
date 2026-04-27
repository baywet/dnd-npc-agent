# Scaffolding Instructions

## Prerequisites

Before getting started, ensure you have the following installed:

- **Azure Developer CLI (azd)** - Required for project scaffolding and deployment
- **Agent Extension** - Install the Azure AI Agents extension for azd:
  ```bash
  azd extension install azure.ai.agents
  ```

## Creating a New Project

### Step 1: Initialize the Agent Project

To create a new v2 hosted agent using Microsoft Agent Framework in .NET, run the following command:

```bash
azd ai agent init -m https://github.com/microsoft/hosted-agents-vnext-private-preview/blob/main/samples/dotnet/hosted-agents/agent-framework/local-tools/agent.manifest.yaml
```

The `-m` parameter specifies the manifest file that defines the agent configuration and scaffolding template for the hosted agent framework.

This command will:
- Create the project structure for a .NET-based hosted agent
- Set up the necessary configurations
- Initialize the local development environment
