---
name: davinci-object-removal-via-patch-replacement-and-mask
description: DaVinci Resolve technique: Object Removal via Patch Replacement and Mask from Instagram Reel C4XYlhONXpF
category: creative/davinci-resolve-techniques
tags: ["vfx", "object-removal", "cleanplate", "masking", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "C4XYlhONXpF"
collection: "Gimbal_Moves"
resolve_page: "Color"
node_graph: "serial"
difficulty: "intermediate"
created: 2026-07-30
---

# Object Removal via Patch Replacement and Mask

**Source:** Instagram Reel `C4XYlhONXpF` (Gimbal_Moves)  
**Page:** Color | **Graph:** serial | **Difficulty:** intermediate

![Object Removal via Patch Replacement and Mask](C4XYlhONXpF.gif)

## Node Graph Structure

- Object Removal
- Power Mask
- Patch Tool

## Parameters

- **Analysis Mode**: Clean Plate
- **Mask Softness**: 0.05
- **Tracking**: Frame-based tracking

## Steps to Reproduce in DaVinci Resolve

1. Import clip to the Color page.
2. Create a new node and draw a Power Mask around the object to be removed (the cameraman).
3. Track the mask throughout the clip to follow the movement.
4. Use the Patch Tool to select a clean area of the background (trees/pillars) to cover the object.
5. Alternatively, use the Object Removal effect in the Fusion page for automated AI-based fill.
6. Adjust mask softness and transparency to blend the patch seamlessly with the environment.

## Tags
`vfx`, `object-removal`, `cleanplate`, `masking`
