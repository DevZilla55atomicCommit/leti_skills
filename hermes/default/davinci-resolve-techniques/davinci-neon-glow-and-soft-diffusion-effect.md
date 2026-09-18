---
name: davinci-neon-glow-and-soft-diffusion-effect
description: DaVinci Resolve technique: Neon Glow and Soft Diffusion Effect from Instagram Reel C1cAX_4yJKN
category: creative/davinci-resolve-techniques
tags: ["glow", "diffusion", "social-media", "neon", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "C1cAX_4yJKN"
collection: "Color_grading"
resolve_page: "Fusion"
node_graph: "serial"
difficulty: "intermediate"
created: 2026-07-30
---

# Neon Glow and Soft Diffusion Effect

**Source:** Instagram Reel `C1cAX_4yJKN` (Color_grading)  
**Page:** Fusion | **Graph:** serial | **Difficulty:** intermediate

![Neon Glow and Soft Diffusion Effect](C1cAX_4yJKN.gif)

## Node Graph Structure

- MediaIn
- SoftBlur
- Glow
- Merge

## Parameters

- **Blur Radius**: 15.0
- **Glow Gain**: 1.5
- **Glow Threshold**: 0.5

## Steps to Reproduce in DaVinci Resolve

1. Import clip into the Fusion page
2. Add a SoftBlur node to the MediaIn to create a dreamy atmosphere
3. Add a Glow node to enhance the luminance of highlights like the neon sign
4. Adjust the Glow Threshold to ensure only the brightest areas bloom
5. Merge the processed layer back with the original or use a mask to isolate the effect

## Tags
`glow`, `diffusion`, `social-media`, `neon`
