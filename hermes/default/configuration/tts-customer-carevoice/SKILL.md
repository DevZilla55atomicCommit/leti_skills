---
name: tts-customer-carevoice
description: "Configure a British male customer‑care voice using Edge TTS."
tags: ["tts", "voice", "customer-care", "british", "edge"]
---
# TTS Voice Configuration – Customer Care Agent Profile

**Trigger** – Use when setting up Hermes TTS for a professional, customer‑care style voice in the UK market.

## Preference
- Voice must be **British male**, clear, authoritative, and sound like a typical customer‑care representative (e.g., “Hello, thank you for calling customer support. My name is Ryan…”).
- Must use **Edge TTS** provider with the **en‑GB‑RyanNeural** voice model.
- This setting overrides any default or previously configured voice.

## Steps to Activate
1. **Select the Edge provider**  
   ```bash
   hermes config set tts.provider edge
   ```
2. **Set the British male voice**  
   ```bash
   hermes config set tts.voice en-GB-RyanNeural
   ```
   *If the `tts.voice` key is flagged as unrecognized, the setting is still saved but may not be read by older Hermes versions. Use `--force` if you encounter the warning.*

3. **Verify** (optional)  
   ```bash
   hermes config get tts
   ```
   Ensure the output lists `edge:` with `voice: en-GB-RyanNeural`.

## Usage Example
```text
Hello, thank you for calling customer support. My name is Ryan. How may I assist you today?
```

## Pitfalls & Fixes
- **Unrecognized `tts.voice` key** – Hermes may warn that the key isn’t part of the official schema. The configuration is still persisted; regenerate the config with `hermes config migrate` if the warning persists.
- **Old configs** – If you previously set a different provider or voice, run `hermes config unset tts.provider` and `hermes config unset tts.voice` before re‑setting to avoid duplicate keys.
- **Version compatibility** – Some older Hermes releases may not read custom top‑level keys. If you upgrade Hermes, re‑apply the voice settings to ensure they persist.

## References
- **Skill**: `hermes-agent` – primary hub for Agent configuration and skill management.
- **Related**: `tts-configuration` (this skill) for version‑specific voice notes.
- **External**: Edge TTS documentation for available voices: https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/text-to-speech

> **Remember**: The voice selection is a user‑level preference that should be stored in the **`user`** memory space so it persists across sessions. If you change the voice, also record the change in memory:
> ```json
> {"preference": "tts.voice", "value": "en-GB-RyanNeural", "context": "customer‑care‑agent‑british‑male"}
> ```