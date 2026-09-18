---
name: davinci-picture-in-picture-comment-overlay
description: DaVinci Resolve technique: Picture-in-Picture Comment Overlay from Instagram Reel DJ9MqeSzX_9
category: creative/davinci-resolve-techniques
tags: ["social media", "pip", "picture-in-picture", "overlay", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "DJ9MqeSzX_9"
collection: "Ideas_for_Shooting_Videos"
resolve_page: "Fusion"
node_graph: "layer-mixer"
difficulty: "beginner"
created: 2026-07-30
---

# Picture-in-Picture Comment Overlay

**Source:** Instagram Reel `DJ9MqeSzX_9` (Ideas_for_Shooting_Videos)  
**Page:** Fusion | **Graph:** layer-mixer | **Difficulty:** beginner

![Picture-in-Picture Comment Overlay](DJ9MqeSzX_9.gif)

## Node Graph Structure

- MediaIn1 (Background)
- MediaIn2 (Overlay Video)
- TextPlus (Comment Bubble)
- Merge1

## Parameters

- **Blend**: 1.0
- **Size**: 0.4
- **Center**: [x, y] coordinates

## Steps to Reproduce in DaVinci Resolve

1. Place the main video background footage on the timeline.
2. Place the secondary video clip on the track above the background.
3. Go to the Fusion page.
4. Add a Transform node to the secondary video clip to scale and position it.
5. Add a TextPlus node to create the comment bubble text.
6. Use Merge nodes to layer the secondary video and text over the background footage.

## Tags
`social media`, `pip`, `picture-in-picture`, `overlay`
