---
name: davinci-selective-glow-masking-and-atmospheric-grading
description: DaVinci Resolve technique: Selective Glow Masking and Atmospheric Grading from Instagram Reel CzyqAq7Rhap
category: creative/davinci-resolve-techniques
tags: ["color grading", "masking", "glow", "cinematic", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "CzyqAq7Rhap"
collection: "Footage_Collection"
resolve_page: "Color"
node_graph: "serial"
difficulty: "intermediate"
created: 2026-07-30
---

# Selective Glow Masking and Atmospheric Grading

**Source:** Instagram Reel `CzyqAq7Rhap` (Footage_Collection)  
**Page:** Color | **Graph:** serial | **Difficulty:** intermediate

![Selective Glow Masking and Atmospheric Grading](CzyqAq7Rhap.gif)

## Node Graph Structure

- Primary Correction
- Qualifier Mask
- Glow Node
- Power Window

## Parameters

- **Softness**: 0.50
- **Gain**: 0.15
- **Threshold**: 0.40
- **Contrast**: 1.2

## Steps to Reproduce in DaVinci Resolve

1. Import clip and perform basic exposure/white balance on the Primary node
2. Use a Qualifier (HSL) to select only the purple flower and the sunlit edges
3. Create a Power Window around the flower with high feathering to isolate the subject
4. Add a Glow effect with a high threshold to create the ethereal light bleed around petals
5. Add a final serial node to deepen shadows and increase contrast using the Curves tool

## Tags
`color grading`, `masking`, `glow`, `cinematic`
