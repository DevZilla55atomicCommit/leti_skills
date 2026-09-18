---
name: davinci-sunburst-lens-flare-simulation
description: DaVinci Resolve technique: Sunburst / Lens Flare Simulation from Instagram Reel C5kjbvpPzw9
category: creative/davinci-resolve-techniques
tags: ["Lens Flare", "Sunburst", "Color Grading", "Golden Hour", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "C5kjbvpPzw9"
collection: "Gimbal_Moves"
resolve_page: "Color"
node_graph: "serial"
difficulty: "intermediate"
created: 2026-07-30
---

# Sunburst / Lens Flare Simulation

**Source:** Instagram Reel `C5kjbvpPzw9` (Gimbal_Moves)  
**Page:** Color | **Graph:** serial | **Difficulty:** intermediate

![Sunburst / Lens Flare Simulation](C5kjbvpPzw9.gif)

## Node Graph Structure

- Input
- Exposure (High Value)
- Saturation

## Parameters

- **exposure_boost**: +10 stops or more for center area
- **saturation_increase**: Significant boost to enhance colors around the sun
- **color_balance**: Warm tones added to simulate golden hour light

## Steps to Reproduce in DaVinci Resolve

1. Identify the position of the sun in your frame.
2. Create a new node on the Color page (or use an existing one).
3. Increase Exposure significantly for that specific area using a radial gradient or mask to isolate the light source.
4. Adjust Saturation to make colors pop around the flare.

## Tags
`Lens Flare`, `Sunburst`, `Color Grading`, `Golden Hour`
