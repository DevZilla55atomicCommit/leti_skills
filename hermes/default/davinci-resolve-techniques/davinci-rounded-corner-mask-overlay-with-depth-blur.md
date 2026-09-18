---
name: davinci-rounded-corner-mask-overlay-with-depth-blur
description: DaVinci Resolve technique: Rounded Corner Mask Overlay with Depth Blur from Instagram Reel C-r7SZNMndS
category: creative/davinci-resolve-techniques
tags: ["masking", "overlay", "picture-in-picture", "tutorial", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "C-r7SZNMndS"
collection: "Ideas_for_Shooting_Videos"
resolve_page: "Fusion"
node_graph: "layer-mixer"
difficulty: "beginner"
created: 2026-07-30
---

# Rounded Corner Mask Overlay with Depth Blur

**Source:** Instagram Reel `C-r7SZNMndS` (Ideas_for_Shooting_Videos)  
**Page:** Fusion | **Graph:** layer-mixer | **Difficulty:** beginner

![Rounded Corner Mask Overlay with Depth Blur](C-r7SZNMndS.gif)

## Node Graph Structure

- MediaIn1
- MediaIn2
- Rectangle
- Transform

## Parameters

- **mask_shape**: Rounded
- **corner_radius**: 0.05
- **softness**: 0.01
- **opacity**: 1.0

## Steps to Reproduce in DaVinci Resolve

1. Place the background video/image on MediaIn1.
2. Place the inset video/image on MediaIn2 above above it.
3. Add a Rectangle mask to MediaIn2 and connect it to the blue input.
4. Increase the 'Corner Radius' in the Rectangle settings to create the rounded edges.
5. Add a Transform node after MediaIn2 to scale and position the inset.
6. Add a Gaussian Blur node to MediaIn1 to create the shallow depth of field effect.

## Tags
`masking`, `overlay`, `picture-in-picture`, `tutorial`
