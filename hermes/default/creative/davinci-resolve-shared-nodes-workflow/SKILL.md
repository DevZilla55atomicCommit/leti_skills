---
name: davinci-resolve-shared-nodes-workflow
description: "DaVinci Resolve Shared Nodes: Centralized utility nodes for faster grading workflow across clips/groups/timeline"
version: 0.1.0
author: Hermes
metadata:
  hermes:
    tags: [DaVinci Resolve, Color Grading, Node Structures, Shared Nodes, Workflow Efficiency, PowerGrade]
---

# DaVinci Resolve Shared Nodes — Centralized Workflow Efficiency

Learn the **Shared Nodes** technique from @marcoherbst.work — save utility nodes (Skin Base, Sharpen, Glow, NR) as Shared Nodes to reuse across clip/group/timeline levels without rewiring.

## When to Use
- Large projects/series with recurring corrections (skin, sharpen, NR, glow)
- Social media formats needing consistent look across many clips
- Team collaboration where utility nodes must be standardized
- Any workflow where switching between clip/group/timeline levels slows you down

## Prerequisites
- DaVinci Resolve (Free or Studio) 18+
- Understanding of node graph levels (Clip / Group / Timeline)
- Basic right-click node operations

## Quick Reference
| Step | Action | Menu Path |
|------|--------|-----------|
| 1 | Create utility node | Build node (e.g., Skin Base, Sharpen, Glow) |
| 2 | Name it clearly | e.g., "Skin Base", "Sharpen", "Glow", "NR" |
| 3 | Save as Shared Node | Right-click node → **Save as Shared Node** |
| 4 | **Uncheck "Lock Node"** | Allows later live adjustment |
| 5 | Insert Shared Node | Right-click Node Tree → **Add Node → Shared Node** |
| 6 | Uncheck Lock on insert | Enables live tweak per clip |
| 7 | Update once, propagate everywhere | Edit Shared Node → all instances update |

## Procedure

### 1. Create Your Utility Nodes
Build the nodes you reuse constantly:
| Utility Node | Typical Contents |
|--------------|------------------|
| **Skin Base** | Qualifier + Hue vs Hue + Layer Mixer protection |
| **Sharpen** | Blur/Sharpen tab, Radius ~0.46, Highlight Mode A/B |
| **Glow/Bloom** | OpenFX Glow, Threshold 0.7–0.85, Radius 20–50 |
| **Noise Reduction** | Spatial NR (Luma/Chroma), Temporal NR if Studio |
| **Film Grain** | OpenFX Film Grain or DCTL grain |
| **Halation** | Custom node tree or DCTL |

### 2. Save as Shared Node
- Right-click the node → **Save as Shared Node**
- **Name descriptively**: `Skin Base`, `Sharpen_Final`, `Glow_Subtle`
- **CRITICAL**: **Uncheck "Lock Node"** — this allows you to adjust the Shared Node later per clip if needed
- Shared Node is now available globally in the project

### 3. Insert Shared Node Anywhere
- Go to any clip (Clip level), group (Group level), or timeline (Timeline level)
- Right-click in Node Tree → **Add Node → Shared Node**
- Select your saved Shared Node
- **Again: Uncheck "Lock Node"** on insertion for maximum flexibility
- Node appears instantly — no rewiring, no level switching

### 4. The Power: Central Control + Local Override
| Scenario | Behavior |
|----------|----------|
| **Edit Shared Node source** | **All instances update automatically** — change Skin Base once, every clip gets it |
| **Unlock on clip & tweak** | Local override — this clip gets custom Skin Base, others unchanged |
| **Re-lock if needed** | Lock again to re-sync with global definition |

**Marco's Insight:** *"So steuerst du Nodes auf Clip-Ebene, obwohl sie logisch auf einer anderen Ebene liegen – ohne ständig zwischen Ebenen zu wechseln."*

### 5. Recommended Shared Node Library
Create a standard set per project type:
```
Project Shared Nodes:
├── 01_Skin_Base          (Qualifier + protection)
├── 02_Sharpen_Final      (Blur/Sharpen, last node)
├── 03_Glow_Subtle        (OFX Glow, low intensity)
├── 04_NR_Clean           (Spatial NR, conservative)
├── 05_Film_Grain         (DCTL or OFX grain)
├── 06_Halation           (Custom/DCTL)
├── 07_Color_Density      (Hue vs Lum parallel)
└── 08_Output_Limiter     (CST + Gamut Map + Legalizer)
```

## Key Principles
| Principle | Application | Why It Works |
|-----------|-------------|--------------|
| **Centralize utilities** | One definition, infinite instances | Single source of truth for recurring grades |
| **Unlock for flexibility** | Default unlocked = per-clip tweak | Best of both: consistency + customization |
| **Clip/Group/Timeline agnostic** | Insert at any level | No more level-switching friction |
| **PowerGrade compatible** | Save Shared Node library as PowerGrade | Portable across projects/machines/team |

## Common Pitfalls & Fixes
| Symptom | Cause | Fix |
|---------|-------|-----|
| Shared Node changes don't propagate | Node is **Locked** on instances | Unlock instances, or re-insert unlocked |
| Can't edit Shared Node per clip | "Lock Node" checked on insert | Right-click instance → uncheck Lock |
| Accidentally changed global | Edited unlocked instance thinking it was local | Always verify Lock status; use "Save as Shared Node" to update global |
| Shared Node missing in new project | Not saved to PowerGrade / Global | Export as PowerGrade → import in new project |
| Too many Shared Nodes clutter menu | No naming convention | Prefix with numbers: `01_Skin`, `02_Sharpen` |

## Verification Checklist
- [ ] Create 3 utility nodes → Save as Shared Nodes (unlocked)
- [ ] Insert each on 5 different clips at Clip/Group/Timeline levels
- [ ] Edit global Shared Node → verify all 15 instances update
- [ ] Unlock one instance → tweak locally → verify others unchanged
- [ ] Save Shared Node library as PowerGrade → import to new project
- [ ] Timeline playback smooth — no performance hit from Shared Nodes

## References
- Source: Instagram @marcoherbst.work — "Shared Nodes in DaVinci Resolve = doppelt so schnell arbeiten" (29 weeks ago)
- Hashtags: #DaVinciResolve #ColorGrading #ColorGradingWorkflow #DaVinciResolveTutorial #PostProduction
- Type: Carousel post (multi-slide educational, German caption)

## Tags
```markdown
#davinci-resolve #shared-nodes #workflow-efficiency #node-structures #power-grade #clip-level #group-level #timeline-level #color-grading #marco-herbst #utility-nodes #centralized-grading
```