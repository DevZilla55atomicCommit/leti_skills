---
name: davinci-masking-transition-using-architectural-lines
description: DaVinci Resolve technique: Masking Transition using Architectural Lines from Instagram Reel C3oKNjevXpL
category: creative/davinci-resolve-techniques
tags: ["cinematography", "transition", "masking", "fusion", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "C3oKNjevXpL"
collection: "Gimbal_Moves"
resolve_page: "Fusion"
node_graph: "layer_mixer"
difficulty: "intermediate"
created: 2026-07-30
---

# Masking Transition using Architectural Lines

**Source:** Instagram Reel `C3oKNjevXpL` (Gimbal_Moves)  
**Page:** Fusion | **Graph:** layer_mixer | **Difficulty:** intermediate

![Masking Transition using Architectural Lines](C3oKNjevXpL.gif)

## Node Graph Structure

- MediaIn1
- MediaIn2
- MaskPaint
- Merge

## Parameters

- **mask_shape**: Polygon
- **soft_edge**: 0.1
- **interpolation**: Linear

## Steps to Reproduce in DaVinci Resolve

1. Place two clips on the timeline where a moving architectural line aligns between them
2. Send both clips to the Fusion page
3. Add a Polygon mask to the top clip
4. Draw the mask following the edge of the architectural element (e.g., a window frame)
5. Keyframe the mask path as the camera moves to reveal the frame
6. Adjust the Soft Edge of the mask to blend the transition

## Tags
`cinematography`, `transition`, `masking`, `fusion`
