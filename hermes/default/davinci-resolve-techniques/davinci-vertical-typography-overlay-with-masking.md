---
name: davinci-vertical-typography-overlay-with-masking
description: DaVinci Resolve technique: Vertical Typography Overlay with Masking from Instagram Reel DFff74zPJpq
category: creative/davinci-resolve-techniques
tags: ["typography", "minimalist", "travel-video", "overlay", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "DFff74zPJpq"
collection: "Ideas_for_Shooting_Videos"
resolve_page: "Fusion"
node_graph: "serial"
difficulty: "beginner"
created: 2026-07-30
---

# Vertical Typography Overlay with Masking

**Source:** Instagram Reel `DFff74zPJpq` (Ideas_for_Shooting_Videos)  
**Page:** Fusion | **Graph:** serial | **Difficulty:** beginner

![Vertical Typography Overlay with Masking](DFff74zPJpq.gif)

## Node Graph Structure

- MediaIn
- Text+
- Merge

## Parameters

- **Font**: Sans-Serif
- **Tracking**: 1.5
- **Opacity**: 0.8
- **Rotation**: 90

## Steps to Reproduce in DaVinci Resolve

1. Import the clip into the Fusion page.
2. Add a Text+ node and type 'THE ART OF TRAVEL'.
3. Rotate the text layer 90 degrees to align with the vertical composition.
4. Use a Merge node to layer the text over the MediaIn.
5. Apply a Mask node to the Merge node if the text needs to appear behind specific rock formations.
6. Adjust tracking and letter spacing to achieve the minimalist travel-film aesthetic.

## Tags
`typography`, `minimalist`, `travel-video`, `overlay`
