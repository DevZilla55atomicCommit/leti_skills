---
name: Selective Glow Masking and Atmospheric Grading
description: DaVinci Resolve technique from Instagram Reel CzyqAq7Rhap
trigger: "selective glow masking and atmospheric grading"
page: Color
difficulty: intermediate
tags: ['color grading', 'masking', 'glow', 'cinematic']
video_id: CzyqAq7Rhap
source: instagram-reel
updated: 2026-07-28T19:32:01.292408
---

# Selective Glow Masking and Atmospheric Grading

**Source:** Instagram Reel `CzyqAq7Rhap`  
**Resolve Page:** Color  
**Difficulty:** intermediate  
**Node Graph Type:** serial

## Key Nodes
- Primary Correction
- Qualifier Mask
- Glow Node
- Power Window

## Parameters
- **Softness:** 0.50
- **Gain:** 0.15
- **Threshold:** 0.40
- **Contrast:** 1.2

## Steps to Reproduce
1. Import clip and perform basic exposure/white balance on the Primary node
2. Use a Qualifier (HSL) to select only the purple flower and the sunlit edges
3. Create a Power Window around the flower with high feathering to isolate the subject
4. Add a Glow effect with a high threshold to create the ethereal light bleed around petals
5. Add a final serial node to deepen shadows and increase contrast using the Curves tool

## Tags
- #color grading
- #masking
- #glow
- #cinematic
