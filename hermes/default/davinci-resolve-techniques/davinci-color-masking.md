---
name: Color - masking
description: 2 related techniques for Color - masking
trigger: Need color technique for masking
category: Color
tags: color grading, color-grading, depth-of-field, isolation, masking, polygon, surrealism
---

# masking (Color)

## Overview
Combined 2 techniques from Instagram Reels for color page.

## Resolve Page
Color

## Node Graph Type
serial

## Key Nodes
- Color Wheels
- Gaussian Blur
- Magic Qualifier Mask
- Primary Correction
- Primary Grade
- Qualifier/Window

## Parameters
- window_type: Polygon
- tracking: Active
- offset: 25.00
- Blur Radius: High
- Mask Edge Softness: Soft
- Saturation (Subject): +15
- Midtone Tint: Cool/Blue

## Steps to Reproduce
1. Go to the Color page
2. Select the Polygon Window tool from the Window tab
3. Draw a custom path around the desired subject
4. Go to the Tracker tab and click play to track the mask to the subject movement
5. Apply color adjustments using the Primary Wheels or Curves to affect the masked area
6. Import footage and go to the Color page.
7. Use the Magic Qualifier or Power Window to select the pink flower and immediate foreground.
8. Refine the mask edges to ensure the flower is isolated from the mountains.
9. Create a separate node for the background and apply a Gaussian Blur to simulate shallow depth of field.
10. On the subject node, increase saturation and contrast to make the flower pop.
11. Apply a cool color grade to the background nodes to create atmospheric depth.

## Difficulty
intermediate

## Tags
color grading, color-grading, depth-of-field, isolation, masking, polygon, surrealism
