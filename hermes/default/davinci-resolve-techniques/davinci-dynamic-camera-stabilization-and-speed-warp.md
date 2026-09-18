---
name: davinci-dynamic-camera-stabilization-and-speed-warp
description: DaVinci Resolve technique: Dynamic Camera Stabilization and Speed Warp from Instagram Reel CuktzjZozAp
category: creative/davinci-resolve-techniques
tags: ["stabilization", "cinematography", "gimbal", "optical-flow", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "CuktzjZozAp"
collection: "Gimbal"
resolve_page: "Color"
node_graph: "serial"
difficulty: "intermediate"
created: 2026-07-30
---

# Dynamic Camera Stabilization and Speed Warp

**Source:** Instagram Reel `CuktzjZozAp` (Gimbal)  
**Page:** Color | **Graph:** serial | **Difficulty:** intermediate

![Dynamic Camera Stabilization and Speed Warp](CuktzjZozAp.gif)

## Node Graph Structure

- Stabilizer
- Speed Warp

## Parameters

- **stabilization_mode**: Perspective
- **smoothing**: 0.5
- **speed_warp_setting**: Optical Flow

## Steps to Reproduce in DaVinci Resolve

1. Import the clip into the Color page
2. Open the Stabilizer tab in the Inspector
3. Set mode to Perspective to fix gimbal jitter
4. Adjust smoothing slider to maintain natural-looking movement
5. Go to Fusion or Edit page to apply Speed Warp
6. Use Optical Flow for smooth-motion to enhance the cinematic walk

## Tags
`stabilization`, `cinematography`, `gimbal`, `optical-flow`
