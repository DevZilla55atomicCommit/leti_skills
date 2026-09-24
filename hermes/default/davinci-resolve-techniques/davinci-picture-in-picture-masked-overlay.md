---
name: davinci-picture-in-picture-masked-overlay
description: DaVinci Resolve technique: Picture-in-Picture Masked Overlay from Instagram Reel C5rRQpEpo35
category: creative/davinci-resolve-techniques
tags: ["cinematic", "overlay", "picture-in-picture", "masking", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "C5rRQpEpo35"
collection: "Gimbal_Moves"
resolve_page: "Edit"
node_graph: "serial"
difficulty: "beginner"
created: 2026-07-30
---

# Picture-in-Picture Masked Overlay

**Source:** Instagram Reel `C5rRQpEpo35` (Gimbal_Moves)  
**Page:** Edit | **Graph:** serial | **Difficulty:** beginner

![Picture-in-Picture Masked Overlay](C5rRQpEpo35.gif)

## Node Graph Structure

- Background Clip
- Overlay Clip

## Parameters

- **Gaussian Blur**: High
- **Crop/Mask**: Rectangular
- **Opacity**: 100%

## Steps to Reproduce in DaVinci Resolve

1. Place the main background clip on Video Track 1.
2. Place the detail clip on Video Track 2 directly above it.
3. Select Track 1 and go to the Effects Library to apply a Gaussian Blur effect to create the blurred background.
4. Select Track 2 and go to the Inspector > Video > Crop.
5. Adjust the Cropping tool sliders to define the rectangular area for the inset.
6. Use the Zoom and Position controls to resize and place the masked inset in the top-left corner.

## Tags
`cinematic`, `overlay`, `picture-in-picture`, `masking`
