---
name: davinci-resolve-color-science-guide
description: "DaVinci Resolve Color Science Guide by Loris Marie — foundational concepts for color management, grading pipelines, and PowerGrade workflow"
version: 0.1.0
author: Hermes
metadata:
  hermes:
    tags: [DaVinci Resolve, Color Grading, Color Science, Color Management, PowerGrade, Educational, Workflow]
---

# DaVinci Resolve Color Science Guide — Loris Marie

Foundational color science concepts from @loris_marie — understanding color management, grading pipelines, and the "Ultimate Powergrade" workflow philosophy.

## When to Use
- Learning color science fundamentals for Resolve
- Setting up proper color-managed pipelines
- Understanding the theory behind grading decisions
- Evaluating PowerGrade/template workflows

## Prerequisites
- DaVinci Resolve (Free or Studio) 18+
- Basic Color Page familiarity

## Quick Reference

| Concept | Description | Practical Application |
|---------|-------------|----------------------|
| **Color Management** | CST pipeline (Log → Working → Output) | Consistent results across cameras/deliverables |
| **Working Space** | DaVinci Wide Gamut (DWG) / ACES | Grade in large space, compress at end |
| **Scene-Referred** | Linear light, camera-native | Preserves data for creative decisions |
| **Display-Referred** | Gamma-encoded for monitor | Final output transform only |
| **PowerGrade Workflow** | Reusable node templates | Speed + consistency across projects |

---

## Core Color Science Concepts

### 1. Color Spaces & Transforms
| Space | Role | When to Use |
|-------|------|-------------|
| **Camera Log** (S-Log3, Apple Log, BRAW) | Acquisition | Source footage — never grade here |
| **DaVinci Wide Gamut (DWG)** | Working/Intermediate | **Primary grading space** — huge gamut, linear-ish |
| **ACEScg / ACEScc** | Working (alternative) | VFX interchange, facility pipelines |
| **Rec.709 / Gamma 2.4** | Display/Output | Final delivery (web, broadcast) |
| **P3-D65 / Gamma 2.6** | Display/Output | Cinema delivery |
| **Rec.2020 / ST.2084** | Display/Output | HDR delivery |

### 2. The Correct Pipeline (Node Order)
```
CAMERA LOG FOOTAGE
        │
        ▼
[Node 01] CST: Camera Log → DWG (or ACEScc)
        │   ★ NO CREATIVE GRADE BEFORE THIS
        ▼
[Node 02-0X] PRIMARY: WB, Exposure, Balance (in DWG)
        │
        ▼
[Node XX] CREATIVE: Look, LUT, Split Tone, etc. (in DWG)
        │
        ▼
[Node Last] CST: DWG → Rec.709/P3/Rec.2020 (Output)
        │   ★ Gamut Mapping ON (Saturation Method)
        ▼
   LEGALIZER / OUTPUT
```

**Golden Rule:** *All creative grading happens in Working Space (DWG), never in Camera Log or Output space.*

### 3. Scene-Referred vs Display-Referred
| Aspect | Scene-Referred (DWG/ACES) | Display-Referred (Rec.709) |
|--------|---------------------------|------------------------|----------------------------|
| **Data** | Linear light, unlimited range | Gamma-encoded, 0-1/64-940 |
| **Grading** | Physically plausible | "Video look" baked in |
| **Flexibility** | Maximum — change output anytime | Locked to display |
| **LUTs** | Technical (CST) only | Creative LUTs work here |
| **When** | **All grading nodes** | **Final output node only** |

### 4. Gamut Mapping (Critical for DWG→Rec.709)
| Setting | Recommendation | Why |
|---------|----------------|-----|
| **Method** | Saturation (Perceptual) | Preserves hue, compresses saturation gracefully |
| **Saturation Max** | 0.90–0.95 | Headroom for specular highlights |
| **Knee** | 0.80–0.90 | Smooth roll-off before clipping |
| **Highlight Rolloff** | Low/Medium | Natural highlight descent |

### 5. PowerGrade Philosophy (Loris's "Ultimate Powergrade")
| Principle | Implementation |
|-----------|----------------|
| **Template, not preset** | Structured node tree with labeled placeholders |
| **Camera-agnostic** | First node = CST from any log to DWG |
| **Modular sections** | Primary / Creative / Skin / Output as Compound Nodes |
| **Keyboard-driven** | MagicGrade-style F-key shortcuts for speed |
| **Versioned** | v1, v2, v3 — evolve with Resolve updates |

---

## Practical Workflow Checklist

### Project Setup (Once Per Project)
- [ ] **Color Management:** DaVinci YRGB Color Managed / DWG
- [ ] **Input CST:** Set per-camera (or use "Auto" with Clip Attributes)
- [ ] **Output CST:** Set per deliverable (Rec.709 2.4, P3, HDR)
- [ ] **Gamut Mapping:** Enable on Output CST, Saturation Method
- [ ] **Monitor:** Calibrated to target output space

### Per-Timeline/Clip
- [ ] Verify Clip Attributes → Input Color Space correct
- [ ] Node 01: CST to DWG (if not auto-managed)
- [ ] Primary balance in DWG (WB, Exposure, Contrast)
- [ ] Creative grade in DWG
- [ ] Skin protection (Qualifier/Parallel/Layer Mixer)
- [ ] Output CST with Gamut Mapping
- [ ] Legalizer/Soft Clip for broadcast

### Quality Control
- [ ] Waveform: Legal range, no unexpected clipping
- [ ] Parade: Neutral balance in grays
- [ ] Vectorscope: Skin tones on line, no gamut warning
- [ ] CIE Scope: All colors within target gamut
- [ ] A/B: Grade vs. bypass — intentional difference only

---

## Common Misconceptions & Corrections

| Misconception | Reality |
|---------------|---------|
| "Grade in Log for film look" | Log is for capture — grade in DWG, apply film LUT at output |
| "LUT first, then grade" | LUT at end (output) or as creative layer in DWG — never first |
| "Rec.709 is a working space" | Rec.709 is **display-referred** — grading here loses data |
| "CST degrades quality" | Proper CST (3D LUT + gamut map) is mathematically lossless in DWG |
| "ACES only for VFX" | ACEScc is a valid working space alternative to DWG |

---

## Loris Marie's "Ultimate Powergrade" Structure
```
┌─────────────────────────────────────────────────────────────┐
│  COMPOUND: INPUT MANAGEMENT                                 │
│  ├── Node 01: CST Camera Log → DWG (per clip)               │
│  ├── Node 02: NR (if needed)                                │
│  └── Node 03: Technical Fix (flicker, sensor issues)        │
├─────────────────────────────────────────────────────────────┤
│  COMPOUND: PRIMARY BALANCE                                  │
│  ├── Node 04: WB (Temp/Tint or RGB Gain, Luma Mix=0)       │
│  ├── Node 05: Exposure (Gain + Pivot, or Offset)            │
│  ├── Node 06: Contrast (S-curve or Pivot/Contrast)          │
│  └── Node 07: Saturation (global, conservative)             │
├─────────────────────────────────────────────────────────────┤
│  COMPOUND: CREATIVE LOOK (Parallel/Layer Mixer branches)    │
│  ├── Branch A: Main Look (Color Wheels, Curves, Color Slice)│
│  ├── Branch B: Skin Protection (Qualifier + Layer Mixer)    │
│  ├── Branch C: Sky/BG Separation (Parallel + Qualifier)     │
│  └── Branch D: Vignette/Grain/Halation (Layer Mixer)        │
├─────────────────────────────────────────────────────────────┤
│  COMPOUND: OUTPUT DELIVERY                                  │
│  ├── Node XX: CST DWG → Output Space (Gamut Map ON)         │
│  ├── Node XX: Legalizer / Soft Clip                         │
│  └── Node XX: Output Transform (if HDR: ST.2084 + Metadata) │
└─────────────────────────────────────────────────────────────┘
```

---

## References

- Source: Instagram @loris_marie — "Color Science Guide 🧬" (32 weeks ago)
- Hashtags: #colorgrading #colorgrade #davinciresolve #filmmkrs
- Type: Carousel post (educational slides, English caption)
- CTA: "Save & share with your filmmaker friend" — PowerGrade link in bio

---

## Tags

```markdown
#davinci-resolve #color-science #color-management #cst #davinci-wide-gamut #aces #working-space #scene-referred #display-referred #gamut-mapping #powergrade #workflow #loris-marie #educational #color-grading
```