---
name: davinci-golden-hour-teal-orange-glow
description: DaVinci Resolve technique: Golden Hour Teal & Orange Glow from Instagram Reel C9ogl36II1L
category: creative/davinci-resolve-techniques
tags: ["cinematic", "teal-and-orange", "golden-hour", "bokeh", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "C9ogl36II1L"
collection: "Ideas_for_Shooting_Videos"
resolve_page: "Color"
node_graph: "serial"
difficulty: "intermediate"
created: 2026-07-30
---

# Golden Hour Teal & Orange Glow

**Source:** Instagram Reel `C9ogl36II1L` (Ideas_for_Shooting_Videos)  
**Page:** Color | **Graph:** serial | **Difficulty:** intermediate

![Golden Hour Teal & Orange Glow](C9ogl36II1L.gif)

## Node Graph Structure

- Primary Balance
- Color Wheels
- Qualifiers
- Soft Glow

## Parameters

- **temperature**: +1500
- **shadow_tint**: Teal
- **highlight_tint**: Orange
- **glow_radius**: 60
- **spread**: 0.5

## Steps to Reproduce in DaVinci Resolve

1. Use Lift/Gamma/Gain to push shadows into teals and highlights into warm oranges.
2. Apply a Qualifier to select only the sunflowers and increase saturation and luminance.
3. Add a Glow node set with a high threshold and low opacity to create the ethereal light bleed around the petals.
4. Use the Curves tool to slightly lift the black point for a faded film-stock look.
5. Apply a slight vignette to draw focus to the central sunflower cluster.

## Tags
`cinematic`, `teal-and-orange`, `golden-hour`, `bokeh`
