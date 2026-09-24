---
name: davinci-cinematic-vignette-and-warm-color-grade
description: DaVinci Resolve technique: Cinematic Vignette and Warm Color Grade from Instagram Reel DMhG87msO1u
category: creative/davinci-resolve-techniques
tags: ["cinematic", "color-grading", "vignette", "storytelling", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "DMhG87msO1u"
collection: "Ideas_for_Shooting_Videos"
resolve_page: "Color"
node_graph: "serial"
difficulty: "beginner"
created: 2026-07-30
---

# Cinematic Vignette and Warm Color Grade

**Source:** Instagram Reel `DMhG87msO1u` (Ideas_for_Shooting_Videos)  
**Page:** Color | **Graph:** serial | **Difficulty:** beginner

![Cinematic Vignette and Warm Color Grade](DMhG87msO1u.gif)

## Node Graph Structure

- Primary Correction
- Vignette Node
- Color Wheels

## Parameters

- **Vignette Softness**: 0.5
- **Vignette Amount**: 0.4
- **Saturation**: 1.2
- **Temperature**: +200

## Steps to Reproduce in DaVinci Resolve

1. Add a primary correction node to balance exposure and contrast.
2. Add a second serial node to slightly increase the temperature and saturation for a warm look.
3. Add a third node and apply a circular window (Power Window) around the subject.
4. Invert the mask and decrease the opacity to create a subtle vignette effect.
5. Adjust the softness/feather of the window edges to ensure a smooth transition at the corners.

## Tags
`cinematic`, `color-grading`, `vignette`, `storytelling`
