---
name: davinci-animated-movement-transition
description: DaVinci Resolve technique: Animated Movement Transition from Instagram Reel C8OnqYuNPUJ
category: creative/davinci-resolve-techniques
tags: ["motion graphics", "animation", "DaVinci Resolve Fusion", "transition", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "C8OnqYuNPUJ"
collection: "Gimbal_Moves"
resolve_page: "Fusion"
node_graph: "serial"
difficulty: "intermediate"
created: 2026-07-30
---

# Animated Movement Transition

**Source:** Instagram Reel `C8OnqYuNPUJ` (Gimbal_Moves)  
**Page:** Fusion | **Graph:** serial | **Difficulty:** intermediate

![Animated Movement Transition](C8OnqYuNPUJ.gif)

## Node Graph Structure

- Text Layer
- Shape Layer (Timeline Graphic)
- Transform Node

## Parameters

- **param_0**: Keyframes for position/opacity on text and shapes
- **param_1**: Font settings for 'MOVEMENT' text
- **param_2**: Position values for START/END markers and bottle icon

## Steps to Reproduce in DaVinci Resolve

1. Create a new Fusion page in DaVinci Resolve.
2. Add a Text node with 'MOVEMENT' as the content and animate its position over time using keyframes.
3. Use Shape nodes to draw START/END markers and the bottle icon, then animate their positions along the timeline path.
4. Connect all nodes in serial order (Text → Transform → Shape) to apply movement sequentially.

## Tags
`motion graphics`, `animation`, `DaVinci Resolve Fusion`, `transition`
