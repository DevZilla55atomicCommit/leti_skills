---
name: davinci-atmospheric-forest-glow-selective-color-grading
description: DaVinci Resolve technique: Atmospheric Forest Glow & Selective Color Grading from Instagram Reel C6qxzZgRrWI
category: creative/davinci-resolve-techniques
tags: ["cinematic", "masking", "glow", "color-grading", "nature", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "C6qxzZgRrWI"
collection: "Footage_Collection"
resolve_page: "Color"
node_graph: "serial"
difficulty: "intermediate"
created: 2026-07-30
---

# Atmospheric Forest Glow & Selective Color Grading

**Source:** Instagram Reel `C6qxzZgRrWI` (Footage_Collection)  
**Page:** Color | **Graph:** serial | **Difficulty:** intermediate

![Atmospheric Forest Glow & Selective Color Grading](C6qxzZgRrWI.gif)

## Node Graph Structure

- Primary Grade
- Power Mask Highlight
- Glow Node
- Qualifier Node

## Parameters

- **Glow Threshold**: 0.5
- **Glow Radius**: 0.1
- **Midtone Detail**: Increased
- **Contrast**: 1.2
- **Saturation**: 1.3

## Steps to Reproduce in DaVinci Resolve

1. Import footage and apply a primary grade to balance the shadows and highlights.
2. Create a Power Window mask around the pink flower to increase saturation and sharpness specifically.
3. Add a Glow effect on a separate node with a soft threshold to simulate the sunburst atmospheric diffusion.
4. Use a Qualifier to select the green moss and shift the hue for a more vibrant forest look.
5. Increase Midtone Detail to bring out the rugged texture of the stone steps.
6. Add a subtle vignette to draw focus to the center.

## Tags
`cinematic`, `masking`, `glow`, `color-grading`, `nature`
