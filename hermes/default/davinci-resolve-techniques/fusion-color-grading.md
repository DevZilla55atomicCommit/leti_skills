---
name: Fusion - color grading
description: 6 related techniques for Fusion - color grading
trigger: Need fusion technique for color grading
category: Fusion
tags: Compositing, DaVinci Resolve, DaVinci Resolve Technique, Double Exposure, Fusion Compositing, Instagram Reel, Motion Blur, Shot Label, Split Screen, Text Overlay
---

# color grading (Fusion)

## Overview
Combined 6 techniques from Instagram Reels for fusion page.

## Resolve Page
Fusion

## Node Graph Type
serial

## Key Nodes
- Compound
- Image Composite
- Layer Mixer
- Mask
- Motion Blur
- Split Screen
- Text
- Transform

## Parameters
- text_alignment: center_vertical
- opacity: 50%
- Blur Amount: High
- blend_mode: Normal
- split_direction: vertical
- text: SHOT #1
- font_size: 40
- position_x: 50%
- position_y: 20%

## Steps to Reproduce
1. Import textured background clip into Fusion workspace
2. Add Text node and input 'Life' text
3. Position text vertically centered in the frame
4. Adjust text opacity to desired level (e.g., 50%)
5. Composite text layer with background using Image Composite node
6. 1. Create a mask to isolate the blurred region (left side of frame).
7. 2. Apply Motion Blur effect to the masked area with high blur intensity.
8. Import two video clips into Fusion timeline
9. Create a Compound node with Layer Mixer
10. Adjust opacity and blend mode for soft visual effect
11. Create a new Fusion page and import the three video clips
12. Add Split Screen node with vertical splits set to 3 panels

## Difficulty
intermediate

## Tags
Compositing, DaVinci Resolve, DaVinci Resolve Technique, Double Exposure, Fusion Compositing, Instagram Reel, Motion Blur, Shot Label, Split Screen, Text Overlay
