---
name: virtual-gimbal-movement--stabilization
description: 'DaVinci Resolve technique: Virtual Gimbal Movement & Stabilization from
  Instagram Reel C9sE4njPHM4'
category: davinci-resolve
tags:
- cinematography
- stabilization
- davinci-resolve
- gimbal
- color
- beginner
version: 1.0.0
source_reel_id: C9sE4njPHM4
resolve_page: Color
node_graph_type: serial
key_nodes:
- Stabilizer
- Transform
parameters:
  Stabilization Mode: Camera Lock
  Smoothing: '50'
  Zoom: '1.15'
steps_to_reproduce:
- Import raw footage into the timeline
- Open the Color page and create a new node
- Apply the Stabilizer effect from the Inspector
- Select 'Camera Lock' to stabilize handheld footage
- Add a Transform node to create manual digital zooms or pans
- Use keyframes to simulate a smooth gimbal-like tilt or movement
difficulty: beginner
---
# Virtual Gimbal Movement & Stabilization

**Source Reel:** C9sE4njPHM4
**Resolve Page:** Color
**Node Graph Type:** serial
**Difficulty:** beginner

## Description
DaVinci Resolve technique extracted from Instagram Reel C9sE4njPHM4.

## Key Nodes
- Stabilizer
- Transform

## Parameters
Stabilization Mode: Camera Lock
Smoothing: '50'
Zoom: '1.15'


## Steps to Reproduce
1. Import raw footage into the timeline
2. Open the Color page and create a new node
3. Apply the Stabilizer effect from the Inspector
4. Select 'Camera Lock' to stabilize handheld footage
5. Add a Transform node to create manual digital zooms or pans
6. Use keyframes to simulate a smooth gimbal-like tilt or movement

## Tags
cinematography, stabilization, davinci-resolve, gimbal
