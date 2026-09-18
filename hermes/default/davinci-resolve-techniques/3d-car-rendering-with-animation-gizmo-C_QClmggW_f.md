---
name: 3d-car-rendering-with-animation-gizmo
description: 'DaVinci Resolve technique: 3D Car Rendering with Animation Gizmo from
  Instagram Reel C_QClmggW_f'
category: davinci-resolve
tags:
- 3D
- rendering
- animation
- car
- Fusion
- fusion
- intermediate
version: 1.0.0
source_reel_id: C_QClmggW_f
resolve_page: Fusion
node_graph_type: serial
key_nodes:
- Loader
- Transform
- Renderer3D
parameters:
  car_model_path: /path/to/car_model.fbx
  animation_gizmo_enabled: true
  gizmo_type: rotation_scale
steps_to_reproduce:
- Import the 3D car model into Fusion using a Loader node.
- Apply a Transform node to position and orient the car in the 3D scene.
- Add a Renderer3D node to render the 3D scene.
- Optionally, add animation controls or a gizmo to the car object for manipulation.
difficulty: intermediate
---
# 3D Car Rendering with Animation Gizmo

**Source Reel:** C_QClmggW_f
**Resolve Page:** Fusion
**Node Graph Type:** serial
**Difficulty:** intermediate

## Description
DaVinci Resolve technique extracted from Instagram Reel C_QClmggW_f.

## Key Nodes
- Loader
- Transform
- Renderer3D

## Parameters
car_model_path: /path/to/car_model.fbx
animation_gizmo_enabled: true
gizmo_type: rotation_scale


## Steps to Reproduce
1. Import the 3D car model into Fusion using a Loader node.
2. Apply a Transform node to position and orient the car in the 3D scene.
3. Add a Renderer3D node to render the 3D scene.
4. Optionally, add animation controls or a gizmo to the car object for manipulation.

## Tags
3D, rendering, animation, car, Fusion
