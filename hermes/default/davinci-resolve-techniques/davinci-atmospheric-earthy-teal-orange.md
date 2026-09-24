---
name: davinci-atmospheric-earthy-teal-orange
description: DaVinci Resolve technique: Atmospheric Earthy Teal & Orange from Instagram Reel C8D9keTSCWy
category: creative/davinci-resolve-techniques
tags: ["cinematic", "aerial", "teal-and-orange", "earth-tones", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "C8D9keTSCWy"
collection: "Ideas_for_Shooting_Videos"
resolve_page: "Color"
node_graph: "serial"
difficulty: "intermediate"
created: 2026-07-30
---

# Atmospheric Earthy Teal & Orange

**Source:** Instagram Reel `C8D9keTSCWy` (Ideas_for_Shooting_Videos)  
**Page:** Color | **Graph:** serial | **Difficulty:** intermediate

![Atmospheric Earthy Teal & Orange](C8D9keTSCWy.gif)

## Node Graph Structure

- Primary Correction
- Sky Balance
- Color Wheels
- Haze Overlay

## Parameters

- **lift**: Lifted slightly to create faded blacks
- **midtones**: Saturated with warm tones
- **highlights**: Cooled down towards cyan
- **saturation**: Reduced globally for a cinematic look

## Steps to Reproduce in DaVinci Resolve

1. Apply a slight lift to the shadows using the Color Wheels for a matte-black look.
2. Use a Qualifier to select the hillside area and push the midtones toward a warm orange/brown palette.
3. Use a Qualifier to select the background/sky and shift the highlights toward a muted teal/blue.
4. Add a Parametric curve to slightly reduce overall saturation while keeping specific colors vibrant.
5. Add a subtle Glow effect on a separate node with a high radius to simulate atmospheric diffusion.

## Tags
`cinematic`, `aerial`, `teal-and-orange`, `earth-tones`
