---
name: Virtual Gimbal Movement & Stabilization
video_id: C9sE4njPHM4
resolve_page: Color
difficulty: beginner
tags: ['cinematography', 'stabilization', 'davinci-resolve', 'gimbal']
---
# Virtual Gimbal Movement & Stabilization

## Overview
This technique focuses on Virtual Gimbal Movement & Stabilization, primarily utilizing the **Color** page in DaVinci Resolve.

### Key Node Graph
- **Type**: serial
- **Key Nodes**: Stabilizer, Transform

### Parameters
- **Stabilization Mode**: Camera Lock
- **Smoothing**: 50
- **Zoom**: 1.15

### Steps to Reproduce
1. Import raw footage into the timeline
2. Open the Color page and create a new node
3. Apply the Stabilizer effect from the Inspector
4. Select 'Camera Lock' to stabilize handheld footage
5. Add a Transform node to create manual digital zooms or pans
6. Use keyframes to simulate a smooth gimbal-like tilt or movement
