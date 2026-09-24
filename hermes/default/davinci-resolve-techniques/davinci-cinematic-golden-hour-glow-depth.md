---
name: davinci-cinematic-golden-hour-glow-depth
description: DaVinci Resolve technique: Cinematic Golden Hour Glow & Depth from Instagram Reel C7CHdc4xluI
category: creative/davinci-resolve-techniques
tags: ["cinematic", "color-grading", "bloom", "golden-hour", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "C7CHdc4xluI"
collection: "Footage_Collection"
resolve_page: "Color"
node_graph: "serial"
difficulty: "intermediate"
created: 2026-07-30
---

# Cinematic Golden Hour Glow & Depth

**Source:** Instagram Reel `C7CHdc4xluI` (Footage_Collection)  
**Page:** Color | **Graph:** serial | **Difficulty:** intermediate

![Cinematic Golden Hour Glow & Depth](C7CHdc4xluI.gif)

## Node Graph Structure

- Primary Grade
- Power Mask
- Glow Node
- Parallel Qualifier

## Parameters

- **Contrast**: High
- **Saturation**: Boosted Highlights
- **Glow Radius**: Large
- **Glow Threshold**: Soft
- **Vette Tint**: Warm/Orange

## Steps to Reproduce in DaVinci Resolve

1. Apply a primary grade to balance contrast and push shadows toward teal and highlights toward orange.
2. Use a Power Mask or Qualifier to isolate the flower and increase its saturation and sharpness.
3. Add a Glow node with a high radius and low opacity to create the ethereal light bleed on the water reflections.
4. Use the Blur tool on a separate node for the background to simulate shallow depth of field if not captured in camera.
5. Add a global vignette to draw focus to the center subject.

## Tags
`cinematic`, `color-grading`, `bloom`, `golden-hour`
