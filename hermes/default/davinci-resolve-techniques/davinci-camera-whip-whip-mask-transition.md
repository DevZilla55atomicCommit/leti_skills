---
name: davinci-camera-whip-whip-mask-transition
description: DaVinci Resolve technique: Camera Whip Whip Mask Transition from Instagram Reel C0JFX1Prqcv
category: creative/davinci-resolve-techniques
tags: ["transition", "whip pan", "cinematic", "masking", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "C0JFX1Prqcv"
collection: "Gimbal_Moves"
resolve_page: "Edit"
node_graph: "serial"
difficulty: "intermediate"
created: 2026-07-30
---

# Camera Whip Whip Mask Transition

**Source:** Instagram Reel `C0JFX1Prqcv` (Gimbal_Moves)  
**Page:** Edit | **Graph:** serial | **Difficulty:** intermediate

![Camera Whip Whip Mask Transition](C0JFX1Prqcv.gif)

## Node Graph Structure

- Clip A
- Clip B
- Adjustment Layer

## Parameters

- **Transition Speed**: Linear
- **Mask Softness**: Medium
- **Keyframes**: Manual

## Steps to Reproduce in DaVinci Resolve

1. Place Clip A (the bedroom shot) and Clip B (the new location) on the timeline.
2. Ensure both clips have a fast camera whip or movement in the same direction.
3. Cut Clip A at the peak of the motion blur.
4. Add a Fusion Composition or use an Adjustment Layer over the cut.
5. Create a mask to follow the edge of the object or camera movement.
6. Animate the mask path to reveal Clip B as the whip completes.
7. Apply a Motion Blur effect to the transition point to hide the seam.

## Tags
`transition`, `whip pan`, `cinematic`, `masking`
