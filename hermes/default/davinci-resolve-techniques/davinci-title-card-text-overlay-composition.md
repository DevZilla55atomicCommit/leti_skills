---
name: davinci-title-card-text-overlay-composition
description: DaVinci Resolve technique: Title Card / Text Overlay Composition from Instagram Reel C4tHjI-gutX
category: creative/davinci-resolve-techniques
tags: [, "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "C4tHjI-gutX"
collection: "Gimbal_Moves"
resolve_page: "Fusion"
node_graph: "parallel"
difficulty: "beginner"
created: 2026-07-30
---

# Title Card / Text Overlay Composition

**Source:** Instagram Reel `C4tHjI-gutX` (Gimbal_Moves)  
**Page:** Fusion | **Graph:** parallel | **Difficulty:** beginner

![Title Card / Text Overlay Composition](C4tHjI-gutX.gif)

## Node Graph Structure

- Video Clip Node (Input)
- Text/Shape Layer Node (Overlay)

## Parameters

- **opacity**: 0.95
- **position_x**: 0.5
- **position_y**: 0.48
- **scale**: 1.2
- **color_balance**: [{'channel': 'R', 'value': 255}, {'channel': 'G', 'value': 255}, {'channel': 'B', 'value': 255}]

## Steps to Reproduce in DaVinci Resolve

1. Import the video footage into a Fusion composition.
2. Add an Image node or Text node to create the large number '3'.
3. Position and scale the text layer so it covers most of the frame (centered).
4. Set the opacity slightly below 100% if desired for transparency effects, otherwise keep at standard levels.
5. Connect the Video Clip as an input to a Merge node or use the composition stack order.

## Tags

