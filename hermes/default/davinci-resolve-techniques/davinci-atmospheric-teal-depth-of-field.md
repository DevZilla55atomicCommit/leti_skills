---
name: davinci-atmospheric-teal-depth-of-field
description: DaVinci Resolve technique: Atmospheric Teal Depth of Field from Instagram Reel C8q495SSWgp
category: creative/davinci-resolve-techniques
tags: ["cinematic", "moody", "teal-and-green", "out-of-focus", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "C8q495SSWgp"
collection: "Ideas_for_Shooting_Videos"
resolve_page: "Color"
node_graph: "serial"
difficulty: "intermediate"
created: 2026-07-30
---

# Atmospheric Teal Depth of Field

**Source:** Instagram Reel `C8q495SSWgp` (Ideas_for_Shooting_Videos)  
**Page:** Color | **Graph:** serial | **Difficulty:** intermediate

![Atmospheric Teal Depth of Field](C8q495SSWgp.gif)

## Node Graph Structure

- Primary Correction
- Color Wheels Offset
- Curves
- Blur/Glow

## Parameters

- **shadow_tint**: Teal/Green
- **saturation**: 0.6
- **contrast**: 1.2
- **glow_radius**: 0.05
- **blur_amount**: 30-50

## Steps to Reproduce in DaVinci Resolve

1. Apply a Gaussian Blur or Lens Blur to the entire clip to simulate shallow depth of field.
2. Use the Color Wheels to push the lift/shadows toward a deep teal/green.
3. Adjust the Curves tool to lift the blacks slightly for a faded-film look.
4. Add a soft Glow node with a high threshold to make the highlights bleed into the shadows.
5. Use a mask/window to keep the vertical structural element sharp while the rest remains blurred.

## Tags
`cinematic`, `moody`, `teal-and-green`, `out-of-focus`
