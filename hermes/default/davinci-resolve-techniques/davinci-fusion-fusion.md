---
name: Fusion - fusion
description: 2 related techniques for Fusion - fusion
trigger: Need fusion technique for fusion
category: Fusion
tags: 3d-depth, fusion, masking, onepiece, specialeffects, text-effect, vfx, warp
---

# fusion (Fusion)

## Overview
Combined 2 techniques from Instagram Reels for fusion page.

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
11. Connect the Polygon mask to the mask input of the TextPlus node
12. Draw the mask around the parts of the cliff that should be in front of the text
13. Adjust the mask boundaries to ensure the text appears behind the cliff edge

## Difficulty
intermediate

## Tags
3d-depth, fusion, masking, onepiece, specialeffects, text-effect, vfx, warp
