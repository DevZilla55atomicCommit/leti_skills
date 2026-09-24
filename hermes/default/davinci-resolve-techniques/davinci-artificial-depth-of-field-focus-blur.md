---
name: davinci-artificial-depth-of-field-focus-blur
description: DaVinci Resolve technique: Artificial Depth of Field / Focus Blur from Instagram Reel Cv2MWyANfG7
category: creative/davinci-resolve-techniques
tags: ["cinematic", "drone", "depth-of-field", "tutorial", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "Cv2MWyANfG7"
collection: "Drone"
resolve_page: "Color"
node_graph: "serial"
difficulty: "intermediate"
created: 2026-07-30
---

# Artificial Depth of Field / Focus Blur

**Source:** Instagram Reel `Cv2MWyANfG7` (Drone)  
**Page:** Color | **Graph:** serial | **Difficulty:** intermediate

![Artificial Depth of Field / Focus Blur](Cv2MWyANfG7.gif)

## Node Graph Structure

- Gaussian Blur
- Magic Mask

## Parameters

- **Blur Radius**: 25.0
- **Strength**: 1.0

## Steps to Reproduce in DaVinci Resolve

1. Import footage and go to the Color Page
2. Use the Magic Mask to isolate the subject (the drone)
3. Create a new node for the background
4. Add a Gaussian Blur or Lens Blur effect to the background node
5. Adjust the blur radius to create a cinematic shallow depth of field

## Tags
`cinematic`, `drone`, `depth-of-field`, `tutorial`
