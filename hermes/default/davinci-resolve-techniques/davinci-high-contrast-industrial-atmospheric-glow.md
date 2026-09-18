---
name: davinci-high-contrast-industrial-atmospheric-glow
description: DaVinci Resolve technique: High-Contrast Industrial Atmospheric Glow from Instagram Reel C4PtepHycEZ
category: creative/davinci-resolve-techniques
tags: ["cinematic", "industrial", "high-contrast", "atmospheric", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "C4PtepHycEZ"
collection: "Ideas_for_Shooting_Videos"
resolve_page: "Color"
node_graph: "serial"
difficulty: "intermediate"
created: 2026-07-30
---

# High-Contrast Industrial Atmospheric Glow

**Source:** Instagram Reel `C4PtepHycEZ` (Ideas_for_Shooting_Videos)  
**Page:** Color | **Graph:** serial | **Difficulty:** intermediate

![High-Contrast Industrial Atmospheric Glow](C4PtepHycEZ.gif)

## Node Graph Structure

- Primary Balance
- Exposure/Contrast
- HSL Qualifier (Orange)
- Glow/Halation
- Vignette

## Parameters

- **Contrast**: 1.4
- **Pivot**: 0.4
- **Shadow_Tint**: Teal
- **Glow_Radius**: 60
- **Saturation**: 0.6

## Steps to Reproduce in DaVinci Resolve

1. Increase contrast and lower the lift to crush blacks and eliminate background noise.
2. Use an HSL Qualifier to isolate the orange pipe and boost saturation/luminance specifically.
3. Apply a Glow effect on a layer node over the smoke with a wide radius to create an ethereal light bleed.
4. Add a slight teal tint to the shadows using the Color Wheels to create color contrast with the orange.
5. Apply a heavy vignette to draw focus to the center-right smoke emission.

## Tags
`cinematic`, `industrial`, `high-contrast`, `atmospheric`
