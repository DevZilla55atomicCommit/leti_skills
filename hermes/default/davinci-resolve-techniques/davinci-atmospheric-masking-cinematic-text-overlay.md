---
name: davinci-atmospheric-masking-cinematic-text-overlay
description: DaVinci Resolve technique: Atmospheric Masking & Cinematic Text Overlay from Instagram Reel C9kvp9gvMHS
category: creative/davinci-resolve-techniques
tags: ["cinematic", "masking", "typography", "vfx", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "C9kvp9gvMHS"
collection: "Ideas_for_Shooting_Videos"
resolve_page: "Fusion"
node_graph: "serial"
difficulty: "intermediate"
created: 2026-07-30
---

# Atmospheric Masking & Cinematic Text Overlay

**Source:** Instagram Reel `C9kvp9gvMHS` (Ideas_for_Shooting_Videos)  
**Page:** Fusion | **Graph:** serial | **Difficulty:** intermediate

![Atmospheric Masking & Cinematic Text Overlay](C9kvp9gvMHS.gif)

## Node Graph Structure

- MediaIn
- Text+
- Gaussian Blur
- Merge

## Parameters

- **Opacity**: 0.8
- **Softness**: 25.0
- **Color**: Gold/Yellow

## Steps to Reproduce in DaVinci Resolve

1. Import the landscape clip into the Fusion page
2. Add a Text+ node for the word 'ALASKA' and rotate vertically
3. Use a Mask node (Polygon or Gradient) to isolate the mountain mist area
4. Apply a Gaussian Blur to the masked area to create the misty depth effect
5. Use a Merge node to layer the text over the masked/blurred background

## Tags
`cinematic`, `masking`, `typography`, `vfx`
