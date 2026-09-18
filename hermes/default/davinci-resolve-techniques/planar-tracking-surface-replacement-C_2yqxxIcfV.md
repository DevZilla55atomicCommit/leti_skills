---
name: planar-tracking-surface-replacement-C_2yqxxIcfV
description: Planar Tracking Surface Replacement - DaVinci Resolve technique from
  Instagram Reel C_2yqxxIcfV
category: davinci-resolve
tags:
- tracking
- motion-graphics
- fusion
- vfx
resolve_page: Fusion
node_graph_type: serial
difficulty: intermediate
key_nodes:
- MediaIn
- Planar
- Merge
- MediaOut
parameters:
  Tracker Mode: Planar
  Operation: Surface
  Path Type: Best Fit Plan
steps_to_reproduce:
- Add the clip to the Fusion page
- Add a Planar Tracker node and connect the MediaIn
- Draw a mask around the surface to be tracked (e.g., the wall)
- Click Track Forward to analyze the motion
- Change Operation to Surface
- Create Text or Image nodes
- Connect the text/image to the Planar Tracker output via a Merge node
- Adjust transform to align the graphic with the tracked surface
source_reel_id: C_2yqxxIcfV
---
# Planar Tracking Surface Replacement

**Source Reel:** C_2yqxxIcfV
**Resolve Page:** Fusion
**Node Graph Type:** serial
**Difficulty:** intermediate

## Description
DaVinci Resolve technique extracted from Instagram Reel C_2yqxxIcfV.

## Key Nodes
- MediaIn
- Planar
- Merge
- MediaOut

## Parameters
Tracker Mode: Planar
Operation: Surface
Path Type: Best Fit Plan


## Steps to Reproduce
1. Add the clip to the Fusion page
2. Add a Planar Tracker node and connect the MediaIn
3. Draw a mask around the surface to be tracked (e.g., the wall)
4. Click Track Forward to analyze the motion
5. Change Operation to Surface
6. Create Text or Image nodes
7. Connect the text/image to the Planar Tracker output via a Merge node
8. Adjust transform to align the graphic with the tracked surface

## Tags
tracking, motion-graphics, fusion, vfx
