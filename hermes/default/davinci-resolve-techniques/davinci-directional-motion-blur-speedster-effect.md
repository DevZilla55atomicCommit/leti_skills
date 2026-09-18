---
name: davinci-directional-motion-blur-speedster-effect
description: DaVinci Resolve technique: Directional Motion Blur Speedster Effect from Instagram Reel C9c_XK2Iu9u
category: creative/davinci-resolve-techniques
tags: ["motion-blur", "vfx", "cinematic", "speedster", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "C9c_XK2Iu9u"
collection: "Ideas_for_Shooting_Videos"
resolve_page: "Fusion"
node_graph: "layer_mixer"
difficulty: "intermediate"
created: 2026-07-30
---

# Directional Motion Blur Speedster Effect

**Source:** Instagram Reel `C9c_XK2Iu9u` (Ideas_for_Shooting_Videos)  
**Page:** Fusion | **Graph:** layer_mixer | **Difficulty:** intermediate

![Directional Motion Blur Speedster Effect](C9c_XK2Iu9u.gif)

## Node Graph Structure

- MediaIn
- Duplicate
- MotionBlur
- Merge

## Parameters

- **Blur_Type**: Directional
- **Length**: 50.0
- **Angle**: Match to movement vector
- **Shutter Angle**: 180

## Steps to Reproduce in DaVinci Resolve

1. Bring the clip into the Fusion page.
2. Add a Duplicate node to create multiple ghosting layers of the subject.
3. Apply a Motion Blur node after the Duplicate node.
4. Adjust the 'Angle' in Motion Blur settings to match the direction of the subject's movement.
5. Merge the blurred layers back with the original footage using low opacity to create the streak effect.

## Tags
`motion-blur`, `vfx`, `cinematic`, `speedster`
