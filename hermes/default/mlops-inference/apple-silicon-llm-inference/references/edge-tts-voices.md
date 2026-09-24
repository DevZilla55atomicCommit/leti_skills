# Edge TTS Voice Catalog by Locale

Complete catalog of Microsoft Edge TTS voices available for free local use with Hermes Agent.

## Voice Selection in Config

```yaml
# ~/.hermes/config.yaml
tts:
  provider: edge
  edge:
    voice: en-ZA-LeahNeural   # South African female
    # voice: en-AU-NatashaNeural  # Australian female
    # voice: en-GB-SoniaNeural    # British female (professional)
```

## Complete Voice Catalog by Region

### 🇿🇦 South Africa (en-ZA)
| Voice ID | Gender | Style/Description |
|----------|--------|-------------------|
| **en-ZA-LeahNeural** | Female | Natural, warm South African accent |
| en-ZA-LukeNeural | Male | Natural South African accent |

### 🇦🇺 Australia (en-AU)
| Voice ID | Gender | Style/Description |
|----------|--------|-------------------|
| **en-AU-NatashaNeural** | Female | Natural, friendly Australian accent |
| en-AU-WilliamNeural | Male | Natural Australian accent |
| en-AU-AdamNeural | Male | Clear, professional Australian accent |

### 🇬🇧 United Kingdom (en-GB)
| Voice ID | Gender | Style/Description |
|----------|--------|-------------------|
| **en-GB-SoniaNeural** | Female | **Professional, clear, authoritative** — best for narration/docs |
| en-GB-LibbyNeural | Female | Friendly, warm British accent |
| en-GB-MaisieNeural | Female | Upbeat, energetic British accent |
| en-GB-RyanNeural | Male | Professional, clear British accent |
| en-GB-ThomasNeural | Male | Natural, conversational British accent |

### 🇺🇸 United States (en-US) — Most Variety
| Voice ID | Gender | Style/Description |
|----------|--------|-------------------|
| en-US-AriaNeural | Female | **Default** — clear, professional, versatile |
| en-US-JennyNeural | Female | Warm, friendly, conversational |
| en-US-GuyNeural | Male | Professional, clear |
| en-US-DavisNeural | Male | Calm, measured |
| en-US-JasonNeural | Male | Confident, articulate |
| en-US-TonyNeural | Male | Deep, authoritative |
| en-US-NancyNeural | Female | Professional, articulate |
| en-US-AmberNeural | Female | Warm, expressive |
| en-US-AnaNeural | Female | Clear, professional |
| en-US-ChristopherNeural | Male | Professional, confident |
| en-US-EricNeural | Male | Natural, conversational |
| en-US-MichelleNeural | Female | Warm, friendly |
| en-US-RogerNeural | Male | Deep, steady |
| en-US-SteffanNeural | Male | Friendly, approachable |

### 🇨🇦 Canada (en-CA)
| Voice ID | Gender | Style |
|----------|--------|-------|
| en-CA-ClaraNeural | Female | Natural Canadian |
| en-CA-LiamNeural | Male | Natural Canadian |

### 🇮🇳 India (en-IN)
| Voice ID | Gender | Style |
|----------|--------|-------|
| en-IN-NeerjaNeural | Female | Indian English |
| en-IN-PrabhatNeural | Male | Indian English |

### 🇮🇪 Ireland (en-IE)
| Voice ID | Gender | Style |
|----------|--------|-------|
| en-IE-EmilyNeural | Female | Irish English |
| en-IE-ConnorNeural | Male | Irish English |

### 🇰🇪 Kenya (en-KE)
| Voice ID | Gender | Style |
|----------|--------|-------|
| en-KE-AsiliaNeural | Female | Kenyan English |
| en-KE-ChilembaNeural | Male | Kenyan English |

### 🇳🇬 Nigeria (en-NG)
| Voice ID | Gender | Style |
|----------|--------|-------|
| en-NG-AbeoNeural | Female | Nigerian English |
| en-NG-EzinneNeural | Female | Nigerian English |
| en-NG-EkeneNeural | Male | Nigerian English |

### 🇵🇭 Philippines (en-PH)
| Voice ID | Gender | Style |
|----------|--------|-------|
| en-PH-JamesNeural | Male | Philippine English |
| en-PH-RosaNeural | Female | Philippine English |

### 🇸🇬 Singapore (en-SG)
| Voice ID | Gender | Style |
|----------|--------|-------|
| en-SG-LunaNeural | Female | Singapore English |
| en-SG-WayneNeural | Male | Singapore English |

### 🇭🇰 Hong Kong (en-HK)
| Voice ID | Gender | Style |
|----------|--------|-------|
| en-HK-SamNeural | Male | Hong Kong English |
| en-HK-YanNeural | Female | Hong Kong English |

## Multilingual Voices (Support Multiple Languages)

| Voice ID | Primary Language | Also Supports |
|----------|------------------|---------------|
| en-US-AriaNeural | English | German, French, Spanish, Italian, Japanese, Chinese, Korean, Portuguese, Russian, Dutch, Polish, Turkish, Arabic, Hindi, Vietnamese, Thai, Indonesian, Malay, Filipino, Swedish, Norwegian, Danish, Finnish, Greek, Hebrew, Czech, Hungarian, Romanian, Slovak, Croatian, Bulgarian, Ukrainian, Latvian, Lithuanian, Estonian, Slovenian |

## Voice Styles (Where Available)

Some voices support style variations via SSML:

```xml
<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US">
    <voice name="en-US-AriaNeural">
        <mstts:express-as style="cheerful">Hello there!</mstts:express-as>
    </voice>
</speak>
```

**Common styles:** `cheerful`, `sad`, `angry`, `fearful`, `disgruntled`, `serious`, `friendly`, `assistant`, `chat`, `customerservice`, `newscast`, `poetry`, `storytelling`

## Testing Voices

```bash
# Quick test any voice
~/.hermes/hermes-agent/venv/bin/python -c "
import edge_tts, asyncio
asyncio.run(edge_tts.Communicate('Hello, this is a test.', 'en-ZA-LeahNeural').save('/tmp/test.mp3'))
print('Saved to /tmp/test.mp3')
"

# List all voices
~/.hermes/hermes-agent/venv/bin/python -m edge_tts --list-voices
```

## Recommendations by Use Case

| Use Case | Recommended Voice | Reason |
|----------|-------------------|--------|
| **Professional documentation** | `en-GB-SoniaNeural` | Clear, authoritative, professional |
| **Friendly chat/assistant** | `en-US-AriaNeural` / `en-US-JennyNeural` | Warm, approachable |
| **Technical tutorials** | `en-US-GuyNeural` / `en-GB-RyanNeural` | Clear, measured pace |
| **Storytelling/narration** | `en-GB-ThomasNeural` / `en-US-TonyNeural` | Engaging, expressive |
| **Regional authenticity** | `en-ZA-LeahNeural` / `en-AU-NatashaNeural` | Genuine regional accents |
| **Accessibility/clarity** | `en-US-AriaNeural` | Best overall clarity, default choice |

## Notes

- All Edge TTS voices are **free**, run **locally** (no API key needed)
- Voices are downloaded on first use (~10-50 MB each)
- Works offline after initial download
- Audio output: MP3 (default) or Opus (.ogg) for Telegram voice bubbles
- No rate limits, no quotas