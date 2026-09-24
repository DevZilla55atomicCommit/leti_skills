---
name: davinci-selective-saturation-via-qualifier-mask
description: DaVinci Resolve technique: Selective Saturation via Qualifier Mask from Instagram Reel C9SWFHvIVeO
category: creative/davinci-resolve-techniques
tags: ["cinematic", "selective-color", "editorial", "masking", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "C9SWFHvIVeO"
collection: "Ideas_for_Shooting_Videos"
resolve_page: "Color"
node_graph: "serial"
difficulty: "intermediate"
created: 2026-07-30
---

# Selective Saturation via Qualifier Mask

**Source:** Instagram Reel `C9SWFHvIVeO` (Ideas_for_Shooting_Videos)  
**Page:** Color | **Graph:** serial | **Difficulty:** intermediate

![Selective Saturation via Qualifier Mask](C9SWFHvIVeO.gif)

## Node Graph Structure

- Primary Grade
- Qualifier Mask
- Desaturation Background Node

## Parameters

- **saturation**: 0.0
- **hue_range**: Skin tones focus
- **softness**: High
- **contrast**: Increased in de-midtones

## Steps to Reproduce in DaVinci Resolve

1. Create a primary node for overall color grading of the entire image.
2. Use the Qualifier tool (Hue vs Hue) to select the subject skin tones and vibrant clothing colors.
3. Refine the selection using Power Windows and Blur to ensure no background elements are included.
4. Invert the selection on a new node to target the background.
5. Drop the saturation on the inverted background node to create the monochromatic effect.
6. Apply a cool tint (blue/cyan) to the background node to match the image aesthetic.

## Tags
`cinematic`, `selective-color`, `editorial`, `masking`
