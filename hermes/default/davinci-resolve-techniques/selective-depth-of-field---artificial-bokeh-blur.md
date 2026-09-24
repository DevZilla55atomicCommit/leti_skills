---
name: Selective Depth of Field / Artificial Bokeh Blur
description: DaVinci Resolve technique from Instagram Reel C66ZyoIRq-8
trigger: "selective depth of field / artificial bokeh blur"
page: Fusion
difficulty: intermediate
tags: ['depth of field', 'selective-focus', 'tilt-shift', 'cinematic']
video_id: C66ZyoIRq-8
source: instagram-reel
updated: 2026-07-28T19:26:57.220997
---

# Selective Depth of Field / Artificial Bokeh Blur

**Source:** Instagram Reel `C66ZyoIRq-8`  
**Resolve Page:** Fusion  
**Difficulty:** intermediate  
**Node Graph Type:** serial

## Key Nodes
- MediaIn
- Blur
- MaskMask
- MediaOut

## Parameters
- **Blur_Radius:** High
- **Mask_Softness:** 0.5
- **Mask_Shape:** Ellipse/Gradient

## Steps to Reproduce
1. Bring the clip into the Fusion page
2. Add a Gaussian Blur node and connect it to MediaIn
3. Add an Ellipse Mask node and connect it to the blue input of the Blur node
4. Adjust the mask over the flower to keep it sharp
5. Adjust the Blur radius to soften the background and foreground elements
6. Increase the Softness of the mask to create a realistic transition

## Tags
- #depth of field
- #selective-focus
- #tilt-shift
- #cinematic
