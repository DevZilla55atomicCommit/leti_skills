---
name: voice-ui-bridge
description: "Build JARVIS voice UI with p5.js/WebGL synced to Hermes TTS."
version: 1.0.0
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [p5js, webgl, websocket, tts, visualization, voice-ui, hermes-integration, fastapi, real-time]
    related_skills: [p5js, tts-elevenlabs-config, hermes-agent]
---

# Voice UI Bridge — Reactive Visualization for Hermes TTS

## When to Use

Use when building a **real-time voice UI visualization** that reacts to Hermes TTS state (idle/listening/speaking/thinking) with professional 3D graphics, waveform animation, and WebSocket synchronization.

**Triggers:**
- "Build a JARVIS-style voice UI"
- "Visualize TTS state in real-time"
- "Connect p5.js/WebGL to Hermes TTS"
- "Create audio-reactive 3D sphere for voice assistant"
- "Build TTS visualization with WebSocket bridge"

## Architecture Overview

```
┌─────────────────┐     WebSocket (ws://localhost:8765/ws)     ┌─────────────────┐
│  Voice UI       │ ◄──────────────────────────────────────────► │  TTS Bridge     │
│  (p5.js/WebGL)  │   State sync + audio levels + commands       │  (FastAPI)      │
└─────────────────┘                                              └─────────────────┘
                                                                       │
                                                                       ▼
                                                            ┌─────────────────┐
                                                            │  Hermes TTS     │
                                                            │  (text_to_speech_│
                                                            │   tool / elevenlabs│
                                                            │   / edge / openai)│
                                                            └─────────────────┘
```

## Components

### 1. Voice UI (p5.js + WebGL)
**File:** `templates/jarvis-voice-ui.html`

**Features:**
- **5 visual modes**: Wireframe Sphere, Particle Field, Concentric Rings, DNA Helix, Torus Knot
- **4 TTS states**: IDLE (slow pulse, muted blue), LISTENING (amber pulse, subtle wave), SPEAKING (mint green, high-freq waveform, pulse rings), THINKING (purple rhythmic, helix mode)
- **Real-time waveform**: 64-bar frequency visualization at bottom
- **Pulse rings**: CSS-animated expanding rings during SPEAKING/LISTENING
- **Core glow**: Multi-layer breathing core at center
- **Camera orbit**: Slow auto-orbit for 3D depth
- **Mouse interaction**: Click/drag adds velocity bursts
- **Hotkeys**: 1-4=states, Space=auto-cycle, S=PNG, G=GIF, R=new seed

### 2. TTS Bridge (FastAPI + WebSocket)
**File:** `templates/jarvis_tts_bridge.py`

**Endpoints:**
- `GET /health` — Bridge status
- `POST /tts` — Generate TTS via Hermes (`{text, provider?, speed?, instructions?}`)
- `POST /state` — Manual state control (`{state, text?}`)
- `WS /ws` — Real-time bidirectional sync

**WebSocket Messages:**
```json
// UI → Bridge
{"type": "tts", "text": "Hello", "provider": "elevenlabs"}
{"type": "state", "state": "speaking", "text": "Processing..."}

// Bridge → UI
{"type": "init", "state": "idle", "amplitude": 0, "waveform": [...]}
{"type": "state_change", "state": "speaking"}
{"type": "audio_update", "amplitude": 0.8, "waveform": [...]}
```

## Quick Start

### 1. Start the Bridge
```bash
cd ~/.hermes/hermes-agent
source venv/bin/activate
python /path/to/jarvis_tts_bridge.py --port 8765
```

### 2. Open the UI
```bash
open /path/to/jarvis-voice-ui.html
# Or serve via bridge: http://localhost:8765/ui/jarvis-voice-ui.html
```

### 3. Connect
Click **"Connect Bridge"** button (green) → status shows "Connected"

### 4. Test TTS
```bash
curl -X POST http://localhost:8765/tts \
  -H "Content-Type: application/json" \
  -d '{"text": "Sir, the deployment is complete.", "provider": "elevenlabs"}'
```

## Configuration

### Hermes TTS Setup (required for ElevenLabs)
```bash
# ~/.hermes/.env
ELEVENLABS_API_KEY=your_key_here

# ~/.hermes/config.yaml
tts:
  provider: elevenlabs
  elevenlabs:
    voice_id: YOUR_VOICE_ID  # e.g., pNInz6obpgDQGcFmaJgB (Adam)
    model_id: eleven_multilingual_v2
```

### Bridge Configuration
```python
# In jarvis_tts_bridge.py or via CLI
WS_URL = "ws://localhost:8765/ws"  # Default
WS_MAX_RECONNECT = 5               # Auto-reconnect attempts
```

## Visual Modes Reference

| Mode | Best For | Description |
|------|----------|-------------|
| `sphere` | Default, speaking | Multi-shell wireframe sphere with noise displacement |
| `particles` | Listening, ambient | 3000 orbital particles with depth sorting + connections |
| `rings` | Thinking, processing | 12 rotating rings with independent speeds |
| `helix` | Thinking, analysis | Double helix with animated base pairs |
| `torus` | Complex states | Particles flowing along (3,7) torus knot |

## State Color Palette

| State | Primary | Pulse Speed | Pulse Amp | Use Case |
|-------|---------|-------------|-----------|----------|
| `idle` | `#446688` | 0.3 Hz | 0.15 | Waiting, no activity |
| `listening` | `#ffcc00` | 1.5 Hz | 0.35 | Awaiting user input |
| `speaking` | `#00ff88` | 8 Hz | 0.6 | TTS actively generating |
| `thinking` | `#cc88ff` | 0.8 Hz | 0.25 | Processing, reasoning |

## Integration Patterns

### From Hermes Skill/Hook
```python
import requests

BRIDGE = "http://localhost:8765"

def on_tts_start(text):
    requests.post(f"{BRIDGE}/state", json={"state": "speaking", "text": text[:50]})

def on_tts_end():
    requests.post(f"{BRIDGE}/state", json={"state": "listening"})

def on_user_message():
    requests.post(f"{BRIDGE}/state", json={"state": "thinking"})

def on_thinking_done():
    requests.post(f"{BRIDGE}/state", json={"state": "speaking"})
```

### From Cron Job (auto-status)
```bash
# In hermes cron job
curl -X POST http://localhost:8765/state \
  -H "Content-Type: application/json" \
  -d '{"state": "idle"}'
```

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Canvas black, no sphere | `new p5()` not called | Ensure `new p5()` in DOMContentLoaded |
| Bridge: Disconnected | Bridge not running | Start `python jarvis_tts_bridge.py` |
| WebSocket fails | CORS / port blocked | Check firewall, use `0.0.0.0:8765` |
| No audio on SPEAKING | ElevenLabs key missing | Add `ELEVENLABS_API_KEY` to `.env` |
| TTS fails silently | Provider not installed | `pip install elevenlabs` or use `edge` |
| Waveform static | UI not receiving audio_update | Check WS connection, bridge `simulate_audio()` |
| Particle count wrong | Slider not wired | Verify `particleCount` event listener |

## Performance Targets

| Metric | Target |
|--------|--------|
| Frame rate (interactive) | 60fps sustained |
| Particle count (WebGL) | 3,000-15,000 at 60fps |
| WebSocket latency | < 50ms local |
| TTS generation (Edge) | < 500ms |
| TTS generation (ElevenLabs) | < 2s |
| Memory (UI) | < 100MB |

## Customization Points

### Add Custom Visual Mode
```javascript
// In CONFIG.visualMode switch, add:
case 'custom':
  renderCustomMode(state);
  break;

// Implement renderCustomMode(state) following renderWireframeSphere pattern
```

### Add Custom State
```javascript
// In STATES object:
custom: { color: '#ff00ff', pulseSpeed: 2, pulseAmp: 0.4, rotation: 0.002, noiseScale: 0.005 }

// In setState(), add button + key handler
```

### Use Instance Mode (multiple UIs)
```javascript
const sketch = (p) => {
  p.setup = () => { p.createCanvas(800, 600, p.WEBGL); };
  p.draw = () => { /* ... */ };
};
new p5(sketch, 'canvas-container-1');
new p5(sketch, 'canvas-container-2');
```

## Templates Included

| File | Description |
|------|-------------|
| `templates/jarvis-voice-ui.html` | Complete standalone UI (single HTML) |
| `templates/jarvis_tts_bridge.py` | FastAPI WebSocket bridge server |

## References

- `references/p5js-patterns.md` — p5.js WebGL best practices from this project
- `references/websocket-protocol.md` — Full WebSocket message schema
- `references/hermes-tts-integration.md` — Hermes TTS tool usage patterns
- `references/performance-tuning.md` — WebGL particle optimization tips

## Changelog

- **1.0.0** — Initial release: JARVIS UI + FastAPI bridge + Hermes TTS integration