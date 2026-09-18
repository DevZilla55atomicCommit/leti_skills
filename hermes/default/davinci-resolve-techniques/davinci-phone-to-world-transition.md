---
name: davinci-phone-to-world-transition
description: DaVinci Resolve technique: Phone-to-World Transition from Instagram Reel DGdHRL7CC4I
category: creative/davinci-resolve-techniques
tags: ["transition", "masking", "fusion", "vfx", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "DGdHRL7CC4I"
collection: "Ideas_for_Shooting_Videos"
resolve_page: "Fusion"
node_graph: "serial"
difficulty: "intermediate"
created: 2026-07-30
---

# Phone-to-World Transition

**Source:** Instagram Reel `DGdHRL7CC4I` (Ideas_for_Shooting_Videos)  
**Page:** Fusion | **Graph:** serial | **Difficulty:** intermediate

![Phone-to-World Transition](DGdHRL7CC4I.gif)

## Node Graph Structure

- MediaIn1
- MediaIn2
- Merge
- Transform

## Parameters

- **Merge Mode**: Over
- **Transform Center**: Keyframed movement

## Steps to Reproduce in DaVinci Resolve

1. Import the clip of the person holding the phone and the destination footage
2. In Fusion, mask the phone screen area using a Polygoner mask
3. Use a Transform node to scale and position the destination footage to fit the phone screen
4. Merge the destination footage over the original clip using the mask as an effect
5. Keyframe the mask or transform to expand the phone screen to reveal the full scene

## Tags
`transition`, `masking`, `fusion`, `vfx`
