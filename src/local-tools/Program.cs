// Copyright (c) Microsoft. All rights reserved.

using Azure.AI.AgentServer.Core;
using Azure.AI.Projects;
using Azure.Identity;
using DotNetEnv;
using Microsoft.Agents.AI;
using Microsoft.Agents.AI.Foundry.Hosting;
using Microsoft.Extensions.AI;

Env.TraversePath().Load();

var projectEndpoint = new Uri(Environment.GetEnvironmentVariable("FOUNDRY_PROJECT_ENDPOINT")
    ?? throw new InvalidOperationException("FOUNDRY_PROJECT_ENDPOINT environment variable is not set."));
var deployment = Environment.GetEnvironmentVariable("AZURE_AI_MODEL_DEPLOYMENT_NAME") ?? "gpt-4o";

AIAgent agent = new AIProjectClient(projectEndpoint, new DefaultAzureCredential())
    .AsAIAgent(
        model: deployment,
        instructions: """
            You are an animator of Non-Playable-Characters (NPCs) for Dungeons and Dragons play sessions.
            Your role is to bring NPCs to life by providing engaging dialogue, personality, and reactions.
            Use the available die-rolling tool to resolve uncertain outcomes and add randomness to interactions.
            Make the game more interactive and fun for all players.
            Whenever a user starts a conversation, ask for the NPC character sheet.
            Do not make up any information about the NPC, and do not answer any question about the character as long as the user has not given you the character sheet.
            """,
        name: "dnd-npc-agent-north-central",
        description: "A D&D NPC agent that animates Non-Playable-Characters with die rolling capabilities",
        tools:
        [
            AIFunctionFactory.Create(ThrowDie, "ThrowDie",
                "Throws a die and returns the result. Specify the number of sides on the die (e.g., 20 for d20, 6 for d6). Optionally add a modifier to be applied to the roll.")
        ]);

var builder = AgentHost.CreateBuilder(args);
builder.Services.AddFoundryResponses(agent);
builder.RegisterProtocol("responses", endpoints => endpoints.MapFoundryResponses());

var app = builder.Build();
app.Run();

static string ThrowDie(int sides = 20, int? modifier = null)
{
    if (sides <= 0)
        return "Error: Die must have at least 1 side.";

    var random = new Random();
    int result = random.Next(1, sides + 1);

    string diceNotation = modifier.HasValue ? $"d{sides} + {modifier}" : $"d{sides}";
    int finalResult = modifier.HasValue ? result + modifier.Value : result;

    return $"🎲 Threw a {diceNotation}: **{finalResult}**";
}
