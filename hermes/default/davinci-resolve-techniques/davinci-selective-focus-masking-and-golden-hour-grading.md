---
name: davinci-selective-focus-masking-and-golden-hour-grading
description: DaVinci Resolve technique: Selective Focus Masking and Golden Hour Grading from Instagram Reel C7JtgxmxumW
category: creative/davinci-resolve-techniques
tags: ["cinematic", "masking", "grading", "nature", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "C7JtgxmxumW"
collection: "Footage_Collection"
resolve_page: "Color"
node_graph: "serial"
difficulty: "intermediate"
created: 2026-07-30
---

# Selective Focus Masking and Golden Hour Grading

**Source:** Instagram Reel `C7JtgxmxumW` (Footage_Collection)  
**Page:** Color | **Graph:** serial | **Difficulty:** intermediate

![Selective Focus Masking and Golden Hour Grading](C7JtgxmxumW.gif)

## Node Graph Structure

- Primary Correction
- Qualifier/Masking
- Power Window

## Parameters

- **Softness**: 50.0
- **Saturation**: +15.0
- **Color Tint (Midtones)**: Warm Orange
- **Vignette**: Subtle Dark

## Steps to Reproduce in DaVinci Resolve

1. Import clip and go to the Color page.
2. Apply primary color correction to balance exposure and contrast across the whole clip.
3. Create a Power Window (circular shape) around the daisy and stem.
4. Increase the Softness of the window edge to ensure a seamless transition.
5. Increase exposure and saturation specifically within the mask to make the flower pop.
6. Use a tracking node to ensure the mask follows the flower if there is camera movement.
7. Apply a global vignette to draw attention further to the center where the flower is located.

## Tags
`cinematic`, `masking`, `grading`, `nature`
