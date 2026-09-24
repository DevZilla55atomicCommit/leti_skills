---
name: artificial-depth-of-field-selective-focus-bokeh-C6wN1b7x-en
description: Artificial Depth of Field / Selective Focus Bokeh - DaVinci Resolve technique
  from Instagram Reel C6wN1b7x-en
category: davinci-resolve
tags:
- bokeh
- selective focus
- depth of field
- masking
resolve_page: Fusion
node_graph_type: serial
difficulty: intermediate
key_nodes:
- MediaIn
- Gaussian Blur
- Color Correct
- MediaOut
parameters:
  Blur Radius: '50.0'
  Softness: '0.5'
  Mask Feathering: '2.0'
steps_to_reproduce:
- Bring the clip into the Fusion page.
- Add a Gaussian Blur node connected to the MediaIn node.
- Increase the Blur Radius to significantly blur the background and foreground elements.
- Create a Polygon Mask and draw it carefully around the flower and the specific rail
  section.
- Invert the mask so the blur is applied everywhere except the flower and the rail.
- Adjust the mask feathering to create a natural-looking transition between the sharp
  and blurred areas.
- Add a Color Correct node to enhance the warm oranges and saturation of the flower.
source_reel_id: C6wN1b7x-en
---
# Artificial Depth of Field / Selective Focus Bokeh

**Source Reel:** C6wN1b7x-en
**Resolve Page:** Fusion
**Node Graph Type:** serial
**Difficulty:** intermediate

## Description
DaVinci Resolve technique extracted from Instagram Reel C6wN1b7x-en.

## Key Nodes
- MediaIn
- Gaussian Blur
- Color Correct
- MediaOut

## Parameters
Blur Radius: '50.0'
Softness: '0.5'
Mask Feathering: '2.0'


## Steps to Reproduce
1. Bring the clip into the Fusion page.
2. Add a Gaussian Blur node connected to the MediaIn node.
3. Increase the Blur Radius to significantly blur the background and foreground elements.
4. Create a Polygon Mask and draw it carefully around the flower and the specific rail section.
5. Invert the mask so the blur is applied everywhere except the flower and the rail.
6. Adjust the mask feathering to create a natural-looking transition between the sharp and blurred areas.
7. Add a Color Correct node to enhance the warm oranges and saturation of the flower.

## Tags
bokeh, selective focus, depth of field, masking
