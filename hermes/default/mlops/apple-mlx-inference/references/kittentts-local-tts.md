# KittenTTS Local TTS Integration (Session Notes)

## Session Context
**Date**: 2025-07-10  
**Hardware**: MacBook Pro M2 16GB  
**Integration**: Hermes Agent TTS toolset with KittenTTS local provider  

---

## Overview
KittenTTS is a **fully local, 25 MB TTS model** (ONNX + ONNX Runtime) with 8 English voices. It runs entirely on-device with no API keys, no network calls, and no cloud dependency.

## Installation
```bash
# Install KittenTTS (includes ONNX Runtime, spaCy, torch, etc.)
pip install https://github.com/KittenML/KittenTTS/releases/download/0.8.1/kittentts-0.8.1-py3-none-any.whl

# Verify
python -c "from kittentts import KittenTTS; print('KittenTTS available:', KittenTTS('KittenML/kitten-tts-nano-0.8-int8').available_voices)"
```

**Dependencies installed**: `torch`, `spacy`, `onnxruntime`, `phonemizer-fork`, `espeakng_loader`, `misaki`, `num2words`, `soundfile`, `curated-transformers`, etc. (~1.5 GB total)

---

## Available Voices (8 Total)

| Voice | Gender | Notes |
|-------|--------|-------|
| **Bella** | Female | Default-ish |
| **Jasper** | Male | |
| **Luna** | Female | |
| **Bruno** | Male | |
| **Rosie** | Female | |
| **Hugo** | Male | |
| **Kiki** | Female | |
| **Leo** | Male | |

All voices are **US English** with neutral accent. No style/emotion control available.

---

## Hermes Configuration

```yaml
# ~/.hermes/config.yaml
tts:
  provider: kittentts
  use_gateway: true
  kittentts:
    model: KittenML/kitten-tts-nano-0.8-int8  # 25 MB quantized model
    # voice: bella  # Not yet configurable in Hermes tool (uses default)
```

**Note**: Voice selection is not yet exposed in Hermes config — the tool uses the first available voice by default.

---

## Testing in Hermes

```bash
# Test via Hermes TTS tool
hermes chat -q "Say hello" --toolsets tts

# Or via Python
python -c "
import sys
sys.path.insert(0, '/Users/alfredkamisese/.hermes/hermes-agent')
from tools.tts_tool import text_to_speech_tool
import json
result = text_to_speech_tool('Hello from KittenTTS local TTS!')
print(json.dumps(result, indent=2))
"
```

**Output**: 29 KB MP3 generated in ~2 seconds on M2 16GB.

---

## Comparison with Other TTS Providers

| Feature | KittenTTS | Edge TTS | ElevenLabs | OpenAI TTS |
|---------|-----------|----------|------------|------------|
| **Local/Cloud** | **Local** | Cloud | Cloud | Cloud |
| **Model Size** | 25 MB | N/A (API) | N/A (API) | N/A (API) |
| **Voices** | 8 (US English) | 323+ (100+ locales) | 100+ | 6 |
| **Languages** | English only | 100+ | 29 | 50+ |
| **Accents** | US only | Many (AU, ZA, GB, etc.) | Many | Several |
| **Styles/Emotions** | None | Many | Yes | Limited |
| **API Key** | None | None | Required | Required |
| **Latency** | ~2s (local) | ~1-2s (network) | ~1-2s | ~1-2s |
| **Cost** | Free | Free | Free tier / Paid | Paid |
| **Privacy** | **Complete** | Microsoft | ElevenLabs | OpenAI |

---

## Use Cases

| Scenario | Recommendation |
|----------|----------------|
| **Offline/private TTS** | ✅ KittenTTS ideal |
| **Multilingual** | ❌ Use Edge TTS |
| **Accent variety (AU, ZA, GB)** | ❌ Use Edge TTS |
| **Expressive/emotional speech** | ❌ Use ElevenLabs/Edge |
| **Voice cloning** | ❌ Use ElevenLabs |
| **Maximum quality** | ❌ Use ElevenLabs |

---

## Current Limitations in Hermes

1. **Voice selection not configurable** — uses default voice (Bella)
2. **English only** — no Japanese, Spanish, etc.
2. **No style control** — cannot adjust speed, pitch, emotion
3. **US accent only** — no British, Australian, South African variants
4. **Model fixed** — `KittenML/kitten-tts-nano-0.8-int8` hardcoded in tool

---

## Future Improvements (Feature Requests)

- Add `voice` parameter to `tts.kittentts` config section
- Expose voice selection in `text_to_speech_tool` arguments
- Support for multiple KittenTTS model variants (if released)
- Language detection / multilingual support (when model supports it)

---

## Verdict

**KittenTTS is excellent for:**
- Privacy-sensitive local TTS
- Zero-cost, zero-dependency TTS
- Simple English-only use cases

**Not suitable for:**
- Multilingual content
- Accent-specific requirements (British, Australian, etc.)
- Expressive/emotional narration
- Production voiceover work

**Current Hermes config**: Edge TTS with `en-AU-NatashaNeural` (Australian female) — better accent coverage for general use.