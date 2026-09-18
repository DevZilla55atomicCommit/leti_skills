---
name: davinci-soft-ethereal-pastel-matte
description: DaVinci Resolve technique: Soft Ethereal Pastel Matte from Instagram Reel C85dqIuy0_S
category: creative/davinci-resolve-techniques
tags: ["cinematic", "high-key", "pastel", "soft", "dreamy", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "C85dqIuy0_S"
collection: "Cinematic"
resolve_page: "Color"
node_graph: "serial"
difficulty: "intermediate"
created: 2026-07-30
---

# Soft Ethereal Pastel Matte

**Source:** Instagram Reel `C85dqIuy0_S` (Cinematic)  
**Page:** Color | **Graph:** serial | **Difficulty:** intermediate

![Soft Ethereal Pastel Matte](C85dqIuy0_S.gif)

## Node Graph Structure

- Primary Correction
- Curves Lift
- Color Wheels
- Glow Overlay

## Parameters

- **lift**: lifted towards grey/blue
- **saturation**: reduced (-15%)
- **contrast**: lowered
- **glow_radius**: large/soft
- **halation_tint**: low/warm

## Steps to Reproduce in DaVinci Resolve

1. Lift the black point in the Curves tool slightly to create a faded, matte look.
2. Reduce overall saturation while boosting luminance in the pink tones.
3. Apply a slight warm tint to the highlights and a cool teal/blue tint to the shadows.
4. Use the Glow effect with a high threshold and low opacity to diffuse the highlights.
5. Add a soft blur filter overlay on a separate node to simulate a diffusion filter.

## Tags
`cinematic`, `high-key`, `pastel`, `soft`, `dreamy`
