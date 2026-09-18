---
name: davinci-basic-white-balance-high-key-lighting-correction
description: DaVinci Resolve technique: Basic White Balance & High-Key Lighting Correction from Instagram Reel C6KYXdXAEtQ
category: creative/davinci-resolve-techniques
tags: ["color_grading", "interior_design", "white_balance", "high_key_lighting", "tutorial", "davinci-resolve", "color-grading", "instagram-reel"]
source_reel: "C6KYXdXAEtQ"
collection: "Gimbal_Moves"
resolve_page: "Color"
node_graph: "serial"
difficulty: "beginner"
created: 2026-07-30
---

# Basic White Balance & High-Key Lighting Correction

**Source:** Instagram Reel `C6KYXdXAEtQ` (Gimbal_Moves)  
**Page:** Color | **Graph:** serial | **Difficulty:** beginner

![Basic White Balance & High-Key Lighting Correction](C6KYXdXAEtQ.gif)

## Node Graph Structure

- Input
- Transform (White Balance)
- Gamma/Color Corrector
- Output

## Parameters

- **white_balance_temperature**: 5600
- **gamma_correction_lift**: 1.2
- **highlight_recovery**: enabled

## Steps to Reproduce in DaVinci Resolve

1. Import footage into the Color page.
2. Add a Transform node to adjust white balance (neutralize cool tones in walls).
3. Use Gamma/Color Corrector to brighten shadows and lift highlights for a high-key look.
4. Apply slight saturation boost if needed.

## Tags
`color_grading`, `interior_design`, `white_balance`, `high_key_lighting`, `tutorial`
