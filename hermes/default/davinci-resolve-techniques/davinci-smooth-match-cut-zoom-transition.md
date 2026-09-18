---
name: davinci-smooth-match-cut-zoom-transition
description: DaVinci Resolve technique: Smooth Match Cut Zoom Transition from Instagram Reel C4ltswrJWkC
category: creative/davinci-resolve-techniques
tags: ["transition", "zoom", "architecture", "smooth", "fusion", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "C4ltswrJWkC"
collection: "Gimbal_Moves"
resolve_page: "Fusion"
node_graph: "serial"
difficulty: "intermediate"
created: 2026-07-30
---

# Smooth Match Cut Zoom Transition

**Source:** Instagram Reel `C4ltswrJWkC` (Gimbal_Moves)  
**Page:** Fusion | **Graph:** serial | **Difficulty:** intermediate

![Smooth Match Cut Zoom Transition](C4ltswrJWkC.gif)

## Node Graph Structure

- MediaIn
- Transform
- Merge
- MediaOut

## Parameters

- **Zoom**: Keyframed scale increase
- **Center**: Keyframed position adjustment
- **Motion Blur**: Enabled (high quality)

## Steps to Reproduce in DaVinci Resolve

1. Import clips into the timeline and place them back-to-back
2. Send clips to Fusion page
3. Add a Transform node after each MediaIn
4. Keyframe the Zoom and Center parameters at the start of the first clip and end of the second
5. Create a rapid zoom-in effect at the cut point to match the composition or focal points
6. Increase Motion Blur on the Transform nodes to hide the cut
7. Apply a mask to the overlapping area to isolate specific architectural elements if needed

## Tags
`transition`, `zoom`, `architecture`, `smooth`, `fusion`
