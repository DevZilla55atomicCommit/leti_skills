---
name: davinci-masked-text-behind-object-depth-effect
description: DaVinci Resolve technique: Masked Text Behind Object (Depth Effect) from Instagram Reel C_S1u6CoqxB
category: creative/davinci-resolve-techniques
tags: ["fusion", "masking", "text-effect", "3d-depth", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "C_S1u6CoqxB"
collection: "Export_Videos"
resolve_page: "Fusion"
node_graph: "serial"
difficulty: "intermediate"
created: 2026-07-30
---

# Masked Text Behind Object (Depth Effect)

**Source:** Instagram Reel `C_S1u6CoqxB` (Export_Videos)  
**Page:** Fusion | **Graph:** serial | **Difficulty:** intermediate

![Masked Text Behind Object (Depth Effect)](C_S1u6CoqxB.gif)

## Node Graph Structure

- Background
- TextPlus
- Merge
- Mask

## Parameters

- **TextColor**: White
- **FontWeight**: Bold
- **MergeMode**: Alpha

## Steps to Reproduce in DaVinci Resolve

1. Import footage into the Fusion page
2. Add a TextPlus node and type the desired text
3. Connect TextPlus to the foreground input of a Merge node
4. Add a Polygon mask to the Fusion node
5. Connect the Polygon mask to the mask input of the TextPlus node
6. Draw the mask around the parts of the cliff that should be in front of the text
7. Adjust the mask boundaries to ensure the text appears behind the cliff edge

## Tags
`fusion`, `masking`, `text-effect`, `3d-depth`
