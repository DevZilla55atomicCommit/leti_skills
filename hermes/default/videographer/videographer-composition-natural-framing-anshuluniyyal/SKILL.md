---
name: videographer-composition-natural-framing-anshuluniyyal
description: "Composition technique: Natural Framing + Negative Space — use environmental elements (branches, arches, doorways) to create frame within frame while letting 60-70% remain active negative space. From @anshuluniyyal Instagram carousel slide 6."
version: 1.0.0
author: Hermes Agent (via instagram-videographer-learning-pipeline)
metadata:
  hermes:
    tags: [videographer, composition, natural-framing, frame-within-frame, negative-space, portal-composition, blue-hour, monochrome, sky-as-subject, davinci-resolve, color-grading]
    source: https://www.instagram.com/p/DaBejwDkznl/
    creator: "@anshuluniyyal"
    content_type: "Carousel Post"
    slide_index: 6
    vault_category: "Composition"

---

# Natural Framing + Negative Space — Composition Skill

> **Source:** [@anshuluniyyal — The Art of Static Shots (Slide 6)](https://www.instagram.com/p/DaBejwDkznl/)
> **Technique Type:** Composition / Framing
> **DaVinci Resolve:** Studio / Free (custom power windows, glow OFX)

---

## 🎯 When to Use This Technique

| Project Type | Application |
|--------------|-------------|
| **Landscape/Travel** | Classic "view through" shots |
| **Narrative** | Character looking out — POV portal |
| **Doc** | Subject in environment; framed by context |
| **Music Video** | Visual metaphor: trapped/framed/free |
| **Commercial** | Rare — "view from the suite" real estate/hotel |
| **Timelapse** | Static portal + moving clouds = perfect base |

---

## 🏗️ Core Principles

| Principle | Execution |
|-----------|-----------|
| **Frame as Portal** | Natural frame = window into world |
| **Negative Space as Subject** | Sky/mist isn't empty — it's the mood |
| **Frame Imperfection** | Branches irregular, incomplete → feels discovered |
| **Scale Via Frame** | Small frame + vast interior = immense space |
| **Color Unity** | Frame tones = space tones → no visual conflict |

---

## 📸 Shot Recipe (Reproducible)

### Pre-Production
- [ ] **Scout for frames:** Tree tunnels, rock arches, doorway ruins, cave mouths, canopy gaps
- [ ] **Check inner view:** Frame must reveal something worth framing (not just more trees)
- [ ] **Time for sky:** Blue hour, storm approach, heavy mist — sky has character
- [ ] **Lens:** 24-35mm (wide enough for frame + interior; not so wide frame disappears)

### Production
- [ ] **Position** so frame edges touch or nearly touch image edges (or slight crop)
- [ ] **Level horizon** inside frame (even if outer frame tilts)
- [ ] **Expose for sky** (brightest) → inner scene silhouettes or shadows
- [ ] **Focus** on inner scene (midground); frame can be slightly soft
- [ ] **Bracket** for HDR — sky vs interior = high DR

### Post-Production (DaVinci Resolve)

```
NODE 01 — Primary Balance
    │  • Lift: -0.05 (deepen shadows in frame)
    │  • Gain: -0.03 (protect sky highlights)
    │  • Temp: -20 (cool blue mood)
    ▼
NODE 02 — Frame Enhancement (Parallel)
    │  • Qualifier: select frame elements (branches/rocks)
    │  • Contrast: +20 | Clarity: +15 (texture)
    │  • Saturation: -30 (frame recedes)
    ▼
NODE 03 — Negative Space Grade (Parallel)
    │  • Qualifier: select sky/mist region
    │  • Glow OFX: Radius 100, Intensity 0.1 (ethereal)
    │  • Hue vs Sat: Blue → -10 (near mono)
    ▼
NODE 04 — Portal Vignette (Serial)
    │  • Power Window: custom shape matching frame interior
    │  • Invert: ON (affects OUTSIDE frame)
    │  • Gain: -0.08 | Feather: 0.4
    │  • *This darkens the frame edges, brightens portal*
    ▼
NODE 05 — Unity Grade (Parallel)
    │  • Hue vs Hue: All → slight blue unification
    │  • Curve: Gentle S for filmic density
    ▼
OUTPUT
```

---

## ⚠️ Common Pitfalls & Fixes

| Problem | Root Cause | Solution |
|---------|------------|----------|
| Frame dominates, view lost | Frame too thick/dense | Choose sparse frame; grade frame darker/desat |
| Sky blown out | Exposed for interior | Expose for sky; bracket; recover interior in grade |
| Frame looks artificial | Perfect arch/doorway | Seek organic/broken frames; irregular edges |
| No depth — looks flat | Frame and interior same tone | Grade frame darker/cooler; interior warmer/brighter |
| Frame cuts subject | Poor positioning | Test compositions; frame should *contain* subject |

---

## ✅ Verification Checklist

- [ ] Frame **touches or nearly touches** 3-4 edges of image
- [ ] **Negative space ≥ 60%** of frame area
- [ ] Inner scene **has clear subject/composition** (not random)
- [ ] Frame **darker/desaturated** vs inner scene (or graded so)
- [ ] Sky/space **has mood** (clouds, mist, gradient, color)
- [ ] Frame **imperfect/organic** — not architectural perfection
- [ ] Horizon **level inside frame** (even if outer frame tilts)

---

## 🔗 Cross-References

| Resource | Link |
|----------|------|
| Depth Cues in Composition | `../Composition/00-MASTER-INDEX.md` |
| Atmospheric Perspective Theory | `../../Camera Theory/02-Atmospheric-Perspective.md` (future) |
| Silhouetting Technique | `../../Camera Theory/02-Silhouetting-Atmospheric-Depth_anshuluniyyal.md` |
| DaVinci Qualifier/Hue vs Hue | `../../DaVinci_Knowledge_Base/Color Grading & Looks/Creative Grading & Looks/` |
| Power Window Shapes | `../../DaVinci_Knowledge_Base/Masking & Power Windows/` |

---

## 📦 Assets (Generated by Pipeline)

```
assets/
├── composition/
│   └── framing/
│       └── natural-framing/
│           ├── demo.gif
│           ├── technique_demo.gif
│           ├── frame_before.png
│           ├── frame_during.png
│           ├── frame_after.png
│           ├── before_after_comparison.png
│           └── node_graph_screenshot.png
├── DaBejwDkznl/
│   ├── slide_06.png
│   ├── carousel_combined.gif
│   └── technique_comparison_grid.png
```

---

## 🏷️ Tags

`#videographer` `#composition` `#framing` `#natural-frame` `#negative-space` `#portal-composition` `#blue-hour` `#monochrome` `#sky-as-subject` `#anshuluniyyal`

---

*Skill generated by `instagram-videographer-learning-pipeline` on 2025-07-17 from Instagram carousel slide DaBejwDkznl/6*