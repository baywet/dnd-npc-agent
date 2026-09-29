using System.Security.Cryptography;
using System.Text;
using System.Text.Json;
using System.Text.Json.Serialization;
using Microsoft.Agents.AI;
using Microsoft.Extensions.AI;

namespace DnDNpcAgent.TemporaryPatches.AgentFramework;

/// <summary>
/// To use until https://github.com/microsoft/agent-framework/pull/8873 is merged and released
/// </summary>
internal sealed class PatchedApprovalReplayChatHistoryProvider : ChatHistoryProvider
{
    private const string PendingApprovalRequestsStateKey = "_pendingApprovalRequests";
    private const string ToolApprovalIdMapStateKey = "Microsoft.Agents.AI.Foundry.Hosting.ToolApprovalIdMap";
    private const string ChatHistoryStateKey = nameof(PatchedApprovalReplayChatHistoryProvider);

    private readonly ProviderSessionState<State> sessionState = new(_ => new State(), ChatHistoryStateKey);

    public override IReadOnlyList<string> StateKeys => [this.sessionState.StateKey, PendingApprovalRequestsStateKey, ToolApprovalIdMapStateKey];

    protected override ValueTask<IEnumerable<ChatMessage>> ProvideChatHistoryAsync(InvokingContext context, CancellationToken cancellationToken = default)
        => new(this.sessionState.GetOrInitializeState(context.Session).Messages);

    protected override ValueTask StoreChatHistoryAsync(InvokedContext context, CancellationToken cancellationToken = default)
    {
        var state = this.sessionState.GetOrInitializeState(context.Session);
        state.Messages.AddRange(context.RequestMessages);
        if (context.ResponseMessages is not null)
        {
            state.Messages.AddRange(context.ResponseMessages);
            RecordPendingApprovalRequests(context.Session, context.ResponseMessages);
        }

        this.sessionState.SaveState(context.Session, state);
        return default;
    }

    private static void RecordPendingApprovalRequests(AgentSession? session, IEnumerable<ChatMessage> responseMessages)
    {
        if (session is null)
        {
            return;
        }

        var approvalRequests = responseMessages
            .SelectMany(message => message.Contents)
            .OfType<ToolApprovalRequestContent>()
            .Select(SnapshotRequest)
            .ToList();

        if (approvalRequests.Count == 0)
        {
            return;
        }

        if (!session.StateBag.TryGetValue<List<ToolApprovalRequestContent>>(PendingApprovalRequestsStateKey, out var pendingRequests) ||
            pendingRequests is null)
        {
            pendingRequests = [];
        }

        foreach (var request in approvalRequests)
        {
            pendingRequests.RemoveAll(pending => string.Equals(pending.RequestId, request.RequestId, StringComparison.Ordinal));
            pendingRequests.Add(request);
            RecordToolApprovalIdMapEntry(session, request);
        }

        session.StateBag.SetValue(PendingApprovalRequestsStateKey, pendingRequests);
    }

    internal static void EnsureApprovalReplayState(AgentSession session)
    {
        if (!session.StateBag.TryGetValue<State>(ChatHistoryStateKey, out var state) || state is null)
        {
            return;
        }

        RecordPendingApprovalRequests(session, state.Messages);
    }

    private static void RecordToolApprovalIdMapEntry(AgentSession session, ToolApprovalRequestContent request)
    {
        if (request.ToolCall is not FunctionCallContent functionCall ||
            string.IsNullOrEmpty(functionCall.CallId) ||
            string.IsNullOrEmpty(functionCall.Name))
        {
            return;
        }

        if (!session.StateBag.TryGetValue<Dictionary<string, ApprovalEntry>>(ToolApprovalIdMapStateKey, out var map) ||
            map is null)
        {
            map = new Dictionary<string, ApprovalEntry>(StringComparer.Ordinal);
        }

        map[ComputeWireId(request.RequestId)] = new ApprovalEntry
        {
            AfRequestId = request.RequestId,
            CallId = functionCall.CallId,
            Name = functionCall.Name,
            Arguments = functionCall.Arguments is null ? "{}" : JsonSerializer.Serialize(functionCall.Arguments)
        };
        session.StateBag.SetValue(ToolApprovalIdMapStateKey, map);
    }

    private static string ComputeWireId(string requestId)
    {
        Span<byte> hash = stackalloc byte[32];
        SHA256.HashData(Encoding.UTF8.GetBytes(requestId), hash);
        return "mcpr_" + Convert.ToHexString(hash).AsSpan(0, 50).ToString();
    }

    private static ToolApprovalRequestContent SnapshotRequest(ToolApprovalRequestContent request)
    {
        if (request.ToolCall is FunctionCallContent functionCall)
        {
            return new ToolApprovalRequestContent(
                request.RequestId,
                new FunctionCallContent(
                    functionCall.CallId,
                    functionCall.Name,
                    functionCall.Arguments is null ? null : new Dictionary<string, object?>(functionCall.Arguments)));
        }

        return request;
    }

    internal sealed class State
    {
        [JsonPropertyName("messages")]
        public List<ChatMessage> Messages { get; set; } = [];
    }

    internal sealed class ApprovalEntry
    {
        public string AfRequestId { get; set; } = string.Empty;

        public string CallId { get; set; } = string.Empty;

        public string Name { get; set; } = string.Empty;

        public string? Arguments { get; set; }
    }
}