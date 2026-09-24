---
name: selective-depth-of-field-artificial-bokeh-blur-C66ZyoIRq-8
description: Selective Depth of Field / Artificial Bokeh Blur - DaVinci Resolve technique
  from Instagram Reel C66ZyoIRq-8
category: davinci-resolve
tags:
- depth of field
- selective-focus
- tilt-shift
- cinematic
resolve_page: Fusion
node_graph_type: serial
difficulty: intermediate
key_nodes:
- MediaIn
- Blur
- MaskMask
- MediaOut
parameters:
  Blur_Radius: High
  Mask_Softness: '0.5'
  Mask_Shape: Ellipse/Gradient
steps_to_reproduce:
- Bring the clip into the Fusion page
- Add a Gaussian Blur node and connect it to MediaIn
- Add an Ellipse Mask node and connect it to the blue input of the Blur node
- Adjust the mask over the flower to keep it sharp
- Adjust the Blur radius to soften the background and foreground elements
- Increase the Softness of the mask to create a realistic transition
source_reel_id: C66ZyoIRq-8
---
# Selective Depth of Field / Artificial Bokeh Blur

**Source Reel:** C66ZyoIRq-8
**Resolve Page:** Fusion
**Node Graph Type:** serial
**Difficulty:** intermediate

## Description
DaVinci Resolve technique extracted from Instagram Reel C66ZyoIRq-8.

## Key Nodes
- MediaIn
- Blur
- MaskMask
- MediaOut

## Parameters
Blur_Radius: High
Mask_Softness: '0.5'
Mask_Shape: Ellipse/Gradient


## Steps to Reproduce
1. Bring the clip into the Fusion page
2. Add a Gaussian Blur node and connect it to MediaIn
3. Add an Ellipse Mask node and connect it to the blue input of the Blur node
4. Adjust the mask over the flower to keep it sharp
5. Adjust the Blur radius to soften the background and foreground elements
6. Increase the Softness of the mask to create a realistic transition

## Tags
depth of field, selective-focus, tilt-shift, cinematic
