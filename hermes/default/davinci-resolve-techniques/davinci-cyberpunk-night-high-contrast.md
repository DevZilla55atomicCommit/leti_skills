---
name: davinci-cyberpunk-night-high-contrast
description: DaVinci Resolve technique: Cyberpunk Night High Contrast from Instagram Reel C81h3wkvXTH
category: creative/davinci-resolve-techniques
tags: ["night-city", "neon", "cyberpunk", "high-contrast", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "C81h3wkvXTH"
collection: "Ideas_for_Shooting_Videos"
resolve_page: "Color"
node_graph: "serial"
difficulty: "intermediate"
created: 2026-07-30
---

# Cyberpunk Night High Contrast

**Source:** Instagram Reel `C81h3wkvXTH` (Ideas_for_Shooting_Videos)  
**Page:** Color | **Graph:** serial | **Difficulty:** intermediate

![Cyberpunk Night High Contrast](C81h3wkvXTH.gif)

## Node Graph Structure

- Primary Correction
- Color Balance
- Color Wheels
- Soft Glow
- Halation

## Parameters

- **contrast**: 1.4
- **saturation**: 1.5
- **pivot**: 0.55
- **glow_threshold**: 0.45
- **glow_size**: 0.60

## Steps to Reproduce in DaVinci Resolve

1. Use the Lift/Gamma to crush the blacks and ensure the foreground remains dark.
2. Increase contrast and saturation to make the neon signs pop.
3. Apply a cold blue/teal tint to the Shadows and a warm orange/red tint to the Highlights using Color Wheels.
4. Add a Glow node with a high threshold and soft light size to create the atmospheric bloom around the signs.
5. Use the Halation node to simulate light bleed on the brightest edges of high-contrast areas.

## Tags
`night-city`, `neon`, `cyberpunk`, `high-contrast`
