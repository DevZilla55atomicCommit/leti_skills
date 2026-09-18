---
name: davinci-green-screen-removal-using-fusion-keyer
description: DaVinci Resolve technique: Green Screen Removal Using Fusion Keyer from Instagram Reel C27lrWuoAqs
category: creative/davinci-resolve-techniques
tags: ["Chroma Key", "Green Screen", "Fusion", "DaVinci Resolve", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "C27lrWuoAqs"
collection: "Color_grading"
resolve_page: "Fusion"
node_graph: "serial"
difficulty: "intermediate"
created: 2026-07-30
---

# Green Screen Removal Using Fusion Keyer

**Source:** Instagram Reel `C27lrWuoAqs` (Color_grading)  
**Page:** Fusion | **Graph:** serial | **Difficulty:** intermediate

![Green Screen Removal Using Fusion Keyer](C27lrWuoAqs.gif)

## Node Graph Structure

- Keyer

## Parameters

- **Screen**: Green
- **Edge Thin**: 0.1

## Steps to Reproduce in DaVinci Resolve

1. Import footage with green screen background into DaVinci Resolve
2. Add a Keyer node in the Fusion page and connect it to the footage
3. Set key type to 'Luma' and adjust Screen color to match the green screen
4. Refine edges using Edge Thin and other parameters for clean removal

## Tags
`Chroma Key`, `Green Screen`, `Fusion`, `DaVinci Resolve`
