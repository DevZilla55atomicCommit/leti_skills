---
name: davinci-3d-text-overlay-with-motion-blur
description: DaVinci Resolve technique: 3D Text Overlay with Motion Blur from Instagram Reel DOMASLBCVmu
category: creative/davinci-resolve-techniques
tags: ["typography", "3d text", "motion blur", "urban style", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "DOMASLBCVmu"
collection: "Ideas_for_Shooting_Videos"
resolve_page: "Fusion"
node_graph: "serial"
difficulty: "intermediate"
created: 2026-07-30
---

# 3D Text Overlay with Motion Blur

**Source:** Instagram Reel `DOMASLBCVmu` (Ideas_for_Shooting_Videos)  
**Page:** Fusion | **Graph:** serial | **Difficulty:** intermediate

![3D Text Overlay with Motion Blur](DOMASLBCVmu.gif)

## Node Graph Structure

- Text3+
- Merge
- Transform

## Parameters

- **Text**: JA
- **PrimaryColor**: #FF0000
- **Motion Blur**: Enabled
- **Softness**: Medium

## Steps to Reproduce in DaVinci Resolve

1. Import footage into the Fusion page
2. Add a Text3+ node and type 'JA'
3. Add a Transform3D node to adjust scale and rotation in 3D space
4. Use a Merge3D node to layer the text over the background footage
5. Enable Motion Blur in the Transform or Merge node settings to simulate camera movement
6. Adjust opacity or add a Glow node to blend the text with the scene lighting

## Tags
`typography`, `3d text`, `motion blur`, `urban style`
