---
name: davinci-object-tracking-with-planar-tracker
description: DaVinci Resolve technique: Object Tracking with Planar Tracker from Instagram Reel C28PzU5pUSf
category: creative/davinci-resolve-techniques
tags: ["tracking", "vfx", "fusion", "motion-graphics", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "C28PzU5pUSf"
collection: "Gimbal_Moves"
resolve_page: "Fusion"
node_graph: "serial"
difficulty: "intermediate"
created: 2026-07-30
---

# Object Tracking with Planar Tracker

**Source:** Instagram Reel `C28PzU5pUSf` (Gimbal_Moves)  
**Page:** Fusion | **Graph:** serial | **Difficulty:** intermediate

![Object Tracking with Planar Tracker](C28PzU5pUSf.gif)

## Node Graph Structure

- MediaIn
- PlanarTracker
- Text+
- Merge

## Parameters

- **tracker_type**: Planar
- **operation**: None
- **tracking_mode**: Surface

## Steps to Reproduce in DaVinci Resolve

1. Bring clip into the Fusion page
2. Add a Planar Tracker node and connect to MediaIn
3. Draw a mask around the object to be tracked
4. In the Inspector, set Operation to Track and click Track Forward
5. Change Operation back to None or use Create Transform to apply tracking data
6. Connect a Text+ node to the Merge node foreground input
7. Position the text over the tracked area

## Tags
`tracking`, `vfx`, `fusion`, `motion-graphics`
