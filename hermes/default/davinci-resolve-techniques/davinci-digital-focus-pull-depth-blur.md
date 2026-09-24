---
name: davinci-digital-focus-pull-depth-blur
description: DaVinci Resolve technique: Digital Focus Pull / Depth Blur from Instagram Reel C-tul9VgTZp
category: creative/davinci-resolve-techniques
tags: ["focus-pull", "depth-of-field", "fusion", "cinematic", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "C-tul9VgTZp"
collection: "Gimbal_Moves"
resolve_page: "Fusion"
node_graph: "serial"
difficulty: "intermediate"
created: 2026-07-30
---

# Digital Focus Pull / Depth Blur

**Source:** Instagram Reel `C-tul9VgTZp` (Gimbal_Moves)  
**Page:** Fusion | **Graph:** serial | **Difficulty:** intermediate

![Digital Focus Pull / Depth Blur](C-tul9VgTZp.gif)

## Node Graph Structure

- MediaIn
- Gaussian Blur
- Merge

## Parameters

- **Blur Radius**: Interpolated via keyframes
- **Edge Range**: All
- **Softness**: Keyframed adjusted

## Steps to Reproduce in DaVinci Resolve

1. Import the clip into the Fusion page.
2. Add a Gaussian Blur node after the MediaIn.
3. Create a Mask (Polygon or Ellipse) to isolate the foreground object.
4. Keyframe the Blur Radius to start at 0 when the object is in focus.
5. Keyframe the Blur Radius to a high value when the focus shifts to the background subject.
6. Adjust the mask feather to ensure a natural transition between planes.

## Tags
`focus-pull`, `depth-of-field`, `fusion`, `cinematic`
