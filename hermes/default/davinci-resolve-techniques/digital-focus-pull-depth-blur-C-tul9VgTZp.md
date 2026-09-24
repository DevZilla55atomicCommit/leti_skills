---
name: digital-focus-pull-depth-blur-C-tul9VgTZp
description: Digital Focus Pull / Depth Blur - DaVinci Resolve technique from Instagram
  Reel C-tul9VgTZp
category: davinci-resolve
tags:
- focus-pull
- depth-of-field
- fusion
- cinematic
resolve_page: Fusion
node_graph_type: serial
difficulty: intermediate
key_nodes:
- MediaIn
- Gaussian Blur
- Merge
parameters:
  Blur Radius: Interpolated via keyframes
  Edge Range: All
  Softness: Keyframed adjusted
steps_to_reproduce:
- Import the clip into the Fusion page.
- Add a Gaussian Blur node after the MediaIn.
- Create a Mask (Polygon or Ellipse) to isolate the foreground object.
- Keyframe the Blur Radius to start at 0 when the object is in focus.
- Keyframe the Blur Radius to a high value when the focus shifts to the background
  subject.
- Adjust the mask feather to ensure a natural transition between planes.
source_reel_id: C-tul9VgTZp
---
# Digital Focus Pull / Depth Blur

**Source Reel:** C-tul9VgTZp
**Resolve Page:** Fusion
**Node Graph Type:** serial
**Difficulty:** intermediate

## Description
DaVinci Resolve technique extracted from Instagram Reel C-tul9VgTZp.

## Key Nodes
- MediaIn
- Gaussian Blur
- Merge

## Parameters
Blur Radius: Interpolated via keyframes
Edge Range: All
Softness: Keyframed adjusted


## Steps to Reproduce
1. Import the clip into the Fusion page.
2. Add a Gaussian Blur node after the MediaIn.
3. Create a Mask (Polygon or Ellipse) to isolate the foreground object.
4. Keyframe the Blur Radius to start at 0 when the object is in focus.
5. Keyframe the Blur Radius to a high value when the focus shifts to the background subject.
6. Adjust the mask feather to ensure a natural transition between planes.

## Tags
focus-pull, depth-of-field, fusion, cinematic
