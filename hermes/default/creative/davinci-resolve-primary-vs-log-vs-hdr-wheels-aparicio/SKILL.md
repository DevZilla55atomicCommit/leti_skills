---
name: davinci-resolve-primary-vs-log-vs-hdr-wheels-aparicio
category: creative
description: "DaVinci Resolve: Primary Wheels vs LOG Wheels vs HDR Wheels — when to use each, differences, and workflow"
tags:
  - davinci-resolve
  - color-wheels
  - primary-wheels
  - log-wheels
  - hdr-wheels
  - color-grading
  - aparicio-co
version: 1.0.0
author: "aparicio.co (extracted by Hermes Agent)"
source_url: "https://www.instagram.com/reel/DJc15zpvqoe/"
---

# DaVinci Resolve: Primary Wheels vs LOG Wheels vs HDR Wheels

## Overview
Comprehensive breakdown of the three color wheel sets in DaVinci Resolve: **Primary (Lift/Gamma/Gain)**, **LOG (Lift/Gamma/Gain)**, and **HDR (Shadows/Midtones/Highlights/Specular)**. Understanding when and why to use each set for efficient grading.

## Core Differences

| Wheel Set | Color Space | Operation | Best For |
|-----------|-------------|-----------|----------|
| **Primary** | Display-referred (gamma) | Perceptual | General grading, Rec.709, quick looks |
| **LOG** | Scene-referred (linear/log) | Photometric | Log footage, CST workflows, precise exposure |
| **HDR** | Scene-referred (extended) | Perceptual + Extended | HDR grading, highlight rolloff, specular control |

## Primary Wheels (Lift / Gamma / Gain)

### Operation
- **Display-referred**: Operates in output gamma space (usually Rec.709 / Gamma 2.4)
- **Perceptual**: Changes match what you see on monitor
- **Lift**: Shadows / blacks
- **Gamma**: Midtones
- **Gain**: Highlights / whites

### When to Use
- **Rec.709 / SDR delivery** grading
- **Quick looks** and dailies
- **Non-color-managed** workflows
- **Final trim** after LOG grade
- **Creative stylization** (teal/orange, etc.)

### Characteristics
- Intuitive, "what you see is what you get"
- Can cause hue shifts at extremes
- Less precise for log-encoded footage
- Good for broadcast-legal work

## LOG Wheels (Lift / Gamma / Gain)

### Operation
- **Scene-referred**: Operates in linear/log space (before output transform)
- **Photometric**: True exposure adjustments — matches how light behaves
- **Lift**: Shadow exposure (pedestal)
- **Gamma**: Midtone exposure (middle gray)
- **Gain**: Highlight exposure (white point)

### When to Use
- **Log footage** (S-Log3, LogC, V-Log, BRAW, etc.)
- **Color Managed / CST workflows** (before output transform)
- **Precise exposure matching** between shots
- **Technical grading** (normalization, balance)
- **Camera-to-camera matching**

### Characteristics
- No hue shift from exposure moves
- Mathematically correct for log encodings
- Requires Color Management or CST to work properly
- "Linear" behavior in scene-referred space

## HDR Wheels (Shadows / Midtones / Highlights / Specular)

### Operation
- **Extended range**: Controls beyond 100 nits (up to 10,000+ nits)
- **Four zones**: Shadows, Midtones, Highlights, Specular
- **Perceptual + Extended**: Combines perceptual feel with HDR range
- **Specular**: Dedicated control for extreme highlights (specular reflections, sun, lights)

### When to Use
- **HDR grading** (PQ / HLG, 1000-4000 nits)
- **Specular highlight control** (protect/sculpt bright reflections)
- **HDR → SDR trim** (simultaneous grading)
- **High dynamic range scenes** (windows, practicals, neon)

### Characteristics
- Unique **Specular** wheel — no equivalent in Primary/LOG
- Smooth rolloff between zones
- Works in Color Managed HDR pipeline
- Requires HDR monitoring for accurate judgment

## Workflow Recommendations

### SDR / Rec.709 Project (Non-HDR)
```
1. LOG Wheels → Technical balance (exposure, WB, camera match)
2. Primary Wheels → Creative look, stylization
3. (Optional) HDR Wheels → If monitoring HDR but delivering SDR
```

### HDR Project (PQ / HLG)
```
1. LOG Wheels → Technical balance (scene-referred)
2. HDR Wheels → Creative + Specular control
3. Primary Wheels → Final trim (display-referred)
```

### Mixed Delivery (HDR + SDR)
```
1. LOG Wheels → Scene-referred base
2. HDR Wheels → HDR creative + Specular
3. Dolby Vision / HDR10 trim pass
4. Primary Wheels → SDR trim (separate timeline/version)
```

## Key Distinctions Summary

| Aspect | Primary | LOG | HDR |
|--------|---------|-----|-----|
| **Space** | Display (gamma) | Scene (linear/log) | Scene (extended) |
| **Math** | Perceptual | Photometric | Perceptual+Extended |
| **Range** | 0-100% (SDR) | 0-1.0+ (scene) | 0-10,000 nits |
| **Specular** | No | No | **Yes (4th wheel)** |
| **Hue Stability** | Shifts at extremes | **Stable** | Good |
| **Monitor Req** | SDR | SDR (with CM) | **HDR** |

## Pro Tips from Comments

> **"What does lift gamma gain affect?"** — @neilchh
> - Lift = shadows/pedestal, Gamma = midtones/middle gray, Gain = highlights/white point
> - In LOG: true exposure; in Primary: perceptual brightness

> **"Súbelo traducido"** — @keanarbe
> - Request for Spanish translation (popular internationally)

> **"Best way to learn color grading as a complete noob?"** — @guythathikes
> - Start with Primary wheels on Rec.709
> - Move to LOG wheels with Color Managed
> - HDR wheels only when delivering HDR

## Common Mistakes

| Mistake | Result | Fix |
|---------|--------|-----|
| Primary on log footage | Hue shifts, crushed blacks | Use LOG wheels first |
| LOG without Color Management | Wrong math, broken grade | Enable YRGB Color Managed or CST |
| HDR wheels on SDR monitor | Guessing specular | Grade HDR on HDR monitor |
| Mixing all three randomly | Conflicting operations | Follow workflow order above |

## Related Skills
- `davinci-resolve-color-wheels-vs-log-wheels` — Creatorsergeant breakdown
- `davinci-resolve-three-color-fundamentals-chrisseinn` — Foundations
- `davinci-resolve-gamma-2-2-vs-2-4-cdvc` — Output gamma standards

## Source
Instagram: @aparicio.co — "Primary Wheels v. LOG Wheels v. HDR Wheels"
URL: https://www.instagram.com/reel/DJc15zpvqoe/
Date: 2025-07-11