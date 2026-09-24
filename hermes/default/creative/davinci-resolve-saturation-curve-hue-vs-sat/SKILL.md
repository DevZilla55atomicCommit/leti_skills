---
name: davinci-resolve-saturation-curve-hue-vs-sat
category: creative
description: "DaVinci Resolve Saturation Curve (Hue vs Sat) — precise hue-selective saturation control for creative grading"
tags:
  - davinci-resolve
  - saturation-curve
  - hue-vs-sat
  - color-grading
  - creative-grading
  - davinciresolved
version: 1.0.0
author: "davinciresolved (extracted by Hermes Agent)"
source_url: "https://www.instagram.com/reel/DGDxMJBvkpf/"
---

# DaVinci Resolve: Saturation Curve (Hue vs Sat) — Precise Hue-Selective Saturation

## Overview
Technique for targeted saturation adjustments using the **Hue vs Sat curve** in DaVinci Resolve's Custom Curves / Color Warper. Allows boosting or reducing saturation for specific hue ranges without affecting others.

## Core Concept

### Why Hue vs Sat?
- **Global saturation** affects all colors equally → can oversaturate skin, clip highlights
- **Hue vs Sat** = surgical: "Boost only reds, protect skin tones, desaturate greens"
- **Vector-based**: Operates on hue angle (0-360°) vs saturation radius

## Node Structure

```
Node 01: Input (Log/Raw)
Node 02: CST (Camera → Working Space)
Node 03: Primary Grade (Exposure, WB, Contrast)
Node 04: **Hue vs Sat Curve** (Targeted saturation)
Node 05: Creative Look / Film Emulation
Node 06: Output CST (Working → Display)
```

## Step-by-Step Workflow

### 1. Open Hue vs Sat Curve
- **Color Warper** → **Hue vs Sat** tab
- OR **Custom Curves OFX** → **Hue vs Sat** mode
- OR **Curves** dropdown → **Hue vs Sat**

### 2. Identify Target Hues
| Hue Range | Color | Common Use |
|-----------|-------|------------|
| 0° / 360° | Red | Skin protection, red accents |
| 30° | Orange | Skin warmth, golden hour |
| 60° | Yellow | Sunlight, practicals |
| 120° | Green | Foliage, color separation |
| 180° | Cyan | Teal shadows, cinematic |
| 240° | Blue | Sky, night scenes |
| 300° | Magenta | Creative, stylized |

### 3. Adjust Saturation by Hue
1. **Click curve** to add control points at target hue angles
2. **Drag UP** → Increase saturation for that hue range
3. **Drag DOWN** → Decrease saturation (desaturate specific colors)
4. **Smooth curves** → Avoid sharp transitions (banding)

### 4. Common Patterns

#### Protect Skin Tones (Orange/Red ~20-40°)
```
Hue: 20° → Point at 1.0 (neutral)
Hue: 30° → Point at 0.8 (slightly desaturate)
Hue: 40° → Point at 1.0 (neutral)
```

#### Cinematic Teal/Orange
```
Hue: 30° (Orange) → UP to 1.3 (warm skin pop)
Hue: 180° (Cyan) → UP to 1.4 (teal shadows pop)
Hue: 120° (Green) → DOWN to 0.7 (mute foliage)
```

#### Desaturate Specific Problem Colors
```
Hue: 60° (Yellow) → DOWN (reduce yellow cast)
Hue: 300° (Magenta) → DOWN (remove sensor magenta)
```

### 5. Verify on Vectorscope
- **Vectorscope HLS** or **Vector** mode
- Check trace doesn't exceed legal limits
- Skin trace stays on skin tone line (~103°)

## Advanced Tips

### Combine with Hue vs Hue
- Shift problematic hues first (Hue vs Hue)
- Then saturate/desaturate (Hue vs Sat)
- Example: Shift yellow-green → pure green, then boost

### Use with Qualifier for Local Control
1. **Qualifier** isolates region (sky, foliage, subject)
2. **Hue vs Sat** on that node only affects qualified pixels
3. Blend with **Key Output Gain**

### Color Warper vs Custom Curves
| Feature | Color Warper | Custom Curves |
|---------|--------------|---------------|
| **UI** | Grid-based, visual | Graph-based |
| **Precision** | Good | Excellent |
| **Hue vs Hue** | Yes | Yes |
| **Hue vs Lum** | Yes | Yes |
| **Lum vs Sat** | Yes | Yes |
| **Keyframing** | Limited | Full |

## Community Insights (from comments)

> **"Seems like some extra unnecessary steps"** — @gregeditss
> - Simpler: Just use Color Wheels global sat? But less control.

> **"Brilliantly simple!🙌"** — @68snaps
> - Once understood, very fast workflow.

> **"I'd recommend not changing the clip color profile. Then all GUI inputs work most correct."** — @simon.kirketerp
> - Color Manage at project level, not clip level.

> **"Try HSV, much better results!"** — @colorsense.io
> - HSV curves (Hue vs Sat in HSV space) can be more perceptual.

> **"Would you add a middle grey point to this or is that not relevant in the HSL node?"** — @camstanleyy
> - Middle gray anchor helps prevent luminance shifts.

> **"Premiere has a dedicated curve for this"** — @gustavo.serrate
> - DaVinci's is more flexible (any hue range).

> **"Useless, you just make it 1000 harder. Get a LUT and refine much faster and easier"** — @interfilmproductions
> - LUTs are fast; curves are precise. Different tools for different jobs.

## Related Skills
- `davinci-resolve-saturation-curve_davinciresolved` — Hue vs Sat curve
- `davinci-resolve-hue-vs-sat-curve_davinciresolved` — Precise hue-selective saturation
- `davinci-resolve-color-density-hsv-hudson-twarren` — HSV density curves
- `davinci-resolve-increase-color-density` — Density vs saturation
- `davinci-resolve-color-grading-hack-gakuyen` — HSV creative hack
- `davinci-resolve-saturation-color-density_hudson-twarren` — Saturation curves

## Source
Instagram: @davinciresolved — "Saturation curve in DaVinci Resolve"
URL: https://www.instagram.com/reel/DGDxMJBvkpf/
Date: 2025-07-11