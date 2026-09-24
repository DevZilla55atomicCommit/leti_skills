---
name: davinci-object-masking-and-compositing
description: DaVinci Resolve technique: Object Masking and Compositing from Instagram Reel Cz77791LlsG
category: creative/davinci-resolve-techniques
tags: ["masking", "compositing", "vfx", "rotoscoping", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "Cz77791LlsG"
collection: "Gimbal_Moves"
resolve_page: "Fusion"
node_graph: "layer"
difficulty: "intermediate"
created: 2026-07-30
---

# Object Masking and Compositing

**Source:** Instagram Reel `Cz77791LlsG` (Gimbal_Moves)  
**Page:** Fusion | **Graph:** layer | **Difficulty:** intermediate

![Object Masking and Compositing](Cz77791LlsG.gif)

## Node Graph Structure

- MediaIn1
- MediaIn2
- Merge
- PolygonMask

## Parameters

- **BlendMode**: Normal
- **SoftEdge**: 0.01

## Steps to Reproduce in DaVinci Resolve

1. Place both the background clip and the subject clip on the Fusion timeline
2. Connect the background clip to the background input of a Merge node
3. Connect the subject clip to the foreground input of the Merge node
4. Add a Polygon Mask to the subject clip node
5. Draw the mask around the person, keyframing to account for movement
6. Adjust the Soft Edge of the mask to blend the edges naturally
7. Refine the mask where the person overlaps with occlusions like tree trunks

## Tags
`masking`, `compositing`, `vfx`, `rotoscoping`
