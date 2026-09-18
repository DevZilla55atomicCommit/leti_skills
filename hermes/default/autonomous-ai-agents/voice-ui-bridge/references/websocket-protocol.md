# WebSocket Protocol — JARVIS Voice UI Bridge

Complete message schema for the WebSocket connection between the Voice UI and TTS Bridge.

## Connection

```
ws://localhost:8765/ws
```

Auto-reconnect: 5 attempts with exponential backoff (2s, 4s, 6s, 8s, 10s)

## Message Types

### UI → Bridge

#### 1. Generate TTS
```json
{
  "type": "tts",
  "text": "Sir, the deployment is complete.",
  "provider": "elevenlabs",
  "speed": 1.0,
  "instructions": "Speak in a calm, professional British accent."
}
```

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| type | Yes | string | Must be "tts" |
| text | Yes | string | Text to synthesize |
| provider | No | string | TTS provider override (edge, elevenlabs, openai, minimax, xai, mistral, gemini, neutts, kittentts, piper) |
| speed | No | float | Playback speed 0.25-4.0 |
| instructions | No | string | Voice design guidance (OpenAI-compatible only) |

#### 2. Manual State Change
```json
{
  "type": "state",
  "state": "speaking",
  "text": "Processing request..."
}
```

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| type | Yes | string | Must be "state" |
| state | Yes | string | One of: "idle", "listening", "speaking", "thinking" |
| text | No | string | Optional display text |

#### 3. Heartbeat
```json
{
  "type": "ping"
}
```
Response: `{"type": "pong"}`

---

### Bridge → UI

#### 1. Initial Sync (sent on connect)
```json
{
  "type": "init",
  "state": "idle",
  "amplitude": 0.0,
  "waveform": [0.0, 0.0, ...],  // 64 floats
  "timestamp": 1722789123.456
}
```

#### 2. State Change
```json
{
  "type": "state_change",
  "state": "speaking",
  "text": "Sir, the deployment is complete.",
  "timestamp": 1722789123.456
}
```

| Field | Type | Description |
|-------|------|-------------|
| type | string | "state_change" |
| state | string | New state: "idle" \| "listening" \| "speaking" \| "thinking" |
| text | string | Associated text (truncated for display) |
| timestamp | float | Unix timestamp |

#### 3. Audio Update (sent ~20fps during active states)
```json
{
  "type": "audio_update",
  "amplitude": 0.73,
  "waveform": [0.12, 0.45, 0.89, ...],  // 64 floats [0,1]
  "timestamp": 1722789123.456
}
```

| Field | Type | Description |
|-------|------|-------------|
| type | string | "audio_update" |
| amplitude | float | Overall RMS amplitude [0,1] |
| waveform | float[64] | Frequency bars for visualization |
| timestamp | float | Unix timestamp |

#### 4. Heartbeat Response
```json
{
  "type": "pong"
}
```

---

## State Machine

```
                    ┌─────────────┐
                    │    IDLE     │
                    └──────┬──────┘
                           │ user message / TTS request
                           ▼
              ┌────────────────────────┐
              │      LISTENING         │ ◄─── idle timeout / no input
              └───────────┬────────────┘
                          │ TTS starts
                          ▼
               ┌────────────────────┐
               │     SPEAKING       │ ◄─── TTS generation
               └─────────┬──────────┘
                         │ TTS complete
                         ▼
               ┌────────────────────┐
               │     LISTENING      │ ◄─── awaiting next input
               └─────────┬──────────┘
                         │ thinking request
                         ▼
               ┌────────────────────┐
               │     THINKING       │ ◄─── processing/reasoning
               └─────────┬──────────┘
                         │ thinking done
                         ▼
               ┌────────────────────┐
               │     SPEAKING       │ ◄─── response generation
               └────────────────────┘
```

## Audio Waveform Details

The `waveform` array contains 64 float values representing frequency bins:

- **Indices 0-7**: Sub-bass / rumble (20-60 Hz)
- **Indices 8-15**: Bass (60-250 Hz)
- **Indices 16-31**: Low-mid (250-1000 Hz) — **formant region**
- **Indices 32-47**: Mid (1-4 kHz) — **speech clarity**
- **Indices 48-63**: High-mid / presence (4-8 kHz)

During SPEAKING, the bridge simulates formant-like frequencies using overlapping sine waves at ~12Hz, ~7Hz, ~19Hz, ~3Hz base rates per bin.

## Error Handling

Bridge sends error state via state_change with error text:
```json
{
  "type": "state_change",
  "state": "idle",
  "text": "TTS Error: ELEVENLABS_API_KEY not set",
  "timestamp": 1722789123.456
}
```

UI should display error in state display briefly, then return to IDLE.

## Reconnection Protocol

1. On `ws.onclose`: wait 2s × attempt_number
2. Max 5 attempts
3. On reconnect: bridge sends `init` message for full state sync
4. UI should not queue messages during disconnect

## Rate Limits

- **Audio updates**: ~20/second (50ms interval) during SPEAKING/LISTENING
- **Audio updates**: ~2/second during IDLE/THINKING
- **State changes**: Event-driven, no limit
- **TTS requests**: Serialized by bridge, one at a time

## Example Session

```javascript
// Connect
ws = new WebSocket('ws://localhost:8765/ws');

ws.onmessage = (event) => {
  const msg = JSON.parse(event.data);
  
  switch(msg.type) {
    case 'init':
      // Full state sync
      setState(msg.state);
      currentAmplitude = msg.amplitude;
      waveformBars = msg.waveform;
      break;
      
    case 'state_change':
      setState(msg.state);
      break;
      
    case 'audio_update':
      currentAmplitude = msg.amplitude;
      waveformBars = msg.waveform;
      break;
  }
};

// Trigger TTS
ws.send(JSON.stringify({
  type: 'tts',
  text: 'Hello from JARVIS',
  provider: 'elevenlabs'
}));

// Manual state
ws.send(JSON.stringify({
  type: 'state',
  state: 'thinking',
  text: 'Analyzing...'
}));
```