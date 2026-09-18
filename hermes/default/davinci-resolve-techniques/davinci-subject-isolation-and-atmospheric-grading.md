---
name: davinci-subject-isolation-and-atmospheric-grading
description: DaVinci Resolve technique: Subject Isolation and Atmospheric Grading from Instagram Reel C6oihedxzrf
category: creative/davinci-resolve-techniques
tags: ["masking", "depth-of-field", "color grading", "surrealism", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "C6oihedxzrf"
collection: "Footage_Collection"
resolve_page: "Color"
node_graph: "serial"
difficulty: "intermediate"
created: 2026-07-30
---

# Subject Isolation and Atmospheric Grading

**Source:** Instagram Reel `C6oihedxzrf` (Footage_Collection)  
**Page:** Color | **Graph:** serial | **Difficulty:** intermediate

![Subject Isolation and Atmospheric Grading](C6oihedxzrf.gif)

## Node Graph Structure

- Primary Correction
- Magic Qualifier Mask
- Gaussian Blur
- Color Wheels

## Parameters

- **Blur Radius**: High
- **Mask Edge Softness**: Soft
- **Saturation (Subject)**: +15
- **Midtone Tint**: Cool/Blue

## Steps to Reproduce in DaVinci Resolve

1. Import footage and go to the Color page.
2. Use the Magic Qualifier or Power Window to select the pink flower and immediate foreground.
3. Refine the mask edges to ensure the flower is isolated from the mountains.
4. Create a separate node for the background and apply a Gaussian Blur to simulate shallow depth of field.
5. On the subject node, increase saturation and contrast to make the flower pop.
6. Apply a cool color grade to the background nodes to create atmospheric depth.

## Tags
`masking`, `depth-of-field`, `color grading`, `surrealism`
