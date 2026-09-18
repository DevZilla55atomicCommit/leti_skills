---
name: Masked Text Behind Object (Depth Effect)
description: DaVinci Resolve technique from Instagram Reel C_S1u6CoqxB
trigger: "masked text behind object (depth effect)"
page: Fusion
difficulty: intermediate
tags: ['fusion', 'masking', 'text-effect', '3d-depth']
video_id: C_S1u6CoqxB
source: instagram-reel
updated: 2026-07-28T16:37:11.310445
---

# Masked Text Behind Object (Depth Effect)

**Source:** Instagram Reel `C_S1u6CoqxB`  
**Resolve Page:** Fusion  
**Difficulty:** intermediate  
**Node Graph Type:** serial

## Key Nodes
- Background
- TextPlus
- Merge
- Mask

## Parameters
- **TextColor:** White
- **FontWeight:** Bold
- **MergeMode:** Alpha

## Steps to Reproduce
1. Import footage into the Fusion page
2. Add a TextPlus node and type the desired text
3. Connect TextPlus to the foreground input of a Merge node
4. Add a Polygon mask to the Fusion node
5. Connect the Polygon mask to the mask input of the TextPlus node
6. Draw the mask around the parts of the cliff that should be in front of the text
7. Adjust the mask boundaries to ensure the text appears behind the cliff edge

## Tags
- #fusion
- #masking
- #text-effect
- #3d-depth
