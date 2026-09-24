---
name: Planar Tracking Surface Replacement
description: DaVinci Resolve technique from Instagram Reel C_2yqxxIcfV
trigger: "planar tracking surface replacement"
page: Fusion
difficulty: intermediate
tags: ['tracking', 'motion-graphics', 'fusion', 'vfx']
video_id: C_2yqxxIcfV
source: instagram-reel
updated: 2026-07-28T19:44:36.058468
---

# Planar Tracking Surface Replacement

**Source:** Instagram Reel `C_2yqxxIcfV`  
**Resolve Page:** Fusion  
**Difficulty:** intermediate  
**Node Graph Type:** serial

## Key Nodes
- MediaIn
- Planar
- Merge
- MediaOut

## Parameters
- **Tracker Mode:** Planar
- **Operation:** Surface
- **Path Type:** Best Fit Plan

## Steps to Reproduce
1. Add the clip to the Fusion page
2. Add a Planar Tracker node and connect the MediaIn
3. Draw a mask around the surface to be tracked (e.g., the wall)
4. Click Track Forward to analyze the motion
5. Change Operation to Surface
6. Create Text or Image nodes
7. Connect the text/image to the Planar Tracker output via a Merge node
8. Adjust transform to align the graphic with the tracked surface

## Tags
- #tracking
- #motion-graphics
- #fusion
- #vfx
