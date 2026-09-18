---
name: davinci-atmospheric-filmic-warm-matte-grade
description: DaVinci Resolve technique: Atmospheric Filmic Warm Matte Grade from Instagram Reel C_P-D_xtb2q
category: creative/davinci-resolve-techniques
tags: ["cinematic", "travel", "matte", "warm", "faded-shadows", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "C_P-D_xtb2q"
collection: "Ideas_for_Shooting_Videos"
resolve_page: "Color"
node_graph: "serial"
difficulty: "beginner"
created: 2026-07-30
---

# Atmospheric Filmic Warm Matte Grade

**Source:** Instagram Reel `C_P-D_xtb2q` (Ideas_for_Shooting_Videos)  
**Page:** Color | **Graph:** serial | **Difficulty:** beginner

![Atmospheric Filmic Warm Matte Grade](C_P-D_xtb2q.gif)

## Node Graph Structure

- Primary Correction
- Curves Contrast
- Color Wheels Balance
- Glow

## Parameters

- **lift**: +0.02
- **gamma**: -0.05
- **saturation**: 0.75
- **glow_threshold**: 0.5
- **glow_spread**: 0.60

## Steps to Reproduce in DaVinci Resolve

1. Lift the black point in the Curves tool to create faded blacks.
2. Apply a warm orange tint to the highlights and a subtle olive tint to the shadows.
3. Desaturate the greens using the Hue/Saturation curve to prevent vibrancy.
4. Add a Glow node with a low threshold and high spread to create the hazy sky effect.
5. Reduce overall contrast slightly to achieve a soft-filmic-matte look.

## Tags
`cinematic`, `travel`, `matte`, `warm`, `faded-shadows`
