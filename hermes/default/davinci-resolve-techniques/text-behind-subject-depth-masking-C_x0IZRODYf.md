---
name: text-behind-subject-depth-masking
description: 'DaVinci Resolve technique: Text Behind Subject (Depth Masking) from
  Instagram Reel C_x0IZRODYf'
category: davinci-resolve
tags:
- vfx
- text-effect
- masking
- fusion
- davinci-resolve
- fusion
- intermediate
version: 1.0.0
source_reel_id: C_x0IZRODYf
resolve_page: Fusion
node_graph_type: serial
key_nodes:
- Text+
- Alpha Output
- Magic Mask
parameters:
  font_style: Bold Serif
  tracking: wide
  mask_softness: low-to-medium
steps_to_reproduce:
- Import the clip to the Fusion page.
- Add a Text+ node and type the desired text (GLOW TEXT EFFECT).
- Use the Magic Mask tool or a manual Polygon mask to select the subject (the person).
- Connect the mask to the Alpha channel of the Text+ node.
- Adjust the text position so the subject overlaps with the letters.
- Merge the masked text over the original background footage.
difficulty: intermediate
---
# Text Behind Subject (Depth Masking)

**Source Reel:** C_x0IZRODYf
**Resolve Page:** Fusion
**Node Graph Type:** serial
**Difficulty:** intermediate

## Description
DaVinci Resolve technique extracted from Instagram Reel C_x0IZRODYf.

## Key Nodes
- Text+
- Alpha Output
- Magic Mask

## Parameters
font_style: Bold Serif
tracking: wide
mask_softness: low-to-medium


## Steps to Reproduce
1. Import the clip to the Fusion page.
2. Add a Text+ node and type the desired text (GLOW TEXT EFFECT).
3. Use the Magic Mask tool or a manual Polygon mask to select the subject (the person).
4. Connect the mask to the Alpha channel of the Text+ node.
5. Adjust the text position so the subject overlaps with the letters.
6. Merge the masked text over the original background footage.

## Tags
vfx, text-effect, masking, fusion, davinci-resolve
