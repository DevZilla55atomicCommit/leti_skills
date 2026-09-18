---
name: davinci-soft-dream-glow-with-motion-blur
description: DaVinci Resolve technique: Soft Dream Glow with Motion Blur from Instagram Reel DLCjH35IUby
category: creative/davinci-resolve-techniques
tags: ["glow", "dreamy", "cinematic", "color-grading", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "DLCjH35IUby"
collection: "Ideas_for_Shooting_Videos"
resolve_page: "Color"
node_graph: "serial"
difficulty: "intermediate"
created: 2026-07-30
---

# Soft Dream Glow with Motion Blur

**Source:** Instagram Reel `DLCjH35IUby` (Ideas_for_Shooting_Videos)  
**Page:** Color | **Graph:** serial | **Difficulty:** intermediate

![Soft Dream Glow with Motion Blur](DLCjH35IUby.gif)

## Node Graph Structure

- MediaIn
- Gaussian Blur
- Color Correct

## Parameters

- **Blur Radius**: 25.0
- **Softness**: High
- **Gain**: 1.2

## Steps to Reproduce in DaVinci Resolve

1. Create a new node in the Color page
2. Add a Gaussian Blur effect and increase the radius significantly
3. Right-click the node and select 'Add Alpha Output'
4. Connect the Alpha channel of the node to the Alpha Output to ensure only highlights glow
5. Adjust the Gain/Exposure to create the ethereal bloom effect
6. Add a slight Motion Blur in Fusion if to enhance the dreamlike movement

## Tags
`glow`, `dreamy`, `cinematic`, `color-grading`
