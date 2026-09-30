// Copyright (c) Microsoft. All rights reserved.

using Azure.AI.AgentServer.Core;

namespace DnDNpcAgent;

internal static class AgentHostAppExtensions
{
    public static AgentHostApp MapDebugMemoryClearEndpoint(
        this AgentHostApp app,
        Func<CancellationToken, Task> clearMemoriesAsync)
    {
#if DEBUG
        app.App.MapDelete("/debug/memory", async (CancellationToken cancellationToken) =>
        {
            await clearMemoriesAsync(cancellationToken).ConfigureAwait(false);
            return Results.NoContent();
        });
#endif

        return app;
    }
}
