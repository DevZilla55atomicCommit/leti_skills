---
name: davinci-orbital-tracking-shot-simulation
description: DaVinci Resolve technique: Orbital Tracking Shot Simulation from Instagram Reel C3Q-N1hPM_x
category: creative/davinci-resolve-techniques
tags: ["cinematography", "gimbal", "orbit", "camera-movement", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "C3Q-N1hPM_x"
collection: "Gimbal_Moves"
resolve_page: "Edit"
node_graph: "serial"
difficulty: "intermediate"
created: 2026-07-30
---

# Orbital Tracking Shot Simulation

**Source:** Instagram Reel `C3Q-N1hPM_x` (Gimbal_Moves)  
**Page:** Edit | **Graph:** serial | **Difficulty:** intermediate

![Orbital Tracking Shot Simulation](C3Q-N1hPM_x.gif)

## Node Graph Structure

- Media Pool
- Dynamic Zoom
- Transform

## Parameters

- **rotation**: arc-based
- **position**: curved-path
- **center_point**: subject-locked

## Steps to Reproduce in DaVinci Resolve

1. Place your footage on the Edit timeline
2. Go to the Fusion page or use the Transform tool
3. Set a keyframe at the start and end of the clip
4. Animate the X and Y position to follow a curved path
5. Animate the Rotation parameter to keep the subject centered as the camera moves
6. Apply Bezier curves to the keyframes for smooth, fluid motion

## Tags
`cinematography`, `gimbal`, `orbit`, `camera-movement`
