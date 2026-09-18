---
name: davinci-text-behind-subject-depth-masking
description: DaVinci Resolve technique: Text Behind Subject (Depth Masking) from Instagram Reel C_x0IZRODYf
category: creative/davinci-resolve-techniques
tags: ["vfx", "text-effect", "masking", "fusion", "davinci-resolve", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "C_x0IZRODYf"
collection: "DaVinci_Tricks"
resolve_page: "Fusion"
node_graph: "serial"
difficulty: "intermediate"
created: 2026-07-30
---

# Text Behind Subject (Depth Masking)

**Source:** Instagram Reel `C_x0IZRODYf` (DaVinci_Tricks)  
**Page:** Fusion | **Graph:** serial | **Difficulty:** intermediate

![Text Behind Subject (Depth Masking)](C_x0IZRODYf.gif)

## Node Graph Structure

- Text+
- Alpha Output
- Magic Mask

## Parameters

- **font_style**: Bold Serif
- **tracking**: wide
- **mask_softness**: low-to-medium

## Steps to Reproduce in DaVinci Resolve

1. Import the clip to the Fusion page.
2. Add a Text+ node and type the desired text (GLOW TEXT EFFECT).
3. Use the Magic Mask tool or a manual Polygon mask to select the subject (the person).
4. Connect the mask to the Alpha channel of the Text+ node.
5. Adjust the text position so the subject overlaps with the letters.
6. Merge the masked text over the original background footage.

## Tags
`vfx`, `text-effect`, `masking`, `fusion`, `davinci-resolve`
