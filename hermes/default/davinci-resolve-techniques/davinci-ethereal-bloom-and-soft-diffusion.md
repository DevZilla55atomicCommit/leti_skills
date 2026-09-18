---
name: davinci-ethereal-bloom-and-soft-diffusion
description: DaVinci Resolve technique: Ethereal Bloom and Soft Diffusion from Instagram Reel C9I9sqpPt5_
category: creative/davinci-resolve-techniques
tags: ["glow", "ethereal", "cinematic", "matte-shadows", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "C9I9sqpPt5_"
collection: "Ideas_for_Shooting_Videos"
resolve_page: "Color"
node_graph: "serial"
difficulty: "intermediate"
created: 2026-07-30
---

# Ethereal Bloom and Soft Diffusion

**Source:** Instagram Reel `C9I9sqpPt5_` (Ideas_for_Shooting_Videos)  
**Page:** Color | **Graph:** serial | **Difficulty:** intermediate

![Ethereal Bloom and Soft Diffusion](C9I9sqpPt5_.gif)

## Node Graph Structure

- Primary Correction
- Soft Glow
- Halation
- Final Color Grade

## Parameters

- **glow_threshold**: 0.45
- **glow_radius**: 0.60
- **glow_opacity**: 0.30
- **lift_offset**: 0.05
- **saturation**: 0.75

## Steps to Reproduce in DaVinci Resolve

1. Apply primary exposure and balance adjustments to ensure a warm skin tone.
2. Lift the blacks in the Curves tool to create a faded, matte shadow look.
3. Add a Glow node: set the threshold to isolate highlights highlights and increase the radius for a soft bleed.
4. Add a Halation node to create subtle red/orange fringes around high-contrast edges.
5. Desaturate the overall image slightly while maintaining the vibrancy of the red dress.

## Tags
`glow`, `ethereal`, `cinematic`, `matte-shadows`
