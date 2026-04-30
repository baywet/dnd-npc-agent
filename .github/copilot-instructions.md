# Copilot Instructions

## Project overview

A Dungeons & Dragons NPC agent built on Azure AI Foundry's hosted-agent platform (Microsoft Agent Framework). The repo contains three .NET 10 projects plus an xUnit test project, all listed in `dnd-npc-agent.slnx`:

- **`src/local-tools/`** — the agent host itself. ASP.NET (`Microsoft.NET.Sdk.Web`) app that registers an `AIAgent` with the Foundry responses protocol via `AgentHost.CreateBuilder`. This is the project deployed by `azd` (see `azure.yaml`, `host: azure.ai.agent`, `language: docker`). Has a `Dockerfile` and `agent.yaml` manifest.
- **`src/agent-evals/`** — console app that runs programmatic evaluations against the deployed agent using Azure AI Foundry evaluators. Datasets live in `agent-eval-datasets/` and are copied to output via `<Content Include>` in the csproj.
- **`src/model-finetuning/`** — console app that drives fine-tuning workflows (file upload, job creation) against an Azure Cognitive Services account, using `Azure.ResourceManager.CognitiveServices` plus the OpenAI SDK.
- **`tests/local-tools.tests.csproj`** — xUnit v3 tests on the Microsoft.Testing.Platform runner; references `local-tools` via `ProjectReference`. The agent's `ThrowDie` function is in `Program.cs` and reachable from tests because top-level statements still emit `Program.<Method>` symbols.

## Build, test, format

The CI workflow (`.github/workflows/ci.yml`) is the source of truth:

```bash
dotnet restore
dotnet build --no-restore --configuration Release
dotnet format --verify-no-changes --verbosity diagnostic
dotnet test  --no-build  --configuration Release
```

- **SDK is pinned** in `global.json` to .NET `10.0.203`. Do not bump without coordinating.
- **Test runner** is Microsoft.Testing.Platform (set in `global.json` and `<UseMicrosoftTestingPlatformRunner>true</UseMicrosoftTestingPlatformRunner>`), not VSTest. Run a single test with the MTP filter syntax:
  ```bash
  dotnet test tests/local-tools.tests.csproj --filter-method "*ThrowDie_WithDefaultSides_ReturnsResultBetween1And20"
  ```
- **`dotnet format` is enforced by CI** (`--verify-no-changes`). Always run it before committing — `CONTRIBUTING.md` makes this explicit.

## Configuration & secrets

- **All projects load `.env` via `DotNetEnv` at the very top of `Program.cs`** using `Env.TraversePath().Load();`. `TraversePath()` walks up parent directories, so a single `.env` at the repo root works for `dotnet run` from any project. `.env` is gitignored — never commit it.
- The library-based load is intentional so the apps work the same whether launched from VS Code (which has its own `envFile` support) or directly via `dotnet run`. When adding a new executable project, follow the same pattern: add `DotNetEnv 3.2.0` and call `Env.TraversePath().Load();` before any `Environment.GetEnvironmentVariable` reads.
- Required env vars per project are validated at startup with `?? throw new InvalidOperationException(...)`. Common keys: `FOUNDRY_PROJECT_ENDPOINT`, `AZURE_AI_MODEL_DEPLOYMENT_NAME`, `AGENT_LOCAL_TOOLS_NAME`, `AZURE_SUBSCRIPTION_ID`, `AZURE_RESOURCE_GROUP`, `AZURE_AI_ACCOUNT_NAME`.
- Auth uses `DefaultAzureCredential` everywhere — `az login` is the developer prerequisite.

## Deployment

- `azd up` provisions infra (`infra/` Bicep) and deploys `local-tools` as a Foundry hosted agent. The `azure.yaml` `services.local-tools` entry uses `host: azure.ai.agent` with `remoteBuild: true` and a `gpt-4o-mini` deployment.
- Region matters — Foundry hosted agents have limited region availability (see `SCAFFOLDING-INSTRUCTIONS.md`).
- A 401 from the agent on first call usually means the SP needs the **Azure AI User** role at the resource-group level (see `DEBUGGING.md`).

## Conventions

- **Top-level statements** are used in every `Program.cs`. Tests reach into them by calling unqualified method names (e.g., `ThrowDie(...)`) thanks to the implicit `Program` class.
- **`#pragma warning disable OPENAI001`** — the OpenAI SDK marks evals/fine-tuning APIs as experimental. Suppress at file scope (or via `<NoWarn>` in the csproj as `agent-evals` does) when calling those APIs; do not work around them differently.
- **Conventional commits** are required (`CONTRIBUTING.md`). Dependabot uses scoped prefixes (`chore(deps):`, `ci(deps):`, `chore(docker):`). Always include the `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>` trailer.
- **Solution file is `.slnx`** (XML-based, new format). Add new projects there, not via legacy `.sln`.
- **Character-sheet markdown** in `character-sheets/` and the `DataGeneration/SKILL.md` skill drive fine-tuning data generation; treat these as data, not docs.
