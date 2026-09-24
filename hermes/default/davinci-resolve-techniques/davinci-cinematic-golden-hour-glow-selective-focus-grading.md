---
name: davinci-cinematic-golden-hour-glow-selective-focus-grading
description: DaVinci Resolve technique: Cinematic Golden Hour Glow & Selective Focus Grading from Instagram Reel C7HNyWqRkIR
category: creative/davinci-resolve-techniques
tags: ["cinematic", "color-grading", "bloom", "golden-hour", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "C7HNyWqRkIR"
collection: "Footage_Collection"
resolve_page: "Color"
node_graph: "serial"
difficulty: "intermediate"
created: 2026-07-30
---

# Cinematic Golden Hour Glow & Selective Focus Grading

**Source:** Instagram Reel `C7HNyWqRkIR` (Footage_Collection)  
**Page:** Color | **Graph:** serial | **Difficulty:** intermediate

![Cinematic Golden Hour Glow & Selective Focus Grading](C7HNyWqRkIR.gif)

## Node Graph Structure

- Exposure Adjustment
- Primary Balance
- Glow Node
- Power Window Mask

## Parameters

- **Glow-Spread**: 0.50
- **Glow-Threshold**: 0.4
- **Midtone Tint**: Warm/Orange
- **Lift**: Teal/Blue

## Steps to Reproduce in DaVinci Resolve

1. Add a primary node to balance exposure, highlighting the sunburst highlights.
2. Apply a Teal and Orange color grade by pushing shadows to blue and highlights to orange.
3. Use a Power Window to track the flower and increase its saturation and sharpness specifically.
4. Add a Glow node with a high threshold and soft spread to create the ethereal light around the petals.
5. Use the Depth of Blur tool on a separate background layer to simulate the shallow focal field if not captured natively.

## Tags
`cinematic`, `color-grading`, `bloom`, `golden-hour`
