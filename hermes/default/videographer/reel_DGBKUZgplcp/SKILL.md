---
name: reel_DGBKUZgplcp
description: "Reel technique from Instagram — Ultra Noise Reduction in DaVinci Resolve from @davinciresolved"
version: 1.0.0
author: Hermes Agent
metadata:
  hermes:
    tags: [videographer, reel, noise-reduction, ultra-nr, davinci-resolve-studio, color-grading, post-production, davinciresolved, instagram-learning]
---

# Ultra Noise Reduction (OFX) — Reel Technique

> **Source:** [Instagram Reel](https://www.instagram.com/reel/DGBKUZgplcp/)
> **Creator:** @davinciresolved
> **Date Processed:** 2026-07-19
> **Instagram Post Code:** DGBKUZgplcp
> **Content Type:** Reel
> **Technique Category:** Color Grading / Noise Reduction

---

## 🎯 Technique Summary

DaVinci Resolve's **Ultra Noise Reduction (Studio only)** is a temporal/spatial noise reduction tool that operates at the OFX level. The reel demonstrates the node placement workflow: add an OFX "Noise Reduction" node, set mode to **Temporal** (for video) or **Spatial** (for stills), adjust **Luma/Chroma** thresholds, and use **Radius** to control softness. Critical: place NR *before* creative grade nodes to avoid amplifying noise in later operations.

---

## 📋 Complete Technique Details

| Parameter | Value | Purpose |
|-----------|-------|---------|
| Technique | Ultra Noise Reduction (OFX) | Core technique |
| Creator | @davinciresolved | Source |
| Discipline | Color Grading / Noise Reduction | Knowledge domain |
| Application | Post-Production / Color Page | Where used |
| Resolve Version | Studio required | Requirement |

---

## 🏗️ Core Principles

| Principle | Description |
|-----------|-------------|
| **Temporal NR** | Analyzes adjacent frames to distinguish noise from detail — best for video |
| **Spatial NR** | Single-frame analysis — best for stills or frozen frames |
| **Pre-Grade Placement** | NR must precede creative nodes; grading after NR amplifies artifacts |
| **Luma/Chroma Separation** | Independent control prevents chroma smoothing from destroying color detail |
| **Radius Control** | Larger radius = stronger reduction but more softening; balance with Threshold |

---

## 🎬 DaVinci Resolve Node Structure

```
Node 01 — CST (Camera Log → DWG/Rec.709)
Node 02 — OFX: Noise Reduction (Ultra NR)
  | Mode: Temporal (video) / Spatial (stills)
  | Luma Threshold: 0.05-0.15 (start conservative)
  | Chroma Threshold: 0.10-0.20 (chroma noise typically higher)
  | Radius: 1-3 (small = detail preservation, large = aggressive)
  | Frames: 3-5 (temporal window)
Node 03 — Primary Balance (Exposure/Contrast/WB)
Node 04 — Creative Look (LUT / Custom Grade)
Node 05 — Film Emulation / Halation / Texture (optional)
Node 06 — Output CST (DWG → Display)
```

---

## 🔧 OFX Noise Reduction Parameters Explained

| Parameter | Range | Typical | Effect |
|-----------|-------|---------|--------|
| **Mode** | Temporal / Spatial | Temporal | Analysis method |
| **Luma Threshold** | 0.0-1.0 | 0.08 | Luminance noise sensitivity |
| **Chroma Threshold** | 0.0-1.0 | 0.15 | Chrominance noise sensitivity |
| **Radius** | 0-10 | 2 | Neighborhood size for averaging |
| **Frames** | 1-9 | 5 | Temporal window (Temporal mode only) |
| **Detail Recovery** | 0.0-1.0 | 0.3 | Reintroduce fine detail post-NR |

---

## 💡 Pro Tips from Community (Comments)

| Tip | Source | Context |
|-----|--------|---------|
| **Studio required** | @maquenchie, @pixalartmedia | Ultra NR is Studio-only feature |
| **NR before or after color?** | @tonyyeperfumer | *Before* creative grade (Node 02 in pipeline above) |
| **Node placement** | @pixalartmedia | Beginning of tree (after CST) — not at end |
| **Laggy performance** | @shakphillips7, @nawhcim | Reduce Frames to 3; lower Radius; use Render Cache |
| **Motion blur interaction** | @andy.jascel | NR can soften motion edges — increase Detail Recovery |

---

## ✅ Verification Checklist

- [ ] Resolve Studio license active (Ultra NR not in Free)
- [ ] NR node placed *before* creative grade nodes
- [ ] CST applied before NR (log → linear for accurate noise analysis)
- [ ] Temporal mode for video, Spatial for stills
- [ ] Luma/Chroma thresholds set independently
- [ ] Radius balanced: noise gone but detail retained
- [ ] Detail Recovery used to restore micro-contrast
- [ ] Render Cache enabled for smooth playback

---

## 🔗 Cross-References

| Topic | Vault Location |
|-------|----------------|
| Noise Reduction Overview | `DaVinci_Knowledge_Base/Videographer/Color_Grading_&_Looks/Noise-Reduction-Overview.md` |
| NR Node Placement Strategy | `DaVinci_Knowledge_Base/Videographer/Color_Grading_&_Looks/NR-Node-Placement.md` |
| Temporal vs Spatial NR | `DaVinci_Knowledge_Base/Videographer/Color_Grading_&_Looks/Temporal-vs-Spatial-NR.md` |
| Studio vs Free Features | `DaVinci_Knowledge_Base/Videographer/Post-Production/Studio-vs-Free.md` |

---

## 🏷️ Tags

`#videographer` `#reel` `#noise-reduction` `#ultra-nr` `#davinci-resolve-studio` `#color-grading` `#post-production` `#davinciresolved` `#instagram-learning`

---

*Skill generated by `instagram-videographer-learning-pipeline` on 2026-07-19 from Instagram Reel*