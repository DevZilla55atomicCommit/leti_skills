---
name: davinci-selective-color-masking-and-depth-isolation
description: DaVinci Resolve technique: Selective Color Masking and Depth Isolation from Instagram Reel C6tp62kRyUK
category: creative/davinci-resolve-techniques
tags: ["cinematic", "selective-color", "masking", "depth-of-field", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "C6tp62kRyUK"
collection: "Footage_Collection"
resolve_page: "Color"
node_graph: "serial"
difficulty: "intermediate"
created: 2026-07-30
---

# Selective Color Masking and Depth Isolation

**Source:** Instagram Reel `C6tp62kRyUK` (Footage_Collection)  
**Page:** Color | **Graph:** serial | **Difficulty:** intermediate

![Selective Color Masking and Depth Isolation](C6tp62kRyUK.gif)

## Node Graph Structure

- Primary Grade Node
- Qualifier/Mask Node
- Power Window Node
- Blur Node

## Parameters

- **Saturation**: +45.0
- **Hue vs Softness**: 50.0
- **Radius**: 50.0
- **Contrast**: 1.2

## Steps to Reproduce in DaVinci Resolve

1. Import the clip and perform a primary color grade to establish the desaturated, moody environment.
2. Use the Qualifier tool or Power Window to select only the red poppy flower.
3. Increase the saturation and luminance specifically on the selection to make the flower stand out.
4. Create a separate node for the background and apply a Gaussian Blur or Lens Blur to simulate a shallow depth of field.
5. Add a Glow effect to the highlights of the flower edges to simulate the golden-hour rim-lighting.

## Tags
`cinematic`, `selective-color`, `masking`, `depth-of-field`
