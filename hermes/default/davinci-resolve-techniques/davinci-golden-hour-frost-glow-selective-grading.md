---
name: davinci-golden-hour-frost-glow-selective-grading
description: DaVinci Resolve technique: Golden Hour Frost Glow & Selective Grading from Instagram Reel C61YhYoRNRG
category: creative/davinci-resolve-techniques
tags: ["cinematic", "lighting", "color-grading", "masking", "frost-effect", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "C61YhYoRNRG"
collection: "Footage_Collection"
resolve_page: "Color"
node_graph: "serial"
difficulty: "intermediate"
created: 2026-07-30
---

# Golden Hour Frost Glow & Selective Grading

**Source:** Instagram Reel `C61YhYoRNRG` (Footage_Collection)  
**Page:** Color | **Graph:** serial | **Difficulty:** intermediate

![Golden Hour Frost Glow & Selective Grading](C61YhYoRNRG.gif)

## Node Graph Structure

- Primary Correction
- Split Tone
- Power Window
- Soft Glow

## Parameters

- **Contrast**: High
- **Highlight Tint**: Warm/Orange
- **Shadow Tint**: Cool/Blue
- **Glow Radius**: High (Midtone de-focus)

## Steps to Reproduce in DaVinci Resolve

1. Apply a primary color grade to lift the shadows toward blue and push highlights toward warm orange
2. Use a Hue Qualifier to isolate the white petals/frost and increase their exposure and saturation
3. Create a Power Window around the rose to slightly increase exposure and saturation
4. Add a Glow node with a high threshold and low opacity to create the ethereal light bleed on the frost
5. Increase contrast slightly in a preceding node to make the beaming highlights pop

## Tags
`cinematic`, `lighting`, `color-grading`, `masking`, `frost-effect`
