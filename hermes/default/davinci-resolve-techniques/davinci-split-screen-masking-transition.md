---
name: davinci-split-screen-masking-transition
description: DaVinci Resolve technique: Split-Screen Masking Transition from Instagram Reel C2ii4dYJ4Pt
category: creative/davinci-resolve-techniques
tags: ["split-screen", "cinematography", "layout", "transition", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "C2ii4dYJ4Pt"
collection: "Gimbal_Moves"
resolve_page: "Edit"
node_graph: "serial"
difficulty: "beginner"
created: 2026-07-30
---

# Split-Screen Masking Transition

**Source:** Instagram Reel `C2ii4dYJ4Pt` (Gimbal_Moves)  
**Page:** Edit | **Graph:** serial | **Difficulty:** beginner

![Split-Screen Masking Transition](C2ii4dYJ4Pt.gif)

## Node Graph Structure

- Adjustment Clip
- Video Track

## Parameters

- **Crop Top**: 50%
- **Transform Y**: 0.0
- **Zoom**: 1.000

## Steps to Reproduce in DaVinci Resolve

1. Place two video clips on different tracks (V1 and V2)
2. Select the top clip (V2) and use the Crop tool in the Inspector to crop the bottom half to 50%
3. Adjust the Transform Y position of clips to align the subjects within their frames
4. Add keyframes to the Crop parameter to create a sliding split effect

## Tags
`split-screen`, `cinematography`, `layout`, `transition`
