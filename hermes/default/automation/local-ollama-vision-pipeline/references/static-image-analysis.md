# Static Image Analysis with Local Ollama Vision Pipeline

This reference documents using the local Ollama vision pipeline (`local_vision_analyze.py`) for **single static images** (posters, photographs, graphics) — not just video frame batches.

## Use Case Demonstrated (2026-08-26)

Analyzed a Hawaiian/tropical event poster image (`776776120_122162398622968476_5441319180214000437_n.jpg`) to extract:
- Visual style classification (retro travel poster / tropical event aesthetic)
- Color palette (warm, high-saturation tropical tones)
- Composition analysis (static, centered, layered)
- Typography observations (bold display with decorative flourishes)
- Effects detection (text overlays, color filters, texture overlays)

## Command Pattern

```bash
# Single image analysis
/opt/homebrew/bin/python3.12 /Users/alfredkamisese/vision_pipeline/local_vision_analyze.py "/path/to/image.jpg"

# The script accepts both single files and directories
# For single files, it processes just that frame
```

## Output Schema for Static Images

The JSON output uses the same DaVinci-oriented schema but adapts for static analysis:

```json
{
  "grading_style": "custom|teal/orange|film look|log|S-Log3|Rec709",
  "camera_movement": "static",
  "lighting": "mixed|natural|artificial|practical",
  "effects": ["text", "filters", "overlays", "transitions"],
  "color_temperature": "warm|cool|neutral|mixed",
  "contrast_level": "high|medium|low|flat/log",
  "saturation": "high|medium|low|desaturated",
  "notes": "Human-readable analysis suitable for poster/design recreation",
  "frame": "/absolute/path/to/image.jpg"
}
```

## Key Differences from Video Frame Analysis

| Aspect | Video Frames | Static Images |
|--------|--------------|---------------|
| Input | Directory of frames | Single file path |
| `camera_movement` | Various (dolly, gimbal, etc.) | Always `static` |
| `effects` | Transitions, composites | Text, filters, overlays |
| Processing time | ~35-50 sec/video (3 frames) | ~10-15 sec/image |
| Batch size | 5-10 videos/batch | 20-50 images/batch |

## Integration with Creative Workflows

### Poster Recreation Workflow

1. **Analyze reference poster** → `local_vision_analyze.py reference.jpg`
2. **Extract structured description** → JSON output with style, palette, composition
3. **Feed into infographic skill** → Use `baoyu-infographic` with `retro-pop-grid` style for similar aesthetic
4. **Generate prompts** → Structured prompts for FLUX/Midjourney/DALL-E
5. **Optional: Programmatic layout** → `p5js` or `pretext` skills for precise SVG/HTML posters

### Style Classification for Poster Types

| Poster Style | Vision Output Indicators | Recommended Infographic Style |
|--------------|--------------------------|-------------------------------|
| Retro travel | Warm palette, text overlays, textured | `retro-pop-grid` |
| Modern minimal | Cool palette, clean lines, high contrast | `corporate-memphis` |
| Vintage/academic | Sepia, serif typography, aged texture | `aged-academia` |
| Cyberpunk/neon | High saturation, glow effects, dark bg | `cyberpunk-neon` |
| Hand-drawn/edu | Sketch lines, pastel palette, whimsical | `hand-drawn-edu` / `craft-handmade` |

## Python Script Modification for Static Images

The existing `local_vision_analyze.py` handles both directories and single files. For static image batches, modify the prompt in the script:

```python
# In local_vision_analyze.py, adjust the prompt for poster/design analysis:
STATIC_IMAGE_PROMPT = """Analyze this poster/design image. Output JSON with:
- grading_style: color grading aesthetic (custom, teal/orange, film look, etc.)
- camera_movement: always "static" for posters
- lighting: key/fill, natural, artificial, mixed
- effects: list of visual effects (text, filters, overlays, textures, gradients)
- color_temperature: warm, cool, neutral, mixed
- contrast_level: high, medium, low, flat/log
- saturation: high, medium, low, desaturated
- notes: detailed description for recreation (style, typography, composition, palette)
- frame: file path"""
```

## Pitfalls Specific to Static Images

1. **Aspect ratio variance** — Posters vary (portrait, landscape, square); video frames are consistent
2. **Text-heavy images** — llava:7b reads text well but may hallucinate small text; verify critical copy manually
3. **Single-frame reliability** — No temporal consistency to cross-check; run 2-3 times for important references
4. **Print vs screen color** — Vision model sees sRGB; poster print uses CMYK; note this gap in `notes` field

## Batch Processing Static Images

```bash
# Process multiple reference posters
cd /Users/alfredkamisese/vision_pipeline
for img in ~/References/Posters/*.jpg; do
  /opt/homebrew/bin/python3.12 local_vision_analyze.py "$img" >> poster_analyses.jsonl
done
```

Each line in `poster_analyses.jsonl` is a valid JSON object — load with `jq` or Python for pattern analysis across a poster collection.