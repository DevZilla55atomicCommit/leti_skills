---
name: davinci-backlit-glow-selective-bloom-enhancement
description: DaVinci Resolve technique: Backlit Glow & Selective Bloom Enhancement from Instagram Reel C6l38Evx83e
category: creative/davinci-resolve-techniques
tags: ["bloom", "glow", "golden-hour", "cinematic", "masking", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "C6l38Evx83e"
collection: "Footage_Collection"
resolve_page: "Color"
node_graph: "serial"
difficulty: "intermediate"
created: 2026-07-30
---

# Backlit Glow & Selective Bloom Enhancement

**Source:** Instagram Reel `C6l38Evx83e` (Footage_Collection)  
**Page:** Color | **Graph:** serial | **Difficulty:** intermediate

![Backlit Glow & Selective Bloom Enhancement](C6l38Evx83e.gif)

## Node Graph Structure

- Primary Correction
- Qualifier Mask
- Glow Node
- Color Grading

## Parameters

- **Glow Threshold**: 0.45
- **Glow Radius**: 0.70
- **Glow Spread**: 0.60
- **Mid Tone**: Warm

## Steps to Reproduce in DaVinci Resolve

1. Create a primary color correction node to balance exposure and white balance.
2. Add a new node and apply the Glow effect.
3. Use a Qualifier or Power Window to isolate the brightest areas (the sun and flower edges).
4. Adjust the Threshold and Radius to create a soft bleed of light without washing out shadows.
5. Increase contrast slightly in a preceding node to make the glow pop.

## Tags
`bloom`, `glow`, `golden-hour`, `cinematic`, `masking`
