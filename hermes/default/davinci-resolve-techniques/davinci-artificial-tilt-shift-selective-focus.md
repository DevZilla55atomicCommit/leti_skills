---
name: davinci-artificial-tilt-shift-selective-focus
description: DaVinci Resolve technique: Artificial Tilt-Shift / Selective Focus from Instagram Reel C6gl25FRp7R
category: creative/davinci-resolve-techniques
tags: ["tilt-shift", "depth-of-field", "focus", "cinematic", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "C6gl25FRp7R"
collection: "Footage_Collection"
resolve_page: "Fusion"
node_graph: "serial"
difficulty: "beginner"
created: 2026-07-30
---

# Artificial Tilt-Shift / Selective Focus

**Source:** Instagram Reel `C6gl25FRp7R` (Footage_Collection)  
**Page:** Fusion | **Graph:** serial | **Difficulty:** beginner

![Artificial Tilt-Shift / Selective Focus](C6gl25FRp7R.gif)

## Node Graph Structure

- MediaIn
- Gaussian Blur
- MergeMask

## Parameters

- **blur_amount**: High
- **feathering**: Soft
- **mask_shape**: Ellipse/Linear Gradient

## Steps to Reproduce in DaVinci Resolve

1. Add the clip to the Fusion page
2. Add a Gaussian Blur node connected to the MediaIn
3. Add an Ellipse mask and connect it to the mask input of the Gaussian Blur
4. Adjust the Ellipse size and position to isolate only the subject (the flower)
5. Increase the feathering on the mask to create a smooth transition between sharp and blurred areas

## Tags
`tilt-shift`, `depth-of-field`, `focus`, `cinematic`
