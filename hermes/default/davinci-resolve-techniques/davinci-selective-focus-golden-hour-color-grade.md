---
name: davinci-selective-focus-golden-hour-color-grade
description: DaVinci Resolve technique: Selective Focus & Golden Hour Color Grade from Instagram Reel C7EvL5ZvHoH
category: creative/davinci-resolve-techniques
tags: ["cinematic", "color-grading", "bokeh", "golden-hour", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "C7EvL5ZvHoH"
collection: "Footage_Collection"
resolve_page: "Color"
node_graph: "serial"
difficulty: "intermediate"
created: 2026-07-30
---

# Selective Focus & Golden Hour Color Grade

**Source:** Instagram Reel `C7EvL5ZvHoH` (Footage_Collection)  
**Page:** Color | **Graph:** serial | **Difficulty:** intermediate

![Selective Focus & Golden Hour Color Grade](C7EvL5ZvHoH.gif)

## Node Graph Structure

- Primary Correction
- Qualifier Mask
- Power Window
- Glow Node

## Parameters

- **Contrast**: 1.20
- **Saturation**: 1.1
- **Glow Spread**: 0.500
- **Midtone Tint**: Warm (Orange/Gold)

## Steps to Reproduce in DaVinci Resolve

1. Import clip and perform primary exposure balancing to preserve the sunset highlights.
2. Use a Power Window (circular) to isolate the daffodil and increase its sharpness/exposure.
3. Apply a Gaussian Blur to a duplicate node or the background to simulate a shallow depth-of-field lens.
4. Add a Glow node to the sun area to create a soft bloom/starburst effect.
5. Use Color Wheels to push warm oranges into the highlights and teals/blues into the shadows for cinematic contrast.

## Tags
`cinematic`, `color-grading`, `bokeh`, `golden-hour`
