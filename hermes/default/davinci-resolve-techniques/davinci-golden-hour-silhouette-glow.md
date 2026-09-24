---
name: davinci-golden-hour-silhouette-glow
description: DaVinci Resolve technique: Golden Hour Silhouette & Glow from Instagram Reel C3a7PJVPooa
category: creative/davinci-resolve-techniques
tags: ["sunset", "cinematic", "silhouette", "golden-hour", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "C3a7PJVPooa"
collection: "Cinematic"
resolve_page: "Color"
node_graph: "serial"
difficulty: "intermediate"
created: 2026-07-30
---

# Golden Hour Silhouette & Glow

**Source:** Instagram Reel `C3a7PJVPooa` (Cinematic)  
**Page:** Color | **Graph:** serial | **Difficulty:** intermediate

![Golden Hour Silhouette & Glow](C3a7PJVPooa.gif)

## Node Graph Structure

- Exposure
- Primary Balance
- Color Wheels
- Qualifiers
- Glow

## Parameters

- **temperature**: +2500
- **saturation**: 1.4
- **shadows_tint**: Teal
- **highlights_tint**: Orange/Gold
- **glow_radius**: 0.5

## Steps to Reproduce in DaVinci Resolve

1. Lower overall exposure and contrast to push palm trees into deep silhouettes.
2. Increase Temperature and Tint to warm the highlights and sky tones.
3. Use Color Wheels to add a subtle teal tint to the shadows for a complementary orange-teal cinematic grade.
4. Apply a Qualifier to select the sun and water reflection to boost luminance specifically.
5. Add a Glow node with a wide radius and low threshold to create the dreamy atmospheric light diffusion.
6. Increase saturation specifically in the orange and yellow hue ranges.

## Tags
`sunset`, `cinematic`, `silhouette`, `golden-hour`
