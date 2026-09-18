---
name: davinci-color-global-offset-color-balancing
description: 12 techniques for Color - Global Offset Color Balancing
trigger: Need Color technique for Global Offset Color Balancing
category: Color
tags: DaVinci Resolve, Instagram Reels, action sports, aerial, automotive, background separation, cinematic, color grading, filmic look, golden hour, gradient overlay, log footage, masking, mobile, moody, offset, overcast sky, photo enhancement, skin tones, subtle adjustments, sun effect, teal-and-orange, tutorial, video editing
---

# Global Offset Color Balancing

## Overview
Combined 12 related techniques from Instagram Reels.

## Resolve Page
Color

## Node Graph Type
serial

## Key Nodes
- Color
- Color Correct
- Color Correction
- Color Wheels
- ColorWheel
- Curves
- Gradient
- Hue/Saturation/Luma
- LUT
- LUT Apply
- Offset Node
- Power Window
- Primary
- Primary Correction
- Primary Wheels
- Qualifier
- Qualifier/Mask
- Secondary

## Parameters
- Offset: 25.00
- Lift: 25.00
- Gamma: Warm (Orange/Yellow)
- Gain: 1.00
- Saturation: -0.3
- Contrast: +0.2
- Midtones: Warm/Orange
- Shadows: Deep Blue/Black
- Midtone: Lift for dust detail
- ColorWheel_Lift_Gamma_Gain: {'lift': [1.0, 1.0, 1.0], 'gamma': [1.0, 1.0, 1.0], 'gain': [1.0, 1.0, 1.0]}
- Curves_Midtones: {'gamma': 1.0}
- Qualifier_Hue: [0.0, 1.0]
- Qualifier_Saturation: [0.0, 1.0]
- Qualifier_Luminance: [0.0, 1.0]
- Highlights: Warm/Yellow
- LUT: Filmic Pro
- Exposure: 0.5
- Gradient Fill: 50%
- lift: 0.1
- gamma: 0.2
- Curves: S-Curve

## Steps to Reproduce
1. Import the video clip into the timeline
2. Navigate to the Color page
3. Select the Offset tool in the color wheels panel
4. Adjust the circular color wheel to balance the global color tint and exposure
5. Monitor the Waveform scopes to ensure highlights are not clipping
6. Add a primary node to adjust contrast and white balance
7. Use the Color Wheels to push shadows toward teal/blue
8. Use the Offset or Wheels to push midtones/highlights toward a warm orange/yellow
9. Use the Hue/Saturation curve to de-saturate greens if they appear distracting
10. Apply a slight vignette to draw focus to the central island formation

## Difficulty
beginner

## Tags
DaVinci Resolve, Instagram Reels, action sports, aerial, automotive, background separation, cinematic, color grading, filmic look, golden hour, gradient overlay, log footage, masking, mobile, moody, offset, overcast sky, photo enhancement, skin tones, subtle adjustments, sun effect, teal-and-orange, tutorial, video editing
