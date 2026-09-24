---
category: color
description: DaVinci Resolve technique from Instagram Reel C95GBSmxyzX
difficulty: intermediate
name: Natural Light Glow & Soft Diffusion Effect
page: Color
tags:
- cinematic
- natural light
- glow
- color grading
trigger: Use when applying natural light glow & soft diffusion effect in DaVinci Resolve
video_id: C95GBSmxyzX
---
# Natural Light Glow & Soft Diffusion Effect

**Source:** Instagram Reel `C95GBSmxyzX`
**Resolve Page:** Color
**Difficulty:** intermediate
**Node Graph Type:** serial

## Overview
DaVinci Resolve technique extracted from Instagram Reel analysis.

## Key Nodes
- Exposure
- Color Correction
- Soft Glow/Glow
- Qualifier Mask

## Parameters
- **Glow Threshold:** 0.4
- **Glow Radius:** 0.50
- **Opacity:** 0.3
- **Highlights Gain:** +1.2

## Steps to Reproduce
1. Import footage and go to the Color page.
2. Add a serial node to balance exposure and white balance.
3. Add a second serial node for effects and apply the Glow effect or use the Glow node.
4. Adjust the Threshold to ensure only the brightest highlights (sun beams) trigger the effect.
5. Increase the Radius and Opacity to create a dreamy bloom around light sources.
6. Use a Qualifier or Mask to isolate the effect so it does not degrade detail in shadows or midtones.

## Tags
- cinematic
- natural light
- glow
- color grading
