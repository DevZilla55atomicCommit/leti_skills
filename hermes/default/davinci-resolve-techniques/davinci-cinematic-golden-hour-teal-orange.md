---
name: davinci-cinematic-golden-hour-teal-orange
description: DaVinci Resolve technique: Cinematic Golden Hour Teal & Orange from Instagram Reel C-4zER-oypa
category: creative/davinci-resolve-techniques
tags: ["cinematic", "golden-hour", "teal-and-orange", "glow", "nature", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "C-4zER-oypa"
collection: "Ideas_for_Shooting_Videos"
resolve_page: "Color"
node_graph: "serial"
difficulty: "intermediate"
created: 2026-07-30
---

# Cinematic Golden Hour Teal & Orange

**Source:** Instagram Reel `C-4zER-oypa` (Ideas_for_Shooting_Videos)  
**Page:** Color | **Graph:** serial | **Difficulty:** intermediate

![Cinematic Golden Hour Teal & Orange](C-4zER-oypa.gif)

## Node Graph Structure

- Primary Balance
- Curves
- Color Wheels
- Glow

## Parameters

- **Contrast**: 1.2
- **Saturation**: 0.6
- **Shadow_Tint**: #002b36
- **Highlight_Tint**: #ffcc66
- **Glow_Radius**: 0.5

## Steps to Reproduce in DaVinci Resolve

1. Apply a slight lift to the blacks to soften them without losing detail.
2. Use Color Wheels to push shadows toward a deep teal/cyan hue.
3. Use Color Wheels to push highlights toward a warm gold/orange hue.
4. Create an S-Curve to increase contrast, specifically protecting the highlights on the water.
5. Add a Glow node at the end of the chain with a low threshold and high radius to create the sun reflection bloom.
6. Desaturate the overall image slightly to let the complementary color contrast pop.

## Tags
`cinematic`, `golden-hour`, `teal-and-orange`, `glow`, `nature`
