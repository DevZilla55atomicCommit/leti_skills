---
name: davinci-warm-sunset-silhouette-glow
description: DaVinci Resolve technique: Warm Sunset Silhouette & Glow from Instagram Reel C-B6SRuPHhn
category: creative/davinci-resolve-techniques
tags: ["cinematic", "sunset", "silhouette", "glow", "warm-tones", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "C-B6SRuPHhn"
collection: "Ideas_for_Shooting_Videos"
resolve_page: "Color"
node_graph: "serial"
difficulty: "intermediate"
created: 2026-07-30
---

# Warm Sunset Silhouette & Glow

**Source:** Instagram Reel `C-B6SRuPHhn` (Ideas_for_Shooting_Videos)  
**Page:** Color | **Graph:** serial | **Difficulty:** intermediate

![Warm Sunset Silhouette & Glow](C-B6SRuPHhn.gif)

## Node Graph Structure

- Exposure
- Primary Balance
- Color Wheels
- Soft Glow
- Power Window

## Parameters

- **exposure**: -1.5
- **saturation**: 0.65
- **glow_threshold**: 0.4
- **glow_radius**: 0.70
- **contrast**: 1.20

## Steps to Reproduce in DaVinci Resolve

1. Use the Primary wheels to underexpose the image until the skyline becomes a silhouette.
2. Use Color Wheels to push the highlights toward orange/yellow and shadows toward a slight purple/blue.
3. Apply a Glow node in the serial chain with a low threshold and high radius to create the dreamy light-bleed.
4. Use a Power Window (linear gradient) to slightly increase the saturation and brightness of the sky specifically.
5. Adjust the Saturation curve to soften the mid-tones while increasing the vibrance of the sunset colors.

## Tags
`cinematic`, `sunset`, `silhouette`, `glow`, `warm-tones`
