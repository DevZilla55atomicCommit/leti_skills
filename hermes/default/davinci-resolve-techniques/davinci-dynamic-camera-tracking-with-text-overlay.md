---
name: davinci-dynamic-camera-tracking-with-text-overlay
description: DaVinci Resolve technique: Dynamic Camera Tracking with Text Overlay from Instagram Reel C2f70-HJ2VS
category: creative/davinci-resolve-techniques
tags: ["motion-graphics", "tracking", "cinematography", "fusion", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "C2f70-HJ2VS"
collection: "Gimbal_Moves"
resolve_page: "Fusion"
node_graph: "serial"
difficulty: "intermediate"
created: 2026-07-30
---

# Dynamic Camera Tracking with Text Overlay

**Source:** Instagram Reel `C2f70-HJ2VS` (Gimbal_Moves)  
**Page:** Fusion | **Graph:** serial | **Difficulty:** intermediate

![Dynamic Camera Tracking with Text Overlay](C2f70-HJ2VS.gif)

## Node Graph Structure

- MediaIn
- Tracker
- TextPlus

## Parameters

- **tracking_mode**: Planar
- **text_alignment**: Center
- **blend_mode**: Normal Light

## Steps to Reproduce in DaVinci Resolve

1. Import the clip into the Fusion page
2. Add a Planar Tracker and select a stable area on the subject or background
3. Perform the track operation to capture the camera movement
4. Add a TextPlus node and type THE MOVE
5. Connect the Tracker output to the TextPlus node transform to pin the text to the scene
6. Adjust text position and opacity to match the aesthetic

## Tags
`motion-graphics`, `tracking`, `cinematography`, `fusion`
