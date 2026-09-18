---
name: davinci-high-contrast-cinematic-silhouette-warm-sunset
description: DaVinci Resolve technique: High-Contrast Cinematic Silhouette & Warm Sunset from Instagram Reel C_qJIy0Bk4Y
category: creative/davinci-resolve-techniques
tags: ["cinematic", "silhouette", "sunset", "high-contrast", "urban", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "C_qJIy0Bk4Y"
collection: "Ideas_for_Shooting_Videos"
resolve_page: "Color"
node_graph: "serial"
difficulty: "beginner"
created: 2026-07-30
---

# High-Contrast Cinematic Silhouette & Warm Sunset

**Source:** Instagram Reel `C_qJIy0Bk4Y` (Ideas_for_Shooting_Videos)  
**Page:** Color | **Graph:** serial | **Difficulty:** beginner

![High-Contrast Cinematic Silhouette & Warm Sunset](C_qJIy0Bk4Y.gif)

## Node Graph Structure

- Exposure
- Curves
- Color Wheels
- Power Window

## Parameters

- **contrast**: 1.4
- **shadows**: crushed
- **highlights**: warm/orange
- **saturation**: boost-in-midtones

## Steps to Reproduce in DaVinci Resolve

1. Use the Primary Wheels to drop lifts and shadows until the city skyline is a black silhouette.
2. Apply a Curves node to create a sharp S-curve, increasing contrast between the sky and the buildings.
3. Use the Gain wheel to push highlights toward a warm orange/yellow hue.
4. Use the Offset wheel to add a slight teal or purple tint to the upper shadows/clouds.
5. Apply a Power Window with a soft feather around the horizon to specifically boost saturation and brightness of the orange fireglow.
6. Add a Gaussian Blur effect on a separate node with a mask for the foreground figure to mimic the shallow depth-of-field look.

## Tags
`cinematic`, `silhouette`, `sunset`, `high-contrast`, `urban`
