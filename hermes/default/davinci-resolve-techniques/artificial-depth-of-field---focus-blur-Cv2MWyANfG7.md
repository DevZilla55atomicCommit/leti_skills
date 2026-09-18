---
name: artificial-depth-of-field---focus-blur
description: 'DaVinci Resolve technique: Artificial Depth of Field / Focus Blur from
  Instagram Reel Cv2MWyANfG7'
category: davinci-resolve
tags:
- cinematic
- drone
- depth-of-field
- tutorial
- color
- intermediate
version: 1.0.0
source_reel_id: Cv2MWyANfG7
resolve_page: Color
node_graph_type: serial
key_nodes:
- Gaussian Blur
- Magic Mask
parameters:
  Blur Radius: '25.0'
  Strength: '1.0'
steps_to_reproduce:
- Import footage and go to the Color Page
- Use the Magic Mask to isolate the subject (the drone)
- Create a new node for the background
- Add a Gaussian Blur or Lens Blur effect to the background node
- Adjust the blur radius to create a cinematic shallow depth of field
difficulty: intermediate
---
# Artificial Depth of Field / Focus Blur

**Source Reel:** Cv2MWyANfG7
**Resolve Page:** Color
**Node Graph Type:** serial
**Difficulty:** intermediate

## Description
DaVinci Resolve technique extracted from Instagram Reel Cv2MWyANfG7.

## Key Nodes
- Gaussian Blur
- Magic Mask

## Parameters
Blur Radius: '25.0'
Strength: '1.0'


## Steps to Reproduce
1. Import footage and go to the Color Page
2. Use the Magic Mask to isolate the subject (the drone)
3. Create a new node for the background
4. Add a Gaussian Blur or Lens Blur effect to the background node
5. Adjust the blur radius to create a cinematic shallow depth of field

## Tags
cinematic, drone, depth-of-field, tutorial
