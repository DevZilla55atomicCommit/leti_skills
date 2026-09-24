---
name: social-media-sharpening--detail-recovery
description: 'DaVinci Resolve technique: Social Media Sharpening & Detail Recovery
  from Instagram Reel DCHcJ2DOzlb'
category: davinci-resolve
tags:
- social-media
- sharpening
- color-grading
- optimization
- color
- beginner
version: 1.0.0
source_reel_id: DCHcJ2DOzlb
resolve_page: Color
node_graph_type: serial
key_nodes:
- Primary Node
- Sharpen Node
parameters:
  Sharpen Amount: 20.0 - 40.0
  Radius: '0.67'
  Midtone Detail: '+1.5'
  Contrast: '+0.05'
steps_to_reproduce:
- Import footage into the Color page
- Add a new serial node at the end of the chain
- Select the Sharpen tool in the Color tab
- Increase the 'Amount' slightly to enhance edge definition
- Use 'Midtone Detail' to bring texture back without creating noise
- Apply a slight boost to contrast to compensate for the flattening effect of Instagram
  compression
difficulty: beginner
---
# Social Media Sharpening & Detail Recovery

**Source Reel:** DCHcJ2DOzlb
**Resolve Page:** Color
**Node Graph Type:** serial
**Difficulty:** beginner

## Description
DaVinci Resolve technique extracted from Instagram Reel DCHcJ2DOzlb.

## Key Nodes
- Primary Node
- Sharpen Node

## Parameters
Sharpen Amount: 20.0 - 40.0
Radius: '0.67'
Midtone Detail: '+1.5'
Contrast: '+0.05'


## Steps to Reproduce
1. Import footage into the Color page
2. Add a new serial node at the end of the chain
3. Select the Sharpen tool in the Color tab
4. Increase the 'Amount' slightly to enhance edge definition
5. Use 'Midtone Detail' to bring texture back without creating noise
6. Apply a slight boost to contrast to compensate for the flattening effect of Instagram compression

## Tags
social-media, sharpening, color-grading, optimization
