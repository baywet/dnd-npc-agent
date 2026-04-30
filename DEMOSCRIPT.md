# Demo Script

## Prerequisites

Before running the demo, ensure you have the following installed:

- **.NET SDK 10** - Required for building and running the agent
- **Visual Studio Code** - Recommended code editor
- **Azure Developer CLI (azd)** - Required for deployment and management
- **azd AI Agent Extension** - Install with `azd extension install azure.ai.agents`
- **Azure CLI (az)** - Required so `DefaultAzureCredential` can authenticate the local programs (agent host, evals, fine-tuning) against the backend APIs
- **Windows Terminal** - Recommended terminal application
- **PowerShell 7+** - Required for running scripts

### Install with winget

Run the following from an elevated PowerShell session to install all prerequisites:

```powershell
sudo winget install --id Microsoft.PowerShell
sudo winget install --id Microsoft.VisualStudioCode
sudo winget install --id Microsoft.Azd
sudo winget install --id Microsoft.AzureCli
sudo winget install --id Microsoft.WindowsTerminal
sudo winget install --id Microsoft.DotNet.SDK.10

azd extension install azure.ai.agents
```

> [!WARNING]
> **Refresh fine-tuning and evaluation artifacts at most one week before the session.**
> Microsoft Foundry does not document a fixed retention for fine-tuning jobs, custom models, uploaded training/validation files, or evaluation runs — they generally persist until you delete them. However, **fine-tuned model deployments are automatically deleted after 15 consecutive days of inactivity** (no chat/response API calls), and individual artifacts can still be cleaned up by service-side maintenance or by other people sharing the project.
> To avoid an embarrassing "the deployment is gone" or "the eval results are missing" moment on stage, **re-run all fine-tuning and evaluation jobs no more than one week before the actual session** so you walk in with fresh, guaranteed-present results.

## Creating the Demonstration Data

> [!IMPORTANT]
> Plan ahead — the full sequence takes **~4 hours end to end** (mostly fine-tuning). The two evaluation runs can be executed in parallel from separate terminals to save time.

1. **Provision Foundry & deploy the faulty agent** — checkout the buggy branch and deploy if no environment exists yet:
   ```bash
   git checkout bug/missing-character-sheet-instructions
   azd up
   ```
2. **Run the agent evaluation (faulty version)** — F5 the `agent-evals` project in VS Code, or:
   ```bash
   dotnet run --project src/agent-evals
   ```
3. **Deploy the fixed agent** — switch back and redeploy:
   ```bash
   git checkout main
   azd deploy
   ```
4. **Run the agent evaluation (fixed version)** — same as step 2 (`dotnet run --project src/agent-evals`).
5. **Run the model fine-tuning** — F5 the `model-finetuning` project, or:
   ```bash
   dotnet run --project src/model-finetuning
   ```
6. **Run the model evaluation** — F5 the `model-eval` project, or:
   ```bash
   dotnet run --project src/model-eval
   ```

> [!TIP]
> Steps 4 and 5 (or 5 and 6) can run concurrently in separate terminals.

## Getting Ready

Before starting the demo, prepare your environment:

1. **Sign in to Azure** - Ensure both `azd` and the Azure CLI are signed in to your corporate identity (the Azure CLI sign-in is what `DefaultAzureCredential` picks up at runtime to call the backend APIs):
   ```bash
   azd auth login
   az login
   ```

2. **Open Terminal** - Open Windows Terminal and navigate to this repository directory

3. **Open Browser Session** - Open the Azure AI Foundry playground in your browser:
   ```
   https://ai.azure.com/nextgen/r/5y5SVPJlTpWb0p7o5zKQUQ,rg-ai-project-dnd-npc-agent-john-cc-dev,,ai-account-3phirl5w4q3ks,ai-project-ai-project-dnd-npc-agent-john-cc-dev/build/agents/local-tools/build?version=3
   ```

   This URL points to:
   - **Resource Group**: rg-ai-project-dnd-npc-agent-john-cc-dev
   - **AI Account**: ai-account-3phirl5w4q3ks
   - **AI Project**: ai-project-dnd-npc-agent-john-cc-dev
   - **Agent**: local-tools (version 3)

4. **Test Agent Responsiveness** - In the playground, send a test message to the agent to verify it's responsive

5. **Redeploy if Needed** - If the agent is not responding, redeploy it using:
   ```bash
   azd up
   ```
   Follow the prompts to select your subscription and resource group. Wait for the deployment to complete before proceeding with the demo.

## Generating a Synthetic Dataset

This demo shows how to create and evaluate a synthetic dataset for the D&D NPC Agent.

### Steps to Generate Synthetic Dataset

1. Open the **Playground**
2. Click **Evaluation** in the navigation
3. Click **Create New Evaluation**
4. Select **Target Agent**
5. Click **Generate Synthetic Dataset**

### Synthetic Dataset Prompt

Use the following prompt when generating the synthetic dataset:

```
This agent will role play non playable characters in dungeons and dragons sessions.

We need to ensure the agent is always asking for a character sheet from Dungeons and Dragons at the beginning of every session. If the user has not provided a character sheet, we need to remind them to do so before answering other character questions.
```

This prompt ensures the evaluation dataset tests the agent's ability to:
- Request character sheets at the start of interactions
- Enforce the requirement for character sheet information before proceeding
- Remind users to provide their character sheet if it's missing
