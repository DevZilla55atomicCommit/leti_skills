---
name: davinci-object-masking-and-layering
description: DaVinci Resolve technique: Object Masking and Layering from Instagram Reel C5nEIc7PyWR
category: creative/davinci-resolve-techniques
tags: ["rotoscoping", "masking", "compositing", "depth", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "C5nEIc7PyWR"
collection: "Gimbal_Moves"
resolve_page: "Fusion"
node_graph: "layer_mixer"
difficulty: "intermediate"
created: 2026-07-30
---

# Object Masking and Layering

**Source:** Instagram Reel `C5nEIc7PyWR` (Gimbal_Moves)  
**Page:** Fusion | **Graph:** layer_mixer | **Difficulty:** intermediate

![Object Masking and Layering](C5nEIc7PyWR.gif)

## Node Graph Structure

- MediaIn1
- MediaIn2
- Merge
- Polygon

## Parameters

- **blend_mode**: Over
- **mask_channel**: Alpha Channel

## Steps to Reproduce in DaVinci Resolve

1. Import footage into Fusion page
2. Duplicate the MediaIn node to create two layers (background and foreground)
3. Add a Merge node to connect them
4. Add a Polygon node and connect it to the mask input of the top layer containing the tree
5. Use the Paint tool or Rotoscope to draw a mask around the tree leaves and branches
6. Refine the mask edges using Soft Edge or Feathering for a natural look
7. Adjust the layer order so the person appears behind the masked tree elements

## Tags
`rotoscoping`, `masking`, `compositing`, `depth`
