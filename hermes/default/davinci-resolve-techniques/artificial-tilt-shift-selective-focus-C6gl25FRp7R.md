---
name: artificial-tilt-shift-selective-focus-C6gl25FRp7R
description: Artificial Tilt-Shift / Selective Focus - DaVinci Resolve technique from
  Instagram Reel C6gl25FRp7R
category: davinci-resolve
tags:
- tilt-shift
- depth-of-field
- focus
- cinematic
resolve_page: Fusion
node_graph_type: serial
difficulty: beginner
key_nodes:
- MediaIn
- Gaussian Blur
- MergeMask
parameters:
  blur_amount: High
  feathering: Soft
  mask_shape: Ellipse/Linear Gradient
steps_to_reproduce:
- Add the clip to the Fusion page
- Add a Gaussian Blur node connected to the MediaIn
- Add an Ellipse mask and connect it to the mask input of the Gaussian Blur
- Adjust the Ellipse size and position to isolate only the subject (the flower)
- Increase the feathering on the mask to create a smooth transition between sharp
  and blurred areas
source_reel_id: C6gl25FRp7R
---
# Artificial Tilt-Shift / Selective Focus

**Source Reel:** C6gl25FRp7R
**Resolve Page:** Fusion
**Node Graph Type:** serial
**Difficulty:** beginner

## Description
DaVinci Resolve technique extracted from Instagram Reel C6gl25FRp7R.

## Key Nodes
- MediaIn
- Gaussian Blur
- MergeMask

## Parameters
blur_amount: High
feathering: Soft
mask_shape: Ellipse/Linear Gradient


## Steps to Reproduce
1. Add the clip to the Fusion page
2. Add a Gaussian Blur node connected to the MediaIn
3. Add an Ellipse mask and connect it to the mask input of the Gaussian Blur
4. Adjust the Ellipse size and position to isolate only the subject (the flower)
5. Increase the feathering on the mask to create a smooth transition between sharp and blurred areas

## Tags
tilt-shift, depth-of-field, focus, cinematic
