---
name: natural-light-glow--soft-diffusion-effect
description: 'DaVinci Resolve technique: Natural Light Glow & Soft Diffusion Effect
  from Instagram Reel C95GBSmxyzX'
category: davinci-resolve
tags:
- cinematic
- natural light
- glow
- color grading
- color
- intermediate
version: 1.0.0
source_reel_id: C95GBSmxyzX
resolve_page: Color
node_graph_type: serial
key_nodes:
- Exposure
- Color Correction
- Soft Glow/Glow
- Qualifier Mask
parameters:
  Glow Threshold: '0.4'
  Glow Radius: '0.50'
  Opacity: '0.3'
  Highlights Gain: '+1.2'
steps_to_reproduce:
- Import footage and go to the Color page.
- Add a serial node to balance exposure and white balance.
- Add a second serial node for effects and apply the Glow effect or use the Glow node.
- Adjust the Threshold to ensure only the brightest highlights (sun beams) trigger
  the effect.
- Increase the Radius and Opacity to create a dreamy bloom around light sources.
- Use a Qualifier or Mask to isolate the effect so it does not degrade detail in shadows
  or midtones.
difficulty: intermediate
---
# Natural Light Glow & Soft Diffusion Effect

**Source Reel:** C95GBSmxyzX
**Resolve Page:** Color
**Node Graph Type:** serial
**Difficulty:** intermediate

## Description
DaVinci Resolve technique extracted from Instagram Reel C95GBSmxyzX.

## Key Nodes
- Exposure
- Color Correction
- Soft Glow/Glow
- Qualifier Mask

## Parameters
Glow Threshold: '0.4'
Glow Radius: '0.50'
Opacity: '0.3'
Highlights Gain: '+1.2'


## Steps to Reproduce
1. Import footage and go to the Color page.
2. Add a serial node to balance exposure and white balance.
3. Add a second serial node for effects and apply the Glow effect or use the Glow node.
4. Adjust the Threshold to ensure only the brightest highlights (sun beams) trigger the effect.
5. Increase the Radius and Opacity to create a dreamy bloom around light sources.
6. Use a Qualifier or Mask to isolate the effect so it does not degrade detail in shadows or midtones.

## Tags
cinematic, natural light, glow, color grading
