// Copyright (c) Microsoft. All rights reserved.

using System.Collections.Concurrent;
using Azure.AI.VoiceLive;
using Azure.Identity;
using DotNetEnv;
using NAudio.Wave;

Env.NoClobber().TraversePath().Load();

VoiceConfiguration configuration = VoiceConfiguration.FromEnvironment();

using var cancellationTokenSource = new CancellationTokenSource();
Console.CancelKeyPress += (_, eventArgs) =>
{
    eventArgs.Cancel = true;
    cancellationTokenSource.Cancel();
};

CheckAudioDevices();

Console.WriteLine(
    $"Connecting Voice Live to the existing hosted agent " +
    $"{configuration.AgentName} in project {configuration.ProjectName}...");

using var assistant = new VoiceAssistant(configuration);

try
{
    await assistant.RunAsync(cancellationTokenSource.Token).ConfigureAwait(false);
}
catch (OperationCanceledException) when (cancellationTokenSource.IsCancellationRequested)
{
    Console.WriteLine("Voice session ended.");
}

static void CheckAudioDevices()
{
    if (WaveInEvent.DeviceCount == 0)
    {
        throw new InvalidOperationException("No audio input device was found. Connect a microphone and try again.");
    }

    using var playbackDevice = new WaveOutEvent();
}

internal sealed record VoiceConfiguration(
    Uri Endpoint,
    string AgentName,
    string ProjectName,
    string VoiceName,
    string? AgentVersion,
    string? ConversationId,
    string? FoundryResourceOverride,
    string? AuthenticationIdentityClientId)
{
    private const string DefaultAgentName = "dnd-npc-agent-framework";
    private const string DefaultVoiceName = "en-US-Ava:DragonHDLatestNeural";

    public static VoiceConfiguration FromEnvironment()
    {
        var projectEndpoint = GetRequiredUri("FOUNDRY_PROJECT_ENDPOINT");
        var endpoint = GetOptionalUri("VOICELIVE_ENDPOINT")
            ?? new Uri(projectEndpoint.GetLeftPart(UriPartial.Authority));
        var projectName = Environment.GetEnvironmentVariable("PROJECT_NAME")
            ?? GetProjectName(projectEndpoint);

        return new VoiceConfiguration(
            endpoint,
            Environment.GetEnvironmentVariable("AGENT_NAME") ?? DefaultAgentName,
            projectName,
            Environment.GetEnvironmentVariable("VOICE_NAME") ?? DefaultVoiceName,
            Environment.GetEnvironmentVariable("AGENT_VERSION"),
            Environment.GetEnvironmentVariable("CONVERSATION_ID"),
            Environment.GetEnvironmentVariable("FOUNDRY_RESOURCE_OVERRIDE"),
            Environment.GetEnvironmentVariable("AGENT_AUTHENTICATION_IDENTITY_CLIENT_ID"));
    }

    private static Uri GetRequiredUri(string variableName)
    {
        var value = Environment.GetEnvironmentVariable(variableName);
        if (string.IsNullOrWhiteSpace(value))
        {
            throw new InvalidOperationException($"{variableName} environment variable is not set.");
        }

        return new Uri(value);
    }

    private static Uri? GetOptionalUri(string variableName)
    {
        var value = Environment.GetEnvironmentVariable(variableName);
        return string.IsNullOrWhiteSpace(value) ? null : new Uri(value);
    }

    private static string GetProjectName(Uri projectEndpoint)
    {
        string[] segments = projectEndpoint.AbsolutePath.Split(
            '/',
            StringSplitOptions.RemoveEmptyEntries | StringSplitOptions.TrimEntries);
        var projectsSegment = Array.FindIndex(
            segments,
            segment => string.Equals(segment, "projects", StringComparison.OrdinalIgnoreCase));

        if (projectsSegment < 0 || projectsSegment == segments.Length - 1)
        {
            throw new InvalidOperationException(
                "PROJECT_NAME could not be derived from FOUNDRY_PROJECT_ENDPOINT. " +
                "Set PROJECT_NAME explicitly.");
        }

        return segments[projectsSegment + 1];
    }
}

internal sealed class VoiceAssistant(VoiceConfiguration configuration) : IDisposable
{
    private VoiceLiveSession? _session;
    private AudioProcessor? _audioProcessor;

    public async Task RunAsync(CancellationToken cancellationToken)
    {
        // AgentSessionConfig routes Voice Live to the deployed Responses-protocol hosted agent.
        // Instructions, tools, skills, approvals, and memory continue to run in that agent.
        var agentConfig = new AgentSessionConfig(configuration.AgentName, configuration.ProjectName)
        {
            AgentVersion = configuration.AgentVersion,
            ConversationId = configuration.ConversationId,
            FoundryResourceOverride = configuration.FoundryResourceOverride,
            AuthenticationIdentityClientId = configuration.AuthenticationIdentityClientId
        };

        var client = new VoiceLiveClient(configuration.Endpoint, new DefaultAzureCredential());
        _session = await client.StartSessionAsync(
            SessionTarget.FromAgent(agentConfig),
            cancellationToken).ConfigureAwait(false);

        _audioProcessor = new AudioProcessor(_session);

        await ConfigureSessionAsync(cancellationToken).ConfigureAwait(false);
        _audioProcessor.StartPlayback();

        Console.WriteLine($"Voice session ready using {configuration.VoiceName}.");
        Console.WriteLine("Start speaking. Press Ctrl+C to end the session.");

        await foreach (SessionUpdate update in _session.GetUpdatesAsync(cancellationToken).ConfigureAwait(false))
        {
            HandleUpdate(update);
        }
    }

    private async Task ConfigureSessionAsync(CancellationToken cancellationToken)
    {
        var interimResponse = new LlmInterimResponseConfig
        {
            Instructions =
                "Use a brief in-character acknowledgement only when tool execution or latency creates a noticeable pause."
        };
        interimResponse.Triggers.Add(InterimResponseTrigger.Tool);
        interimResponse.Triggers.Add(InterimResponseTrigger.Latency);

        var options = new VoiceLiveSessionOptions
        {
            InputAudioFormat = InputAudioFormat.Pcm16,
            OutputAudioFormat = OutputAudioFormat.Pcm16,
            Voice = new AzureStandardVoice(configuration.VoiceName),
            InterimResponse = BinaryData.FromObjectAsJson(interimResponse)
        };

        await _session!.ConfigureSessionAsync(options, cancellationToken).ConfigureAwait(false);
    }

    private void HandleUpdate(SessionUpdate update)
    {
        switch (update)
        {
            case SessionUpdateSessionUpdated:
                _audioProcessor?.StartCapture();
                break;

            case SessionUpdateConversationItemInputAudioTranscriptionCompleted transcription:
                Console.WriteLine($"You: {transcription.Transcript}");
                break;

            case SessionUpdateResponseAudioTranscriptDone transcript:
                Console.WriteLine($"Agent: {transcript.Transcript}");
                break;

            case SessionUpdateInputAudioBufferSpeechStarted:
                _audioProcessor?.SkipPendingAudio();
                break;

            case SessionUpdateResponseAudioDelta audio when audio.Delta is not null:
                _audioProcessor?.QueueAudio(audio.Delta.ToArray());
                break;

            case SessionUpdateError error:
                throw new InvalidOperationException($"Voice Live error: {error.Error?.Message}");
        }
    }

    public void Dispose()
    {
        _audioProcessor?.Dispose();
        _session?.Dispose();
    }
}

internal sealed class AudioProcessor(VoiceLiveSession session) : IDisposable
{
    private const int SampleRate = 24000;
    private const int BitsPerSample = 16;
    private const int Channels = 1;

    private readonly BlockingCollection<byte[]> _sendQueue = new(new ConcurrentQueue<byte[]>());
    private readonly BlockingCollection<byte[]> _playbackQueue = new(new ConcurrentQueue<byte[]>());
    private readonly CancellationTokenSource _cancellationTokenSource = new();
    private WaveInEvent? _waveIn;
    private WaveOutEvent? _waveOut;
    private BufferedWaveProvider? _playbackBuffer;
    private Task? _sendTask;
    private Task? _playbackTask;
    private bool _isCapturing;

    public void StartCapture()
    {
        if (_isCapturing)
        {
            return;
        }

        _isCapturing = true;
        _waveIn = new WaveInEvent
        {
            WaveFormat = new WaveFormat(SampleRate, BitsPerSample, Channels),
            BufferMilliseconds = 50
        };
        _waveIn.DataAvailable += OnAudioAvailable;
        _waveIn.StartRecording();
        _sendTask = Task.Run(SendAudioAsync);
    }

    public void StartPlayback()
    {
        _playbackBuffer = new BufferedWaveProvider(new WaveFormat(SampleRate, BitsPerSample, Channels))
        {
            BufferDuration = TimeSpan.FromSeconds(10),
            DiscardOnBufferOverflow = true
        };
        _waveOut = new WaveOutEvent { DesiredLatency = 100 };
        _waveOut.Init(_playbackBuffer);
        _waveOut.Play();
        _playbackTask = Task.Run(PlayAudio);
    }

    public void QueueAudio(byte[] audio)
    {
        if (audio.Length > 0)
        {
            _playbackQueue.Add(audio, _cancellationTokenSource.Token);
        }
    }

    public void SkipPendingAudio()
    {
        while (_playbackQueue.TryTake(out _))
        {
        }

        _playbackBuffer?.ClearBuffer();
    }

    private void OnAudioAvailable(object? sender, WaveInEventArgs eventArgs)
    {
        if (!_isCapturing || eventArgs.BytesRecorded == 0)
        {
            return;
        }

        var audio = eventArgs.Buffer.AsSpan(0, eventArgs.BytesRecorded).ToArray();
        _sendQueue.Add(audio, _cancellationTokenSource.Token);
    }

    private async Task SendAudioAsync()
    {
        foreach (var audio in _sendQueue.GetConsumingEnumerable(_cancellationTokenSource.Token))
        {
            await session.SendInputAudioAsync(audio, _cancellationTokenSource.Token).ConfigureAwait(false);
        }
    }

    private void PlayAudio()
    {
        foreach (var audio in _playbackQueue.GetConsumingEnumerable(_cancellationTokenSource.Token))
        {
            _playbackBuffer?.AddSamples(audio, 0, audio.Length);
        }
    }

    public void Dispose()
    {
        _isCapturing = false;
        _cancellationTokenSource.Cancel();
        _sendQueue.CompleteAdding();
        _playbackQueue.CompleteAdding();

        if (_waveIn is not null)
        {
            _waveIn.DataAvailable -= OnAudioAvailable;
            _waveIn.StopRecording();
            _waveIn.Dispose();
        }

        _waveOut?.Stop();
        _waveOut?.Dispose();

        WaitForCompletion(_sendTask);
        WaitForCompletion(_playbackTask);

        _sendQueue.Dispose();
        _playbackQueue.Dispose();
        _cancellationTokenSource.Dispose();
    }

    private static void WaitForCompletion(Task? task)
    {
        if (task is null)
        {
            return;
        }

        try
        {
            task.Wait(TimeSpan.FromSeconds(2));
        }
        catch (AggregateException exception) when (
            exception.InnerExceptions.All(inner => inner is OperationCanceledException))
        {
        }
    }
}
