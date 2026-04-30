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

## Demos

### Showcase the agent (faulty vs. fixed)

1. Checkout the buggy branch: `git checkout bug/missing-character-sheet-instructions`.
1. Open `src/local-tools` in VS Code and press **F5** to run the agent locally.
1. Explain at a high level: a D&D character sheet is the structured stat block (HP, AC, attacks, traits) that defines what an NPC can do — without it the agent has no source of truth.
1. From a separate terminal, invoke the agent:
   ```powershell
   azd ai agent invoke --local "You're being attacked, what's your armor class? and do you run or take the blow?"
   ```
1. Show that the agent **makes something up** — it has no sheet and no instruction to ask for one.
1. Stop the debugger, `git checkout main`, and **F5** again.
1. Re-run the same `azd ai agent invoke --local "..."` command — the agent now refuses and asks for a character sheet.
1. Feed it a real sheet and re-ask:
   ```powershell
   $sheet = Get-Content -Raw character-sheets/Goblin_Skirmisher_CR025.md
   azd ai agent invoke --local "$sheet`n`nYou're being attacked, what's your armor class? and do you run or take the blow?"
   ```
1. Show that the answer is now grounded in the stat block (correct AC, in-character decision).
1. Conclude: this is exactly the kind of regression we want to catch automatically — next we'll build evaluations to guarantee the agent always asks for the character sheet first.

### Programmatic agent evaluations

1. Open `src/agent-evals/Program.cs`.
1. Open `agent-eval-datasets/character_sheet_requirement.jsonl` to show the dataset, and explain **JSONL**: one self-contained JSON object per line, easy to stream/append, the de-facto format for AI datasets — we'll see it again for fine-tuning and model evaluation.
1. Walk through the key blocks:
   - `AIProjectClient` + `GetEvaluationClient()` — same auth story (`DefaultAzureCredential`).
   - `testingCriteria` — `task_completion` and `task_adherence` Azure AI evaluators wired to the judge deployment.
   - `dataSourceConfig` + `runDataItems` — JSONL dataset reshaped into `{{item.query}}`.
   - The `azure_ai_target_completions` data source pointing at our deployed agent (`name = AGENT_LOCAL_TOOLS_NAME`).
1. Stress that this can also be done from the portal, but doing it in code gives us **repeatability** and lets us run the same evaluation from a **CI/CD pipeline** on every change.
1. Open the evaluation in the portal: [Character Sheet Requirement Evaluation](https://ai.azure.com/nextgen/r/5y5SVPJlTpWb0p7o5zKQUQ,rg-ai-project-dnd-npc-agent-john-cc-dev,,ai-account-3phirl5w4q3ks,ai-project-ai-project-dnd-npc-agent-john-cc-dev/build/evaluations/eval_ddb13660bf554a6495cf2928988717da).
1. Explain the concepts on screen:
   - **Evaluation** — the named container holding all runs that share the same dataset schema and criteria.
   - **Run** — one execution against a target (agent version, model, etc.).
   - **Evaluators** — the metrics computing pass/fail per row (`task_completion`, `task_adherence`).
   - **Metrics** — aggregate scores over the dataset.
1. Compare the two runs (faulty branch vs. `main`): point out the noticeably better **task adherence** score on the fixed version — the agent now sticks to the instruction to request a character sheet first.

