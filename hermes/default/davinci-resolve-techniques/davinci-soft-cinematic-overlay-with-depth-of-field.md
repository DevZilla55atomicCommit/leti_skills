---
name: davinci-soft-cinematic-overlay-with-depth-of-field
description: DaVinci Resolve technique: Soft Cinematic Overlay with Depth of Field from Instagram Reel C-C8LOQyDaD
category: creative/davinci-resolve-techniques
tags: ["cinematic", "aesthetic", "overlay", "soft-lighting", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "C-C8LOQyDaD"
collection: "Ideas_for_Shooting_Videos"
resolve_page: "Color"
node_graph: "serial"
difficulty: "intermediate"
created: 2026-07-30
---

# Soft Cinematic Overlay with Depth of Field

**Source:** Instagram Reel `C-C8LOQyDaD` (Ideas_for_Shooting_Videos)  
**Page:** Color | **Graph:** serial | **Difficulty:** intermediate

![Soft Cinematic Overlay with Depth of Field](C-C8LOQyDaD.gif)

## Node Graph Structure

- Primary Correction
- Window/Mask
- Qualifier
- Overlay Node

## Parameters

- **contrast**: 1.15
- **saturation**: 0.9
- **soft_glow_radius**: 0.5
- **overlay_opacity**: 0.6

## Steps to Reproduce in DaVinci Resolve

1. Apply a soft blur to the background footage to simulate a shallow depth of field.
2. Use the Primary wheels to lift the blacks and slightly reduce saturation for a clean look.
3. Import the music interface UI as a separate track or use a Fusion Media In.
4. Apply a 'Screen' or 'Overlay' blend mode to the UI layer and reduce opacity to allow the background subject to be seen through.
5. Add a slight Glow effect to the subject highlights to enhance the soft skin tones.

## Tags
`cinematic`, `aesthetic`, `overlay`, `soft-lighting`
