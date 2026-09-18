---
name: Fusion - bokeh
description: 3 related techniques for Fusion - bokeh
trigger: Need fusion technique for bokeh
category: Fusion
tags: bokeh, cinematic, depth of field, masking, selective focus, selective-focus
---

# bokeh (Fusion)

## Overview
Combined 3 techniques from Instagram Reels for fusion page.

## Resolve Page
Fusion

## Node Graph Type
serial

## Key Nodes
- Blur
- Color Correct
- ColorCorrect
- Gaussian Blur
- Mask
- MaskPaint
- MediaIn
- MediaOut
- Merge

## Parameters
- Blur Radius: High (50+)
- Softness: 0.5
- Mask Feathering: 2.0
- Mask Edge Softness: High
- Temperature: Warm (Yellow/Orange)
- Saturation: Increased Midtones
- Mask Softness: High
- Invert Mask: True (to isolate subject)

## Steps to Reproduce
1. Bring the clip into the Fusion page.
2. Add a Gaussian Blur node connected to the MediaIn node.
3. Increase the Blur Radius to significantly blur the background and foreground elements.
4. Create a Polygon Mask and draw it carefully around the flower and the specific rail section.
5. Invert the mask so the blur is applied everywhere except the flower and the rail.
6. Adjust the mask feathering to create a natural-looking transition between the sharp and blurred areas.
7. Add a Color Correct node to enhance the warm oranges and saturation of the flower.
8. Import clip into the Fusion page
9. Add a Gaussian Blur node and increase the radius to blur the background
10. Create an Ellipse Mask and draw it carefully around the flower
11. Invert the mask so the blur is applied everywhere except the flower
12. Adjust the mask feathering to create a natural transition between the sharp and blurred areas
13. Add a Color Correct node to enhance the warm oranges and saturation
14. Import clip into Fusion page
15. Add a Gaussian Blur node connected to the MediaIn

## Difficulty
intermediate

## Tags
bokeh, cinematic, depth of field, masking, selective focus, selective-focus
