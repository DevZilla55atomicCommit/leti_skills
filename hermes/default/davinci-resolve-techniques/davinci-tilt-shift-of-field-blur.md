---
name: davinci-tilt-shift-of-field-blur
description: DaVinci Resolve technique: Tilt-Shift of Field Blur from Instagram Reel C4QSzF4AKGL
category: creative/davinci-resolve-techniques
tags: ["depth-of-field", "blur", "cinematic", "focus", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "C4QSzF4AKGL"
collection: "Ideas_for_Shooting_Videos"
resolve_page: "Fusion"
node_graph: "serial"
difficulty: "intermediate"
created: 2026-07-30
---

# Tilt-Shift of Field Blur

**Source:** Instagram Reel `C4QSzF4AKGL` (Ideas_for_Shooting_Videos)  
**Page:** Fusion | **Graph:** serial | **Difficulty:** intermediate

![Tilt-Shift of Field Blur](C4QSzF4AKGL.gif)

## Node Graph Structure

- MediaIn
- GaussianBlur
- MergeMask

## Parameters

- **Blur Radius**: High (Adjustable)
- **Softness**: High
- **Mask Type**: Ellipse or Gradient Mask

## Steps to Reproduce in DaVinci Resolve

1. Send the clip to the Fusion page
2. Add a GaussianBlur node connected to the MediaIn
3. Add an Ellipse Mask and connect it to the blue input of the GaussianBlur
4. Invert the mask so the center remains sharp
5. Adjust the mask size and feathering to isolate the focus on the subject
6. Animate the mask position or size if the subject moves

## Tags
`depth-of-field`, `blur`, `cinematic`, `focus`
