---
name: davinci-cinematic-parallax-dolly-zoom
description: DaVinci Resolve technique: Cinematic Parallax Dolly Zoom from Instagram Reel Cz7i5bIP-3D
category: creative/davinci-resolve-techniques
tags: ["cinematic", "gimbal", "parallax", "fusion", "zoom", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "Cz7i5bIP-3D"
collection: "Gimbal_Moves"
resolve_page: "Fusion"
node_graph: "serial"
difficulty: "intermediate"
created: 2026-07-30
---

# Cinematic Parallax Dolly Zoom

**Source:** Instagram Reel `Cz7i5bIP-3D` (Gimbal_Moves)  
**Page:** Fusion | **Graph:** serial | **Difficulty:** intermediate

![Cinematic Parallax Dolly Zoom](Cz7i5bIP-3D.gif)

## Node Graph Structure

- MediaIn
- Transform
- Merge
- MediaOut

## Parameters

- **Center**: Keyframed horizontal movement
- **Scale**: Keyframed inverse zoom
- **Motion Blur**: Spline-based smoothing

## Steps to Reproduce in DaVinci Resolve

1. Bring the clip into the Fusion page
2. Add a Transform node after the MediaIn node
3. Set a keyframe at the start of the clip for Scale and Center
4. Move to the end of the clip and increase the Scale value significantly
5. Adjust the Center X coordinates to keep the subject framed in the center
6. Open the Spline editor to smooth the curves for fluid movement

## Tags
`cinematic`, `gimbal`, `parallax`, `fusion`, `zoom`
