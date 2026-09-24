---
name: davinci-golden-hour-cinematic-warmth-glow
description: DaVinci Resolve technique: Golden Hour Cinematic Warmth Glow from Instagram Reel C3Z_nlTsF_u
category: creative/davinci-resolve-techniques
tags: ["cinematic", "golden-hour", "travel-vlog", "warm-tone", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "C3Z_nlTsF_u"
collection: "Cinematic"
resolve_page: "Color"
node_graph: "serial"
difficulty: "intermediate"
created: 2026-07-30
---

# Golden Hour Cinematic Warmth Glow

**Source:** Instagram Reel `C3Z_nlTsF_u` (Cinematic)  
**Page:** Color | **Graph:** serial | **Difficulty:** intermediate

![Golden Hour Cinematic Warmth Glow](C3Z_nlTsF_u.gif)

## Node Graph Structure

- Primary Exposure
- Color Balance
- HSL Curves
- Glow/Diffusion
- Halation

## Parameters

- **Temperature**: +15.0
- **Tint**: +5.0
- **Contrast**: 1.200
- **Glow Intensity**: 0.25
- **Glow Spread**: 0.60

## Steps to Reproduce in DaVinci Resolve

1. Adjust Primary wheels to underexpose shadows slightly while protecting highlight detail.
2. Use the Color Wheels to push midtones toward orange/yellow and shadows toward a warm teal or brown.
3. Apply a Curves node to slightly lift the black point for a matte, cinematic look.
4. Add a Glow effect with a high spread and low threshold to create the atmospheric haze/bloom around the sun.
5. Add a subtle Halation effect on high-contrast edges to simulate film stock behavior.

## Tags
`cinematic`, `golden-hour`, `travel-vlog`, `warm-tone`
