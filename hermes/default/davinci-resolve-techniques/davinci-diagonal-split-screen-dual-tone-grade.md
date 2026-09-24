---
name: davinci-diagonal-split-screen-dual-tone-grade
description: DaVinci Resolve technique: Diagonal Split-Screen Dual-Tone Grade from Instagram Reel C9Ar1tBslvy
category: creative/davinci-resolve-techniques
tags: ["split-screen", "masking", "monochrome", "cinematic", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "C9Ar1tBslvy"
collection: "Ideas_for_Shooting_Videos"
resolve_page: "Color"
node_graph: "parallel"
difficulty: "intermediate"
created: 2026-07-30
---

# Diagonal Split-Screen Dual-Tone Grade

**Source:** Instagram Reel `C9Ar1tBslvy` (Ideas_for_Shooting_Videos)  
**Page:** Color | **Graph:** parallel | **Difficulty:** intermediate

![Diagonal Split-Screen Dual-Tone Grade](C9Ar1tBslvy.gif)

## Node Graph Structure

- Primary Correction
- Qualifier Mask
- Grayscale Node
- Final Vignette

## Parameters

- **mask_shape**: Diagonal Linear
- **saturation**: 0.0
- **contrast**: 1.2
- **soft_edge**: 0.15

## Steps to Reproduce in DaVinci Resolve

1. Place both clips on separate tracks in the Edit page
2. Go to the Color page and use a Window mask to draw a diagonal line across the frame
3. Apply a soft edge to the window mask to blend the transition
4. Create a parallel node for the bottom-half clip and drop the Saturation to 0
5. Apply a slight warm tint to the highlights and shadows of the top-half color clip
6. Add a text overlay on a Title layer overlapping the intersection

## Tags
`split-screen`, `masking`, `monochrome`, `cinematic`
