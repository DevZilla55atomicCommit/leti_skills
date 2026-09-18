---
name: horizontal-triple-split-screen-C6FCb-qJjrx
description: Horizontal Triple Split-Screen - DaVinci Resolve technique from Instagram
  Reel C6FCb-qJjrx
category: davinci-resolve
tags:
- split-screen
- layout
- composition
- video-editing
resolve_page: Fusion
node_graph_type: parallel
difficulty: beginner
key_nodes:
- MediaIn
- Crop
- Merge
- Text+
parameters:
  Crop_Top: 33%
  Crop_Bottom: 33%
  Center_Y: variable
steps_to_reproduce:
- Bring three instances of the same clip into the Fusion timeline.
- Add a Crop node after each MediaIn.
- Adjust the Crop parameters of the top clip to show only the upper 33%.
- Adjust the Crop parameters of the middle clip to show only the center 33%.
- Adjust the Crop parameters of the bottom clip to show only the lower 33%.
- Use two Merge nodes to stack the three clips vertically by adjusting their Y-Center
  position.
- Add a Text+ node over the middle layer.
source_reel_id: C6FCb-qJjrx
---
# Horizontal Triple Split-Screen

**Source Reel:** C6FCb-qJjrx
**Resolve Page:** Fusion
**Node Graph Type:** parallel
**Difficulty:** beginner

## Description
DaVinci Resolve technique extracted from Instagram Reel C6FCb-qJjrx.

## Key Nodes
- MediaIn
- Crop
- Merge
- Text+

## Parameters
Crop_Top: 33%
Crop_Bottom: 33%
Center_Y: variable


## Steps to Reproduce
1. Bring three instances of the same clip into the Fusion timeline.
2. Add a Crop node after each MediaIn.
3. Adjust the Crop parameters of the top clip to show only the upper 33%.
4. Adjust the Crop parameters of the middle clip to show only the center 33%.
5. Adjust the Crop parameters of the bottom clip to show only the lower 33%.
6. Use two Merge nodes to stack the three clips vertically by adjusting their Y-Center position.
7. Add a Text+ node over the middle layer.

## Tags
split-screen, layout, composition, video-editing
