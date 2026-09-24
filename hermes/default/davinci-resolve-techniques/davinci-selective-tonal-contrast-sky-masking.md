---
name: davinci-selective-tonal-contrast-sky-masking
description: DaVinci Resolve technique: Selective Tonal Contrast & Sky Masking from Instagram Reel DEzts-4tXus
category: creative/davinci-resolve-techniques
tags: ["color grading", "cinematic", "masking", "travel edit", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "DEzts-4tXus"
collection: "Ideas_for_Shooting_Videos"
resolve_page: "Color"
node_graph: "serial"
difficulty: "intermediate"
created: 2026-07-30
---

# Selective Tonal Contrast & Sky Masking

**Source:** Instagram Reel `DEzts-4tXus` (Ideas_for_Shooting_Videos)  
**Page:** Color | **Graph:** serial | **Difficulty:** intermediate

![Selective Tonal Contrast & Sky Masking](DEzts-4tXus.gif)

## Node Graph Structure

- Primary Correction
- Qualifier/Masking
- Color Curves
- Power Window

## Parameters

- **Saturation**: +15
- **Contrast**: +1.2
- **Midtones**: Teal/Blue shift
- **Highlights**: Warm/Orange shift

## Steps to Reproduce in DaVinci Resolve

1. Import clip and perform basic exposure/white balance using Primary wheels.
2. Add a new node and use a Magic or Qualifier to isolate the rock formation.
3. Increase saturation and shift warmth on the isolated rocks to enhance orange/red tones.
4. Add a separate node for the sky using a Power Window mask.
5. Deepen the blues in the sky using the Hue Hue curve to create color contrast.
6. Apply a soft vignette to draw focus to the mountain peak.

## Tags
`color grading`, `cinematic`, `masking`, `travel edit`
