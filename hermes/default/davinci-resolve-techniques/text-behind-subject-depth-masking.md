---
name: Text Behind Subject (Depth Masking)
description: DaVinci Resolve technique from Instagram Reel C_x0IZRODYf
trigger: "text behind subject (depth masking)"
page: Fusion
difficulty: intermediate
tags: ['vfx', 'text-effect', 'masking', 'fusion', 'davinci-resolve']
video_id: C_x0IZRODYf
source: instagram-reel
updated: 2026-07-27T09:56:33.251041
---

# Text Behind Subject (Depth Masking)

**Source:** Instagram Reel `C_x0IZRODYf`  
**Resolve Page:** Fusion  
**Difficulty:** intermediate  
**Node Graph Type:** serial

## Key Nodes
- Text+
- Alpha Output
- Magic Mask

## Parameters
- **font_style:** Bold Serif
- **tracking:** wide
- **mask_softness:** low-to-medium

## Steps to Reproduce
1. Import the clip to the Fusion page.
2. Add a Text+ node and type the desired text (GLOW TEXT EFFECT).
3. Use the Magic Mask tool or a manual Polygon mask to select the subject (the person).
4. Connect the mask to the Alpha channel of the Text+ node.
5. Adjust the text position so the subject overlaps with the letters.
6. Merge the masked text over the original background footage.

## Tags
- #vfx
- #text-effect
- #masking
- #fusion
- #davinci-resolve
