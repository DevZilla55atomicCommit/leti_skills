---
name: davinci-volumetric-silhouette-rim-glow
description: DaVinci Resolve technique: Volumetric Silhouette & Rim Glow from Instagram Reel C-R9OJip1h0
category: creative/davinci-resolve-techniques
tags: ["volumetric light", "silhouette", "rim light", "cinematic", "glow", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "C-R9OJip1h0"
collection: "Ideas_for_Shooting_Videos"
resolve_page: "Fusion"
node_graph: "serial"
difficulty: "intermediate"
created: 2026-07-30
---

# Volumetric Silhouette & Rim Glow

**Source:** Instagram Reel `C-R9OJip1h0` (Ideas_for_Shooting_Videos)  
**Page:** Fusion | **Graph:** serial | **Difficulty:** intermediate

![Volumetric Silhouette & Rim Glow](C-R9OJip1h0.gif)

## Node Graph Structure

- MediaIn
- Glow
- SoftGlow
- Merge

## Parameters

- **Glow Gain**: 1.5
- **Glow Size**: 25.0
- **Threshold**: 0.4
- **Contrast**: 1.2

## Steps to Reproduce in DaVinci Resolve

1. Import clip into the Fusion page.
2. Use a Polygon mask or Magic Mask to isolate the hand and invert it to create a silhouette effect.
3. Apply a Glow or SoftGlow node to the light source to create the ethereal bloom.
4. Add a Fast Noise node with a radial gradient mask to simulate volumetric light beams (god rays).
5. Use a Color Correction node to crush the blacks and push the blue/teal highlights.
6. Adjust the threshold to ensure the light only catches the brightest edges of the hand.

## Tags
`volumetric light`, `silhouette`, `rim light`, `cinematic`, `glow`
