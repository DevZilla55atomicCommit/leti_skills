---
name: davinci-resolve-power-windows-parallel-nodes
category: creative
description: DaVinci Resolve Power Windows using parallel nodes for independent adjustments
tags:
  - davinci-resolve
  - power-windows
  - parallel-nodes
  - masking
  - color-grading
  - aparicio-co
  - workflow
version: 1.0.0
author: aparicio.co (extracted by Hermes Agent)
source_url: https://www.instagram.com/reel/DGjQ5LCPFPJ/
---

# DaVinci Resolve: Power Windows with Parallel Nodes

## Overview
This technique uses **parallel nodes** for Power Window adjustments, allowing each window to be applied independently from the same source channel, then blended equally. This prevents unwanted stacking of adjustments that could break the image.

## Core Concept

### Why Parallel Nodes for Power Windows?

- **Independent processing**: Each Power Window receives the same source, processes independently
- **No stacking artifacts**: Windows don't compound on top of each other unpredictably
- **Equal contribution**: All windows blend with equal weight unless adjusted
- **Clean isolation**: Easy to toggle, modify, or remove individual windows

### Node Tree Structure

```
Node 01: Input/Log Footage (or previous grade)
  │
  ├─── Parallel Node 1: Power Window A (e.g., Sky)
  ├─── Parallel Node 2: Power Window B (e.g., Subject Face)
  ├─── Parallel Node 3: Power Window C (e.g., Background)
  ├─── Parallel Node 4: Power Window D (e.g., Foreground)
  │
  └─── Layer Mixer: Equal blend of all parallel window branches
```

## Step-by-Step Workflow

### 1. Base Grade First
- Apply base correction (CST, WB, Exposure) in serial nodes
- This becomes the source for all parallel windows

### 2. Create Parallel Mixer for Windows
1. Right-click node graph → **Add Parallel Mixer** (Option+P / Alt+P)
2. Create 3-5 parallel branches (one per Power Window)

### 3. Configure Each Parallel Branch

| Branch | Window Target | Typical Adjustment |
|--------|---------------|-------------------|
| **Parallel 1** | Sky / Highlights | Exposure drop, Blue push, Graduated filter |
| **Parallel 2** | Subject / Face | Skin tone cleanup, Exposure lift, Contrast |
| **Parallel 3** | Background | Separation, Color contrast, Blur/Depth |
| **Parallel 4** | Foreground | Vignette, Texture, Leading lines |

### 4. Power Window Settings Per Branch
- **Shape**: Circle, Square, Custom (Bezier), Gradient
- **Tracker**: Enable for moving subjects (Frame/Pixel/Planar)
- **Softness**: Feather edges (20-50px typical)
- **Invert**: Use for "everything except" selections

### 5. Blend Mode
- **Layer Mixer**: Set to "Normal" or "Add" for equal contribution
- Adjust **Gain** per branch if windows need different weights

## Key Advantages

1. **No stacking artifacts**: Windows don't double-apply corrections
2. **Independent tracking**: Each window tracks separately
3. **Easy revisions**: Disable one window without affecting others
4. **Clean node graph**: Organized, readable structure

## Pro Tips

- **Label windows**: "SKY", "FACE", "BG", "FG" in node labels
- **Use qualifiers INSIDE windows**: Combine Power Window + Qualifier for precision
- **Gradient windows**: For skies/horizons (linear gradient, soft edge)
- **Inverted windows**: "Everything but subject" for background separation

## Comparison: Serial vs Parallel Windows

| Aspect | Serial Windows | Parallel Windows |
|--------|---------------|------------------|
| Stacking | Compounds adjustments | Independent |
| Order dependency | High | None |
| Toggle single window | Affects downstream | Clean isolation |
| Performance | Slightly faster | Slightly heavier |

## Related Skills
- `davinci-resolve-power-masking` — Radial → Magic Mask → Inverted BG
- `davinci-resolve-realistic-wall-shadows-power-window` — Wall shadows with tracking
- `davinci-resolve-node-structure-parallel-powergrade` — General parallel node structure

## Source
Instagram: @aparicio.co — "Using POWER WINDOWS in Davinci Resolve!"
URL: https://www.instagram.com/reel/DGjQ5LCPFPJ/
Date: 2025-07-11