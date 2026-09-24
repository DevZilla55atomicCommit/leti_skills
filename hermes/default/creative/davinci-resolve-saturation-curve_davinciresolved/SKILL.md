---
name: davinci-resolve-saturation-curve_davinciresolved
category: creative
description: "Hue vs Sat curve in DaVinci Resolve — precise hue-selective saturation control with skin tone protection for cinematic color density"
tags:
  - davinci-resolve
  - color-grading
  - saturation-curve
  - hue-vs-sat
  - custom-curves
  - color-density
  - selective-saturation
  - skin-tone-protection
version: "1.0"
author: "Hermes Agent"
source_url: "https://www.instagram.com/reel/DGDxMJBvkpf/"
creator: "@davinciresolved"
vault_file: "Creative Grading & Looks/52-Saturation-Curve_davinciresolved_Hue-vs-Sat.md"
---

# Saturation Curve in DaVinci Resolve — Hue vs Sat for Cinematic Density

## Overview
Professional hue-selective saturation using Custom Curves (Hue vs Sat) — protects skin tones while boosting nature colors (foliage, sky) for rich, cinematic density without global saturation damage.

## When to Use
- Every grade wanting "rich" look without clown colors
- When global saturation slider breaks skin/highlights
- Creative color palette sculpting
- Film emulation base (before LUT)
- **Not for**: Quick social edits (global sat +10 is fine)

## Prerequisites
- DaVinci Resolve (Free or Studio)
- Custom Curves OFX / Curves panel knowledge
- Vectorscope reading (hue angles)
- Primary grade completed first

## Core Principle

> **Anchor skin first, then sculpt** — Global saturation is a blunt instrument; Hue vs Sat is a scalpel.

## Node Structure

```
Node 01: CST / Input Transform
Node 02: Primary Balance (Exposure, WB, Contrast)
Node 03: [CUSTOM CURVES] — Hue vs Sat (Main density)
Node 04: [CUSTOM CURVES] — Lum vs Sat (Luminance density) [Optional]
Node 05: [CUSTOM CURVES] — Sat vs Sat (Saturation compression) [Optional]
Node 06: Global Polish / LUT / Grain
```

## Step-by-Step Procedure

### 1. Primary Grade First (Node 01-02)
- CST / Color Managed pipeline correct
- Exposure, White Balance, Contrast/Pivot set
- Neutral, balanced image

### 2. Open Hue vs Sat Curve (Node 03)
- Effects → Resolve FX Color → Custom Curves
- Or Color page → Curves dropdown → **Hue vs Sat**
- Mode: **Custom**

### 3. Identify Key Hues (Vectorscope)
| Subject | Hue Angle | Action |
|---------|-----------|--------|
| **Skin** | ~35° | **ANCHOR (protect)** |
| Foliage/Green | ~120° | Boost |
| Sky/Cyan | ~200° | Boost |
| Blue | ~240° | Moderate boost |
| Magenta | ~320° | Moderate (skin adjacent) |

### 4. Anchor Skin Tone (CRITICAL — Do First)
```
Add points at 30°, 35°, 40° → Set Y = 0.6-0.8
```
- Curve **must pass through** these points
- Skin saturation locked regardless of other adjustments
- Verify: Toggle curve → skin stable on Vectorscope

### 5. Sculpt Nature Colors
```
Green (~120°):    Point → Y = 1.3-1.5
Cyan (~200°):     Point → Y = 1.2-1.4
Blue (~240°):     Point → Y = 1.1-1.3
Yellow (~60°):    Point → Y = 1.0-1.2
Magenta (~320°):  Point → Y = 0.8-1.0
Red (~0/360°):    Point → Y = 0.9-1.1
```

### 6. Smooth Bezier Handles
- No sharp corners = no posterization
- Smooth transitions between anchor points

### 7. Verify
- **Vectorscope**: Skin trace stable, nature colors expand outward
- **Parade RGB**: No channel clipping
- **Toggle ON/OFF**: Skin unchanged, image richer

## Parameter Presets

| Look | Skin (35°) | Green (120°) | Cyan (200°) | Blue (240°) | Magenta (320°) |
|------|------------|--------------|-------------|-------------|----------------|
| **Natural** | 0.7 | 1.1 | 1.0 | 1.0 | 0.9 |
| **Cinematic Rich** | 0.6 | **1.4** | **1.3** | 1.2 | 0.8 |
| **Vibrant Pop** | 0.7 | 1.3 | 1.2 | 1.2 | 1.0 |
| **Moody/Desat** | 0.5 | 0.8 | 0.8 | 0.7 | 0.6 |
| **Teal/Orange** | 0.6 | 1.0 | **1.4** | 1.1 | 0.7 |
| **Film Emu** | 0.65 | 1.2 | 1.1 | 1.0 | 0.75 |

## Advanced: 3-Curve Density System

### Node 03: Hue vs Sat (Hue-selective)
- As above — per-hue saturation

### Node 04: Lum vs Sat (Luminance-selective)
```
Shadows (0-0.3):     0.7-0.9 (dense, not noisy)
Midtones (0.3-0.7):  1.1-1.3 (PEAK RICHNESS)
Highlights (0.7-1.0): 0.4-0.7 (FILMIC DESATURATION)
```

### Node 05: Sat vs Sat (Saturation compression)
```
Low sat (0-0.3):     Expand (0→0.1, 0.3→0.5) — wake muted
Mid sat (0.3-0.7):   Linear
High sat (0.7-1.0):  Compress (1.0→0.85) — filmic rolloff
```

## Pro Tips from Community

- **@colorsense.io**: "Try HSV, much better results!" — HSV curves = more perceptual
- **@simon.kirketerp**: Work in native/DWG space, not transformed — GUI inputs more accurate
- **@camstanleyy**: Middle gray anchor helps luminance stability
- **@gregeditss**: "Extra steps" vs LUT — but curves = control
- **@z4ck.3d**: Premiere has same — concept transfers
- **@interfilmproductions**: Hybrid = LUT + curves tweak

## Common Pitfalls

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| No skin anchor | Orange faces | **Always anchor skin first** |
| Global sat +50 | Clown colors | Curves only, global +10 max |
| Sharp corners | Posterization | Smooth bezier handles |
| Ignore highlights | Digital whites | Lum vs Sat: HL desat |
| Same curve all shots | Inconsistent | Per-shot, gallery stills |
| Curves before balance | Unpredictable | Primary grade FIRST |

## Color Science Why It Works

1. **Perceptual Sensitivity** — Vision more sensitive to green/blue sat changes
2. **Memory Colors** — Foliage, sky, skin have "expected" saturation
3. **Soft Gamut Map** — Curves = smooth compression vs hard clip
4. **Film Response** — Film desats highlights, saturates midtones (Lum vs Sat mimics)

## Related Skills
- `davinci-resolve-saturation-color-density_hudson-twarren` — 3-curve density system
- `davinci-resolve-increase-color-density-creatorsergeant` — Hue vs Lum density
- `davinci-resolve-color60-cinematic-saturation-hsv` — HSV density
- `davinci-resolve-orange-teal-parallel-nodes` — Complementary grading

## References
- Source: @davinciresolved Instagram Reel (Feb 14, 2025)
- Hashtags: #davinciresolve #colorgrading #videoediting #davinci
- Engagement: 14K likes, 65 comments
- Community: HSV debate, color space workflow, LUT vs curves