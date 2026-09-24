---
name: davinci-resolve-edge-detect-soften
description: "Edge Detect OFX for softening in DaVinci Resolve — alternative to Texture Pop, soften sharp images using native Edge Detect."
version: 0.1.0
author: Hermes
metadata:
  hermes:
    tags: [DaVinci Resolve, Color Grading, Edge Detect, Softening, Texture]
    source_url: "https://www.instagram.com/reel/DUa_Z1ZkX5k/"
    source_creator: "@davinciresolved"
    source_date: "2025-05-15"
    vault_category: "Creative Grading & Looks"
    skill_level: "Intermediate"
    tags: [Edge Detect, Softening, OFX, Texture Pop, Davinci Resolved]
---

# DaVinci Resolve: Edge Detect Soften — @davinciresolved

**Source:** [@davinciresolved Instagram Reel](https://www.instagram.com/reel/DUa_Z1ZkX5k/) — "Edge detect soften in DaVinci Resolve"

## Technique Overview

Using **Edge Detect OFX** in an unconventional way — not for stylized edges, but for **softening** sharp images. Alternative/complement to Texture Pop.

> *"Comment 'link' to upgrade your workflow with the RESOLVED Editor Bundle"*

---

## Node Structure

```
Node 01: Base Grade
Node 02: EDGE DETECT SOFTEN
  ├── Edge Detect OFX
  │   ├── Mode: Soften (not Outline)
  │   ├── Radius: 1-3 (subtle)
  │   └── Mix: 30-50% (Opacity)
  └── Composite: Normal / Soft Light
```

---

## Step-by-Step

### 1. Add Edge Detect OFX
- OpenFX → **Edge Detect**
- Default is "Outline" mode — **change to "Soften"**

### 2. Settings for Softening
| Parameter | Value | Purpose |
|-----------|-------|---------|
| **Mode** | **Soften** | Inverts edge detection → blur |
| **Radius** | 1-3 pixels | Subtle, not obvious blur |
| **Strength** | 0.3-0.5 | Blend amount |
| **Mix/Opacity** | 30-50% | Natural look |

### 3. Composite Mode
- **Normal:** Straight blend
- **Soft Light:** More organic, preserves contrast

---

## Edge Detect Soften vs Texture Pop

| Aspect | Edge Detect Soften | Texture Pop |
|--------|-------------------|-------------|
| **Tool** | Edge Detect OFX (Soften mode) | Texture Pop OFX |
| **Intent** | Reduce excessive sharpness | Enhance micro-contrast |
| **Use Case** | Over-sharpened footage, digital look | Flat footage, add "pop" |
| **Radius** | 1-3 (subtle) | 10-50 (local contrast) |
| **Look** | Organic, film-like | Crisp, modern |

---

## Pro Tips from Comments

| Question | Answer |
|----------|--------|
| @elhippy.exe: *"Why would you want to soften sharp image?"* | Over-sharpened digital footage, vintage lens mismatch, skin smoothing |
| @lemad.o: *"Difference between this and Texture Pop?"* | **Opposite intents** — Soften reduces detail, Texture Pop enhances it |
| @niceboy.wav: *"Tutorial on opposite — sharpen soft vintage glass"* | Use **Sharpen** OFX or **Spatial NR negative sharpen** (see: 3 Sharpening Hacks) |

---

## When to Use

| Scenario | Recommended |
|----------|-------------|
| Over-sharpened digital footage | ✅ Perfect |
| Skin smoothing (subtle) | ✅ With qualifier |
| Vintage lens + modern sensor mismatch | ✅ Blend characteristics |
| Intentional sharp look | ❌ Skip |
| Need more "pop" | ❌ Use Texture Pop instead |

---

## Related Techniques

- `davinci-resolve-edge-detect-effect` — Edge Detect for stylized outlines (outline mode)
- `davinci-resolve-sharpening-3-hacks` — Spatial NR negative sharpen, Edge Detect + Soft Light
- `davinci-resolve-soften-skin-free` — Face Refinement + Circle Mask + Blur

---

## Tags

`#davinciresolve` `#colorgrading` `#edge-detect` `#softening` `#texture-pop` `#davinciresolved` `#ofx`