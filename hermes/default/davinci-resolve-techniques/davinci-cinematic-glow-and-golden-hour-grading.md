---
name: davinci-cinematic-glow-and-golden-hour-grading
description: DaVinci Resolve technique: Cinematic Glow and Golden Hour Grading from Instagram Reel DCaE1p7tnaW
category: creative/davinci-resolve-techniques
tags: ["cinematic", "glow", "golden-hour", "color-grading", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "DCaE1p7tnaW"
collection: "Ideas_for_Shooting_Videos"
resolve_page: "Color"
node_graph: "layer_mixer"
difficulty: "intermediate"
created: 2026-07-30
---

# Cinematic Glow and Golden Hour Grading

**Source:** Instagram Reel `DCaE1p7tnaW` (Ideas_for_Shooting_Videos)  
**Page:** Color | **Graph:** layer_mixer | **Difficulty:** intermediate

![Cinematic Glow and Golden Hour Grading](DCaE1p7tnaW.gif)

## Node Graph Structure

- Primary Correction
- Glow Node
- Color Tone Overlay

## Parameters

- **Glow Threshold**: 0.4
- **Glow Softness**: 0.6
- **Glow Gain**: 0.15
- **Saturation**: 1.2
- **Temperature**: 6500K (Warm shift)

## Steps to Reproduce in DaVinci Resolve

1. Create a primary node to balance exposure and boost warm yellow/orange tones.
2. Add a new node and right-click to select Add Layer Node.
3. Apply the Glow effect to the layer node.
4. Adjust the Glow Threshold to ensure only the brightest highlights bleed light.
5. Increase Glow Softness to create the ethereal haze seen in the sky.
6. Use the Layer Mixer to blend the glow back with the original image, adjusting opacity.
7. Apply a Teal and Orange color wheels adjustment to deepen the shadows while keeping highlights golden.

## Tags
`cinematic`, `glow`, `golden-hour`, `color-grading`
