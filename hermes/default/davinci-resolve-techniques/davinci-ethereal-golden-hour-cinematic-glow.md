---
name: davinci-ethereal-golden-hour-cinematic-glow
description: DaVinci Resolve technique: Ethereal Golden Hour Cinematic Glow from Instagram Reel C7gMA4mRrRQ
category: creative/davinci-resolve-techniques
tags: ["cinematic", "warm", "glow", "golden-hour", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "C7gMA4mRrRQ"
collection: "Ideas_for_Shooting_Videos"
resolve_page: "Color"
node_graph: "serial"
difficulty: "intermediate"
created: 2026-07-30
---

# Ethereal Golden Hour Cinematic Glow

**Source:** Instagram Reel `C7gMA4mRrRQ` (Ideas_for_Shooting_Videos)  
**Page:** Color | **Graph:** serial | **Difficulty:** intermediate

![Ethereal Golden Hour Cinematic Glow](C7gMA4mRrRQ.gif)

## Node Graph Structure

- Primary Balance
- Curves (Contrast)
- Color Wheels (Warmth)
- Glow/Diffusion

## Parameters

- **lift**: -0.02
- **gamma**: +0.05
- **gain**: +0.10
- **saturation**: 0.75
- **glow_threshold**: 0.50
- **glow_blur**: 0.60
- **glow_opacity**: 0.20
- **midtone_tint**: Amber/Orange

## Steps to Reproduce in DaVinci Resolve

1. Apply a slight S-curve in the Curves tool to add contrast.
2. Shift the Midtones and Highlights toward a warm orange/yellow hue using the Color Wheels.
3. Desaturate the overall image slightly to achieve a filmic look.
4. Add a Glow OpenFX effect on a separate node with a high threshold and low opacity to create the dreamy bloom.
5. Use a Power Window to isolate the subject and slightly increase sharpness/exposure to pop against the soft background.

## Tags
`cinematic`, `warm`, `glow`, `golden-hour`
