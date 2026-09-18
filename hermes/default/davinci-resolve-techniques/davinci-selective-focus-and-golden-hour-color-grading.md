---
name: davinci-selective-focus-and-golden-hour-color-grading
description: DaVinci Resolve technique: Selective Focus and Golden Hour Color Grading from Instagram Reel C6_phVax0DA
category: creative/davinci-resolve-techniques
tags: ["cinematic", "bokeh", "golden-hour", "selective-masking", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "C6_phVax0DA"
collection: "Footage_Collection"
resolve_page: "Color"
node_graph: "serial"
difficulty: "intermediate"
created: 2026-07-30
---

# Selective Focus and Golden Hour Color Grading

**Source:** Instagram Reel `C6_phVax0DA` (Footage_Collection)  
**Page:** Color | **Graph:** serial | **Difficulty:** intermediate

![Selective Focus and Golden Hour Color Grading](C6_phVax0DA.gif)

## Node Graph Structure

- Primary Correction
- Power Window Mask
- Gaussian Blur
- Color Wheels

## Parameters

- **Radius**: Soft edge
- **Temperature**: Warm (+1500)
- **Contrast**: High
- **Saturation**: Moderate (+1.1)

## Steps to Reproduce in DaVinci Resolve

1. Import footage and use Primary Wheels to balance exposure and warm up the highlights
2. Apply a Power Window (circular) around the daisy to increase its exposure
3. Add Gaussian Blur to the background area to simulate a shallow depth of field
4. Use the Tint wheel to add golden/orange tones to the highlights
5. Apply a slight vignette to draw focus to the center subject

## Tags
`cinematic`, `bokeh`, `golden-hour`, `selective-masking`
