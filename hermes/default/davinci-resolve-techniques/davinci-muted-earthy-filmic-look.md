---
name: davinci-muted-earthy-filmic-look
description: DaVinci Resolve technique: Muted Earthy Filmic Look from Instagram Reel C-Az-_SoskP
category: creative/davinci-resolve-techniques
tags: ["cinematic", "muted", "desaturated", "matte", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "C-Az-_SoskP"
collection: "Ideas_for_Shooting_Videos"
resolve_page: "Color"
node_graph: "serial"
difficulty: "intermediate"
created: 2026-07-30
---

# Muted Earthy Filmic Look

**Source:** Instagram Reel `C-Az-_SoskP` (Ideas_for_Shooting_Videos)  
**Page:** Color | **Graph:** serial | **Difficulty:** intermediate

![Muted Earthy Filmic Look](C-Az-_SoskP.gif)

## Node Graph Structure

- Exposure
- Curves
- Color Wheels
- Hue Sat
- Soft Glow

## Parameters

- **lift**: +0.02
- **gamma**: -0.05
- **saturation**: 0.75
- **contrast**: 0.9
- **shadow_tint**: Teal/Blue

## Steps to Reproduce in DaVinci Resolve

1. Apply a Sony SLog3 to Rec709 transform to normalize footage.
2. Use the Lift wheel to slightly raise the blacks for a matte/faded look.
3. Decrease overall saturation to achieve a muted aesthetic.
4. Use Hue vs Saturation curves to specifically desaturate greens and yellows while protecting skin tones.
5. Add a slight blue/teal tint to the shadows and a warm tint to the highlights using Color Wheels.
6. Add a Glow node with a low threshold and high falloff to soften the skin and highlights.

## Tags
`cinematic`, `muted`, `desaturated`, `matte`
