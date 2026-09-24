---
name: davinci-object-masking-and-background-replacement
description: DaVinci Resolve technique: Object Masking and Background Replacement from Instagram Reel DK1rDDlsQoL
category: creative/davinci-resolve-techniques
tags: ["rotoscoping", "masking", "visual-effects", "fusion", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "DK1rDDlsQoL"
collection: "Ideas_for_Shooting_Videos"
resolve_page: "Fusion"
node_graph: "serial"
difficulty: "intermediate"
created: 2026-07-30
---

# Object Masking and Background Replacement

**Source:** Instagram Reel `DK1rDDlsQoL` (Ideas_for_Shooting_Videos)  
**Page:** Fusion | **Graph:** serial | **Difficulty:** intermediate

![Object Masking and Background Replacement](DK1rDDlsQoL.gif)

## Node Graph Structure

- MediaIn1
- DeltaMask1
- Merge1

## Parameters

- **mask_type**: Magic Mask or Manual Path
- **blend_mode**: over

## Steps to Reproduce in DaVinci Resolve

1. Import footage into the Fusion page
2. Use the Magic Mask tool or draw a Polygon mask to isolate the person
3. Connect the mask to the blue input of a Merge node
4. Place the background layer or effect on the yellow input of the Merge node
5. Adjust softness and feather for a natural blend

## Tags
`rotoscoping`, `masking`, `visual-effects`, `fusion`
