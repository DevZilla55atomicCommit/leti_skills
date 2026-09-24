---
name: Selective Color Masking and Depth Isolation
description: DaVinci Resolve technique from Instagram Reel C6tp62kRyUK
trigger: "selective color masking and depth isolation"
page: Color
difficulty: intermediate
tags: ['cinematic', 'selective-color', 'masking', 'depth-of-field']
video_id: C6tp62kRyUK
source: instagram-reel
updated: 2026-07-28T18:03:27.966192
---

# Selective Color Masking and Depth Isolation

**Source:** Instagram Reel `C6tp62kRyUK`  
**Resolve Page:** Color  
**Difficulty:** intermediate  
**Node Graph Type:** serial

## Key Nodes
- Primary Grade Node
- Qualifier/Mask Node
- Power Window Node
- Blur Node

## Parameters
- **Saturation:** +45.0
- **Hue vs Softness:** 50.0
- **Radius:** 50.0
- **Contrast:** 1.2

## Steps to Reproduce
1. Import the clip and perform a primary color grade to establish the desaturated, moody environment.
2. Use the Qualifier tool or Power Window to select only the red poppy flower.
3. Increase the saturation and luminance specifically on the selection to make the flower stand out.
4. Create a separate node for the background and apply a Gaussian Blur or Lens Blur to simulate a shallow depth of field.
5. Add a Glow effect to the highlights of the flower edges to simulate the golden-hour rim-lighting.

## Tags
- #cinematic
- #selective-color
- #masking
- #depth-of-field
