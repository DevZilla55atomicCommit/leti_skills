---
name: davinci-speed-ramping-with-motion-blur
description: DaVinci Resolve technique: Speed Ramping with Motion Blur from Instagram Reel DFm0XygovZN
category: creative/davinci-resolve-techniques
tags: ["speed-ramp", "cinematic", "transitions", "automotive", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "DFm0XygovZN"
collection: "Gimbal_Moves"
resolve_page: "Edit"
node_graph: "serial"
difficulty: "intermediate"
created: 2026-07-30
---

# Speed Ramping with Motion Blur

**Source:** Instagram Reel `DFm0XygovZN` (Gimbal_Moves)  
**Page:** Edit | **Graph:** serial | **Difficulty:** intermediate

![Speed Ramping with Motion Blur](DFm0XygovZN.gif)

## Node Graph Structure

- Clip
- Retime Editor

## Parameters

- **Retime Curve**: Bezier
- **Motion Blur**: Optical Flow

## Steps to Reproduce in DaVinci Resolve

1. Right-click the clip on the timeline and select Retime Speed
2. Open the Retime Curve in the Inspector or timeline
3. Add keyframes where you want the speed to change
4. Adjust the speed points between keyframes to create a ramp up effect
5. Smooth the keyframes using Bezier handles for fluid transitions
6. Enable Motion Blur in the Inspector to hide jump-cut artifacts

## Tags
`speed-ramp`, `cinematic`, `transitions`, `automotive`
