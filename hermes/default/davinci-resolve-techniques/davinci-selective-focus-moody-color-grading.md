---
name: davinci-selective-focus-moody-color-grading
description: DaVinci Resolve technique: Selective Focus & Moody Color Grading from Instagram Reel DBRNJD5MoG5
category: creative/davinci-resolve-techniques
tags: ["cinematic", "masking", "color-grading", "nature", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "DBRNJD5MoG5"
collection: "Ideas_for_Shooting_Videos"
resolve_page: "Color"
node_graph: "serial"
difficulty: "intermediate"
created: 2026-07-30
---

# Selective Focus & Moody Color Grading

**Source:** Instagram Reel `DBRNJD5MoG5` (Ideas_for_Shooting_Videos)  
**Page:** Color | **Graph:** serial | **Difficulty:** intermediate

![Selective Focus & Moody Color Grading](DBRNJD5MoG5.gif)

## Node Graph Structure

- Primary Grade Node
- Window Node
- Track Node

## Parameters

- **Window Type**: Circle/Ellipse
- **Softness**: High
- **Saturation**: Increased on subject
- **Contrast**: Increased
- **Lift**: Blue/Teal tint

## Steps to Reproduce in DaVinci Resolve

1. Import clip and go to the Color page
2. Create a new node and apply a circular window (mask) around the leaf
3. Increase the softness/feathering of the window edges to create a seamless transition
4. Use the Tracker to ensure the mask follows the leaf if the camera or subject moves
5. Create a second node for global grading: lower exposure, increase contrast, and add a cool tint to the shadows
6. In a third node, increase saturation specifically for the greens to make the leaf pop

## Tags
`cinematic`, `masking`, `color-grading`, `nature`
