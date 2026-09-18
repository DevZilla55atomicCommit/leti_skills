---
name: videographer-composition-layering-silhouette-anshuluniyyal
description: "Composition technique: Layering + Silhouetting (3 Depth Planes) — FG texture, MG subject, BG atmosphere. All backlit, separated by tone and haze. From @anshuluniyyal Instagram carousel slide 4."
version: 1.0.0
author: Hermes Agent (via instagram-videographer-learning-pipeline)
metadata:
  hermes:
    tags: [videographer, composition, layering, depth-layers, silhouetting, atmospheric-perspective, three-plane-rule, tone-separation, mist, fog, davinci-resolve, color-grading]
    source: https://www.instagram.com/p/DaBejwDkznl/
    creator: "@anshuluniyyal"
    content_type: "Carousel Post"
    slide_index: 4
    vault_category: "Composition"

---

# Layering + Silhouetting (3 Depth Planes) — Composition Skill

> **Source:** [@anshuluniyyal — The Art of Static Shots (Slide 4)](https://www.instagram.com/p/DaBejwDkznl/)
> **Technique Type:** Composition / Depth Layers
> **DaVinci Resolve:** Studio / Free (parallel node grading, glow OFX)

---

## 🎯 When to Use This Technique

| Project Type | Application |
|--------------|-------------|
| **Landscape/Travel** | Classic "three-layer" vista shots |
| **Doc/Environmental** | Subject in habitat; context = layers |
| **Narrative** | Character isolated in world; thematic depth |
| **Commercial** | Product in environment (rare — usually want separation) |
| **Timelapse Base** | Static 3-layer = perfect for cloud/mist timelapse |

---

## 🏗️ Core Principles

| Principle | Execution |
|-----------|-----------|
| **Three-Plane Rule** | FG texture / MG subject / BG atmosphere |
| **Tone Separation** | Each plane distinctly lighter than previous |
| **Atmospheric Haze as Separator** | Mist/fog naturally lightens distant layers |
| **Silhouette Unity** | All planes backlit → clean graphic forms |
| **FG Texture as Frame** | Blurred grass = vignette + immersion |

---

## 📸 Shot Recipe (Reproducible)

### Pre-Production
- [ ] Location: Layered terrain (ridge → valley → distant peaks) prone to mist
- [ ] Time: Early morning (radiation fog) or post-rain (evaporation mist)
- [ ] Lens: 35-50mm (compresses layers slightly; avoids wide distortion)
- [ ] **Scout for:** Clear FG element (grass, rocks), MG trees/structures, BG mountains

### Production
- [ ] **Tripod lock** — zero movement; layer alignment must be perfect
- [ ] **Focus** on midground (subject plane); FG slightly soft = intentional
- [ ] **Expose for BG** (brightest) → FG/MG fall to silhouette
- [ ] **Wait for mist** — shoot sequence as haze shifts between planes
- [ ] **Bracket** ±2 stops for HDR merge if DR exceeds sensor

### Post-Production (DaVinci Resolve)

```
NODE 01 — Primary Balance
    │  • Lift: -0.08 (deepen all silhouettes)
    │  • Gain: -0.03 (protect BG highlight detail)
    │  • Temp: +20 (cool blue mood)
    ▼
NODE 02 — Plane Separation (Parallel x3)
    │  • Node A (FG): Qualifier on darkest tones → Contrast +15
    │  • Node B (MG): Qualifier on mid tones → Clarity +10
    │  • Node C (BG): Qualifier on light tones → Gamma +0.1, Sat -20
    ▼
NODE 03 — Atmosphere Enhancement (Serial)
    │  • Glow OFX: Radius 80, Intensity 0.15 (on BG only via qualifier)
    │  • Add subtle haze: Solid Color (dark blue) + Composite: Screen @ 5%
    ▼
NODE 04 — Tone Grade (Parallel)
    │  • Hue vs Hue: All → Cool (-10)
    │  • Hue vs Sat: Global -30 (near mono)
    ▼
NODE 05 — Vignette & Grain
    │  • Power Window: oval, feather 0.9, gain -0.12
    │  • Film Grain: Kodak 2383 @ 15%
    ▼
OUTPUT
```

---

## ⚠️ Common Pitfalls & Fixes

| Problem | Root Cause | Solution |
|---------|------------|----------|
| Planes merge (no separation) | Similar tones across layers | Grade each plane separately (parallel nodes) |
| FG too sharp/distracting | Focus on FG or too wide aperture | Focus on MG; f/8-f/11; FG blur = feature |
| BG blown out (pure white) | Exposed for FG/MG | Expose for BG; bracket; recover in grade |
| Looks flat in grade | No tone separation | Qualifier each plane; offset lift/gamma |
| Mist looks fake in post | Overdone glow/haze | Subtle: 5-10% opacity; match light direction |

---

## ✅ Verification Checklist

- [ ] **3 distinct tone bands** visible in waveform (low/mid/high)
- [ ] FG has **texture** (not pure black) — grass, rock, foliage detail
- [ ] MG has **recognizable shapes** — trees, structures, subject
- [ ] BG **lightest + least saturated** — atmospheric perspective
- [ ] Mist/haze **visible between planes** — not just at BG
- [ ] Subject **placed in MG** — not FG or BG
- [ ] Horizon **level** (unless intentional Dutch)

---

## 🔗 Cross-References

| Resource | Link |
|----------|------|
| Depth Cues in Composition | `../Composition/00-MASTER-INDEX.md` |
| Atmospheric Perspective Theory | `../../Camera Theory/02-Atmospheric-Perspective.md` (future) |
| Silhouetting Technique | `../../Camera Theory/02-Silhouetting-Atmospheric-Depth_anshuluniyyal.md` |
| DaVinci Parallel Node Grading | `../../DaVinci_Knowledge_Base/Node Structures & Templates/` |
| Qualifier/Hue vs Hue | `../../DaVinci_Knowledge_Base/Color Grading & Looks/Creative Grading & Looks/` |

---

## 📦 Assets (Generated by Pipeline)

```
assets/
├── composition/
│   └── depth-layers/
│       └── layering-silhouette/
│           ├── demo.gif
│           ├── technique_demo.gif
│           ├── frame_before.png
│           ├── frame_during.png
│           ├── frame_after.png
│           ├── before_after_comparison.png
│           └── node_graph_screenshot.png
├── DaBejwDkznl/
│   ├── slide_04.png
│   ├── carousel_combined.gif
│   └── technique_comparison_grid.png
```

---

## 🏷️ Tags

`#videographer` `#composition` `#layering` `#depth-layers` `#silhouetting` `#atmospheric-perspective` `#three-plane-rule` `#tone-separation` `#mist` `#fog` `#anshuluniyyal`

---

*Skill generated by `instagram-videographer-learning-pipeline` on 2025-07-17 from Instagram carousel slide DaBejwDkznl/4*