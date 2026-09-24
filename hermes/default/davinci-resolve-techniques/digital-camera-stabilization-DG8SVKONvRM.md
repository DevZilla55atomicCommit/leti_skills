---
name: digital-camera-stabilization-DG8SVKONvRM
description: Digital Camera Stabilization - DaVinci Resolve technique from Instagram
  Reel DG8SVKONvRM
category: davinci-resolve
tags:
- stabilization
- cinematography
- davinci-resolve
- post-production
resolve_page: Color
node_graph_type: serial
difficulty: beginner
key_nodes:
- Primary Node
- Stabilizer
parameters:
  Mode: Camera
  Smoothing: '50.0'
  Inter-window: None
  Zoom: Auto-crop
steps_to_reproduce:
- Import the shaky clip into the Color page
- Select the clip and create a new primary node
- Open the Inspector panel and navigate to the Stabilizer tab
- Set the Mode to 'Camera' for full movement stabilization
- Adjust the Smoothing slider until the jitter is removed
- Increase the Zoom slider to hide black edges created by the transformation
source_reel_id: DG8SVKONvRM
---
# Digital Camera Stabilization

**Source Reel:** DG8SVKONvRM
**Resolve Page:** Color
**Node Graph Type:** serial
**Difficulty:** beginner

## Description
DaVinci Resolve technique extracted from Instagram Reel DG8SVKONvRM.

## Key Nodes
- Primary Node
- Stabilizer

## Parameters
Mode: Camera
Smoothing: '50.0'
Inter-window: None
Zoom: Auto-crop


## Steps to Reproduce
1. Import the shaky clip into the Color page
2. Select the clip and create a new primary node
3. Open the Inspector panel and navigate to the Stabilizer tab
4. Set the Mode to 'Camera' for full movement stabilization
5. Adjust the Smoothing slider until the jitter is removed
6. Increase the Zoom slider to hide black edges created by the transformation

## Tags
stabilization, cinematography, davinci-resolve, post-production
