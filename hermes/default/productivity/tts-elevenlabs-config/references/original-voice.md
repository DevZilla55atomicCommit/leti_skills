# Original Voice Configuration

The default TTS voice configured for Hermes uses the Edge provider with the South African English voice `en-ZA-LeahNeural`.

## Configuration Location

The voice settings are stored in `~/.hermes/config.yaml` under the `tts` section:

```yaml
tts:
  provider: edge
  edge:
    voice: en-ZA-LeahNeural
  elevenlabs:
    voice_id: en-ZA-LeahNeural
    model_id: eleven_multilingual_v2
```

## Reverting to Original Voice

If a custom voice was selected and you wish to revert to the original:

1. Open `~/.hermes/config.yaml`.
2. Under the `tts` section, set:
   ```yaml
   tts:
     provider: edge
     edge:
       voice: en-ZA-LeahNeural
     elevenlabs:
       voice_id: en-ZA-LeahNeural
       model_id: eleven_multilingual_v2
   ```
3. Save the file and restart Hermes Agent for changes to take effect.

## Testing the Original Voice

You can test the original voice configuration with:

```bash
echo "Hermes is using the original default voice." | text_to_speech --provider edge --voice en-ZA-LeahNeural
```

This will generate an audio file confirming the voice is working as expected.