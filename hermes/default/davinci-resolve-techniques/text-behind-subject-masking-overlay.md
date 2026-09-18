---
name: Text Behind Subject (Masking Overlay)
description: DaVinci Resolve technique from Instagram Reel C-Nty_eP-Rk
trigger: "text behind subject (masking overlay)"
page: Edit
difficulty: intermediate
tags: ['masking', 'text effect', 'motion tracking', 'compositing']
video_id: C-Nty_eP-Rk
source: instagram-reel
updated: 2026-07-28T11:17:19.721459
---

# Text Behind Subject (Masking Overlay)

**Source:** Instagram Reel `C-Nty_eP-Rk`  
**Resolve Page:** Edit  
**Difficulty:** intermediate  
**Node Graph Type:** serial

## Key Nodes
- Background Clip
- Duplicate Clip
- Text+

## Parameters
- **mask_method:** Power Window or Magic Mask
- **feathering:** Soft
- **blend_mode:** Normal

## Steps to Reproduce
1. Place your video clip on the timeline.
2. Duplicate the clip (Alt+Drag) to create a second layer directly above.
3. Add a Text+ title on a layer between the two video clips.
4. Select the top video clip and go to Color page.
5. Use the Power Window or Magic Mask to isolate the subject.
6. Track the mask across the clip to follow the movement.
7. Adjust the text layer position so it appears behind the masked subject.

## Tags
- #masking
- #text effect
- #motion tracking
- #compositing
