---
name: tts-elevenlabs-config
description: ElevenLabs TTS configuration, testing, and troubleshooting for Hermes Agent. Covers config.yaml setup, .env API key management, voice selection, gateway integration, and validation scripts.
tags: [hermes, tts, elevenlabs, voice, text-to-speech, gateway, telegram, discord, voice-messages]
version: 1.0.0
author: Alfred Kamisese
license: MIT
metadata:
  hermes:
    tags: [hermes, tts, elevenlabs, voice, text-to-speech, gateway, telegram, discord, voice-messages]
---

# ElevenLabs TTS Configuration for Hermes Agent

Complete workflow for setting up, testing, and troubleshooting ElevenLabs text-to-speech in Hermes Agent — from config.yaml to gateway voice delivery.

## When to Use

- First-time ElevenLabs TTS setup in Hermes
- Voice not working on messaging platforms (Telegram, Discord, Slack)
- Need to verify/change voice_id or model_id
- Debugging "ELEVENLABS_API_KEY not set" errors
- Testing voice output before enabling `/voice tts`

## Quick Start

### 1. Get ElevenLabs API Key

1. Sign up at https://elevenlabs.io
2. Go to Profile → API Key → Copy
3. Add to `~/.hermes/.env`:

```bash
ELEVENLABS_API_KEY=your_actual_key_here
```

### 2. Pick a Voice

```bash
# List your voices (requires API key in env)
~/.hermes/hermes-agent/venv/bin/python -c "
import os
os.environ['ELEVENLABS_API_KEY'] = 'your_key'
from elevenlabs.client import ElevenLabs
client = ElevenLabs(api_key=os.environ['ELEVENLABS_API_KEY'])
for v in client.voices.get_all().voices:
    print(f'{v.voice_id}: {v.name}')
"
```

### 3. Configure Hermes

**~/.hermes/config.yaml** (tts section):

```yaml
tts:
  provider: elevenlabs
  use_gateway: true
  elevenlabs:
    voice_id: YOUR_VOICE_ID_HERE
    model_id: eleven_multilingual_v2
```

### 4. Test

```bash
# Via Hermes TTS tool
~/.hermes/hermes-agent/venv/bin/python -c "
import sys
sys.path.insert(0, '/Users/alfredkamisese/.hermes/hermes-agent')
from tools.tts_tool import text_to_speech_tool
import json
result = text_to_speech_tool(text='Hello from Hermes ElevenLabs TTS!')
print(json.dumps(json.loads(result), indent=2))
"
```

Expected: `{"success": true, "file_path": "...", "media_tag": "MEDIA:...", "provider": "elevenlabs"}`

## Architecture

```
User message → Hermes Agent → TTS Tool → ElevenLabs API → MP3 file
                                    ↓
                            Gateway intercepts MEDIA tag
                                    ↓
                            Platform-native voice message
```

- **Config source**: `~/.hermes/config.yaml` (voice_id, model_id)
- **Secrets source**: `~/.hermes/.env` (ELEVENLABS_API_KEY)
- **Output**: `~/.hermes/cache/audio/tts_*.mp3` or `~/voice-memos/`
- **Gateway**: Delivers as native voice bubble on Telegram/Discord/Slack/WhatsApp

## Voice Selection Guide

| Model ID | Best For | Latency | Quality |
|----------|----------|---------|---------|
| `eleven_multilingual_v2` | General, multilingual | Medium | High |
| `eleven_turbo_v2_5` | Speed, real-time | Low | Good |
| `eleven_flash_v2_5` | Maximum speed | Lowest | Fair |

**Recommended**: `eleven_multilingual_v2` for quality, `eleven_turbo_v2_5` for speed.

## Gateway Integration

`use_gateway: true` enables platform-native voice delivery:

| Platform | Format | Notes |
|----------|--------|-------|
| Telegram | Opus (.ogg) | Native voice bubble ✅ |
| Discord | Opus | Voice message ✅ |
| Slack | MP3 | File upload ✅ |
| WhatsApp | Opus | Voice note ✅ |
| Signal | Opus | Voice message ✅ |
| CLI | MP3 | Saved to `~/voice-memos/` |

**Telegram Opus requirement**: Voice must support Opus output. If `voice_compatible: false`, falls back to MP3 file upload.

## Common Issues

| Symptom | Cause | Fix |
|---------|-------|-----|
| `ELEVENLABS_API_KEY not set` | Key missing from .env | Add to `~/.hermes/.env` |
| `voice_compatible: false` | Voice doesn't support Opus | Use different voice or accept MP3 fallback |
| No audio on Telegram | FFmpeg missing for conversion | `brew install ffmpeg` |
| "Unauthorized" / 401 | Invalid/expired API key | Regenerate key at elevenlabs.io |
| Voice not found | Wrong voice_id | List voices, copy exact ID |
| Slow generation | Model too large | Use `eleven_turbo_v2_5` |

## Files in This Skill

| File | Purpose |
|------|---------|
| `scripts/test_elevenlabs.py` | Standalone voice test script (run with API key) |
| `templates/tts-config.yaml` | Copy-paste config.yaml snippets |
| `references/troubleshooting-log.md` | Session logs, common fixes, command references |
| `references/original-voice.md` | Original voice configuration and instructions to revert to default voice |

## Usage

```bash
# Test a voice quickly
ELEVENLABS_API_KEY=xxx ~/.hermes/hermes-agent/venv/bin/python \
  ~/.hermes/skills/productivity/tts-elevenlabs-config/scripts/test_elevenlabs.py

# Copy config template
cat ~/.hermes/skills/productivity/tts-elevenlabs-config/templates/tts-config.yaml
```

## Related Skills

- `apple-mlx-inference` — For local TTS alternatives (Piper, NeuTTS)
- `hermes-agent` — Core Hermes configuration patterns