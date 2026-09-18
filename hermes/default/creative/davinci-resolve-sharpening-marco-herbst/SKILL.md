---
name: davinci-resolve-sharpening-marco-herbst
description: Marco Herbst's proper sharpening technique in DaVinci Resolve — last node, Blur/Sharpen tab, radius ~0.46, Highlight Mode A/B for visual feedback, scaling for fine-tuning
category: creative
tags: [davinci-resolve, sharpening, color-grading, marco-herbst, finishing, blur-sharpen]
source_url: https://www.instagram.com/reel/DK1S-3QMfbA/
author: marcoherbst.work
---

# DaVinci Resolve: Proper Sharpening Technique — Marco Herbst

> **"Feinschliff für dein Grading in DaVinci Resolve!"** — Marco Herbst

## Core Technique: Final-Node Sharpening

Apply sharpening as the **very last node** in your node tree (after all grading, LUTs, film emulation, grain, etc.).

### Step-by-Step

1. **Add a new serial node at the end** of your node tree
2. **Open the Blur tab** (not the Blur OFX — the built-in Blur/Sharpen panel)
3. **Set Radius to ~0.46** (adjust to taste; 0.4–0.5 typical)
4. **Enable Highlight Mode → A/B** to visualize exactly where sharpening is applied
5. **Fine-tune via Scaling** parameter for subtle control

### Key Principles

| Principle | Why It Matters |
|-----------|----------------|
| **Last node only** | Prevents sharpening artifacts from being amplified by subsequent operations (CST, LUT, grain, etc.) |
| **Highlight Mode A/B** | Visual feedback — toggle between original (A) and sharpened (B) to avoid "crunchy" over-sharpening |
| **Radius ~0.46** | Small radius = micro-contrast enhancement, not halo-producing edge detection |
| **Scaling** | Global intensity control — dial back if it feels artificial |

### Pro Tip from Comments

> *"Ich sehe oft bessere Ergebnisse im Microkontrast, wenn ich das Log Footage schärfe, statt die Ebene ganz zum Schluss"* — muellermedia.group
> 
> **Translation:** Often better micro-contrast results when sharpening **log footage early** (before CST/LUT) rather than at the very end. Test both workflows!

### Hashtags / Search Terms

#davinciresolve #colorgrading #colorist #filmmakingtips #sharpening

---

## Quick Reference Card

```
NODE TREE (end):
[Grade] → [CST] → [LUT] → [Grain] → [HALATION] → [SHARPEN ⬅️ LAST]

SHARPEN NODE SETTINGS:
├── Blur Tab → Blur/Sharpen
├── Radius: 0.46
├── Highlight Mode: A/B (toggle to compare)
└── Scaling: adjust to taste (start 1.0)
```

## Related Skills

- `davinci-resolve-sharpening-3-hacks` — 3 sharpening approaches (Spatial NR, Edge Detect, 3-stage)
- `davinci-resolve-edge-detect-soften` — Edge Detect OFX for softening (inverse technique)