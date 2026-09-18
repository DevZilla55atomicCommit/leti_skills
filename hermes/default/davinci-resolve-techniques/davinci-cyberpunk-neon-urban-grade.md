---
name: davinci-cyberpunk-neon-urban-grade
description: DaVinci Resolve technique: Cyberpunk Neon Urban Grade from Instagram Reel C-ucAkovMto
category: creative/davinci-resolve-techniques
tags: ["urban-nightlife", "cyberpunk", "neon", "teal-and-orange", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "C-ucAkovMto"
collection: "Ideas_for_Shooting_Videos"
resolve_page: "Color"
node_graph: "serial"
difficulty: "intermediate"
created: 2026-07-30
---

# Cyberpunk Neon Urban Grade

**Source:** Instagram Reel `C-ucAkovMto` (Ideas_for_Shooting_Videos)  
**Page:** Color | **Graph:** serial | **Difficulty:** intermediate

![Cyberpunk Neon Urban Grade](C-ucAkovMto.gif)

## Node Graph Structure

- Primary Balance
- Curves
- Color Wheels
- Qualifier / Mask
- Glow

## Parameters

- **contrast**: +0.15
- **saturation**: +0.20
- **pivot**: 0.5
- **shadow_tint**: Teal/Blue
- **highlight_tint**: Magenta/Red
- **glow_radius**: 50

## Steps to Reproduce in DaVinci Resolve

1. Increase contrast and lift the blacks slightly to create a matte shadow look.
2. Use the Curves tool to create an S-curve for punchy highlights.
3. In Color Wheels, push shadows toward Teal and highlights toward Magenta/Red.
4. Use a Qualifier or Power Window to isolate the bright neon signs and increase their saturation and gain specifically.
5. Add a Glow node at the end chain with a soft radius and high threshold to simulate light bleed from the LED screens.
6. Apply a slight vignette to focus attention on the center-subject.

## Tags
`urban-nightlife`, `cyberpunk`, `neon`, `teal-and-orange`
