---
name: davinci-golden-hour-cinematic-depth-of-field
description: DaVinci Resolve technique: Golden Hour Cinematic Depth of Field from Instagram Reel ChH34PyAcjs
category: creative/davinci-resolve-techniques
tags: ["cinematic", "golden-hour", "depth-of-field", "urban", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "ChH34PyAcjs"
collection: "Ideas_for_Shooting_Videos"
resolve_page: "Color"
node_graph: "serial"
difficulty: "intermediate"
created: 2026-07-30
---

# Golden Hour Cinematic Depth of Field

**Source:** Instagram Reel `ChH34PyAcjs` (Ideas_for_Shooting_Videos)  
**Page:** Color | **Graph:** serial | **Difficulty:** intermediate

![Golden Hour Cinematic Depth of Field](ChH34PyAcjs.gif)

## Node Graph Structure

- Primary Correction
- Power Windows
- Color Blur
- Qualifiers

## Parameters

- **temperature**: 6500K
- **saturation**: 0.45
- **lift_offset**: +0.02
- **glow_intensity**: 0.15

## Steps to Reproduce in DaVinci Resolve

1. Apply a warm color balance using the Temperature and Tint sliders to mimic sunset light.
2. Use a Power Window on the subject to slightly darken them, separating them from the background.
3. Use the Color Blur tool on the background masked area to simulate shallow depth of field/bokeh.
4. Add a Glow effect with a high threshold to soften the highlights on the buildings and the Burj Khalifa.
5. Lift the shadows slightly in the Color Wheels to achieve a faded cinematic look.

## Tags
`cinematic`, `golden-hour`, `depth-of-field`, `urban`
