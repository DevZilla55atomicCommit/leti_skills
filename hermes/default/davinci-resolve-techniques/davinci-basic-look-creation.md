---
name: davinci-basic-look-creation
description: DaVinci Resolve technique: Basic Look Creation from Instagram Reel C6zi2VLgGok
category: creative/davinci-resolve-techniques
tags: [, "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "C6zi2VLgGok"
collection: "Gimbal_Moves"
resolve_page: "Color"
node_graph: "serial"
difficulty: "beginner"
created: 2026-07-30
---

# Basic Look Creation

**Source:** Instagram Reel `C6zi2VLgGok` (Gimbal_Moves)  
**Page:** Color | **Graph:** serial | **Difficulty:** beginner

![Basic Look Creation](C6zi2VLgGok.gif)

## Node Graph Structure

- Primary Correction
- Power Windows

## Parameters

- **primary_correction**: True
- **power_windows**: True

## Steps to Reproduce in DaVinci Resolve

1. Import footage into the Color page.
2. Apply Primary Correction node to balance exposure (compensate for dusk lighting).
3. Use Power Windows or Luma Key nodes to isolate warm interior lights and apply orange/yellow hue shift (+R, +G).
4. Isolate exterior elements with a separate window/mask and apply cool blue/cyan hues (-B, -Y) to create contrast.

## Tags

