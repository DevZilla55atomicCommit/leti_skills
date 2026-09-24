---
name: davinci-mask-based-object-insertion
description: DaVinci Resolve technique: Mask-Based Object Insertion from Instagram Reel Cx3FCzYSD4W
category: creative/davinci-resolve-techniques
tags: ["masking", "compositing", "fusion", "vfx", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "Cx3FCzYSD4W"
collection: "Gimbal_Moves"
resolve_page: "Fusion"
node_graph: "serial"
difficulty: "intermediate"
created: 2026-07-30
---

# Mask-Based Object Insertion

**Source:** Instagram Reel `Cx3FCzYSD4W` (Gimbal_Moves)  
**Page:** Fusion | **Graph:** serial | **Difficulty:** intermediate

![Mask-Based Object Insertion](Cx3FCzYSD4W.gif)

## Node Graph Structure

- MediaIn1
- MediaIn2
- Merge
- PolygonMask

## Parameters

- **Mode**: Normal
- **Soft Edge**: 0.01
- **Tracking**: Planar

## Steps to Reproduce in DaVinci Resolve

1. Import both the background house clip and the foreground person clip into the Edit page.
2. Place the person clip on the track above the house clip.
3. Select both clips and Open in Fusion.
4. Add a Merge node to connect the person clip to the background.
5. Add a Polygon Mask to the person node and draw an outline around the person.
6. Keyframe the mask path to match the person movement if they are moving.
7. Adjust the Soft Edge of the mask to blend the edges with the background.

## Tags
`masking`, `compositing`, `fusion`, `vfx`
