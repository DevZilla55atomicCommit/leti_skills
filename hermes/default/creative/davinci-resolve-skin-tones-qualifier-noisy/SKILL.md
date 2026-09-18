---
name: davinci-resolve-skin-tones-qualifier-noisy
description: "Skin tones workflow — addressing Qualifier noise issues, clean skin isolation techniques using vectorscope skin tone line, noise reduction in qualifier."
version: 0.1.0
author: Hermes
metadata:
  hermes:
    tags: [DaVinci Resolve, Color Grading, Skin Tones, Qualifier, Noise, Vectorscope]
    source_url: "https://www.instagram.com/reel/DT08--lALF_/"
    source_creator: "@ivarbrauer"
    source_date: "2025-01-22"
    vault_category: "Skin Tones"
    skill_level: "Intermediate"
    tags: [Skin Tones, Qualifier, Noise, Vectorscope, Skin Tone Line, Ivar Brauer]
---

# DaVinci Resolve: Skin Tones & Qualifier Noise — @ivarbrauer

**Source:** [@ivarbrauer Instagram Reel](https://www.instagram.com/reel/DT08--lALF_/) — "Skin tones, very, very important!"

## Technique Overview

Skin tone grading workflow focusing on **clean Qualifier isolation** — addressing the common issue of **noisy Qualifier selections** when pulling keys for skin tones. Uses Vectorscope skin tone line as reference.

> *"Skin tones, very, very important!"* — @ivarbrauer

---

## Problem: Noisy Qualifier Selections

**Comment from @yellow._.doogy:** *"I'm having issues where when I use the qualifier tool it gets extremely noisy"*

### Causes of Noisy Qualifier:
| Cause | Solution |
|-------|----------|
| **Footage noise** (high ISO, log) | Pre-NR node before Qualifier |
| **Wide hue range** | Narrow Hue range (~30-40° around skin) |
| **Wide luma range** | Restrict to mid-tones (avoid highlights/shadows) |
| **Low bit depth** | Work in DWG Intermediate (32-bit float) |
| **Compression artifacts** | Spatial NR before Qualifier |

---

## Clean Skin Isolation Workflow

### Node Structure
```
Node 01: CST (Log → DWG Intermediate) — 32-bit float, clean data
Node 02: **TEMP NR** (Spatial NR, Light/Temp) — Clean for Qualifier
Node 03: **QUALIFIER NODE** (Skin isolation)
  ├── Hue: 25-45° (narrow!)
  ├── Luma: Mid-tones only (0.3-0.7)
  ├── Sat: Wide (skin varies)
  └── Clean Black/White: Refine edges
Node 04: Skin Grade (Hue vs Hue, Hue vs Sat cleanup)
Node 05: Layer Mixer — Composite clean skin OVER creative grade
Node 06: Remove Temp NR (or keep if needed)
Node 07: Output CST
```

---

## Qualifier Settings for Clean Skin

| Parameter | Value | Why |
|-----------|-------|-----|
| **Hue Center** | ~35° (skin tone line) | Vectorscope reference |
| **Hue Width** | **30-40°** (narrow!) | Exclude background colors |
| **Luma Low** | 0.25-0.30 | Exclude shadows |
| **Luma High** | 0.65-0.75 | Exclude highlights |
| **Sat Low** | 0.10 | Include desaturated skin |
| **Sat High** | 1.0 | Include saturated skin |
| **Clean Black** | 0.02-0.05 | Remove noise in blacks |
| **Clean White** | 0.02-0.05 | Remove noise in highlights |
| **Blur Radius** | 2-4 | Soften mask edges |

---

## Vectorscope Skin Tone Line

| Reference | Value |
|-----------|-------|
| **Ideal Skin Tone** | ~11° (FLESH line) |
| **Acceptable Range** | 25°-45° (Hue) |
| **Verification** | Qualifier highlight mode shows selection |

---

## Pro Tips

1. **Pre-NR for Qualifier only** — Dedicated node, disable for final output
2. **Narrow Hue!** — Most common mistake = too wide hue range
3. **Mid-tones only** — Skin in highlights/shadows = different hue
4. **Layer Mixer composite** — Clean skin OVER grade, not under
5. **Hue vs Hue cleanup** — Shift problematic hues toward skin line

---

## Related Techniques

- `davinci-resolve-qualifier-picker-measurement-tool` — Qualifier as measurement tool
- `davinci-resolve-skin-tone-correction-waqas-qazi` — Layer Node skin protection workflow
- `davinci-resolve-soften-skin-free` — Face Refinement + Circle Mask + Blur

---

## Tags

`#davinciresolve` `#colorgrading` `#skin-tones` `#qualifier` `#noise` `#vectorscope` `#ivarbrauer`