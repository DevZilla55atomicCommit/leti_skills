---
name: davinci-spiral-orbit-camera-movement
description: DaVinci Resolve technique: Spiral Orbit Camera Movement from Instagram Reel DK17L3OTVrD
category: creative/davinci-resolve-techniques
tags: ["cinematography", "camera-movement", "fusion", "orbit-shot", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "DK17L3OTVrD"
collection: "Ideas_for_Shooting_Videos"
resolve_page: "Fusion"
node_graph: "serial"
difficulty: "intermediate"
created: 2026-07-30
---

# Spiral Orbit Camera Movement

**Source:** Instagram Reel `DK17L3OTVrD` (Ideas_for_Shooting_Videos)  
**Page:** Fusion | **Graph:** serial | **Difficulty:** intermediate

![Spiral Orbit Camera Movement](DK17L3OTVrD.gif)

## Node Graph Structure

- MediaIn
- Transform
- Camera3D
- Merge3D
- Render3

## Parameters

- **path_type**: Spiral
- **rotation**: Dynamic
- **focus**: Locked on Subject

## Steps to Reproduce in DaVinci Resolve

1. Bring the clip into the Fusion page
2. Add a Camera3D node and a Merge3D node
3. Create a Background or use a mask to define the spiral path
4. Link the Camera3D position path to the spiral shape
5. Animate the Camera's rotation to keep the subject centered while moving
6. Add a Render3 node to output back to the 2D timeline

## Tags
`cinematography`, `camera-movement`, `fusion`, `orbit-shot`
