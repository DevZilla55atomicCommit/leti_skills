---
name: davinci-vertical-split-screen-with-title-overlay
description: DaVinci Resolve technique: Vertical Split-Screen with Title Overlay from Instagram Reel Cv4GQ5btHk8
category: creative/davinci-resolve-techniques
tags: ["split-screen", "layout", "social media", "overlay", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "Cv4GQ5btHk8"
collection: "Gimbal_Moves"
resolve_page: "Edit"
node_graph: "serial"
difficulty: "beginner"
created: 2026-07-30
---

# Vertical Split-Screen with Title Overlay

**Source:** Instagram Reel `Cv4GQ5btHk8` (Gimbal_Moves)  
**Page:** Edit | **Graph:** serial | **Difficulty:** beginner

![Vertical Split-Screen with Title Overlay](Cv4GQ5btHk8.gif)

## Node Graph Structure

- Video Clip 1
- Video Clip 2
- Text+

## Parameters

- **Crop Top**: 50%
- **Transform Y**: 0.5
- **Background Opacity**: 0.5

## Steps to Reproduce in DaVinci Resolve

1. Place the two video clips on separate video tracks (one above the other).
2. Select the top clip and use the Inspector to crop the bottom 50% or adjust Transform position.
3. Select the bottom clip and adjust the Transform Y position to fill the top half of the frame.
4. Add a Text+ title on a track above the video clips.
5. Create a background rectangle or use the Text background settings to create the semi-transparent bar.
6. Position the text in the center of the screen.

## Tags
`split-screen`, `layout`, `social media`, `overlay`
