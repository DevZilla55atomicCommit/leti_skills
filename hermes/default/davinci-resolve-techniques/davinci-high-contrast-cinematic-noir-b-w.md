---
name: davinci-high-contrast-cinematic-noir-b-w
description: DaVinci Resolve technique: High-Contrast Cinematic Noir B&W from Instagram Reel C0Q_WeysU5T
category: creative/davinci-resolve-techniques
tags: ["black-and-white", "cinematic", "editorial", "high-contrast", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "C0Q_WeysU5T"
collection: "Ideas_for_Shooting_Videos"
resolve_page: "Color"
node_graph: "serial"
difficulty: "beginner"
created: 2026-07-30
---

# High-Contrast Cinematic Noir B&W

**Source:** Instagram Reel `C0Q_WeysU5T` (Ideas_for_Shooting_Videos)  
**Page:** Color | **Graph:** serial | **Difficulty:** beginner

![High-Contrast Cinematic Noir B&W](C0Q_WeysU5T.gif)

## Node Graph Structure

- Primary Correction
- Curves
- Power Windows
- Film Grain

## Parameters

- **Contrast**: 1.45
- **Saturation**: 0.0
- **Shadows**: -15dB
- **Highlights**: +10dB

## Steps to Reproduce in DaVinci Resolve

1. Add a Saturation node and drop Saturation to 0 to convert to B&W.
2. Use the Prim Wheels to lift the blacks slightly and crush the shadows for a matte look.
3. Use the Curves tool to create a slight S-Curve to enhance mid-tone contrast and pop.
4. Apply a Power Window (circular mask) around the subject to slightly increase her exposure and pop her from the background.
5. Add a subtle Film Grain effect in the final node to simulate cinematic film stock.

## Tags
`black-and-white`, `cinematic`, `editorial`, `high-contrast`
