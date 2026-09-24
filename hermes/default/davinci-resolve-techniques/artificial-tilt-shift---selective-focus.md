---
name: Artificial Tilt-Shift / Selective Focus
description: DaVinci Resolve technique from Instagram Reel C6gl25FRp7R
trigger: "artificial tilt-shift / selective focus"
page: Fusion
difficulty: beginner
tags: ['tilt-shift', 'depth-of-field', 'focus', 'cinematic']
video_id: C6gl25FRp7R
source: instagram-reel
updated: 2026-07-28T17:25:51.390965
---

# Artificial Tilt-Shift / Selective Focus

**Source:** Instagram Reel `C6gl25FRp7R`  
**Resolve Page:** Fusion  
**Difficulty:** beginner  
**Node Graph Type:** serial

## Key Nodes
- MediaIn
- Gaussian Blur
- MergeMask

## Parameters
- **blur_amount:** High
- **feathering:** Soft
- **mask_shape:** Ellipse/Linear Gradient

## Steps to Reproduce
1. Add the clip to the Fusion page
2. Add a Gaussian Blur node connected to the MediaIn
3. Add an Ellipse mask and connect it to the mask input of the Gaussian Blur
4. Adjust the Ellipse size and position to isolate only the subject (the flower)
5. Increase the feathering on the mask to create a smooth transition between sharp and blurred areas

## Tags
- #tilt-shift
- #depth-of-field
- #focus
- #cinematic
