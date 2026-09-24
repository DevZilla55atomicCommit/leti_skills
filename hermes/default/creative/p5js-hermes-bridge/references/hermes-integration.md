# Hermes Integration Patterns — p5.js ↔ Hermes TTS Bridge

How to connect Hermes hooks, skills, and cron jobs to the JARVIS bridge for real-time UI sync.

## Prerequisites

- Bridge running: `~/.hermes/hermes-agent/venv/bin/python scripts/jarvis_tts_bridge.py --port 8765`
- `requests` available in Hermes venv (installed by default)

---

## 1. TTS State Sync (Hooks)

Add to your Hermes TTS hook or skill that wraps `text_to_speech_tool`:

```python
# In a skill or hook file
import requests

BRIDGE_URL = "http://localhost:8765"

def bridge_set_state(state: str, text: str = ""):
    """Send state change to JARVIS bridge."""
    try:
        requests.post(
            f"{BRIDGE_URL}/state",
            json={"state": state, "text": text[:80]},
            timeout=1.0
        )
    except Exception as e:
        # Non-blocking - UI sync is best-effort
        pass

def bridge_tts(text: str, provider: str = None):
    """Trigger TTS via bridge (also sets speaking state)."""
    try:
        payload = {"text": text}
        if provider:
            payload["provider"] = provider
        requests.post(f"{BRIDGE_URL}/tts", json=payload, timeout=5.0)
    except Exception:
        pass
```

### Auto-TTS Hook Integration

In `~/.hermes/hooks/hooks.json` or a custom hook:

```json
{
  "hooks": [
    {
      "event": "PreToolUse",
      "matcher": "text_to_speech_tool",
      "command": "python3 -c \"import requests; requests.post('http://localhost:8765/state', json={'state': 'speaking', 'text': 'TTS starting...'}, timeout=1)\""
    },
    {
      "event": "PostToolUse", 
      "matcher": "text_to_speech_tool",
      "command": "python3 -c \"import requests; requests.post('http://localhost:8765/state', json={'state': 'listening'}, timeout=1)\""
    }
  ]
}
```

---

## 2. Session State Sync (Skills)

From any Hermes skill that runs agent work:

```python
# In a skill's Python helper or agent
import requests

def sync_ui_to_agent_state(agent_name: str, phase: str, detail: str = ""):
    """Map agent phases to JARVIS states."""
    state_map = {
        "planner": ("thinking", "Planning..."),
        "code-reviewer": ("thinking", "Reviewing code..."),
        "security-reviewer": ("thinking", "Security scan..."),
        "tdd-guide": ("thinking", "Writing tests..."),
        "architect": ("thinking", "Designing..."),
        "build-error-resolver": ("speaking", "Fixing build..."),
    }
    
    state, default_text = state_map.get(agent_name, ("thinking", "Working..."))
    text = detail or default_text
    
    try:
        requests.post(
            "http://localhost:8765/state",
            json={"state": state, "text": text},
            timeout=0.5
        )
    except Exception:
        pass

# Usage in skill
sync_ui_to_agent_state("planner", "start", "Breaking down feature...")
# ... do work ...
sync_ui_to_agent_state("planner", "done", "Plan ready")
```

---

## 3. Cron Job Integration

Scheduled jobs can announce themselves:

```python
# In a cron job script
import requests
import time

BRIDGE = "http://localhost:8765"

def cron_announce(job_name: str, phase: str, detail: str = ""):
    state = "speaking" if phase in ("start", "done") else "thinking"
    requests.post(f"{BRIDGE}/state", 
        json={"state": state, "text": f"{job_name}: {detail or phase}"},
        timeout=1)

# Example cron job
cron_announce("daily-backup", "start", "Starting backup...")
# ... do backup ...
cron_announce("daily-backup", "done", "Backup complete")
```

Or use the TTS endpoint for voice announcements:

```python
requests.post(f"{BRIDGE}/tts",
    json={"text": "Daily backup completed successfully.", "provider": "elevenlabs"},
    timeout=10)
```

---

## 4. Streaming TTS (Advanced)

For real-time audio level streaming during TTS generation, extend the bridge:

### Server-side (in `jarvis_tts_bridge.py`)

```python
async def stream_tts_with_levels(text: str, provider: str = None):
    """Generate TTS and stream audio levels via WebSocket."""
    from tools.tts_tool import text_to_speech_tool
    from tools.tts_streaming import stream_tts  # if available
    
    await jarvis.set_state("speaking", text)
    
    # If provider supports streaming (OpenAI, ElevenLabs)
    async for chunk in stream_tts(text, provider):
        # Compute RMS level from chunk
        level = compute_rms(chunk)
        waveform = compute_fft(chunk)
        await jarvis.update_audio(level, waveform)
        # Forward chunk to client if needed
    
    await jarvis.set_state("listening")
```

### Client-side (p5.js)

```javascript
// Already handled by audio_update messages
// waveformBars updates at ~20Hz during speaking
```

---

## 5. Multi-Platform Notes

| Platform | Bridge Access | Notes |
|----------|---------------|-------|
| Desktop (TUI/CLI) | `localhost:8765` | Direct |
| Telegram/Discord | `localhost:8765` | Direct from gateway |
| Cron | `localhost:8765` | Direct from scheduler |
| Skills | `localhost:8765` | Direct from skill Python |
| Remote SSH | Tunnel required | `ssh -L 8765:localhost:8765 user@host` |

---

## 6. Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| `Connection refused` | Bridge not running | Start bridge script |
| State not updating | Firewall/port | Check `ufw status`, port 8765 |
| TTS fails silently | No provider configured | Check `tts.provider` in config.yaml |
| ElevenLabs 401 | API key missing | Add `ELEVENLABS_API_KEY` to `~/.hermes/.env` |
| WebSocket drops | Network blip | Client auto-reconnects (max 5x) |

---

## 7. Example: Full Skill with Bridge

```python
# skills/my-voice-skill/skill.py
from skills.my_voice_skill.bridge import bridge_set_state, bridge_tts

class MyVoiceSkill:
    def run(self, task: str):
        bridge_set_state("thinking", f"Analyzing: {task[:40]}")
        
        # ... do work ...
        
        bridge_tts("Analysis complete. Here are the findings.")
        bridge_set_state("listening")
```

---

## Files

| File | Purpose |
|------|---------|
| `scripts/jarvis_tts_bridge.py` | Bridge server |
| `templates/jarvis-voice-ui.html` | Example UI |
| `references/websocket-protocol.md` | Message spec |
| `references/hermes-integration.md` | This file |