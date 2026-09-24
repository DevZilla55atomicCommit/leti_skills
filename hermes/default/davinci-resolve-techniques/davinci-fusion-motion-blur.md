---
name: Fusion - motion-blur
description: 2 related techniques for Fusion - motion-blur
trigger: Need fusion technique for motion-blur
category: Fusion
tags: dreamy, fusion, motion-blur, vfx, zoom, zoom-blur
---

# motion-blur (Fusion)

## Overview
Combined 2 techniques from Instagram Reels for fusion page.

## Resolve Page
Fusion

## Node Graph Type
serial

## Key Nodes
- MediaIn
- MergeOut
- Motion Blur
- MotionBlur
- Transform

## Parameters
- Amount: 0.80
- Length: 32
- Filter-Type: Zoom
- Transform Scale: Keyframed animation
- Motion Blur: Enabled
- Quality: High
- Shutter Angle: 180

## Steps to Reproduce
1. Bring the clip into the Fusion page
2. Add a Motion Blur node after the MediaIn node
3. Increase the 'Amount' parameter to create the blur
4. Change the Filter-Type to 'Zoom' to create the radial stretching effect
5. Adjust the 'Length' to match the speed of the movement
6. Send the clip to the Fusion page
7. Add a Transform node connected to MediaIn
8. Keyframe the Scale parameter to create a fast zoom-in effect
9. Go to the Motion Blur tab in the Transform node
10. Enable Motion Blur
11. Adjust the Shutter Angle and Quality to match the speed of the zoom

## Difficulty
intermediate

## Tags
dreamy, fusion, motion-blur, vfx, zoom, zoom-blur
