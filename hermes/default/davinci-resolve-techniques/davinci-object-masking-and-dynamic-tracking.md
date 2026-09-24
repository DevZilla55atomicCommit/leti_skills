---
name: davinci-object-masking-and-dynamic-tracking
description: DaVinci Resolve technique: Object Masking and Dynamic Tracking from Instagram Reel C3izajXxsuO
category: creative/davinci-resolve-techniques
tags: ["masking", "tracking", "motion-graphics", "fusion", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "C3izajXxsuO"
collection: "Gimbal_Moves"
resolve_page: "Fusion"
node_graph: "serial"
difficulty: "intermediate"
created: 2026-07-30
---

# Object Masking and Dynamic Tracking

**Source:** Instagram Reel `C3izajXxsuO` (Gimbal_Moves)  
**Page:** Fusion | **Graph:** serial | **Difficulty:** intermediate

![Object Masking and Dynamic Tracking](C3izajXxsuO.gif)

## Node Graph Structure

- MediaIn
- MaskPaint
- Tracker
- Merge

## Parameters

- **mask_type**: Bine
- **tracking_mode**: Planar
- **blend_mode**: Over

## Steps to Reproduce in DaVinci Resolve

1. Import clip into the Fusion page
2. Add a MaskPaint node and draw a mask around the specific object or area
3. Apply a Planar Tracker to the mask to follow the movement of the scene
4. Add a Text+ node or MediaIn node for the overlay element
5. Use a Merge node to layer the text/element behind the masked area
6. Adjust the soft edge of the mask to ensure seamless integration

## Tags
`masking`, `tracking`, `motion-graphics`, `fusion`
