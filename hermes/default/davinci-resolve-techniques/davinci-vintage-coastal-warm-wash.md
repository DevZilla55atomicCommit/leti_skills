---
name: davinci-vintage-coastal-warm-wash
description: DaVinci Resolve technique: Vintage Coastal Warm Wash from Instagram Reel C9Ut0qqJDP8
category: creative/davinci-resolve-techniques
tags: ["vintage", "warm", "faded", "cinematic", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "C9Ut0qqJDP8"
collection: "Ideas_for_Shooting_Videos"
resolve_page: "Color"
node_graph: "serial"
difficulty: "intermediate"
created: 2026-07-30
---

# Vintage Coastal Warm Wash

**Source:** Instagram Reel `C9Ut0qqJDP8` (Ideas_for_Shooting_Videos)  
**Page:** Color | **Graph:** serial | **Difficulty:** intermediate

![Vintage Coastal Warm Wash](C9Ut0qqJDP8.gif)

## Node Graph Structure

- Primary Balance
- Curves
- Color Wheels
- Soft Glow

## Parameters

- **lift_tint**: Teal/Blue
- **gain_tint**: Warm Orange/Yellow
- **saturation**: 0.75
- **contrast**: 0.9
- **faded_blacks**: 0.15

## Steps to Reproduce in DaVinci Resolve

1. Lift the black point in the Curves tool to create faded blacks.
2. Apply a warm tint to the Gain/Highlights and a subtle cool tint to the Lift/Shadows.
3. Use the Qualifier to desaturate everything except for the reds of the umbrellas.
4. Add a Soft Glow node with a high threshold and low opacity to de-diffuse highlights.
5. Desaturate global saturation slightly to achieve a cinematic film look.

## Tags
`vintage`, `warm`, `faded`, `cinematic`
