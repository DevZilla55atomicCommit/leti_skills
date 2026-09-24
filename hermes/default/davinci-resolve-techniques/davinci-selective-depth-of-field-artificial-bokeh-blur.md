---
name: davinci-selective-depth-of-field-artificial-bokeh-blur
description: DaVinci Resolve technique: Selective Depth of Field / Artificial Bokeh Blur from Instagram Reel C66ZyoIRq-8
category: creative/davinci-resolve-techniques
tags: ["depth of field", "selective-focus", "tilt-shift", "cinematic", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "C66ZyoIRq-8"
collection: "Footage_Collection"
resolve_page: "Fusion"
node_graph: "serial"
difficulty: "intermediate"
created: 2026-07-30
---

# Selective Depth of Field / Artificial Bokeh Blur

**Source:** Instagram Reel `C66ZyoIRq-8` (Footage_Collection)  
**Page:** Fusion | **Graph:** serial | **Difficulty:** intermediate

![Selective Depth of Field / Artificial Bokeh Blur](C66ZyoIRq-8.gif)

## Node Graph Structure

- MediaIn
- Blur
- MaskMask
- MediaOut

## Parameters

- **Blur_Radius**: High
- **Mask_Softness**: 0.5
- **Mask_Shape**: Ellipse/Gradient

## Steps to Reproduce in DaVinci Resolve

1. Bring the clip into the Fusion page
2. Add a Gaussian Blur node and connect it to MediaIn
3. Add an Ellipse Mask node and connect it to the blue input of the Blur node
4. Adjust the mask over the flower to keep it sharp
5. Adjust the Blur radius to soften the background and foreground elements
6. Increase the Softness of the mask to create a realistic transition

## Tags
`depth of field`, `selective-focus`, `tilt-shift`, `cinematic`
