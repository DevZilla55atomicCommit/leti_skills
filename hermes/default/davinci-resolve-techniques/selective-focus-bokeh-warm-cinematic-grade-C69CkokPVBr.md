---
name: selective-focus-bokeh-warm-cinematic-grade-C69CkokPVBr
description: Selective Focus Bokeh & Warm Cinematic Grade - DaVinci Resolve technique
  from Instagram Reel C69CkokPVBr
category: davinci-resolve
tags:
- bokeh
- depth of field
- cinematic
- selective-focus
resolve_page: Fusion
node_graph_type: serial
difficulty: intermediate
key_nodes:
- MediaIn
- Blur
- Mask
- ColorCorrect
parameters:
  Blur Radius: High
  Mask Edge Softness: High
  Temperature: Warm (Yellow/Orange)
  Saturation: Increased Midtones
steps_to_reproduce:
- Import clip into the Fusion page
- Add a Gaussian Blur node and increase the radius to blur the background
- Create an Ellipse Mask and draw it carefully around the flower
- Invert the mask so the blur is applied everywhere except the flower
- Adjust the mask feathering to create a natural transition between the sharp and
  blurred areas
- Add a Color Correct node to enhance the warm oranges and saturation
source_reel_id: C69CkokPVBr
---
# Selective Focus Bokeh & Warm Cinematic Grade

**Source Reel:** C69CkokPVBr
**Resolve Page:** Fusion
**Node Graph Type:** serial
**Difficulty:** intermediate

## Description
DaVinci Resolve technique extracted from Instagram Reel C69CkokPVBr.

## Key Nodes
- MediaIn
- Blur
- Mask
- ColorCorrect

## Parameters
Blur Radius: High
Mask Edge Softness: High
Temperature: Warm (Yellow/Orange)
Saturation: Increased Midtones


## Steps to Reproduce
1. Import clip into the Fusion page
2. Add a Gaussian Blur node and increase the radius to blur the background
3. Create an Ellipse Mask and draw it carefully around the flower
4. Invert the mask so the blur is applied everywhere except the flower
5. Adjust the mask feathering to create a natural transition between the sharp and blurred areas
6. Add a Color Correct node to enhance the warm oranges and saturation

## Tags
bokeh, depth of field, cinematic, selective-focus
