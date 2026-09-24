---
name: davinci-high-contrast-teal-orange-cinematic-glow
description: DaVinci Resolve technique: High-Contrast Teal & Orange Cinematic Glow from Instagram Reel C-FbEeKgvNu
category: creative/davinci-resolve-techniques
tags: ["cinematic", "teal and orange", "shallow depth of field", "moody", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "C-FbEeKgvNu"
collection: "Ideas_for_Shooting_Videos"
resolve_page: "Color"
node_graph: "serial"
difficulty: "intermediate"
created: 2026-07-30
---

# High-Contrast Teal & Orange Cinematic Glow

**Source:** Instagram Reel `C-FbEeKgvNu` (Ideas_for_Shooting_Videos)  
**Page:** Color | **Graph:** serial | **Difficulty:** intermediate

![High-Contrast Teal & Orange Cinematic Glow](C-FbEeKgvNu.gif)

## Node Graph Structure

- Primary Correction
- Color Wheels
- Power Window
- Glow

## Parameters

- **contrast**: 1.45
- **pivot**: 0.45
- **midtone_offset**: Teal
- **highlight_offset**: Warm Orange
- **glow_radius**: 64.0

## Steps to Reproduce in DaVinci Resolve

1. Increase contrast and adjust the pivot to deepen the blacks.
2. Use the Lift Color Wheel to push shadows toward a teal/cyan hue.
3. Use the Gain and Gamma wheels to push highlights and midtones toward a warm orange/peach tone.
4. Apply a soft Power Window around the hands to slightly brighten and warm the skin tones.
5. Add a Glow node at the end with high threshold and low opacity to create the soft diffusion on the white gloves.
6. Apply a vignette to further draw focus to the center where the hands are.

## Tags
`cinematic`, `teal and orange`, `shallow depth of field`, `moody`
