---
name: masked-text-behind-object-depth-effect-C_S1u6CoqxB
description: Masked Text Behind Object (Depth Effect) - DaVinci Resolve technique
  from Instagram Reel C_S1u6CoqxB
category: davinci-resolve
tags:
- fusion
- masking
- text-effect
- 3d-depth
resolve_page: Fusion
node_graph_type: serial
difficulty: intermediate
key_nodes:
- Background
- TextPlus
- Merge
- Mask
parameters:
  TextColor: White
  FontWeight: Bold
  MergeMode: Alpha
steps_to_reproduce:
- Import footage into the Fusion page
- Add a TextPlus node and type the desired text
- Connect TextPlus to the foreground input of a Merge node
- Add a Polygon mask to the Fusion node
- Connect the Polygon mask to the mask input of the TextPlus node
- Draw the mask around the parts of the cliff that should be in front of the text
- Adjust the mask boundaries to ensure the text appears behind the cliff edge
source_reel_id: C_S1u6CoqxB
---
# Masked Text Behind Object (Depth Effect)

**Source Reel:** C_S1u6CoqxB
**Resolve Page:** Fusion
**Node Graph Type:** serial
**Difficulty:** intermediate

## Description
DaVinci Resolve technique extracted from Instagram Reel C_S1u6CoqxB.

## Key Nodes
- Background
- TextPlus
- Merge
- Mask

## Parameters
TextColor: White
FontWeight: Bold
MergeMode: Alpha


## Steps to Reproduce
1. Import footage into the Fusion page
2. Add a TextPlus node and type the desired text
3. Connect TextPlus to the foreground input of a Merge node
4. Add a Polygon mask to the Fusion node
5. Connect the Polygon mask to the mask input of the TextPlus node
6. Draw the mask around the parts of the cliff that should be in front of the text
7. Adjust the mask boundaries to ensure the text appears behind the cliff edge

## Tags
fusion, masking, text-effect, 3d-depth
