# WebSocket Protocol — p5.js ↔ Hermes TTS Bridge

Complete message specification for the WebSocket bridge between p5.js UIs and Hermes TTS.

## Connection

```
WebSocket URL: ws://localhost:8765/ws
Protocol: Plain WebSocket (no subprotocols)
Auto-reconnect: Client handles (max 5 attempts, exponential backoff)
Heartbeat: Ping/pong (client sends `{"type":"ping"}`, server responds `{"type":"pong"}`)
```

---

## Client → Server Messages

### 1. Trigger TTS Generation
```json
{
  "type": "tts",
  "text": "string (required)",
  "provider": "string (optional) — edge, elevenlabs, openai, minimax, xai, mistral, gemini, neutts, kittentts, piper",
  "speed": "number (optional) — 0.25 to 4.0",
  "instructions": "string (optional) — voice design guidance for OpenAI-compatible backends"
}
```

**Response:** Server processes via Hermes `text_to_speech_tool`, broadcasts `state_change` → `speaking`, then `audio_update` during generation, then `state_change` → `listening` when done.

### 2. Force State Change
```json
{
  "type": "state",
  "state": "string (required) — idle, listening, speaking, thinking",
  "text": "string (optional) — displayed in UI state badge"
}
```

**Response:** Immediate broadcast of `state_change` to all clients.

### 3. Heartbeat
```json
{"type": "ping"}
```

**Response:** `{"type": "pong"}`

---

## Server → Client Messages

### 1. Initial Sync (on connect)
```json
{
  "type": "init",
  "state": "string — current state (idle|listening|speaking|thinking)",
  "amplitude": "number — 0.0 to 1.0",
  "waveform": "number[64] — normalized waveform bar heights (0.0 to 1.0)",
  "timestamp": "number — epoch ms"
}
```

### 2. State Change
```json
{
  "type": "state_change",
  "state": "string — idle|listening|speaking|thinking",
  "text": "string — display text (truncated to ~50 chars)",
  "timestamp": "number — epoch ms"
}
```

### 3. Audio Level Update
```json
{
  "type": "audio_update",
  "amplitude": "number — 0.0 to 1.0 (peak level)",
  "waveform": "number[64] — per-bar heights for visualization",
  "timestamp": "number — epoch ms"
}
```
Sent at ~20Hz during speaking state; sparse in other states.

### 4. Heartbeat Response
```json
{"type": "pong"}
```

---

## State Definitions

| State | Color | Animation | Typical Trigger |
|-------|-------|-----------|-----------------|
| `idle` | Muted blue | Slow breathing pulse (0.3Hz) | No activity |
| `listening` | Amber | Medium pulse (1.5Hz), subtle waveform | Awaiting user input |
| `speaking` | Mint green | Fast pulse (8Hz), full waveform, pulse rings | Hermes TTS active |
| `thinking` | Purple | Rhythmic pulse (0.8Hz) | Agent processing |

---

## HTTP Endpoints (Alternative to WS)

### GET /health
```json
{"status": "ok", "state": "idle"}
```

### POST /tts
```json
{"text": "Hello", "provider": "elevenlabs", "speed": 1.2, "instructions": "Cheerful"}
```
Returns Hermes TTS tool result:
```json
{"success": true, "file_path": "...", "media_tag": "MEDIA:...", "provider": "elevenlabs"}
```

### POST /state
```json
{"state": "speaking", "text": "Processing request..."}
```

---

## Error Handling

- Invalid JSON → connection stays open, error logged server-side
- Unknown `type` → logged, ignored
- TTS failure → `state_change` to `listening`, error logged
- WebSocket close → server cleans up client, broadcasts continue to others

---

## Implementation Notes

- All timestamps: `Date.now()` (epoch milliseconds)
- Waveform array always length 64, values 0.0–1.0
- Amplitude is peak level, not RMS
- Bridge runs in Hermes venv (has `fastapi`, `uvicorn`, `pydantic`)
- Calls `tools.tts_tool.text_to_speech_tool` — respects `tts.provider` config
- Audio files saved to `~/.hermes/cache/audio/tts_*.mp3` (or `.ogg` for Opus)