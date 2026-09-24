---
name: davinci-selective-golden-hour-glow-masking
description: DaVinci Resolve technique: Selective Golden Hour Glow & Masking from Instagram Reel C6jMqtFxf5O
category: creative/davinci-resolve-techniques
tags: ["cinematic", "golden-hour", "masking", "macro-style", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "C6jMqtFxf5O"
collection: "Footage_Collection"
resolve_page: "Color"
node_graph: "serial"
difficulty: "intermediate"
created: 2026-07-30
---

# Selective Golden Hour Glow & Masking

**Source:** Instagram Reel `C6jMqtFxf5O` (Footage_Collection)  
**Page:** Color | **Graph:** serial | **Difficulty:** intermediate

![Selective Golden Hour Glow & Masking](C6jMqtFxf5O.gif)

## Node Graph Structure

- Primary Correction
- Qualifier/Power Mask
- Glow/Soft Light
- Color Sharpening

## Parameters

- **Contrast**: High
- **Saturation**: Increased in yellows
- **Glow Radius**: Medium-Large
- **Highlights**: Boosted for starburst effect

## Steps to Reproduce in DaVinci Resolve

1. Perform a primary color grade to balance the blue-toned shadows and golden-toned highlights.
2. Use a Qualifier or Power Window to select only the yellow dandelions and the sun reflections.
3. Apply a Glow effect to the masked area to create an ethereal light bleed around the flowers.
4. Use a Parallel node to de-aturate the blue ice areas to make the flowers pop.
5. Add a sharpening pass specifically to the dandelion petals to define the fine textures.

## Tags
`cinematic`, `golden-hour`, `masking`, `macro-style`
