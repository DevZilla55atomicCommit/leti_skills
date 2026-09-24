---
name: davinci-vertical-split-screen-comparison
description: DaVinci Resolve technique: Vertical Split-Screen Comparison from Instagram Reel C4gqp94Jhrm
category: creative/davinci-resolve-techniques
tags: ["split-screen", "comparison", "interior-design", "video-editing", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "C4gqp94Jhrm"
collection: "Gimbal_Moves"
resolve_page: "Edit"
node_graph: "serial"
difficulty: "beginner"
created: 2026-07-30
---

# Vertical Split-Screen Comparison

**Source:** Instagram Reel `C4gqp94Jhrm` (Gimbal_Moves)  
**Page:** Edit | **Graph:** serial | **Difficulty:** beginner

![Vertical Split-Screen Comparison](C4gqp94Jhrm.gif)

## Node Graph Structure

- Video Clip 1
- Video Clip 2
- Transform

## Parameters

- **Crop Top**: 50
- **Position Y**: 540

## Steps to Reproduce in DaVinci Resolve

1. Place the two video clips on separate tracks in the timeline (V2 for top, V1 for bottom).
2. Select the top clip (V2).
3. In the Inspector, go to Crop and set Crop Top to 50% to reveal the bottom clip.
4. Adjust 'Position Y' on both clips to perfectly align the subjects within the frame.
5. Adjust 'Zoom' on both clips to ensure they fill their respective halves perfectly.

## Tags
`split-screen`, `comparison`, `interior-design`, `video-editing`
