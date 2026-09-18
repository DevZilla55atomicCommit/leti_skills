---
name: selective-focus-golden-hour-color-grade-C7EvL5ZvHoH
description: Selective Focus & Golden Hour Color Grade - DaVinci Resolve technique
  from Instagram Reel C7EvL5ZvHoH
category: davinci-resolve
tags:
- cinematic
- color-grading
- bokeh
- golden-hour
resolve_page: Color
node_graph_type: serial
difficulty: intermediate
key_nodes:
- Primary Correction
- Qualifier Mask
- Power Window
- Glow Node
parameters:
  Contrast: '1.20'
  Saturation: '1.1'
  Glow Spread: '0.500'
  Midtone Tint: Warm (Orange/Gold)
steps_to_reproduce:
- Import clip and perform primary exposure balancing to preserve the sunset highlights.
- Use a Power Window (circular) to isolate the daffodil and increase its sharpness/exposure.
- Apply a Gaussian Blur to a duplicate node or the background to simulate a shallow
  depth-of-field lens.
- Add a Glow node to the sun area to create a soft bloom/starburst effect.
- Use Color Wheels to push warm oranges into the highlights and teals/blues into the
  shadows for cinematic contrast.
source_reel_id: C7EvL5ZvHoH
---
# Selective Focus & Golden Hour Color Grade

**Source Reel:** C7EvL5ZvHoH
**Resolve Page:** Color
**Node Graph Type:** serial
**Difficulty:** intermediate

## Description
DaVinci Resolve technique extracted from Instagram Reel C7EvL5ZvHoH.

## Key Nodes
- Primary Correction
- Qualifier Mask
- Power Window
- Glow Node

## Parameters
Contrast: '1.20'
Saturation: '1.1'
Glow Spread: '0.500'
Midtone Tint: Warm (Orange/Gold)


## Steps to Reproduce
1. Import clip and perform primary exposure balancing to preserve the sunset highlights.
2. Use a Power Window (circular) to isolate the daffodil and increase its sharpness/exposure.
3. Apply a Gaussian Blur to a duplicate node or the background to simulate a shallow depth-of-field lens.
4. Add a Glow node to the sun area to create a soft bloom/starburst effect.
5. Use Color Wheels to push warm oranges into the highlights and teals/blues into the shadows for cinematic contrast.

## Tags
cinematic, color-grading, bokeh, golden-hour
