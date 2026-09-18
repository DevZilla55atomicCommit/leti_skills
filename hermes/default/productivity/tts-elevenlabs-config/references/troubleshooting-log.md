# ElevenLabs TTS Troubleshooting Log

## Session: 2026-07-10

### Problem
User wanted to verify ElevenLabs TTS configuration in Hermes Agent and test voice output.

### Findings

1. **Config.yaml had voice settings but missing API key**
   - `tts.provider: elevenlabs` ✅
   - `tts.elevenlabs.voice_id: pNInz6obpgDQGcFmaJgB` ✅
   - `tts.elevenlabs.model_id: eleven_multilingual_v2` ✅
   - **Missing**: `ELEVENLABS_API_KEY` in ~/.hermes/.env

2. **API key was placeholder in .env**
   ```
   ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
   ```

3. **Voice ID verification**
   - Voice `pNInz6obpgDQGcFmaJgB` exists in user's ElevenLabs account (26 voices total)
   - Confirmed via ElevenLabs API

4. **Test results**
   - Direct Python API: ✅ Works (84 KB MP3 generated)
   - Hermes TTS tool: ✅ Works (77 KB MP3, MEDIA tag returned)
   - `voice_compatible: false` = voice doesn't support native Opus for Telegram bubbles (MP3 fallback works)

### Fix Applied

1. Updated ~/.hermes/.env with actual API key
2. Verified config.yaml has correct elevenlabs section
3. Tested end-to-end via Hermes TTS tool

### Files Modified
- `~/.hermes/.env` — Added real ELEVENLABS_API_KEY
- `~/.hermes/config.yaml` — Confirmed tts.elevenlabs section correct

### Commands for Future Testing

```bash
# Quick voice test
export ELEVENLABS_API_KEY=your_key
~/.hermes/hermes-agent/venv/bin/python -c "
from tools.tts_tool import text_to_speech_tool
import json
result = text_to_speech_tool(text='Test message')
print(json.dumps(json.loads(result), indent=2))
"

# List voices
python3 -c "
import os
os.environ['ELEVENLABS_API_KEY'] = 'your_key'
from elevenlabs.client import ElevenLabs
client = ElevenLabs(api_key=os.environ['ELEVENLABS_API_KEY'])
for v in client.voices.get_all().voices:
    print(f'{v.voice_id}: {v.name}')
"
```

### Key Takeaway
Hermes TTS reads API key from `.env` (not config.yaml). The config.yaml only specifies voice_id and model_id. This separation of secrets (env) from config (yaml) is by design.