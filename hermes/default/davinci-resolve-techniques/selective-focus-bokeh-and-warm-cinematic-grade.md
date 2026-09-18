---
name: Selective Focus Bokeh & Warm Cinematic Grade
description: DaVinci Resolve technique from Instagram Reel C69CkokPVBr
trigger: "selective focus bokeh & warm cinematic grade"
page: Fusion
difficulty: intermediate
tags: ['bokeh', 'depth of field', 'cinematic', 'selective-focus']
video_id: C69CkokPVBr
source: instagram-reel
updated: 2026-07-28T17:55:13.412606
---

# Selective Focus Bokeh & Warm Cinematic Grade

**Source:** Instagram Reel `C69CkokPVBr`  
**Resolve Page:** Fusion  
**Difficulty:** intermediate  
**Node Graph Type:** serial

## Key Nodes
- MediaIn
- Blur
- Mask
- ColorCorrect

## Parameters
- **Blur Radius:** High
- **Mask Edge Softness:** High
- **Temperature:** Warm (Yellow/Orange)
- **Saturation:** Increased Midtones

## Steps to Reproduce
1. Import clip into the Fusion page
2. Add a Gaussian Blur node and increase the radius to blur the background
3. Create an Ellipse Mask and draw it carefully around the flower
4. Invert the mask so the blur is applied everywhere except the flower
5. Adjust the mask feathering to create a natural transition between the sharp and blurred areas
6. Add a Color Correct node to enhance the warm oranges and saturation

## Tags
- #bokeh
- #depth of field
- #cinematic
- #selective-focus
