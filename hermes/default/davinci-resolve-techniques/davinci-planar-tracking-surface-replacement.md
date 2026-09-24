---
name: davinci-planar-tracking-surface-replacement
description: DaVinci Resolve technique: Planar Tracking Surface Replacement from Instagram Reel C_2yqxxIcfV
category: creative/davinci-resolve-techniques
tags: ["tracking", "motion-graphics", "fusion", "vfx", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "C_2yqxxIcfV"
collection: "Gimbal_Moves"
resolve_page: "Fusion"
node_graph: "serial"
difficulty: "intermediate"
created: 2026-07-30
---

# Planar Tracking Surface Replacement

**Source:** Instagram Reel `C_2yqxxIcfV` (Gimbal_Moves)  
**Page:** Fusion | **Graph:** serial | **Difficulty:** intermediate

![Planar Tracking Surface Replacement](C_2yqxxIcfV.gif)

## Node Graph Structure

- MediaIn
- Planar
- Merge
- MediaOut

## Parameters

- **Tracker Mode**: Planar
- **Operation**: Surface
- **Path Type**: Best Fit Plan

## Steps to Reproduce in DaVinci Resolve

1. Add the clip to the Fusion page
2. Add a Planar Tracker node and connect the MediaIn
3. Draw a mask around the surface to be tracked (e.g., the wall)
4. Click Track Forward to analyze the motion
5. Change Operation to Surface
6. Create Text or Image nodes
7. Connect the text/image to the Planar Tracker output via a Merge node
8. Adjust transform to align the graphic with the tracked surface

## Tags
`tracking`, `motion-graphics`, `fusion`, `vfx`
