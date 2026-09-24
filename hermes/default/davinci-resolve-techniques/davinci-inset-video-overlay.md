---
name: davinci-inset-video-overlay
description: DaVinci Resolve technique: Inset Video Overlay from Instagram Reel C7C1mRbJIU1
category: creative/davinci-resolve-techniques
tags: ["Instagram Reel", "Split Screen", "Inset Video", "DaVinci Resolve", "Fusion", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "C7C1mRbJIU1"
collection: "Gimbal_Moves"
resolve_page: "Fusion"
node_graph: "compound"
difficulty: "intermediate"
created: 2026-07-30
---

# Inset Video Overlay

**Source:** Instagram Reel `C7C1mRbJIU1` (Gimbal_Moves)  
**Page:** Fusion | **Graph:** compound | **Difficulty:** intermediate

![Inset Video Overlay](C7C1mRbJIU1.gif)

## Node Graph Structure

- Compound
- Position
- Scale

## Parameters

- **param_0**: {'parameter': 'position', 'value': '[x: 100, y: 50]'}
- **param_1**: {'parameter': 'scale', 'value': '0.5 (50% size)'}
- **param_2**: {'parameter': 'opacity', 'value': '0.7 (semi-transparent)'}

## Steps to Reproduce in DaVinci Resolve

1. Import main footage and inset video into Fusion timeline
2. Create a Compound node with main footage as base layer
3. Add inset video as top layer within the compound
4. Adjust Position to top-left corner, Scale to reduce size, and Opacity for visibility

## Tags
`Instagram Reel`, `Split Screen`, `Inset Video`, `DaVinci Resolve`, `Fusion`
