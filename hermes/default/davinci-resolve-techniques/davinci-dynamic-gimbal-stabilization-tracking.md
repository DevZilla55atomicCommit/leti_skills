---
name: davinci-dynamic-gimbal-stabilization-tracking
description: DaVinci Resolve technique: Dynamic Gimbal Stabilization & Tracking from Instagram Reel C0jhrCjvFoa
category: creative/davinci-resolve-techniques
tags: ["stabilization", "gimbal", "cinematic", "video-editing", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "C0jhrCjvFoa"
collection: "Gimbal_Moves"
resolve_page: "Color"
node_graph: "serial"
difficulty: "intermediate"
created: 2026-07-30
---

# Dynamic Gimbal Stabilization & Tracking

**Source:** Instagram Reel `C0jhrCjvFoa` (Gimbal_Moves)  
**Page:** Color | **Graph:** serial | **Difficulty:** intermediate

![Dynamic Gimbal Stabilization & Tracking](C0jhrCjvFoa.gif)

## Node Graph Structure

- MediaIn
- Stabilizer
- MediaOut

## Parameters

- **Mode**: Planar Projection
- **Smoothing**: 50.0
- **Camera Lock**: 0.0

## Steps to Reproduce in DaVinci Resolve

1. Import the footage into the timeline
2. Go to the Color page
3. Open the Stabilizer tab
4. Select Planar Projection for better camera movement handling
5. Adjust Smoothing values to remove micro-jitters
6. Click Stabilize to apply the effect to the duration of the clip

## Tags
`stabilization`, `gimbal`, `cinematic`, `video-editing`
