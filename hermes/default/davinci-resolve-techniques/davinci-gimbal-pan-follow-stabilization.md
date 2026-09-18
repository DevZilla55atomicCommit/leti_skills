---
name: davinci-gimbal-pan-follow-stabilization
description: DaVinci Resolve technique: Gimbal Pan Follow Stabilization from Instagram Reel C0DrUvkr_vU
category: creative/davinci-resolve-techniques
tags: ["cinematography", "stabilization", "gimbal", "camera movement", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "C0DrUvkr_vU"
collection: "Gimbal_Moves"
resolve_page: "Edit"
node_graph: "serial"
difficulty: "beginner"
created: 2026-07-30
---

# Gimbal Pan Follow Stabilization

**Source:** Instagram Reel `C0DrUvkr_vU` (Gimbal_Moves)  
**Page:** Edit | **Graph:** serial | **Difficulty:** beginner

![Gimbal Pan Follow Stabilization](C0DrUvkr_vU.gif)

## Node Graph Structure

- Camera Clip
- Stabilizer

## Parameters

- **Stabilization Mode**: Camera Plane
- **Smoothing**: 50.0
- **Locking**: None

## Steps to Reproduce in DaVinci Resolve

1. Import the handheld pan footage into the Edit timeline
2. Open the Inspector tab
3. Navigate to the Stabilizer tool
4. Set Mode to Camera Plane to allow for lateral movement
5. Adjust the Smoothing value to remove jitter without cropping too much
6. Enable Dynamic Zoom to hide the frame edges

## Tags
`cinematography`, `stabilization`, `gimbal`, `camera movement`
