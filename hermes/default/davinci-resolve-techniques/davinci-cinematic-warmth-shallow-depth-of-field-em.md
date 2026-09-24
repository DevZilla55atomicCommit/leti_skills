---
name: davinci-cinematic-warmth-shallow-depth-of-field-em
description: DaVinci Resolve technique: Cinematic Warmth & Shallow Depth of Field Em from Instagram Reel C6LIFcoScsa
category: creative/davinci-resolve-techniques
tags: ["cinematic", "warm-tones", "close-up", "bokeh", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "C6LIFcoScsa"
collection: "Ideas_for_Shooting_Videos"
resolve_page: "Color"
node_graph: "serial"
difficulty: "intermediate"
created: 2026-07-30
---

# Cinematic Warmth & Shallow Depth of Field Em

**Source:** Instagram Reel `C6LIFcoScsa` (Ideas_for_Shooting_Videos)  
**Page:** Color | **Graph:** serial | **Difficulty:** intermediate

![Cinematic Warmth & Shallow Depth of Field Em](C6LIFcoScsa.gif)

## Node Graph Structure

- Primary Correction
- Exposure/Contrast
- Color Balance (Warm)
- Halation/Glow

## Parameters

- **contrast**: 1.2
- **pivot**: 0.45
- **lift_offset**: -0.02
- **saturation**: 1.15
- **midtone_tint**: Warm/Golden Orange

## Steps to Reproduce in DaVinci Resolve

1. Apply a power window to isolate the eye and slightly increase sharpness to draw the eye.
2. Use the Color Wheels to slightly lift the blacks for a faded matte look.
3. Increase contrast and adjust the pivot to protect the skin tone midtones.
4. Add a warm orange tint to the midtones and highlights to enhance the golden skin tones.
5. Add a Glow node with a low threshold and high softness to soften the highlights on the skin.

## Tags
`cinematic`, `warm-tones`, `close-up`, `bokeh`
