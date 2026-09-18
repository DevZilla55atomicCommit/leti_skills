---
name: davinci-resolve-cinematic-glow-mansourmelouli
category: creative
description: DaVinci Resolve cinematic glow effect using Glow OFX with Soft Light composite for highlight rolloff
tags:
  - davinci-resolve
  - glow-effect
  - cinematic-look
  - soft-light
  - highlight-rolloff
  - mansourmelouli
  - glow-ofx
version: 1.0.0
author: "mansourmelouli (extracted by Hermes Agent)"
source_url: "https://www.instagram.com/reel/DJoYjV8Iuy5/"
---

# DaVinci Resolve: Cinematic Glow Effect — Glow OFX with Soft Light

## Overview
Technique for adding a cinematic glow to highlights using the native **Glow OFX** plugin with **Soft Light** composite mode. Creates softness and depth in highlights, especially useful for beauty shots and emotional scenes.

## Core Concept

### Why Glow + Soft Light?
- **Highlight targeting**: Glow naturally affects brightest areas
- **Soft Light blend**: Adds contrast + glow simultaneously, organic feel
- **Threshold control**: Precise isolation of highlight range
- **Recover highlights**: Bright Region Recovery prevents clipping

## Node Structure

```
Node 01: Input / Base Grade
Node 02: CST (Log → Working Space)
...
Node N-1: Creative Grade Complete
Node N:   **Glow OFX** (Insert BEFORE final CST)
Node N+1: Output CST (Working → Display)
```

**Critical**: Place Glow **before** final CST/Output Transform so glow operates in working gamut with full highlight data.

## Glow OFX Settings

| Parameter | Setting | Purpose |
|-----------|---------|---------|
| **Shine Threshold** | All the way LEFT (0) | Capture maximum highlight range |
| **Composite Type** | **Soft Light** | Blends glow organically (not Add/Screen) |
| **Spread** | Adjust to taste (10-50 typical) | Controls glow radius / haziness |
| **Global Blend** | Start at 0, increase slowly | Overall intensity control |
| **Bright Region Recovery** | Enable + adjust | Fixes highlight clipping from glow |

## Step-by-Step Workflow

1. **Complete Base Grade**: Finish all color, contrast, look adjustments
2. **Add Serial Node**: Label "Cinematic Glow" — place BEFORE output CST
3. **Open Effects**: Search **"Glow"** → Drag **Glow (OFX)** onto node
4. **Set Shine Threshold**: Drag **all the way left (0)** — captures full highlight rolloff
5. **Change Composite Type**: Dropdown → **Soft Light** (not Add, not Screen)
6. **Adjust Spread**: 
   - Low (5-15): Subtle highlight bloom
   - Medium (20-35): Visible glow, dreamy
   - High (40+): Strong halation, stylized
7. **Global Blend**: Start at **0**, slowly increase until desired (typically 0.15-0.4)
8. **Check Highlights**: If clipping → enable **Bright Region Recovery** → adjust
9. **Fine-tune**: Toggle node on/off to compare

## Why This Order Matters

```
WRONG:  Grade → CST → Glow → Output
        (Glow in display space, clipped highlights, wrong color)

RIGHT:  Grade → Glow → CST → Output  
        (Glow in working space, full highlight data, correct color)
```

## Pro Tips

- **Spread vs Blend**: Spread = size, Blend = intensity — adjust independently
- **Soft Light vs Add**: Soft Light adds contrast + glow; Add only brightens
- **Beauty Shots**: Lower Spread (10-20), subtle Blend (0.1-0.2) for skin glow
- **Emotional/Dreamy**: Higher Spread (30-50), stronger Blend (0.3-0.5)
- **Combine with Halation**: Separate node for film-style halation (red channel spread)
- **Protect Skin**: Qualifier on Glow node to exclude skin from excessive glow

## Common Issues & Fixes

| Issue | Cause | Fix |
|-------|-------|-----|
| Highlights clipping | Glow pushes over 1.0 | Enable Bright Region Recovery |
| Glow looks "digital" | Composite = Add/Screen | Switch to **Soft Light** |
| Too strong on skin | No isolation | Qualifier to exclude skin tones |
| Color shift in glow | Glow after CST | Move Glow **before** output CST |
| Noise amplified | High ISO footage | Lower Shine Threshold slightly right |

## Related Skills
- `davinci-resolve-cinematic-haze-effect` — Native tools haze/glow
- `davinci-resolve-glow-halation-cinematic` — Glow + halation combo
- `davinci-resolve-soft-light-glow-cinematic-emotion` — Soft Light glow technique
- `davinci-resolve-filmic-highlight-glow-davinciresolved` — Highlight glow variant

## Source
Instagram: @mansourmelouli — "How to add a cinematic glow to your image?"
URL: https://www.instagram.com/reel/DJoYjV8Iuy5/
Date: 2025-07-11