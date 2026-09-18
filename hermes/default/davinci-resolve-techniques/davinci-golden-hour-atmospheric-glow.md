---
name: davinci-golden-hour-atmospheric-glow
description: DaVinci Resolve technique: Golden Hour Atmospheric Glow from Instagram Reel C9WuwXdh_0B
category: creative/davinci-resolve-techniques
tags: ["cinematic", "golden-hour", "atmospheric", "landscape", "warm-tones", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "C9WuwXdh_0B"
collection: "Ideas_for_Shooting_Videos"
resolve_page: "Color"
node_graph: "serial"
difficulty: "intermediate"
created: 2026-07-30
---

# Golden Hour Atmospheric Glow

**Source:** Instagram Reel `C9WuwXdh_0B` (Ideas_for_Shooting_Videos)  
**Page:** Color | **Graph:** serial | **Difficulty:** intermediate

![Golden Hour Atmospheric Glow](C9WuwXdh_0B.gif)

## Node Graph Structure

- Exposure
- Curves
- Color Wheels
- Power Window
- Soft Glow

## Parameters

- **Temperature**: +1500
- **Tint**: -5.0
- **Contrast**: 1.2
- **Saturation**: 0.65
- **Midtone Detail**: +0.15

## Steps to Reproduce in DaVinci Resolve

1. Adjust Exposure to lift shadows slightly while keeping highlights de-saturated.
2. Use the Curves node to create a slight S-curve, compressing the highlights and shadows for a filmic look.
3. Apply Color Wheels: push the Highlights toward a warm orange/gold and the Shadows toward a subtle teal/blue.
4. Use a Power Window on the sunlit buildings to increase saturation and luminance specifically where the light hits the architecture.
5. Add a Soft Glow effect with a high threshold and low opacity to create the atmospheric bloom/mist effect.
6. Use the Gradient tool to add a subtle warm gradient coming from one corner to simulate the sun area.

## Tags
`cinematic`, `golden-hour`, `atmospheric`, `landscape`, `warm-tones`
