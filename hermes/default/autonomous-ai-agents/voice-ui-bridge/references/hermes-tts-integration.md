# Hermes TTS Integration — Voice UI Bridge

How to use Hermes' built-in `text_to_speech_tool` from external scripts and skills.

## Overview

Hermes provides a unified TTS tool (`tools.tts_tool.text_to_speech_tool`) that abstracts multiple providers:

| Provider | Quality | Speed | API Key Required | Native Opus |
|----------|---------|-------|------------------|-------------|
| Edge TTS | Good | Fast | No | No (needs ffmpeg) |
| ElevenLabs | Excellent | Medium | Yes | Yes |
| OpenAI TTS | Good | Medium | Yes | Yes |
| Mistral (Voxtral) | Good | Fast | Yes | Yes |
| MiniMax | Excellent | Medium | Yes | No |
| xAI | Good | Fast | Yes | No |
| Gemini | Good | Medium | Yes | No |
| NeuTTS (local) | Fair | Fast | No | No |
| KittenTTS (local) | Fair | Fast | No | No |
| Piper (local) | Good | Fast | No | No |

## Basic Usage (from Python)

```python
# Add Hermes to path
import sys
from pathlib import Path
HERMES_AGENT = Path.home() / ".hermes" / "hermes-agent"
sys.path.insert(0, str(HERMES_AGENT))

from tools.tts_tool import text_to_speech_tool
import json

# Simple generation
result = text_to_speech_tool(text="Hello from Hermes!")
print(json.loads(result))
```

**Output:**
```json
{
  "success": true,
  "file_path": "/Users/alfred/.hermes/cache/audio/tts_20260804_143022_123456.mp3",
  "media_tag": "MEDIA:/Users/alfred/.hermes/cache/audio/tts_20260804_143022_123456.mp3",
  "provider": "edge",
  "voice_compatible": false
}
```

## Parameters

```python
result = text_to_speech_tool(
    text="Hello world",           # Required: text to synthesize
    output_path=None,             # Optional: custom save path
    speed=1.0,                    # Optional: 0.25-4.0 playback speed
    instructions=None,            # Optional: voice design (OpenAI only)
    provider="elevenlabs"         # Optional: override configured provider
)
```

## Provider Configuration

Hermes reads config from `~/.hermes/config.yaml`:

```yaml
tts:
  provider: elevenlabs
  elevenlabs:
    voice_id: pNInz6obpgDQGcFmaJgB  # Adam (default)
    model_id: eleven_multilingual_v2
  openai:
    model: gpt-4o-mini-tts
    voice: echo
  edge:
    voice: en-US-AriaNeural
```

### ElevenLabs Setup (Required for Your Voice)

```bash
# 1. Get API key from elevenlabs.io
# 2. Add to ~/.hermes/.env
ELEVENLABS_API_KEY=your_actual_key_here

# 3. List voices to find your preferred one
python -c "
import os
from elevenlabs.client import ElevenLabs
client = ElevenLabs(api_key=os.environ['ELEVENLABS_API_KEY'])
for v in client.voices.get_all().voices:
    print(f'{v.voice_id}: {v.name}')
"
```

### Voice Recommendations for JARVIS

| Voice ID | Name | Style |
|----------|------|-------|
| pNInz6obpgDQGcFmaJgB | Adam | Deep, professional (default) |
| 21m00Tcm4TlvDq8ikWAM | Rachel | Clear, professional |
| EXAVITQu4vr4xnSDxMaL | Bella | Warm, friendly |
| ErXwobaYiN019PkySvjV | Antoni | Deep, authoritative |
| TX3LPaxmHKxFdv7VOQHJ | Josh | Professional, articulate |

For British female (your preference):
- Use OpenAI `nova` or `shimmer` with `instructions: "Speak in a youthful, professional British accent"`
- Or ElevenLabs custom voice

## Advanced: Streaming TTS (Low Latency)

For real-time voice UI, use streaming:

```python
# Hermes internal - for reference
from tools.tts_streaming import stream_tts

async for chunk in stream_tts(text="Long text...", provider="elevenlabs"):
    # chunk is raw audio bytes (Opus/MP3)
    await websocket.send(chunk)
```

## Output Formats & Platform Delivery

| Platform | Format | Delivery |
|----------|--------|----------|
| Telegram | Opus (.ogg) | Native voice bubble |
| Discord | Opus | Voice message |
| WhatsApp | Opus | Voice note |
| Slack | MP3 | File upload |
| CLI | MP3 | Saved to `~/voice-memos/` |

Hermes auto-converts Edge TTS MP3 → Opus via ffmpeg for Telegram.

## Error Handling

```python
result = json.loads(text_to_speech_tool(text="Test"))

if not result["success"]:
    error = result["error"]
    if "ELEVENLABS_API_KEY not set" in error:
        # Fallback to Edge TTS
        result = json.loads(text_to_speech_tool(text="Test", provider="edge"))
    elif "voice_compatible: false" in str(result):
        # Voice doesn't support Opus, will send as file
        pass
    else:
        raise RuntimeError(f"TTS failed: {error}")
```

## Integration with Voice UI Bridge

The bridge calls this exact function:

```python
# In jarvis_tts_bridge.py
from tools.tts_tool import text_to_speech_tool

async def generate_tts(text, provider=None, speed=None, instructions=None):
    result = text_to_speech_tool(
        text=text,
        provider=provider,
        speed=speed,
        instructions=instructions
    )
    return json.loads(result)
```

## Testing TTS from CLI

```bash
# Quick test via Hermes venv
~/.hermes/hermes-agent/venv/bin/python -c "
import sys
sys.path.insert(0, '/Users/alfred/.hermes/hermes-agent')
from tools.tts_tool import text_to_speech_tool
import json
result = text_to_speech_tool(text='Hello from Hermes TTS!')
print(json.dumps(json.loads(result), indent=2))
"
```

## Common Issues

| Issue | Fix |
|-------|-----|
| `ELEVENLABS_API_KEY not set` | Add to `~/.hermes/.env` |
| `voice_compatible: false` | Voice doesn't support Opus, falls back to MP3 |
| `Unauthorized / 401` | Regenerate API key at elevenlabs.io |
| Slow generation | Use `eleven_turbo_v2_5` model or Edge TTS |
| No audio on Telegram | Install ffmpeg: `brew install ffmpeg` |
| TTS text too long | OpenAI: 4096 chars, ElevenLabs: 10k (v2) / 40k (flash) |

## Character Limits by Provider

| Provider | Max Chars |
|----------|-----------|
| OpenAI | 4,096 |
| xAI | 15,000 |
| MiniMax | 10,000 |
| ElevenLabs (v2) | 10,000 |
| ElevenLabs (flash) | 40,000 |
| Mistral | 4,000 |
| Edge | 5,000 |

Long text is auto-truncated with warning.

## In Skill Context

```python
# From a Hermes skill
from tools.tts_tool import text_to_speech_tool

def speak(text, provider=None):
    result = text_to_speech_tool(text=text, provider=provider)
    return json.loads(result)

# With auto-state for voice UI
def speak_with_ui(text, provider=None):
    # Notify UI
    requests.post("http://localhost:8765/state", 
        json={"state": "speaking", "text": text[:50]})
    
    result = speak(text, provider)
    
    # Return to listening
    requests.post("http://localhost:8765/state", 
        json={"state": "listening"})
    return result
```