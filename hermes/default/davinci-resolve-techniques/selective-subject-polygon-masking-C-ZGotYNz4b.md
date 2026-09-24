---
name: selective-subject-polygon-masking
description: 'DaVinci Resolve technique: Selective Subject Polygon Masking from Instagram
  Reel C-ZGotYNz4b'
category: davinci-resolve
tags:
- masking
- color-grading
- polygon
- isolation
- color
- intermediate
version: 1.0.0
source_reel_id: C-ZGotYNz4b
resolve_page: Color
node_graph_type: serial
key_nodes:
- Qualifier/Window
- Primary Grade
parameters:
  window_type: Polygon
  tracking: Active
  offset: '25.00'
steps_to_reproduce:
- Go to the Color page
- Select the Polygon Window tool from the Window tab
- Draw a custom path around the desired subject
- Go to the Tracker tab and click play to track the mask to the subject movement
- Apply color adjustments using the Primary Wheels or Curves to affect the masked
  area
difficulty: intermediate
---
# Selective Subject Polygon Masking

**Source Reel:** C-ZGotYNz4b
**Resolve Page:** Color
**Node Graph Type:** serial
**Difficulty:** intermediate

## Description
DaVinci Resolve technique extracted from Instagram Reel C-ZGotYNz4b.

## Key Nodes
- Qualifier/Window
- Primary Grade

## Parameters
window_type: Polygon
tracking: Active
offset: '25.00'


## Steps to Reproduce
1. Go to the Color page
2. Select the Polygon Window tool from the Window tab
3. Draw a custom path around the desired subject
4. Go to the Tracker tab and click play to track the mask to the subject movement
5. Apply color adjustments using the Primary Wheels or Curves to affect the masked area

## Tags
masking, color-grading, polygon, isolation
