# DaVinci Resolve Technique Prompt Schema

## Full Prompt for llava:7b

```
Analyze this video frame for DaVinci Resolve color grading and editing techniques.
Identify and output ONLY valid JSON with these keys:
{
  "grading_style": "string (e.g., teal/orange, film look, log, S-Log3, Rec709, custom)",
  "camera_movement": "string (static, dolly, gimbal, handheld, tripod, slider, drone, crane)",
  "lighting": "string (key/fill ratio, soft/hard, natural, artificial, practical, mixed)",
  "effects": "array of strings (transitions, overlays, text, LUTs, filters, composites)",
  "color_temperature": "string (warm, cool, neutral, mixed)",
  "contrast_level": "string (high, low, medium, flat/log)",
  "saturation": "string (high, low, medium, desaturated)",
  "notes": "string (any additional DaVinci-relevant observations)"
}
```

## Field Definitions

### grading_style
- `teal/orange` — Classic blockbuster look
- `film look` — Film emulation (Kodak 2383, Fuji, etc.)
- `log` — Flat log profile (S-Log3, V-Log, C-Log)
- `S-Log3` — Sony S-Log3 specific
- `Rec709` — Standard video look
- `custom` — Doesn't match standard categories

### camera_movement
- `static` — Locked off, tripod
- `dolly` — Smooth linear movement
- `gimbal` — Stabilized handheld
- `handheld` — Unstabilized, organic shake
- `tripod` — Pan/tilt on tripod
- `slider` — Lateral slide
- `drone` — Aerial
- `crane` — Vertical boom

### lighting
Describe key/fill ratio, quality (soft/hard), and sources:
- `key:fill 2:1, soft, mixed natural/artificial`
- `high key, soft, practical`
- `low key, hard, single source`

### effects (array)
Common Instagram Reel effects:
- `transitions` — Cuts, dissolves, wipes, morph cuts
- `overlays` — Text, graphics, lower thirds
- `text` — Animated captions, kinetic typography
- `LUTs` — Creative LUT application
- `filters` — Glow, vignette, film grain, halation
- `composites` — Split screen, picture-in-picture, matte

### color_temperature
- `warm` — Golden, sunset, tungsten
- `cool` — Blue, moonlight, daylight
- `neutral` — Balanced
- `mixed` — Multiple temps in frame

### contrast_level
- `high` — Crushed blacks, blown highlights
- `low` — Flat, lifted shadows
- `medium` — Balanced
- `flat/log` — Log curve preserved

### saturation
- `high` — Vibrant, poppy
- `low` — Muted, desaturated
- `medium` — Natural
- `desaturated` — Near B&W

### notes
Free-form observations relevant to DaVinci:
- Specific node structures observed
- Power window usage
- Qualifier/HSL isolation
- Magic Mask tracking
- Depth Map usage
- Relight tool evidence

## Example Output

```json
{
  "grading_style": "teal/orange",
  "camera_movement": "gimbal",
  "lighting": "key:fill 2:1, soft, mixed natural/LED",
  "effects": ["transitions", "text", "LUTs"],
  "color_temperature": "mixed",
  "contrast_level": "medium",
  "saturation": "high",
  "notes": "Strong teal shadows via Hue vs Hue curve. Text overlay uses kinetic typography with motion blur. LUT appears to be Kodak 2383 emulation applied at 50% opacity on parallel node."
}
```

## llava:7b Response Handling

llava often wraps JSON in markdown:
```markdown
```json
{...}
```
```

**Always strip wrapper:**
```python
if "```json" in response:
    response = response.split("```json")[1].split("```")[0].strip()
elif "```" in response:
    response = response.split("```")[1].split("```")[0].strip()
```