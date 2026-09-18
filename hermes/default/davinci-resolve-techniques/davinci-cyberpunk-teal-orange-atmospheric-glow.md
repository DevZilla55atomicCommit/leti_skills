---
name: davinci-cyberpunk-teal-orange-atmospheric-glow
description: DaVinci Resolve technique: Cyberpunk Teal & Orange Atmospheric Glow from Instagram Reel C91i03uyUns
category: creative/davinci-resolve-techniques
tags: ["cityscape", "cyberpunk", "teal-and-orange", "cinematic", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "C91i03uyUns"
collection: "Ideas_for_Shooting_Videos"
resolve_page: "Color"
node_graph: "serial"
difficulty: "intermediate"
created: 2026-07-30
---

# Cyberpunk Teal & Orange Atmospheric Glow

**Source:** Instagram Reel `C91i03uyUns` (Ideas_for_Shooting_Videos)  
**Page:** Color | **Graph:** serial | **Difficulty:** intermediate

![Cyberpunk Teal & Orange Atmospheric Glow](C91i03uyUns.gif)

## Node Graph Structure

- Primary Balance
- Curves
- Color Wheels
- Glow
- Halation

## Parameters

- **lift_color**: Deep Blue
- **midtones_color**: Cyan/Teal
- **highlights_color**: Orange/Magenta
- **glow_threshold**: 0.05
- **glow_radius**: 50.0

## Steps to Reproduce in DaVinci Resolve

1. Apply a slight S-curve in Curves nodes to increase contrast.
2. Use Color Wheels to push shadows into a deep blue and highlights into a warm orange/magenta.
3. Use a Qualifier to isolate bright light sources and increase saturation specifically in pink/cyan tones.
4. Add a Glow node with a low threshold and large radius to simulate atmospheric bloom.
5. Add a Halation node to create a subtle red-fringe glow around the brightest light sources.
6. Increase Midtone detail in the midtones to make the city lights pop.

## Tags
`cityscape`, `cyberpunk`, `teal-and-orange`, `cinematic`
