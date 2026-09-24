---
name: davinci-selective-warm-glow-and-temperature-contrast
description: DaVinci Resolve technique: Selective Warm Glow and Temperature Contrast from Instagram Reel C0Q4-B_rGzD
category: creative/davinci-resolve-techniques
tags: ["color grading", "cinematic", "tealandorange", "architectural", "power windows", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "C0Q4-B_rGzD"
collection: "Gimbal_Moves"
resolve_page: "Color"
node_graph: "serial"
difficulty: "intermediate"
created: 2026-07-30
---

# Selective Warm Glow and Temperature Contrast

**Source:** Instagram Reel `C0Q4-B_rGzD` (Gimbal_Moves)  
**Page:** Color | **Graph:** serial | **Difficulty:** intermediate

![Selective Warm Glow and Temperature Contrast](C0Q4-B_rGzD.gif)

## Node Graph Structure

- Primary Grade
- Power Window/Mask
- Qualifier/Mask Tracking

## Parameters

- **Gain**: +2dB
- **Temperature**: -10
- **Saturation**: +15
- **Window Softness**: 50-100 pixels

## Steps to Reproduce in DaVinci Resolve

1. Add a primary node to drop the global temperature for a blue/teal tint in the shadows.
2. Create a Power Window (mask) around the windows and exterior light sconces.
3. Increase the Gain and shift Temperature upward on the masked area to create a warm glow.
4. Apply a soft feather to the mask edges to ensure the light blends naturally into the architecture.
5. Use a secondary node with a tracker to slightly increase exposure on the subject in the white shirt to make them pop against the background.

## Tags
`color grading`, `cinematic`, `tealandorange`, `architectural`, `power windows`
