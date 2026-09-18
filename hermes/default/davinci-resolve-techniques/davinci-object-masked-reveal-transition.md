---
name: davinci-object-masked-reveal-transition
description: DaVinci Resolve technique: Object Masked Reveal Transition from Instagram Reel C6hVsRapY0k
category: creative/davinci-resolve-techniques
tags: ["transition", "masking", "tracking", "reveal", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "C6hVsRapY0k"
collection: "Gimbal_Moves"
resolve_page: "Fusion"
node_graph: "serial"
difficulty: "intermediate"
created: 2026-07-30
---

# Object Masked Reveal Transition

**Source:** Instagram Reel `C6hVsRapY0k` (Gimbal_Moves)  
**Page:** Fusion | **Graph:** serial | **Difficulty:** intermediate

![Object Masked Reveal Transition](C6hVsRapY0k.gif)

## Node Graph Structure

- MediaIn1
- MediaIn2
- MaskPaint
- Merge

## Parameters

- **mask_mode**: In
- **softness**: 0.05
- **tracking_type**: planar

## Steps to Reproduce in DaVinci Resolve

1. Import the two clips into the Fusion page
2. Add a MaskPaint node to the first clip and draw a mask around the subject or the window frame
3. Use the Tracker node to follow the movement of the person or the glass edge
4. Connect the second clip to the foreground input of a Merge node
5. Adjust the mask feather to ensure a smooth blend between the two clips as the subject moves

## Tags
`transition`, `masking`, `tracking`, `reveal`
