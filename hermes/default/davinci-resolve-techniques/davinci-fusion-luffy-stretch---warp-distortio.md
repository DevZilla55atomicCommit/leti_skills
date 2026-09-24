---
name: davinci-fusion-luffy-stretch---warp-distortio
description: 2 techniques for Fusion - Luffy Stretch / Warp Distortion
trigger: Need Fusion technique for Luffy Stretch / Warp Distortion
category: Fusion
tags: 3d-depth, fusion, masking, onepiece, specialeffects, text-effect, vfx, warp
---

# Luffy Stretch / Warp Distortion

## Overview
Combined 2 related techniques from Instagram Reels.

## Resolve Page
Fusion

## Node Graph Type
serial

## Key Nodes
- Background
- Grid Warp
- Mask
- MediaIn
- MediaOut
- Merge
- TextPlus
- Transform

## Parameters
- gridWarp_type: Bilinear
- mesh_density: High
- smoothness: Medium
- TextColor: White
- FontWeight: Bold
- MergeMode: Alpha

## Steps to Reproduce
1. Add the clip to the Fusion page
2. Add a Grid Warp node after the MediaIn
3. Increase the mesh density to allow for finer control over the subject limbs
4. Keyframe the vertex points of the grid to stretch the arms or torso rubbery
5. Apply a Transform node to adjust the final framing after the distortion
6. Add a Blur node if necessary to soften the edges of the distortion
7. Import footage into the Fusion page
8. Add a TextPlus node and type the desired text
9. Connect TextPlus to the foreground input of a Merge node
10. Add a Polygon mask to the Fusion node

## Difficulty
intermediate

## Tags
3d-depth, fusion, masking, onepiece, specialeffects, text-effect, vfx, warp
