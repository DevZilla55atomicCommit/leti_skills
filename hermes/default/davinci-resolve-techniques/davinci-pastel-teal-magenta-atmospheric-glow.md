---
name: davinci-pastel-teal-magenta-atmospheric-glow
description: DaVinci Resolve technique: Pastel Teal & Magenta Atmospheric Glow from Instagram Reel C9DScBltuEd
category: creative/davinci-resolve-techniques
tags: ["cinematic", "pastel", "tealandorange", "dreamy", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "C9DScBltuEd"
collection: "Ideas_for_Shooting_Videos"
resolve_page: "Color"
node_graph: "serial"
difficulty: "intermediate"
created: 2026-07-30
---

# Pastel Teal & Magenta Atmospheric Glow

**Source:** Instagram Reel `C9DScBltuEd` (Ideas_for_Shooting_Videos)  
**Page:** Color | **Graph:** serial | **Difficulty:** intermediate

![Pastel Teal & Magenta Atmospheric Glow](C9DScBltuEd.gif)

## Node Graph Structure

- Primary Balance
- Curves
- Color Wheels
- Soft Glow

## Parameters

- **lift_tint**: Teal/Cyan
- **gamma_tint**: Magenta/Pink
- **highlight_tint**: Warm/Orange
- **glow_threshold**: 0.45
- **glow_radius**: 0.60

## Steps to Reproduce in DaVinci Resolve

1. Apply a slight lift to the blacks in the Curves tool for a faded look.
2. Use the Color Wheels to push shadows toward a deep teal and midtones toward a soft magenta/pink.
3. Use Hue/Saturation curves to isolate the sky and increase saturation in pink tones.
4. Add a Glow node at the end of the chain, set the blend to Soft, and increase the radius to create the ethereal atmospheric light bleed.
5. Lower the contrast specifically in the mid-tones to maintain the dream-like aesthetic.

## Tags
`cinematic`, `pastel`, `tealandorange`, `dreamy`
