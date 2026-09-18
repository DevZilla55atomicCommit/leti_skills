---
name: golden-hour-atmospheric-grade
description: Cinematic atmospheric/haze grading for golden hour, aerial, and landscape footage — lowered contrast, teal-blue shadow tint, warm highlights, glow/mist effects, and midtone detail recovery in DaVinci Resolve Color page.
trigger: User grading golden hour, sunset/sunrise, aerial/drone, landscape, or atmospheric/moody footage
category: davinci-resolve-color-grading
tags:
  - cinematic
  - aerial
  - colorgrading
  - haze
  - golden-hour
  - atmospheric
  - glow
  - mist
parameters:
  - name: contrast_reduction
    description: Overall contrast lowering for hazy look
    default: "-10% to -20% (Pivot 0.5)"
    type: string
  - name: shadow_tint
    description: Teal/blue shift in shadows
    default: "Lift: +0.03-0.05 Blue, -0.02 Green"
    type: string
  - name: highlight_warmth
    description: Warm/orange shift in highlights
    default: "Gain: +0.03-0.05 Red, +0.02 Yellow"
    type: string
  - name: glow_threshold
    description: Glow effect threshold for light sources
    default: "0.4-0.5 (highlights only)"
    type: string
  - name: midtone_detail
    description: Texture recovery in water/trees
    default: "+10 to +20 Midtone Detail"
    type: string
steps:
  - step: "Node 1 - Primary: Lower contrast (Contrast 0.8-0.9, Pivot 0.5), slight exposure lift +0.1, reduce saturation -5 to -10%"
  - step: "Node 2 - Power Window: Gradient/linear mask on landmass/foreground, local saturation +10-15%, contrast +5%"
  - step: "Node 3 - Glow/Mist: Add Glow OFX (Threshold 0.4-0.5, Radius 0.4-0.6, Opacity 0.2-0.3) OR Blur node + Screen blend at 15-25% opacity"
  - step: "Node 4 - Color Wheels: Lift → Teal/Blue; Gamma → Neutral; Gain → Warm/Orange; use Offset for global warmth"
  - step: "Node 5 - Midtone Detail: Increase Midtone Detail +10 to +20 to restore texture in water, trees, distant details"
  - step: "Optional Node 6 - HSL Curves: Hue vs Sat — desaturate greens/yellows -10 to -20% for muted foliage"
difficulty: intermediate
resolve_page: Color
node_graph_type: serial
key_nodes:
  - Primary Wheels (Contrast, Pivot, Saturation)
  - Power Window (Gradient/Linear)
  - Glow OFX / Blur + Screen Blend
  - Color Wheels (Lift/Gamma/Gain split toning)
  - Midtone Detail
  - HSL Curves (Hue vs Sat)
source_techniques:
  - video_id: C_s_3BrqhAl
    technique_name: Atmospheric Haze & Cinematic Grading
    tags: [cinematic, aerial, colorgrading, haze]
  - video_id: C_lLHxVgEyc
    technique_name: Cinematic Teal and Orange Color Grading
    tags: [color-grading, cinematic, golden-hour, automotive]
  - video_id: C95GBSmxyzX
    technique_name: Natural Light Glow & Soft Diffusion Effect
    tags: [cinematic, natural light, glow, color grading]
---

# Golden Hour & Atmospheric Haze Grade

Cinematic grading for golden hour, aerial/drone, landscape, and atmospheric footage — creating that "magic hour" haze with teal shadows, warm highlights, glow, and preserved midtone texture.

## When to Use
- Golden hour / magic hour footage
- Sunrise/sunset landscapes
- Aerial/drone cinematography
- Atmospheric/moody narratives
- Travel/cinematic vlogs
- Real estate golden hour shots

## Node Graph (Serial)

```
Node 1: Primary (Low Contrast, Desat, Exp Lift)
    ↓
Node 2: Power Window → Land/Foreground (Local Sat/Contrast)
    ↓
Node 3: Glow/Mist Effect (Glow OFX or Blur+Screen)
    ↓
Node 4: Split Toning (Lift=Teal, Gain=Warm)
    ↓
Node 5: Midtone Detail Recovery (+10 to +20)
    ↓
Node 6 (Opt): HSL Curves → Desaturate Greens/Yellows
```

## Node Details

### Node 1: Primary — Base Haze Look
| Parameter | Value | Effect |
|-----------|-------|--------|
| Contrast | 0.80 - 0.90 | Flattens image for haze |
| Pivot | 0.50 | Contrast pivot at mid-gray |
| Exposure | +0.05 to +0.15 | Lifts shadows, reveals detail |
| Saturation | 90-95% | Muted, filmic look |
| Temp | +100 to +200 (warmer) | Golden hour base warmth |
| Tint | +5 to +10 (magenta) | Subtle film emulation |

### Node 2: Power Window — Landmass/Foreground Pop
- **Shape**: Linear/Gradient (bottom 40-60% of frame) OR Custom on landmass
- **Feather**: 40-60 (seamless transition)
- **Adjustments**:
  - Saturation: +10% to +15% (local color pop)
  - Contrast: +5 to +10 (definition)
  - Exposure: +0.05 (lift foreground)
- **Purpose**: Ground the image, prevent "flat everywhere" look

### Node 3: Glow / Atmospheric Mist
**Option A: Glow OFX (Resolve Studio)**
| Setting | Value |
|---------|-------|
| Threshold | 0.40 - 0.50 |
| Radius | 0.40 - 0.60 |
| Intensity | 0.20 - 0.35 |
| Mix | Screen / Add |

**Option B: Blur + Screen Blend (Free/Studio)**
1. Add Serial Node → Blur (Radius 30-60)
2. Change Composite Mode: **Screen** (or Soft Light)
3. Opacity: 15-25%
4. Optional: Mask to sky/highlights only via Qualifier (Lum > 0.7)

### Node 4: Split Toning via Color Wheels
| Wheel | Adjustment | Values |
|-------|------------|--------|
| **Lift (Shadows)** | Teal/Blue push | Blue +0.03 to +0.05, Green -0.02 |
| **Gamma (Midtones)** | Neutral/Subtle warm | Red +0.01, Green 0, Blue -0.01 |
| **Gain (Highlights)** | Warm/Orange | Red +0.03 to +0.05, Green +0.01 to +0.02 |
| **Offset (Global)** | Overall warmth | Temp +50 to +150, Tint +5 |

> **Pro Tip**: Use **Offset wheel** for global warmth instead of pushing Gain too hard — preserves highlight detail.

### Node 5: Midtone Detail — Texture Recovery
- **Midtone Detail**: +10 to +20
- **Brings back**: Water texture, tree bark, rock detail, cloud definition
- **Caution**: Don't exceed +25 or noise appears in shadows

### Node 6 (Optional): HSL Curves — Muted Foliage
- **Hue vs Sat**: Target Green (120°) and Yellow (60°) → -10% to -20% saturation
- **Hue vs Hue**: Shift Yellow → Orange slightly (+5°) for autumn feel
- **Sat vs Sat**: Reduce saturation in low-sat regions (compress)

## Scope Targets
- **Waveform**: Shadows 15-25 IRE (lifted), Highlights 85-95 IRE (soft roll-off)
- **Vectorscope**: Cluster near center (desat), skin tones on line, teal/orange separation
- **Parade**: Blue lifted in shadows, Red lifted in highlights — classic split tone

## Pro Tips from Source Techniques

### From C_s_3BrqhAl (Atmospheric Haze)
> "Lower overall contrast → Power Window on landmass for local saturation → Glow/Blur for mist → Shift shadows blue, highlights warm → Midtone Detail for water/tree texture"

### From C95GBSmxyzX (Natural Light Glow)
> "Glow Threshold 0.4-0.5 catches only sun beams → Radius 0.5, Opacity 0.3 for dreamy bloom → Qualifier mask protects shadows/midtones from glow bleed"

### From C_lLHxVgEyc (Teal/Orange Automotive)
> "Power Window on subject (car) for exposure/sat boost → Vignette to center focus → Works equally for landscape subject isolation"

## Common Pitfalls
- ❌ Contrast too low → looks "milky" not "hazy" (keep ≥ 0.8)
- ❌ Glow on everything → mask to highlights only (Qualifier Lum > 0.7)
- ❌ Teal shadows too strong → skin tones go green; protect with Qualifier
- ❌ No midtone detail → water/trees look like plastic; +10 to +20 is sweet spot
- ❌ Saturation too low → dead image; 90-95% not 70%

## Variations

### **Moody Blue Hour** (pre-dawn/post-sunset)
- Contrast: 0.85 | Temp: -200 (cool) | Lift: Heavy Blue | Gain: Neutral | Glow: OFF

### **Warm Golden Hour** (classic)
- Contrast: 0.90 | Temp: +300 | Lift: Teal | Gain: Heavy Orange | Glow: ON (sun flares)

### **Desert/Arid Haze**
- Contrast: 0.95 | Sat: 85% | Lift: Yellow-Brown | Gain: Warm | Midtone Detail: +25 (texture!)

## Related Skills
- `teal-orange-cinematic-grade` — for stylized split-toning
- `skin-tone-portrait-grade` — if people in golden hour
- `gimbal-automotive-cinematic-grade` — for vehicle golden hour
- `social-media-sharpening-export` — delivery
- `hdr-social-media-grade` — HDR golden hour