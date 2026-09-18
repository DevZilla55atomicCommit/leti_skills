---
name: davinci-inverted-landscape-split-tone-mirror
description: DaVinci Resolve technique: Inverted Landscape Split-Tone Mirror from Instagram Reel C-xEAOoMFpF
category: creative/davinci-resolve-techniques
tags: ["surreal", "mirror-effect", "split-tone", "landscape", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "C-xEAOoMFpF"
collection: "Ideas_for_Shooting_Videos"
resolve_page: "Color"
node_graph: "parallel"
difficulty: "intermediate"
created: 2026-07-30
---

# Inverted Landscape Split-Tone Mirror

**Source:** Instagram Reel `C-xEAOoMFpF` (Ideas_for_Shooting_Videos)  
**Page:** Color | **Graph:** parallel | **Difficulty:** intermediate

![Inverted Landscape Split-Tone Mirror](C-xEAOoMFpF.gif)

## Node Graph Structure

- Primary Correction
- Split Mask
- Mirror Flip
- Color Balance (Cool)
- Color Balance (Warm)

## Parameters

- **mask_type**: Linear Gradient
- **soft_edge**: 0.0
- **contrast**: 1.2
- **saturation**: 1.4

## Steps to Reproduce in DaVinci Resolve

1. Import clip and go to the Color page.
2. Create a parallel node structure to split the image into top and bottom halves.
3. On the top node, apply a Linear Gradient mask to isolate the upper half.
4. Apply a 'Flip' effect or use Fusion to rotate the isolated layer 180 degrees.
5. On the top-half node, grade using Teal/Blue tones in the shadows and highlights.
6. On the bottom-half node, grade using Warm/Orange tones in the midtones and increase contrast.
7. Adjust the mask softness to zero to ensure the seam is perfectly sharp for the surreal effect.

## Tags
`surreal`, `mirror-effect`, `split-tone`, `landscape`
