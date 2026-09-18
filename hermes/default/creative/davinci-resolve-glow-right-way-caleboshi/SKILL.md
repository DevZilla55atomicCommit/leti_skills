---
name: davinci-resolve-glow-right-way-caleboshi
category: creative
description: "DaVinci Resolve: Glow the Right Way — Native Glow OFX, Soft Light composite, highlight rolloff for cinematic halation"
tags:
  - davinci-resolve
  - glow
  - halation
  - cinematic-look
  - soft-light
  - glow-ofx
  - highlight-rolloff
  - caleboshi
version: 1.0.0
author: "caleboshi (extracted by Hermes Agent)"
source_url: "https://www.instagram.com/reel/DH69ylBy1SL/"
---

# DaVinci Resolve: Glow the Right Way — Native Glow OFX for Cinematic Halation

## Overview
Proper cinematic glow/halation technique using **DaVinci Resolve's native Glow OFX** with **Soft Light composite** and **highlight rolloff** control. Avoids the "cheap bloom" look by isolating highlights and controlling falloff.

## Core Concept

### Why "The Right Way"?
- **Bad glow**: Global blur + Add/Screen blend = hazy, low-contrast mess
- **Good glow**: Isolate highlights → Blur → Soft Light → Controlled rolloff
- **Key**: Glow OFX has built-in threshold, falloff, and blend modes

## Node Structure

```
Node 01: Input (Log/Raw)
Node 02: CST (Camera → Working Space)
Node 03: Primary Grade (Exposure, WB, Contrast)
Node 04: **Glow OFX Node** (Isolated highlights)
Node 05: Creative Grade / Film Emulation
Node 06: Output CST (Working → Display)
```

## Step-by-Step Workflow

### 1. Add Glow OFX
- **Effects Panel** → **OpenFX** → **Resolve FX Light** → **Glow**
- Drag onto **new Serial Node** (Label: "Glow/Halation")

### 2. Critical Glow OFX Settings

| Parameter | Setting | Why |
|-----------|---------|-----|
| **Blend Mode** | **Soft Light** | Natural highlight bloom, preserves contrast |
| **Threshold** | ~0.7–0.9 | Only brightest highlights glow |
| **Size / Radius** | 20–100 | Spread of glow (scene dependent) |
| **Intensity** | 0.3–1.0 | Strength of effect |
| **Falloff** | **Smooth / Gaussian** | Natural rolloff, not hard edge |
| **HDR Mode** | **On** (if HDR) | Proper highlight handling |

### 3. Soft Light Blend Mode — The Secret
- **Add/Screen** = blows out, loses contrast, "foggy"
- **Soft Light** = multiplies highlights, screens shadows = **photorealistic bloom**
- Mimics **film halation**: light scattering in emulsion layers

### 4. Threshold Control
- **Low threshold (0.3)**: Everything glows → milkiness
- **High threshold (0.85+)**: Only specular highlights → cinematic
- **Sweet spot**: 0.75–0.9 for most narrative work

### 5. Optional: Pre-Glow Qualifier (Advanced)
1. Add **Serial Node BEFORE Glow** → Label "Glow Mask"
2. **Qualifier**: Select highlights (Luma > 0.8)
3. **Blur Radius**: 2–5px (soften mask edge)
4. **Glow Node**: Enable **Mask Input** (blue dot) → Connect from Qualifier node
5. Result: **Only qualified highlights glow**

## Pro Tips

- **Anamorphic Look**: Increase **Horizontal** > **Vertical** size ratio (2:1)
- **Color Fringing**: Add slight **Chromatic Aberration** (Resolve FX Distort) after Glow
- **Film Emulation**: Glow BEFORE film LUT/DCTL for authentic halation in emulsion
- **Skin Protection**: Qualifier mask to EXCLUDE skin tones from glow
- **Night Scenes**: Lower threshold (0.6), higher intensity for streetlight bloom
- **Day Interiors**: Higher threshold (0.9), subtle intensity for window blowout

## Common Mistakes

| Mistake | Result | Fix |
|---------|--------|-----|
| Blend = Add/Screen | Hazy, washed out | **Soft Light** |
| Threshold too low | Everything glows | Raise to 0.8+ |
| No falloff control | Hard glow edge | Enable Falloff = Smooth |
| Glow after LUT | Wrong color space | Glow in working space (pre-LUT) |
| Global glow on faces | Plastic skin | Qualifier mask to exclude skin |

## Footage Pack Note
@caleboshi mentions: "Comment MIST and grab my SLOG3 Ungraded Footage Pack!" — Practice material for S-Log3 workflows.

## Related Skills
- `davinci-resolve-cinematic-haze-effect` — Native haze (3rdvisionfilm)
- `davinci-resolve-cinematic-haze-20-2` — Creatorsergeant Resolve 20.2 haze
- `davinci-resolve-cinematic-glow-mansourmelouli` — Glow OFX + Soft Light + Highlight rolloff
- `davinci-resolve-diffusion-soft-light` — Blur + Soft Light diffusion
- `davinci-resolve-soft-light-glow-cinematic-emotion` — Mastermotion soft light glow
- `davinci-resolve-free-halation-effect` — Free halation technique

## Source
Instagram: @caleboshi — "Glow the Right Way / Footage Pack"
URL: https://www.instagram.com/reel/DH69ylBy1SL/
Date: 2025-07-11