---
name: davinci-urban-cinematic-high-contrast-with-warm-glow
description: DaVinci Resolve technique: Urban Cinematic High Contrast with Warm Glow from Instagram Reel C8XKNI2ub5o
category: creative/davinci-resolve-techniques
tags: ["cinematic", "night-time", "high-contrast", "urban", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "C8XKNI2ub5o"
collection: "Ideas_for_Shooting_Videos"
resolve_page: "Color"
node_graph: "serial"
difficulty: "intermediate"
created: 2026-07-30
---

# Urban Cinematic High Contrast with Warm Glow

**Source:** Instagram Reel `C8XKNI2ub5o` (Ideas_for_Shooting_Videos)  
**Page:** Color | **Graph:** serial | **Difficulty:** intermediate

![Urban Cinematic High Contrast with Warm Glow](C8XKNI2ub5o.gif)

## Node Graph Structure

- Primary Correction
- Color Wheels
- Glow Node
- Halation/Diffusion

## Parameters

- **contrast**: 1.2
- **saturation**: 1.4
- **midtone_tint**: Warm/Orange
- **glow_threshold**: 0.45
- **glow_spread**: 0.60

## Steps to Reproduce in DaVinci Resolve

1. Adjust Lift and Gain to create deep shadows and bright highlights
2. Apply a Power Window to the subject to desaturate the background slightly while keeping the reds in the jacket vibrant
3. Use the Color Wheels to push warmth into the highlights and cool tones into the shadows
4. Add a Glow node with a high threshold and low opacity to simulate the light streak/flare effect
5. Add a subtle Halation effect to soften the edges of the bright light sources

## Tags
`cinematic`, `night-time`, `high-contrast`, `urban`
