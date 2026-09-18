---
name: text-behind-subject-(masking-overlay)
description: 'DaVinci Resolve technique: Text Behind Subject (Masking Overlay) from
  Instagram Reel C-Nty_eP-Rk'
category: davinci-resolve
tags:
- masking
- text effect
- motion tracking
- compositing
- edit
- intermediate
version: 1.0.0
source_reel_id: C-Nty_eP-Rk
resolve_page: Edit
node_graph_type: serial
key_nodes:
- Background Clip
- Duplicate Clip
- Text+
parameters:
  mask_method: Power Window or Magic Mask
  feathering: Soft
  blend_mode: Normal
steps_to_reproduce:
- Place your video clip on the timeline.
- Duplicate the clip (Alt+Drag) to create a second layer directly above.
- Add a Text+ title on a layer between the two video clips.
- Select the top video clip and go to Color page.
- Use the Power Window or Magic Mask to isolate the subject.
- Track the mask across the clip to follow the movement.
- Adjust the text layer position so it appears behind the masked subject.
difficulty: intermediate
---
# Text Behind Subject (Masking Overlay)

**Source Reel:** C-Nty_eP-Rk
**Resolve Page:** Edit
**Node Graph Type:** serial
**Difficulty:** intermediate

## Description
DaVinci Resolve technique extracted from Instagram Reel C-Nty_eP-Rk.

## Key Nodes
- Background Clip
- Duplicate Clip
- Text+

## Parameters
mask_method: Power Window or Magic Mask
feathering: Soft
blend_mode: Normal


## Steps to Reproduce
1. Place your video clip on the timeline.
2. Duplicate the clip (Alt+Drag) to create a second layer directly above.
3. Add a Text+ title on a layer between the two video clips.
4. Select the top video clip and go to Color page.
5. Use the Power Window or Magic Mask to isolate the subject.
6. Track the mask across the clip to follow the movement.
7. Adjust the text layer position so it appears behind the masked subject.

## Tags
masking, text effect, motion tracking, compositing
