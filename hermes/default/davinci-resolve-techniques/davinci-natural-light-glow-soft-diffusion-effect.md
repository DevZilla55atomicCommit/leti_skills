---
name: davinci-natural-light-glow-soft-diffusion-effect
description: DaVinci Resolve technique: Natural Light Glow & Soft Diffusion Effect from Instagram Reel C95GBSmxyzX
category: creative/davinci-resolve-techniques
tags: ["cinematic", "natural light", "glow", "color grading", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "C95GBSmxyzX"
collection: "Car_Shooting_tips"
resolve_page: "Color"
node_graph: "serial"
difficulty: "intermediate"
created: 2026-07-30
---

# Natural Light Glow & Soft Diffusion Effect

**Source:** Instagram Reel `C95GBSmxyzX` (Car_Shooting_tips)  
**Page:** Color | **Graph:** serial | **Difficulty:** intermediate

![Natural Light Glow & Soft Diffusion Effect](C95GBSmxyzX.gif)

## Node Graph Structure

- Exposure
- Color Correction
- Soft Glow/Glow
- Qualifier Mask

## Parameters

- **Glow Threshold**: 0.4
- **Glow Radius**: 0.50
- **Opacity**: 0.3
- **Highlights Gain**: +1.2

## Steps to Reproduce in DaVinci Resolve

1. Import footage and go to the Color page.
2. Add a serial node to balance exposure and white balance.
3. Add a second serial node for effects and apply the Glow effect or use the Glow node.
4. Adjust the Threshold to ensure only the brightest highlights (sun beams) trigger the effect.
5. Increase the Radius and Opacity to create a dreamy bloom around light sources.
6. Use a Qualifier or Mask to isolate the effect so it does not degrade detail in shadows or midtones.

## Tags
`cinematic`, `natural light`, `glow`, `color grading`
