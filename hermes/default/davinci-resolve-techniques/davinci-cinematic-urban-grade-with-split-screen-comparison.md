---
name: davinci-cinematic-urban-grade-with-split-screen-comparison
description: DaVinci Resolve technique: Cinematic Urban Grade with Split-Screen Comparison from Instagram Reel C9BJVXAyRjn
category: creative/davinci-resolve-techniques
tags: ["color grading", "cinematic", "split-screen", "urban", "workflow", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "C9BJVXAyRjn"
collection: "Ideas_for_Shooting_Videos"
resolve_page: "Color"
node_graph: "serial"
difficulty: "intermediate"
created: 2026-07-30
---

# Cinematic Urban Grade with Split-Screen Comparison

**Source:** Instagram Reel `C9BJVXAyRjn` (Ideas_for_Shooting_Videos)  
**Page:** Color | **Graph:** serial | **Difficulty:** intermediate

![Cinematic Urban Grade with Split-Screen Comparison](C9BJVXAyRjn.gif)

## Node Graph Structure

- Primary Correction
- Color Wheels
- Power Windows
- Split Screen Mask

## Parameters

- **contrast**: 1.22
- **saturation**: 4.5
- **lift**: -0.02
- **gamma**: 0.05
- **color_offset**: Teal/Orange balance

## Steps to Reproduce in DaVinci Resolve

1. Import footage and create a Serial Node for the base grade.
2. Use Color Wheels to lift blacks and push contrast for a moody look.
3. Apply a Teal tint to shadows and a warm Orange tint to highlights using the Wheels.
4. Open the Split Screen tool in the top viewer.
5. Set Screen 1 to show the Before grade and Screen 2 to show the After grade.
6. Use a Linear Wipe or Mask on one node to create the vertical split-screen effect.

## Tags
`color grading`, `cinematic`, `split-screen`, `urban`, `workflow`
