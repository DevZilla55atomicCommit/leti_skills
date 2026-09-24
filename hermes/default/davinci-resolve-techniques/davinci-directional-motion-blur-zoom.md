---
name: davinci-directional-motion-blur-zoom
description: DaVinci Resolve technique: Directional Motion Blur Zoom from Instagram Reel DAEAlmSMV02
category: creative/davinci-resolve-techniques
tags: ["motion-blur", "cinematic", "fusion", "speed-ramp", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "DAEAlmSMV02"
collection: "Ideas_for_Shooting_Videos"
resolve_page: "Fusion"
node_graph: "serial"
difficulty: "beginner"
created: 2026-07-30
---

# Directional Motion Blur Zoom

**Source:** Instagram Reel `DAEAlmSMV02` (Ideas_for_Shooting_Videos)  
**Page:** Fusion | **Graph:** serial | **Difficulty:** beginner

![Directional Motion Blur Zoom](DAEAlmSMV02.gif)

## Node Graph Structure

- MediaIn
- Motion Blur
- MediaOut

## Parameters

- **Quality**: 10
- **Length**: 16
- **Shutter Angle**: 180
- **Angle**: 90.0

## Steps to Reproduce in DaVinci Resolve

1. Import the clip into the Fusion page.
2. Add a Transform node after the MediaIn node.
3. Rotate the image by 90 degrees to fix the orientation.
4. Go to the Motion Blur tab in the Transform node.
5. Enable Motion Blur.
6. Set the 'Type' to 'Directional' or use Zoom keyframes to create movement.
7. Adjust the 'Shutter Angle' and 'Length' to increase the intensity of the blur streak.

## Tags
`motion-blur`, `cinematic`, `fusion`, `speed-ramp`
