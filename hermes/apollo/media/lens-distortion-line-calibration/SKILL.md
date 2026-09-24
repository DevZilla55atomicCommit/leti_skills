---
name: lens-distortion-line-calibration
description: "Line-based lens calibration with Krokodove Lens Distortion."
version: 1.0.0
author: Apollo (Hermes Agent)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [DaVinci Resolve, Fusion, Krokodove, Lens, Calibration, v21.1]
    related_skills: [davinci-resolve-version-tracker]
---

# Krokodove Lens Distortion Line-Based Calibration

## When to Use

Use when you need to calibrate lens distortion using straight line detection instead of checkerboard patterns. New in DaVinci Resolve 21.1.

## Video Reference
- **Video ID:** Wi44XLKQ3YA
- **Timestamp:** 9:33-9:41
- **Resolve Page:** Fusion

## Tool Location
Fusion Effects Library → Krokodove → Lens Distortion → Calibration Type: Lines

## Calibration Types
| Type | Method | Best For |
|------|--------|----------|
| Checkerboard | Grid corners | Traditional lens calibration |
| **Lines** | **Straight edge detection** | **Architectural, drone, wide-angle** |
| Hybrid | Both | Maximum accuracy |

## Line Calibration Workflow
1. Add Lens Distortion tool
2. Set Calibration Type to "Lines"
3. Import footage with visible straight lines
4. Tool auto-detects line features
5. Adjust line sensitivity threshold
6. Apply correction to footage

## Parameters
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| Calibration Type | Enum | Checkerboard | Checkerboard/Lines/Hybrid |
| Line Sensitivity | Float | 0.5 | Edge detection threshold |
| Min Line Length | Float | 0.1 | Minimum line length (normalized) |
| Max Lines | Integer | 50 | Maximum lines to process |
| Distortion Model | Enum | Brown-Conrady | Brown-Conrady/Kannala-Brandt |

## Use Cases
- Drone footage correction
- Architectural photography
- Wide-angle lens correction
- Action camera footage
- Footage without calibration patterns

## Tips
- Works best with high-contrast straight edges
- Buildings, horizons, door frames ideal
- Combine with Hybrid for best results
- Animate calibration for zoom lenses

## Cross-References
- **Related Skills:** `krokodove-connect-3d`, `krokodove-3d-region`
- **Tags:** `krokodove`, `fusion`, `lens`, `distortion`, `calibration`, `v21.1`
- **Collection:** `krokodove-tools`