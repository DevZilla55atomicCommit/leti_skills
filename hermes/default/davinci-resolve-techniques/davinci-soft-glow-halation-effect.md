---
name: davinci-soft-glow-halation-effect
description: DaVinci Resolve technique: Soft Glow / Halation Effect from Instagram Reel DLihs8SOlbN
category: creative/davinci-resolve-techniques
tags: ["cinematic", "glow", "night-photography", "atmosphere", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "DLihs8SOlbN"
collection: "Ideas_for_Shooting_Videos"
resolve_page: "Color"
node_graph: "serial"
difficulty: "beginner"
created: 2026-07-30
---

# Soft Glow / Halation Effect

**Source:** Instagram Reel `DLihs8SOlbN` (Ideas_for_Shooting_Videos)  
**Page:** Color | **Graph:** serial | **Difficulty:** beginner

![Soft Glow / Halation Effect](DLihs8SOlbN.gif)

## Node Graph Structure

- Primary Grade
- Glow Node
- Soft Light Node

## Parameters

- **Glow Threshold**: 0.5
- **Glow Tone**: 0.7
- **Glow Spread**: 0.50
- **Blur Radius**: 15.0

## Steps to Reproduce in DaVinci Resolve

1. Create a primary node for basic color grading to increase contrast and warmth.
2. Create a new serial node and apply the Glow effect.
3. Use a Qualifier or High-Key mask to isolate only the highlights (the lanterns).
4. Adjust the Threshold and Spread to create a soft light bleed.
5. Add a final node with a slight Gaussian Blur and Soft Light blend mode to simulate lens diffusion/halation.

## Tags
`cinematic`, `glow`, `night-photography`, `atmosphere`
