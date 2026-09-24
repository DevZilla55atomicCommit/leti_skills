---
name: object-masked-reveal-transition-C6hVsRapY0k
description: Object Masked Reveal Transition - DaVinci Resolve technique from Instagram
  Reel C6hVsRapY0k
category: davinci-resolve
tags:
- transition
- masking
- tracking
- reveal
resolve_page: Fusion
node_graph_type: serial
difficulty: intermediate
key_nodes:
- MediaIn1
- MediaIn2
- MaskPaint
- Merge
parameters:
  mask_mode: In
  softness: '0.05'
  tracking_type: planar
steps_to_reproduce:
- Import the two clips into the Fusion page
- Add a MaskPaint node to the first clip and draw a mask around the subject or the
  window frame
- Use the Tracker node to follow the movement of the person or the glass edge
- Connect the second clip to the foreground input of a Merge node
- Adjust the mask feather to ensure a smooth blend between the two clips as the subject
  moves
source_reel_id: C6hVsRapY0k
---
# Object Masked Reveal Transition

**Source Reel:** C6hVsRapY0k
**Resolve Page:** Fusion
**Node Graph Type:** serial
**Difficulty:** intermediate

## Description
DaVinci Resolve technique extracted from Instagram Reel C6hVsRapY0k.

## Key Nodes
- MediaIn1
- MediaIn2
- MaskPaint
- Merge

## Parameters
mask_mode: In
softness: '0.05'
tracking_type: planar


## Steps to Reproduce
1. Import the two clips into the Fusion page
2. Add a MaskPaint node to the first clip and draw a mask around the subject or the window frame
3. Use the Tracker node to follow the movement of the person or the glass edge
4. Connect the second clip to the foreground input of a Merge node
5. Adjust the mask feather to ensure a smooth blend between the two clips as the subject moves

## Tags
transition, masking, tracking, reveal
