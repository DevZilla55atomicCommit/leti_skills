---
name: davinci-text-behind-subject-masking-overlay
description: DaVinci Resolve technique: Text Behind Subject (Masking Overlay) from Instagram Reel C-Nty_eP-Rk
category: creative/davinci-resolve-techniques
tags: ["masking", "text effect", "motion tracking", "compositing", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "C-Nty_eP-Rk"
collection: "DaVinci_Tricks"
resolve_page: "Edit"
node_graph: "serial"
difficulty: "intermediate"
created: 2026-07-30
---

# Text Behind Subject (Masking Overlay)

**Source:** Instagram Reel `C-Nty_eP-Rk` (DaVinci_Tricks)  
**Page:** Edit | **Graph:** serial | **Difficulty:** intermediate

![Text Behind Subject (Masking Overlay)](C-Nty_eP-Rk.gif)

## Node Graph Structure

- Background Clip
- Duplicate Clip
- Text+

## Parameters

- **mask_method**: Power Window or Magic Mask
- **feathering**: Soft
- **blend_mode**: Normal

## Steps to Reproduce in DaVinci Resolve

1. Place your video clip on the timeline.
2. Duplicate the clip (Alt+Drag) to create a second layer directly above.
3. Add a Text+ title on a layer between the two video clips.
4. Select the top video clip and go to Color page.
5. Use the Power Window or Magic Mask to isolate the subject.
6. Track the mask across the clip to follow the movement.
7. Adjust the text layer position so it appears behind the masked subject.

## Tags
`masking`, `text effect`, `motion tracking`, `compositing`
