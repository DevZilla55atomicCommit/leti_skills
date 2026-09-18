---
name: davinci-digital-zoom-with-radial-motion-blur
description: DaVinci Resolve technique: Digital Zoom with Radial Motion Blur from Instagram Reel C5TkCbEo8UX
category: creative/davinci-resolve-techniques
tags: ["motion-blur", "zoom", "fusion", "vfx", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "C5TkCbEo8UX"
collection: "Export_Videos"
resolve_page: "Fusion"
node_graph: "serial"
difficulty: "intermediate"
created: 2026-07-30
---

# Digital Zoom with Radial Motion Blur

**Source:** Instagram Reel `C5TkCbEo8UX` (Export_Videos)  
**Page:** Fusion | **Graph:** serial | **Difficulty:** intermediate

![Digital Zoom with Radial Motion Blur](C5TkCbEo8UX.gif)

## Node Graph Structure

- MediaIn
- Transform
- Motion Blur

## Parameters

- **Transform Scale**: Keyframed animation
- **Motion Blur**: Enabled
- **Quality**: High
- **Shutter Angle**: 180

## Steps to Reproduce in DaVinci Resolve

1. Send the clip to the Fusion page
2. Add a Transform node connected to MediaIn
3. Keyframe the Scale parameter to create a fast zoom-in effect
4. Go to the Motion Blur tab in the Transform node
5. Enable Motion Blur
6. Adjust the Shutter Angle and Quality to match the speed of the zoom

## Tags
`motion-blur`, `zoom`, `fusion`, `vfx`
