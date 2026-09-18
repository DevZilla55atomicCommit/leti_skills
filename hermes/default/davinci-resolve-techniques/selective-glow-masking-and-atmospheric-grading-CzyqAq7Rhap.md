---
name: selective-glow-masking-and-atmospheric-grading-CzyqAq7Rhap
description: Selective Glow Masking and Atmospheric Grading - DaVinci Resolve technique
  from Instagram Reel CzyqAq7Rhap
category: davinci-resolve
tags:
- color grading
- masking
- glow
- cinematic
resolve_page: Color
node_graph_type: serial
difficulty: intermediate
key_nodes:
- Primary Correction
- Qualifier Mask
- Glow Node
- Power Window
parameters:
  Softness: '0.50'
  Gain: '0.15'
  Threshold: '0.40'
  Contrast: '1.2'
steps_to_reproduce:
- Import clip and perform basic exposure/white balance on the Primary node
- Use a Qualifier (HSL) to select only the purple flower and the sunlit edges
- Create a Power Window around the flower with high feathering to isolate the subject
- Add a Glow effect with a high threshold to create the ethereal light bleed around
  petals
- Add a final serial node to deepen shadows and increase contrast using the Curves
  tool
source_reel_id: CzyqAq7Rhap
---
# Selective Glow Masking and Atmospheric Grading

**Source Reel:** CzyqAq7Rhap
**Resolve Page:** Color
**Node Graph Type:** serial
**Difficulty:** intermediate

## Description
DaVinci Resolve technique extracted from Instagram Reel CzyqAq7Rhap.

## Key Nodes
- Primary Correction
- Qualifier Mask
- Glow Node
- Power Window

## Parameters
Softness: '0.50'
Gain: '0.15'
Threshold: '0.40'
Contrast: '1.2'


## Steps to Reproduce
1. Import clip and perform basic exposure/white balance on the Primary node
2. Use a Qualifier (HSL) to select only the purple flower and the sunlit edges
3. Create a Power Window around the flower with high feathering to isolate the subject
4. Add a Glow effect with a high threshold to create the ethereal light bleed around petals
5. Add a final serial node to deepen shadows and increase contrast using the Curves tool

## Tags
color grading, masking, glow, cinematic
