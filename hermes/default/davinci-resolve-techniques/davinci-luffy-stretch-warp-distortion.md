---
name: davinci-luffy-stretch-warp-distortion
description: DaVinci Resolve technique: Luffy Stretch / Warp Distortion from Instagram Reel C-nf4xytQUu
category: creative/davinci-resolve-techniques
tags: ["fusion", "warp", "vfx", "onepiece", "specialeffects", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "C-nf4xytQUu"
collection: "DaVinci_Tricks"
resolve_page: "Fusion"
node_graph: "serial"
difficulty: "intermediate"
created: 2026-07-30
---

# Luffy Stretch / Warp Distortion

**Source:** Instagram Reel `C-nf4xytQUu` (DaVinci_Tricks)  
**Page:** Fusion | **Graph:** serial | **Difficulty:** intermediate

![Luffy Stretch / Warp Distortion](C-nf4xytQUu.gif)

## Node Graph Structure

- MediaIn
- Grid Warp
- Transform
- MediaOut

## Parameters

- **gridWarp_type**: Bilinear
- **mesh_density**: High
- **smoothness**: Medium

## Steps to Reproduce in DaVinci Resolve

1. Add the clip to the Fusion page
2. Add a Grid Warp node after the MediaIn
3. Increase the mesh density to allow for finer control over the subject limbs
4. Keyframe the vertex points of the grid to stretch the arms or torso rubbery
5. Apply a Transform node to adjust the final framing after the distortion
6. Add a Blur node if necessary to soften the edges of the distortion

## Tags
`fusion`, `warp`, `vfx`, `onepiece`, `specialeffects`
