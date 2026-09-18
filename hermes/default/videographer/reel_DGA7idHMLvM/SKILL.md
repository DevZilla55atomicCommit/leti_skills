---
name: reel_DGA7idHMLvM
description: "Reel technique from Instagram — Fusion Page 60-Second Overview from @creatorsergeant"
version: 1.0.0
author: Hermes Agent
metadata:
  hermes:
    tags: [videographer, reel, fusion-page, node-based-compositing, davinci-resolve, vfx, compositing, creatorsergeant, instagram-learning]
---

# Fusion Page 60-Second Overview — Reel Technique

> **Source:** [Instagram Reel](https://www.instagram.com/reel/DGA7idHMLvM/)
> **Creator:** @creatorsergeant
> **Date Processed:** 2026-07-19
> **Instagram Post Code:** DGA7idHMLvM
> **Content Type:** Reel
> **Technique Category:** VFX & Compositing / Fusion Fundamentals

---

## 🎯 Technique Summary

The **Fusion page** in DaVinci Resolve is a node-based compositing environment (similar to Nuke) built directly into the Edit/Color timeline. This reel provides a rapid-fire overview: media in → node graph → tools (Blur, Transform, Merge, ColorCorrector, Text+) → MediaOut. Key insight: Fusion operates in **linear color space** by default — wrap grades with **Gamut/Gamma** tools (CST) when moving between Edit/Color (scene-referred) and Fusion (linear).

---

## 📋 Complete Technique Details

| Parameter | Value | Purpose |
|-----------|-------|---------|
| Technique | Fusion Page Overview / Node Graph Basics | Core technique |
| Creator | @creatorsergeant | Source |
| Discipline | VFX & Compositing / Fusion | Knowledge domain |
| Application | Post-Production / Fusion Page | Where used |
| Resolve Version | Free + Studio | Requirement |

---

## 🏗️ Core Principles

| Principle | Description |
|-----------|-------------|
| **Node-Based Compositing** | Every operation = a node; connections = data flow (left→right) |
| **MediaIn / MediaOut** | Source footage enters via MediaIn; final composite exits via MediaOut |
| **Merge Tool** | The "layer" equivalent — combines foreground over background (A over B) |
| **Transform Tool** | Position, scale, rotate, anchor — all keyframeable |
| **Color Space** | Fusion = linear by default; use **CST** or **Gamut** tools to convert |

---

## 🎬 Essential Fusion Node Graph (Starter Template)

```
MediaIn1 (plate) ─────────────────────────┐
                                           ├── Merge (FG over BG) ── MediaOut
MediaIn2 (foreground element) ────────────┘
     │
     ├── Transform (position/scale/rotate)
     ├── Blur / Edge Blend (integration)
     ├── ColorCorrector (match grade)
     └── Mask (Power Window / Polygon)
```

**Color Pipeline (critical):**
```
Edit/Color (DWG/Scene-Referred) 
    → CST (DWG → Linear sRGB/ACEScg) 
    → Fusion (Linear) 
    → CST (Linear → DWG) 
    → Edit/Color
```

---

## 🔧 Key Tools Referenced

| Tool | Category | Purpose |
|------|----------|---------|
| **Merge** | Composite | Layer FG over BG (Operation: "Over") |
| **Transform** | Transform | Position, Scale, Rotation, Anchor, Pivot |
| **Blur** | Filter | Edge softening, integration, depth of field |
| **ColorCorrector** | Color | Lift/Gamma/Gain, Saturation, Contrast |
| **Text+** | Text | Advanced titling (Fusion-native, not Edit page) |
| **Tracker** | Tracker | Planar/point tracking for matchmove |
| **DeltaKeyer / UltraKeyer** | Keying | Green/blue screen, luminance keying |
| **Camera3D / Renderer3D** | 3D | True 3D compositing, projections |

---

## 💡 Pro Tips from Comments

| Tip | Source | Context |
|-----|--------|---------|
| **Windows laptop recs** | @problemdirector_ | Community asked for affordable Fusion-capable Windows machines |
| **Fusion basics needed** | @solo_editor01, @varousisg | Requests for "Fusion for dummies" content |
| **Horizontal video in Fusion** | @hrishikeshlifts | Vertical footage appears horizontal — transform/rotate in MediaIn |
| **Treasure of DaVinci** | @solo_editor01 | Fusion = most powerful but underused page |

---

## ✅ Verification Checklist

- [ ] Understand node-based vs layer-based workflow
- [ ] MediaIn → Node Graph → MediaOut flow internalized
- [ ] Color space conversion (CST) between Edit/Color ↔ Fusion configured
- [ ] Merge tool operation ("Over", "Under", "Add", "Multiply") understood
- [ ] Transform keyframing for animation working
- [ ] Render order: Fusion comp renders *before* Color page grade (unless using Fusion clip on timeline)

---

## 🔗 Cross-References

| Topic | Vault Location |
|-------|----------------|
| Fusion Page Deep Dive | `DaVinci_Knowledge_Base/Videographer/VFX_&_Compositing/Fusion-Page-Deep-Dive.md` |
| Node-Based Compositing 101 | `DaVinci_Knowledge_Base/Videographer/VFX_&_Compositing/Node-Based-Compositing-101.md` |
| Color Space: Linear vs Scene-Referred | `DaVinci_Knowledge_Base/Videographer/Color_Grading_&_Looks/Linear-vs-Scene-Referred.md` |
| CST for Fusion Round-Trip | `DaVinci_Knowledge_Base/Videographer/VFX_&_Compositing/CST-Fusion-Roundtrip.md` |
| Text+ vs Edit Page Titles | `DaVinci_Knowledge_Base/Videographer/VFX_&_Compositing/TextPlus-Guide.md` |

---

## 🏷️ Tags

`#videographer` `#reel` `#fusion-page` `#node-based-compositing` `#davinci-resolve` `#vfx` `#compositing` `#creatorsergeant` `#instagram-learning`

---

*Skill generated by `instagram-videographer-learning-pipeline` on 2026-07-19 from Instagram Reel*