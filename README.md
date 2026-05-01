# D&D NPC Agent

A .NET 10 demo that brings Dungeons & Dragons non‑player characters (NPCs) to life as an AI agent hosted on **Microsoft Foundry** with the **Microsoft Agent Framework**. Ask the agent to roll dice, role‑play a kobold trapmaster, or generate a stat block — and watch a full agent lifecycle play out: local development, hosted deployment, programmatic evaluation, and model fine‑tuning.

## What this repository demonstrates

This repo is a hands‑on reference for building, shipping, and improving a code‑based hosted agent on Microsoft Foundry. It walks through the end‑to‑end story:

- **Authoring an agent in C#** — `src/local-tools/` registers an `AIAgent` via `AgentHost.CreateBuilder` and exposes local function tools (e.g. `ThrowDie`) that the LLM can invoke. Highlights why code‑based agents with real tool calls beat prompt‑only agents.
- **Deploying to Microsoft Foundry** — `azure.yaml` + Bicep under `infra/` provision the project and deploy the agent through `azd up` using the `azure.ai.agent` host with remote container build.
- **Evaluating agent quality** — `src/agent-evals/` runs Microsoft Foundry evaluators (task completion, task adherence) against JSONL datasets in `agent-eval-datasets/` for repeatable regression testing.
- **Fine‑tuning a custom model** — `src/model-finetuning/` uploads training files and drives fine‑tuning jobs against an Azure Cognitive Services account, with training data generated from the markdown stat blocks in `character-sheets/`.
- **Testing C# agent code** — `tests/` uses xUnit v3 on the Microsoft Testing Platform runner to cover tool implementations.

The D&D NPC theme is the through‑line: the agent's job is to make characters like *Kobold Wyrmspeaker Sovereign* or *Gnoll Fang of Ruin* feel real, with tools for dice rolls and a corpus of stat blocks for grounding and fine‑tuning.

## Repository layout

### `src/local-tools/` — the agent host

ASP.NET (`Microsoft.NET.Sdk.Web`) app that registers an `AIAgent` via `AgentHost.CreateBuilder` and speaks the Microsoft Foundry responses protocol. Defines local C# function tools the LLM can invoke (e.g. `ThrowDie`) and ships with a `Dockerfile` and `agent.yaml` manifest. This is the project that `azd up` deploys to Microsoft Foundry.

### `src/agent-evals/` — programmatic evaluations

Console app that runs Microsoft Foundry evaluators (task completion and task adherence) against the deployed agent, reading test cases from `agent-eval-datasets/` and reporting Pass/Fail per case.

### `src/model-finetuning/` — fine‑tuning workflows

Console app that drives the fine‑tuning lifecycle (training‑file upload, job creation) against an Azure Cognitive Services account using `Azure.ResourceManager.CognitiveServices` plus the OpenAI SDK.

- `data/` — the prepared `dnd_npc_data_{train,valid,test}.jsonl` splits fed into fine‑tuning jobs.
- `DataGeneration/` — the `SKILL.md` data‑generation prompt plus Python scripts (`generate_data.py`, `validate.py`, `split.py`) used to turn the markdown stat blocks into a JSONL preference dataset and split it into train/valid/test sets.

### `tests/` — agent unit tests

xUnit v3 tests on the Microsoft Testing Platform runner. References `local-tools` via `ProjectReference` and exercises the agent's local tool functions directly (top‑level statements expose them as `Program.<Method>` symbols).

### `character-sheets/` — NPC stat blocks (data corpus)

A library of D&D 5e‑style NPC stat blocks written in Markdown, organized by creature family and Challenge Rating (CR):

- **Goblin**: `Goblin_Skirmisher_CR025`, `Goblin_Raider_Captain_CR3`, `Goblin_Hexblade_Stalker_CR7`, `Goblin_Warlord_Ascendant_CR12`
- **Kobold**: `Kobold_Tunneler_CR025`, `Kobold_Trapmaster_CR3`, `Kobold_Dragon_Herald_CR7`, `Kobold_Wyrmspeaker_Sovereign_CR12`
- **Gnoll**: `Gnoll_Scavenger_CR025`, `Gnoll_Packmaster_CR3`, `Gnoll_Fang_of_Ruin_CR7`, `Gnoll_Butcher_of_Yeenoghu_CR12`
- `Statblock_Quick_Reference_Guide.md` — the schema/style guide all stat blocks follow.

These files are treated as **data**, not docs: they are the source material the data‑generation skill turns into fine‑tuning JSONL, and the lore the agent draws on when role‑playing characters.

### `agent-eval-datasets/` — evaluation test cases

JSONL datasets consumed by `src/agent-evals/`. One JSON object per line with `query`/`response` fields.

- `character_sheet_requirement.jsonl` — checks the agent produces stat blocks that meet the requirements implied by a request.
- `local_tools_72ksdj74lb.jsonl` — checks the agent correctly invokes its local function tools (e.g. dice rolling) for tool‑use scenarios.

### `infra/` — Bicep infrastructure as code

Provisions the Microsoft Foundry project and its dependencies. `main.bicep` is the entry point; `core/` is split by concern: `ai/` (Microsoft Foundry project + connections + ACR role assignments), `host/acr.bicep` (container registry for the agent image), `monitor/` (Log Analytics + Application Insights + dashboard), `search/` (Bing grounding, Bing custom grounding, Azure AI Search), and `storage/`.

### Top‑level files

- `azure.yaml` — `azd` service definition (`host: azure.ai.agent`, `language: docker`, `remoteBuild: true`) for the Microsoft Foundry hosted agent.
- `dnd-npc-agent.slnx` — the new XML‑based .NET solution file (add new projects here, not to a legacy `.sln`).
- `global.json` — pins the .NET SDK and selects the Microsoft Testing Platform runner.

## Prerequisites

- [.NET SDK 10.0.203](https://dotnet.microsoft.com/download) (pinned in `global.json`)
- [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli) — sign in with `az login` (auth uses `DefaultAzureCredential` everywhere)
- [Azure Developer CLI (`azd`)](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd) for deployment
- [Docker](https://www.docker.com/) for the hosted‑agent container build
- An Azure subscription with access to Microsoft Foundry in a [supported region](./SCAFFOLDING-INSTRUCTIONS.md)

## Build, format, and test

The CI workflow (`.github/workflows/ci.yml`) is the source of truth:

```bash
dotnet restore
dotnet build --no-restore --configuration Release
dotnet format --verify-no-changes --verbosity diagnostic
dotnet test  --no-build  --configuration Release
```

`dotnet format` is enforced by CI — always run it before committing.

## Configuration

Each executable project loads a single repo‑root `.env` via `DotNetEnv` (`Env.TraversePath().Load()`), so `dotnet run` works from any directory. `.env` is gitignored — never commit secrets. Common variables include:

- `FOUNDRY_PROJECT_ENDPOINT`
- `AZURE_AI_MODEL_DEPLOYMENT_NAME`
- `AGENT_LOCAL_TOOLS_NAME`
- `AZURE_SUBSCRIPTION_ID`, `AZURE_RESOURCE_GROUP`, `AZURE_AI_ACCOUNT_NAME`

See each project's README for project‑specific variables.

## Running the agent host locally

```bash
dotnet run --project src/local-tools
```

Then send it a request:

```bash
curl -X POST http://localhost:8088/responses \
  -H "Content-Type: application/json" \
  -d '{"input": "Roll initiative for a Kobold Trapmaster (CR 3).", "stream": false}'
```

## Deploying the agent to Microsoft Foundry

```bash
azd up
```

This provisions the infrastructure under `infra/` and deploys `local-tools` as a Microsoft Foundry hosted agent (`gpt-4o-mini` deployment by default). If your first call returns a 401, your service principal likely needs the **Azure AI User** role at the resource‑group level — see [`DEBUGGING.md`](./DEBUGGING.md).

## Further reading

- [`CONTRIBUTING.md`](./CONTRIBUTING.md) — conventional commits, formatting, and PR guidance
- [`DEMOSCRIPT.md`](./DEMOSCRIPT.md) — walkthrough of the demo flow
- [`SCAFFOLDING-INSTRUCTIONS.md`](./SCAFFOLDING-INSTRUCTIONS.md) — how this repo was bootstrapped and regional considerations
- [`DEBUGGING.md`](./DEBUGGING.md) — common issues (auth, deployment, tool errors)
- Per‑project READMEs in `src/local-tools/`, `src/agent-evals/`, and `src/model-finetuning/DataGeneration/SKILL.md`
