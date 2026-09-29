using Microsoft.Agents.AI;

namespace DnDNpcAgent.TemporaryPatches.AgentFramework;

#pragma warning disable MAAI001
internal sealed class PatchedApprovalReplaySessionStore(AgentSessionStore innerStore) : AgentSessionStore
{
    public override ValueTask<AgentSession?> GetSessionAsync(
        AIAgent agent,
        AgentSessionStoreKey key,
        CancellationToken cancellationToken = default)
        => innerStore.GetSessionAsync(agent, key, cancellationToken);

    public override ValueTask SaveSessionAsync(
        AIAgent agent,
        AgentSessionStoreKey key,
        AgentSession session,
        CancellationToken cancellationToken = default)
    {
        PatchedApprovalReplayChatHistoryProvider.EnsureApprovalReplayState(session);
        return innerStore.SaveSessionAsync(agent, key, session, cancellationToken);
    }

    public override object? GetService(Type serviceType, object? serviceKey = null)
        => base.GetService(serviceType, serviceKey) ?? innerStore.GetService(serviceType, serviceKey);
}
#pragma warning restore MAAI001