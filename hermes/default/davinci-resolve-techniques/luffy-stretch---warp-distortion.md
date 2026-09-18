---
name: Luffy Stretch / Warp Distortion
description: DaVinci Resolve technique from Instagram Reel C-nf4xytQUu
trigger: "luffy stretch / warp distortion"
page: Fusion
difficulty: intermediate
tags: ['fusion', 'warp', 'vfx', 'onepiece', 'specialeffects']
video_id: C-nf4xytQUu
source: instagram-reel
updated: 2026-07-28T11:18:02.164909
---

# Luffy Stretch / Warp Distortion

**Source:** Instagram Reel `C-nf4xytQUu`  
**Resolve Page:** Fusion  
**Difficulty:** intermediate  
**Node Graph Type:** serial

## Key Nodes
- MediaIn
- Grid Warp
- Transform
- MediaOut

## Parameters
- **gridWarp_type:** Bilinear
- **mesh_density:** High
- **smoothness:** Medium

## Steps to Reproduce
1. Add the clip to the Fusion page
2. Add a Grid Warp node after the MediaIn
3. Increase the mesh density to allow for finer control over the subject limbs
4. Keyframe the vertex points of the grid to stretch the arms or torso rubbery
5. Apply a Transform node to adjust the final framing after the distortion
6. Add a Blur node if necessary to soften the edges of the distortion

## Tags
- #fusion
- #warp
- #vfx
- #onepiece
- #specialeffects
