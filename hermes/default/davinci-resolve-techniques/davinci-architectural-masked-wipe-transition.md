---
name: davinci-architectural-masked-wipe-transition
description: DaVinci Resolve technique: Architectural Masked Wipe Transition from Instagram Reel CxC953sLA2w
category: creative/davinci-resolve-techniques
tags: ["transition", "masking", "fusion", "cinematography", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "CxC953sLA2w"
collection: "Gimbal_Moves"
resolve_page: "Fusion"
node_graph: "serial"
difficulty: "intermediate"
created: 2026-07-30
---

# Architectural Masked Wipe Transition

**Source:** Instagram Reel `CxC953sLA2w` (Gimbal_Moves)  
**Page:** Fusion | **Graph:** serial | **Difficulty:** intermediate

![Architectural Masked Wipe Transition](CxC953sLA2w.gif)

## Node Graph Structure

- MediaIn1
- MediaIn2
- Merge
- Polygon

## Parameters

- **Mask Softness**: 10-20
- **Channel**: Alpha
- **Keyframe Mode**: Frame

## Steps to Reproduce in DaVinci Resolve

1. Place two clips on the timeline back-to-back
2. Right-click and select 'Open in Fusion'
3. Add a Merge node and connect both MediaIn nodes
4. Add a Polygon mask to the Merge node's blue input
5. Draw the mask around the edge of the architectural structure
6. Keyframe the mask path to follow the building edge during the camera movement
7. Adjust Mask Softness to create a seamless blend

## Tags
`transition`, `masking`, `fusion`, `cinematography`
