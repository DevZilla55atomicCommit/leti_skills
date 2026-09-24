---
name: luffy-stretch---warp-distortion
description: 'DaVinci Resolve technique: Luffy Stretch / Warp Distortion from Instagram
  Reel C-nf4xytQUu'
category: davinci-resolve
tags:
- fusion
- warp
- vfx
- onepiece
- specialeffects
- fusion
- intermediate
version: 1.0.0
source_reel_id: C-nf4xytQUu
resolve_page: Fusion
node_graph_type: serial
key_nodes:
- MediaIn
- Grid Warp
- Transform
- MediaOut
parameters:
  gridWarp_type: Bilinear
  mesh_density: High
  smoothness: Medium
steps_to_reproduce:
- Add the clip to the Fusion page
- Add a Grid Warp node after the MediaIn
- Increase the mesh density to allow for finer control over the subject limbs
- Keyframe the vertex points of the grid to stretch the arms or torso rubbery
- Apply a Transform node to adjust the final framing after the distortion
- Add a Blur node if necessary to soften the edges of the distortion
difficulty: intermediate
---
# Luffy Stretch / Warp Distortion

**Source Reel:** C-nf4xytQUu
**Resolve Page:** Fusion
**Node Graph Type:** serial
**Difficulty:** intermediate

## Description
DaVinci Resolve technique extracted from Instagram Reel C-nf4xytQUu.

## Key Nodes
- MediaIn
- Grid Warp
- Transform
- MediaOut

## Parameters
gridWarp_type: Bilinear
mesh_density: High
smoothness: Medium


## Steps to Reproduce
1. Add the clip to the Fusion page
2. Add a Grid Warp node after the MediaIn
3. Increase the mesh density to allow for finer control over the subject limbs
4. Keyframe the vertex points of the grid to stretch the arms or torso rubbery
5. Apply a Transform node to adjust the final framing after the distortion
6. Add a Blur node if necessary to soften the edges of the distortion

## Tags
fusion, warp, vfx, onepiece, specialeffects
