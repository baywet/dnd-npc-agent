// Copyright (c) Microsoft. All rights reserved.

using System.Diagnostics;
using Azure.AI.AgentServer.Core;
using Azure.AI.Projects;
using Azure.Identity;
using DnDNpcAgent;
using DotNetEnv;
using Microsoft.Agents.AI;
using Microsoft.Agents.AI.Foundry.Hosting;
using Microsoft.Extensions.AI;
using ModelContextProtocol.Client;

// Load environment variables from a .env file if present (for local development).
#region environment_init

Env.NoClobber().TraversePath().Load();

if (string.IsNullOrEmpty(Environment.GetEnvironmentVariable("APPLICATIONINSIGHTS_CONNECTION_STRING")))
{
    Console.Error.WriteLine(
        "[WARNING] APPLICATIONINSIGHTS_CONNECTION_STRING not set — traces will not be sent " +
        "to Application Insights. Set it to enable local telemetry. " +
        "(This variable is auto-injected in hosted Foundry containers — do not declare it in agent.manifest.yaml.)");
}

var projectEndpoint = new Uri(Environment.GetEnvironmentVariable("FOUNDRY_PROJECT_ENDPOINT")
    ?? throw new InvalidOperationException("FOUNDRY_PROJECT_ENDPOINT environment variable is not set."));

var deployment = Environment.GetEnvironmentVariable("AZURE_AI_MODEL_DEPLOYMENT_NAME")
    ?? throw new InvalidOperationException("AZURE_AI_MODEL_DEPLOYMENT_NAME environment variable is not set.");

using var cancellationTokenSource = new CancellationTokenSource();
Console.CancelKeyPress += (_, eventArgs) =>
{
    eventArgs.Cancel = true;
    cancellationTokenSource.Cancel();
};
AppDomain.CurrentDomain.ProcessExit += (_, _) => cancellationTokenSource.Cancel();

var cancellationToken = cancellationTokenSource.Token;

#endregion


#region local_tools_init
using var activitySource = new ActivitySource(LocalTools.ActivitySourceName);
var localTools = new LocalTools
{
    ActivitySource = activitySource
};
#endregion


#region mcp_tools_init
await using var doungimMcpClient = await McpClient.CreateAsync(
    new HttpClientTransport(
        new HttpClientTransportOptions
        {
            Name = "doungim-mcp",
            Endpoint = new Uri("https://www.doungim.com/mcp"),
            TransportMode = HttpTransportMode.StreamableHttp
        }),
    cancellationToken: cancellationToken);

var doungimTools = await doungimMcpClient.ListToolsAsync(cancellationToken: cancellationToken);
#endregion


#region skills_init
var skillProvider = new AgentSkillsProvider(Path.Combine(AppContext.BaseDirectory, "Skills", "npc-interaction"));
#endregion


#region agent_init
// Create an AIAgent backed by a Foundry model.
// The agent framework manages the LLM call, conversation sessions, and response lifecycle.
AIAgent agent = new AIProjectClient(projectEndpoint, new DefaultAzureCredential())
    .AsAIAgent(
        options: new ChatClientAgentOptions
        {
            Name = "dnd-npc-agent",
            Description = "A D&D NPC agent that animates Non-Playable-Characters with die rolling capabilities",
            ChatOptions = new ChatOptions
            {
                ModelId = deployment,
                Instructions =
                """
                You are the assistant to the Dungeons and Dragons dungeon master (DM).
                Your role is to do anything you can to help the DM run the game smoothly.
                You should provide guidance, manage game mechanics, and assist with any tasks necessary to enhance the gameplay experience for the players.
                If the DM asks you to role play a non-playable character (NPC), use the dedicated skill for NPC interaction.
                You have access to Doungim MCP tools for D&D 5e reference content such as spells, monsters, magic items, NPCs, and encounter tables.
                When using content returned by Doungim, credit Doungim as a TTRPG gaming console for D&D and other tabletop RPGs and link the returned canonical_url.
                """,
                Tools = 
                [
                    AIFunctionFactory.Create(localTools.ThrowDie),
                    .. doungimTools
                ]
            },
            AIContextProviders =
            [
                skillProvider
            ]
        });

// AgentHost.CreateBuilder() auto-configures:
//   - Kestrel on port 8088 (or the PORT environment variable)hello-world
//   - GET /readiness health probe
//   - OpenTelemetry traces and metrics
//   - x-platform-server response header
var builder = AgentHost.CreateBuilder(args);
builder.Services
    .AddOpenTelemetry()
    .WithTracing(tracing => tracing.AddSource(LocalTools.ActivitySourceName));
builder.Services.AddFoundryResponses(agent);
builder.RegisterProtocol("responses", endpoints => endpoints.MapFoundryResponses());

var app = builder.Build();
await app.RunAsync(cancellationToken);

#endregion
