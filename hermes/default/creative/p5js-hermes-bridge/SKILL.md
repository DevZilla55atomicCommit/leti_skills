---
name: p5js-hermes-bridge
description: "Bridge p5.js UIs to Hermes TTS via local WebSocket server."
version: 1.0.0
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [p5js, websocket, tts, hermes, bridge, real-time, voice-ui]
    related_skills: [p5js, tts-elevenlabs-config, hermes-agent]
---

# p5.js ↔ Hermes TTS Bridge

Pattern for connecting browser-based p5.js visualizations to Hermes Agent's TTS system via a local WebSocket/FastAPI bridge.

## When to Use

- Building reactive voice UIs (JARVIS-style spheres, audio visualizers, speaking avatars)
- Need real-time TTS state sync (idle/listening/speaking/thinking) from Hermes to browser
- Want to trigger TTS from browser UI and have Hermes generate audio
- Building dashboards that reflect Hermes session state live
- Creating "operator console" visualizations for Hermes/agent work

## Architecture

```
┌──────────────────┐     WebSocket      ┌─────────────────┐
│  p5.js UI        │ ◄─────────────────► │  Bridge Server  │
│  (browser)       │   state/audio sync  │  (FastAPI)      │
└──────────────────┘                     └────────┬────────┘
                                                  │
                                                  ▼
                                         ┌──────────────────┐
                                         │  Hermes TTS      │
                                         │  text_to_speech_ │
                                         │  _tool           │
                                         └──────────────────┘
```

## Components

### 1. Bridge Server (`scripts/jarvis_tts_bridge.py`)

FastAPI + WebSocket server that:
- Maintains shared `JarvisState` (state, amplitude, waveform, connected clients)
- Exposes `/ws` for real-time sync, `/tts` and `/state` HTTP endpoints
- Calls Hermes' `text_to_speech_tool` programmatically
- Auto-reconnects clients, heartbeats via ping/pong

Key classes:
```python
class JarvisState:
    state: str  # idle, listening, speaking, thinking
    amplitude: float
    waveform: list[float]
    websocket_clients: set

async def generate_tts(text, provider=None, speed=None, instructions=None) -> dict:
    from tools.tts_tool import text_to_speech_tool
    return json.loads(text_to_speech_tool(text=text, provider=provider, ...))
```

### 2. p5.js Client (embedded in sketch)

```javascript
let ws = new WebSocket('ws://localhost:8765/ws');
ws.onmessage = (event) => {
  const msg = JSON.parse(event.data);
  switch (msg.type) {
    case 'init': setState(msg.state); currentAmplitude = msg.amplitude; break;
    case 'state_change': setState(msg.state); break;
    case 'audio_update': currentAmplitude = msg.amplitude; waveformBars = msg.waveform; break;
  }
};
function sendTTS(text) { ws.send(JSON.stringify({type: 'tts', text})); }
```

### 3. Hermes Integration

```python
import requests

# From hooks/skills - sync UI to Hermes TTS state
def on_tts_start(text):
    requests.post("http://localhost:8765/state",
        json={"state": "speaking", "text": text[:50]})

def on_tts_end():
    requests.post("http://localhost:8765/state",
        json={"state": "listening"})

# Trigger TTS from Hermes
requests.post("http://localhost:8765/tts",
    json={"text": "Deployment complete, sir.", "provider": "elevenlabs"})
```

## Running

```bash
# From Hermes venv (has fastapi, uvicorn, pydantic)
~/.hermes/hermes-agent/venv/bin/python scripts/jarvis_tts_bridge.py --port 8765

# Health check
curl http://localhost:8765/health
# {"status":"ok","state":"idle"}
```

## WebSocket Protocol

**Client → Server:**
```json
{"type": "tts", "text": "Hello", "provider": "edge", "speed": 1.0}
{"type": "state", "state": "speaking", "text": "Processing..."}
{"type": "ping"}
```

**Server → Client:**
```json
{"type": "init", "state": "idle", "amplitude": 0.0, "waveform": [...]}
{"type": "state_change", "state": "speaking", "text": "Hello", "timestamp": 1234567890}
{"type": "audio_update", "amplitude": 0.75, "waveform": [...], "timestamp": 1234567890}
{"type": "pong"}
```

## HTTP Endpoints

| Method | Path | Body | Description |
|--------|------|------|-------------|
| GET | `/health` | — | Bridge status |
| POST | `/tts` | `{text, provider?, speed?, instructions?}` | Generate TTS via Hermes |
| POST | `/state` | `{state, text?}` | Force UI state change |
| WS | `/ws` | — | Real-time bidirectional sync |

## Example UI

See `templates/jarvis-voice-ui.html` — a complete JARVIS-style reactive sphere with:
- 5 visual modes (sphere, particles, rings, helix, torus knot)
- 4 states (idle, listening, speaking, thinking) with distinct colors/animations
- Live waveform bars driven by simulated/formant audio
- Bridge connect/disconnect button with auto-reconnect
- State buttons + keyboard shortcuts (1-4, Space, S/G/R)

## Integration Notes

## Pitfalls
- **Bridge not running**: Ensure the FastAPI process is started (use `background=true, notify_on_complete=true`). Verify with `curl http://localhost:8765/health`. If you see a connection error, the port may be in use or the script terminated; check the Hermes logs for traceback.
- **WebSocket connection fails**: Confirm the client URL matches the server (`ws://localhost:8765/ws`). If you see “Failed to connect”, the bridge might not be listening on the expected interface; run `netstat -an | grep 8765` to confirm.
- **Pane appears blank**: Open the developer console (⌘Option+I) and look for JavaScript errors. Common mistakes: forgetting to import `@hermes/plugin-sdk`, using JSX syntax, or not calling `ctx.register` correctly.
- **Particle performance**: On older Mac hardware, reduce `PARTICLE_COUNT` (e.g., from 300 to 150) in `plugin.js` to keep CPU usage low.
- **State not updating**: Make sure the bridge sends an initial `init` message; otherwise the UI will stay in the default idle state.



- **TTS Provider**: Uses Hermes configured provider (`tts.provider` in config.yaml). Override per-call via `provider` param.
- **Audio Output**: Files saved to `~/.hermes/cache/audio/tts_*.mp3` (or `.ogg` for Telegram with Opus providers)
- **ElevenLabs**: Set `ELEVENLABS_API_KEY` in `~/.hermes/.env` for premium voices
- **Microphone Input**: Replace `simulateAudio()` with Web Audio `AnalyserNode` for true live reactivity
- **Multi-client**: Bridge broadcasts to all connected WebSocket clients

## Files in This Skill

| Path | Purpose |
|------|---------|
| `scripts/jarvis_tts_bridge.py` | Bridge server (FastAPI + WebSocket) |
| `templates/jarvis-voice-ui.html` | Complete example p5.js UI |
| `references/websocket-protocol.md` | Full message spec |
| `references/hermes-integration.md` | Hook/skill integration patterns |

## Related Skills

- `p5js` — Core p5.js production pipeline
- `tts-elevenlabs-config` — ElevenLabs setup in Hermes
- `hermes-agent` — Hermes configuration and tooling