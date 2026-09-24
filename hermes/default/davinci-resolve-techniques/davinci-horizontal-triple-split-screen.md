---
name: davinci-horizontal-triple-split-screen
description: DaVinci Resolve technique: Horizontal Triple Split-Screen from Instagram Reel C6FCb-qJjrx
category: creative/davinci-resolve-techniques
tags: ["split-screen", "layout", "composition", "video-editing", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "C6FCb-qJjrx"
collection: "Gimbal_Moves"
resolve_page: "Fusion"
node_graph: "parallel"
difficulty: "beginner"
created: 2026-07-30
---

# Horizontal Triple Split-Screen

**Source:** Instagram Reel `C6FCb-qJjrx` (Gimbal_Moves)  
**Page:** Fusion | **Graph:** parallel | **Difficulty:** beginner

![Horizontal Triple Split-Screen](C6FCb-qJjrx.gif)

## Node Graph Structure

- MediaIn
- Crop
- Merge
- Text+

## Parameters

- **Crop_Top**: 33%
- **Crop_Bottom**: 33%
- **Center_Y**: variable

## Steps to Reproduce in DaVinci Resolve

1. Bring three instances of the same clip into the Fusion timeline.
2. Add a Crop node after each MediaIn.
3. Adjust the Crop parameters of the top clip to show only the upper 33%.
4. Adjust the Crop parameters of the middle clip to show only the center 33%.
5. Adjust the Crop parameters of the bottom clip to show only the lower 33%.
6. Use two Merge nodes to stack the three clips vertically by adjusting their Y-Center position.
7. Add a Text+ node over the middle layer.

## Tags
`split-screen`, `layout`, `composition`, `video-editing`
