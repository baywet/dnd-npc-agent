# D&D NPC Agent

This repository contains a Microsoft Foundry hosted agent demo built with the .NET Agent Framework and the Responses protocol. The agent acts as an assistant for a Dungeons & Dragons dungeon master: it can roll dice, look up D&D reference material through an MCP server, load a skill before roleplaying an NPC, persist useful table preferences in Foundry memory, and hold real-time voice conversations through Azure AI Voice Live.

The point of the demo is to show how the same hosted agent can combine precise local tools, externally hosted MCP tools, skill-guided behavior, approvals, telemetry, citations, and memory while still being runnable locally and deployable to Foundry.

## What the Demo Shows

1. **Agent definition and hosting**
   The app creates an `AIAgent` backed by a Foundry model, hosts it with `AgentHost.CreateBuilder`, and exposes the Responses protocol on port `8088`.

2. **Local tool execution**
   The agent has a local `ThrowDie` tool for dice rolls. The tool is registered directly with the model, does not require approval, and emits custom OpenTelemetry activity tags for the roll notation, result, and die size.

3. **MCP reference tools with approval**
   The agent connects to the Doungim MCP server for D&D 5e reference content such as monsters, spells, magic items, NPCs, and encounter tables. Those MCP tools are wrapped in approval requirements so a user can inspect and approve access before execution.

4. **Skill-guided NPC roleplay**
   The `npc-behaviour` skill is loaded before the agent impersonates a creature or NPC. It requires the agent to retrieve the relevant official stat block, stay in character, avoid exposing mechanics while roleplaying, use dice rolls when outcomes are uncertain, and return structured voice-performance direction with every in-character response.

5. **Persistent memory**
   The agent uses Foundry memory to remember table preferences, such as favorite NPC voices, across new conversations. In debug builds the app also exposes a memory-clear endpoint for resetting the demo.

6. **Real-time voice**
   A local .NET voice client connects Voice Live to the deployed Foundry agent, streams microphone audio, plays generated speech, prints transcripts, and supports interruption while the agent is speaking.

## Demo Overview

The demo is intentionally organized around a few Agent Framework capabilities rather than a scripted product tour. The detailed presenter runbook lives in `src/dnd-npc-agent-framework/DEMOSCRIPT.md`; the README keeps the conceptual map:

- **Local tool**: `ThrowDie` is a local C# function exposed to the agent for dice rolls. It demonstrates tightly defined behavior, direct tool registration, and custom telemetry for tool execution.
- **MCP tool**: The agent connects to the Doungim MCP server for D&D 5e reference data. It demonstrates how a hosted agent can use external capabilities without baking that data or behavior into the app.
- **Approval flow**: Doungim MCP tools are wrapped as approval-required functions. This demonstrates how user consent fits into tool execution, especially when a tool reaches outside the agent host.
- **Skill**: The `npc-behaviour` skill gives the model domain-specific guidance for NPC impersonation. It demonstrates how skills can shape broad behavior that is not a single deterministic tool call.
- **Memory**: Foundry memory stores table preferences across conversations. This demonstrates how an agent can preserve useful user context while keeping the conversational session model clean.

## How It Is Built

The project started from the `azd ai agent init` hosted-agent template using the .NET Hello World Agent Framework option, then was renamed and extended into the D&D demo. The creation flow was:

```shell
azd ai agent init
# choose .NET / Hello World / Agent Framework
# rename the generated project for the D&D NPC agent
azd up
```

The main implementation lives in `src/dnd-npc-agent-framework`:

- `Program.cs` wires environment configuration, Foundry credentials, the model-backed `AIAgent`, local tools, MCP tools, skills, memory, telemetry, and Responses protocol hosting.
- `src/dnd-npc-agent-voice-client` contains only the Voice Live microphone and playback client. It targets the deployed Responses-protocol hosted agent; the agent definition remains exclusively in `src/dnd-npc-agent-framework/Program.cs`.
- `LocalTools.cs` defines the local dice-rolling tool and emits custom activity tags for tracing.
- `Skills/npc-interaction/npc-behaviour/SKILL.md` defines the roleplay workflow and guardrails used when the DM asks the agent to impersonate an NPC or creature.
- `TemporaryPatches/AgentFramework` contains temporary approval replay patches used by this demo.
- `DEMOSCRIPT.md` contains the short runbook for presenting the demo live.

## Prerequisites

1. [.NET 10 SDK](https://dotnet.microsoft.com/download/dotnet/10.0) or later.
2. [Azure Developer CLI](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd) with the Foundry extension.
3. Azure authentication through `azd auth login` or `az login`.
4. A Foundry project and model deployment configured through `azure.yaml` and environment variables.

Install the Foundry extension if needed:

```shell
azd ext install microsoft.foundry
```

## Run Locally

Start the hosted agent locally:

```shell
azd ai agent run
```

The agent host listens on `http://localhost:8088`. You can invoke it from another terminal:

```shell
azd ai agent invoke --local "hello what can you do"
```

You can also run the project directly after restoring dependencies and configuring the required environment variables:

```shell
dotnet restore
dotnet run --project src/dnd-npc-agent-framework/dnd-npc-agent-framework.csproj
```

The app loads a local `.env` file if present. The required values are:

- `FOUNDRY_PROJECT_ENDPOINT`
- `AZURE_AI_MODEL_DEPLOYMENT_NAME`

Optional values include:

- `APPLICATIONINSIGHTS_CONNECTION_STRING` for local telemetry export.
- `AZURE_AI_MEMORY_STORE_ID` to choose the Foundry memory store name.
- `FOUNDRY_EMBEDDING_MODEL` to choose the embedding model used by memory.

## Run with Voice

Deploy the hosted agent first, authenticate with Azure, then run the local voice client:

```shell
az login
dotnet run --project src/dnd-npc-agent-voice-client/dnd-npc-agent-voice-client.csproj
```

The voice client reuses `FOUNDRY_PROJECT_ENDPOINT` to derive the Voice Live resource endpoint and Foundry project name. It also defaults the agent name to `dnd-npc-agent-framework`, so no additional configuration is required for this repository's standard deployment. Voice Live routes each turn to that deployed hosted agent, which means the existing instructions, local and MCP tools, skill provider, approval handling, and Foundry memory provider are used without a second agent definition.

Optional voice overrides are:

- `VOICELIVE_ENDPOINT` when Voice Live uses a different Foundry resource.
- `PROJECT_NAME` when it cannot be derived from `FOUNDRY_PROJECT_ENDPOINT`.
- `AGENT_NAME` to target a differently named deployed agent.
- `VOICE_NAME` to select another Azure voice.
- `AGENT_VERSION` and `CONVERSATION_ID` to pin an agent version or resume a conversation.
- `FOUNDRY_RESOURCE_OVERRIDE` and `AGENT_AUTHENTICATION_IDENTITY_CLIENT_ID` for cross-resource agent connections.

The Voice Live agent integration uses Microsoft Entra ID authentication; API-key authentication is not supported in agent mode. The local computer must have a microphone and audio output device.

## Deploy

Deploy or update the hosted agent in Foundry with:

```shell
azd up
```

After deployment, invoke the hosted agent with:

```shell
azd ai agent invoke "hello what can you do"
```

## Useful Demo Reset

In debug builds, clear stored demo memory with:

```shell
curl -i -X DELETE "http://localhost:8088/debug/memory"
```

This is only for keeping the live demo repeatable; production agents should use an intentional memory management flow.
