---
name: davinci-vertical-mask-split-transition-overlay-reveal
description: DaVinci Resolve technique: Vertical Mask Split Transition / Overlay Reveal from Instagram Reel CzWN95iNG0a
category: creative/davinci-resolve-techniques
tags: ["transition", "masking", "fusion", "split-screen", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "CzWN95iNG0a"
collection: "Gimbal_Moves"
resolve_page: "Fusion"
node_graph: "serial"
difficulty: "beginner"
created: 2026-07-30
---

# Vertical Mask Split Transition / Overlay Reveal

**Source:** Instagram Reel `CzWN95iNG0a` (Gimbal_Moves)  
**Page:** Fusion | **Graph:** serial | **Difficulty:** beginner

![Vertical Mask Split Transition / Overlay Reveal](CzWN95iNG0a.gif)

## Node Graph Structure

- MediaIn1
- MediaIn2
- Merge
- Mask

## Parameters

- **SoftEdge**: 0.05
- **Hardness**: 0.0
- **Center**: Y-axis animation

## Steps to Reproduce in DaVinci Resolve

1. Bring both clips into the Fusion page
2. Add a Merge node and connect the top clip as the foreground and bottom clip as the background
3. Add a Rectangle or Polygon mask node
4. Connect the mask node to the mask input of the Merge node
5. Adjust the mask size and position to cover exactly half the screen
6. Animate the Center Y position of the mask over time to slide one clip over the other
7. Increase Soft Edge to blend the transition between the two shots

## Tags
`transition`, `masking`, `fusion`, `split-screen`
