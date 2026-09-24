---
name: davinci-resolve-four-essential-node-types
description: "DaVinci Resolve 4 Essential Node Types: Serial, Parallel, Layer Mixer, Outside Node — foundation for clean professional grading workflows"
version: 0.1.0
author: Hermes
metadata:
  hermes:
    tags: [DaVinci Resolve, Color Grading, Node Structures, Serial Node, Parallel Node, Layer Mixer, Outside Node, Educational, Workflow]
---

# DaVinci Resolve — 4 Essential Node Types

Learn the **4 fundamental node types** from @marcoherbst.work — the foundation every colorist must master for clean, professional, efficient grading workflows.

## When to Use
- Building any node tree from scratch
- Teaching/learning Resolve node architecture
- Debugging why a grade behaves unexpectedly
- Optimizing workflow for speed and clarity

## Prerequisites
- DaVinci Resolve (Free or Studio) 18+
- Basic Color Page navigation

## Quick Reference

| Node Type | Icon | Purpose | Key Behavior |
|-----------|------|---------|--------------|
| **Serial** | → | Linear chain | Each node builds on previous output |
| **Parallel** | ║ | Independent branches | All inputs feed from same source |
| **Layer Mixer** | ☐+☐ | Composite with blend modes | Photoshop-like layer compositing |
| **Outside** | ⊘ | Invert previous mask | Auto-inverts predecessor's qualifier/window |

---

## Procedure

### 1️⃣ Serial Node — The Workhorse
**Purpose:** Linear, step-by-step processing where each operation depends on the previous.

```
INPUT → [WB] → [Exposure] → [Contrast] → [Look] → OUTPUT
        ↑        ↑           ↑           ↑
      Node 1   Node 2      Node 3      Node 4
```

| Characteristic | Detail |
|----------------|--------|
| **Flow** | Downstream only — output of N becomes input of N+1 |
| **Use For** | White Balance → Exposure → Contrast → Creative Look → Output CST |
| **Order Matters** | Yes — changing Node 2 affects everything after |
| **Analogy** | River: everything flows downstream |

**Marco's Insight:** *"Sie verarbeitet dein Bild Schritt für Schritt in Reihenfolge. Jede Node baut auf der vorherigen auf. Ideal für lineare Korrekturen wie White Balance → Exposure → Contrast → Look."*

### 2️⃣ Parallel Node — Independent Branches
**Purpose:** Apply different corrections to different image areas simultaneously, all feeding from the **same source**.

```
INPUT → PARALLEL MIXER → OUTPUT
         ├─→ [Skin Grade]
         ├─→ [Sky Grade]
         └─→ [BG Grade]
```

| Characteristic | Detail |
|----------------|--------|
| **Flow** | All branches receive **identical input** (the node before Parallel Mixer) |
| **Independence** | Branches don't affect each other |
| **Composite** | Parallel Mixer blends results (Normal, Add, Multiply, etc.) |
| **Use For** | Skin vs Sky vs Background — separate grades, same source |

**Marco's Insight:** *"Perfekt, um verschiedene Bereiche separat zu korrigieren, ohne dass sie sich gegenseitig beeinflussen – zum Beispiel Haut, Himmel oder Kleidung."*

### 3️⃣ Layer Mixer — Photoshop-Style Compositing
**Purpose:** Composite multiple grades using **blend modes** (Normal, Overlay, Soft Light, Multiply, Screen, etc.) — like Photoshop layers.

```
LAYER MIXER
├── Input 1 (Bottom): Base Grade
├── Input 2: Look Grade (Overlay 50%)
├── Input 3: Grain (Soft Light)
└── Input 4: Vignette (Multiply)
```

| Characteristic | Detail |
|----------------|--------|
| **Blend Modes** | Full set: Normal, Add, Multiply, Screen, Overlay, Soft Light, etc. |
| **Opacity** | Per-input opacity control |
| **Order** | Bottom → Top (like layer stack) |
| **Use For** | Creative look stacking, texture overlays, controlled composites |

**Marco's Insight:** *"Damit kannst du Nodes wie in Photoshop mischen und Compositing-Modi nutzen. Super für komplexe Look-Builds und kreative Grading-Strukturen."*

### 4️⃣ Outside Node — Auto-Invert Mask
**Purpose:** Automatically inverts the **qualifier/window** of the **immediately preceding node** — grade inside vs. outside a mask without manual inversion.

```
[Node N: Power Window on Face] → [Outside Node] → Grades BACKGROUND only
                                    ↑
                              Auto-inverts Node N's mask
```

| Characteristic | Detail |
|----------------|--------|
| **Magic** | Reads predecessor's Key Output → inverts automatically |
| **No Manual Invert** | Don't check "Invert" — Outside Node does it |
| **Chainable** | Serial: Mask → Outside → Outside → ... alternates |
| **Use For** | Face vs Background, Sky vs Ground, Product vs Environment |

**Marco's Insight:** *"Sie invertiert automatisch die Maske der vorherigen Node. Damit kannst du Innen und Außen getrennt bearbeiten, etwa: Gesicht heller, Hintergrund dunkler – präzise und schnell."*

---

## Key Principles

| Principle | Application | Why It Matters |
|-----------|-------------|----------------|
| **Serial = Dependency** | WB before Exposure before Look | Downstream inherits upstream decisions |
| **Parallel = Independence** | Skin/Sky/BG from same source | No cross-contamination between zones |
| **Layer Mixer = Composite** | Blend modes + opacity | Creative stacking, not just correction |
| **Outside = Auto-Invert** | One mask → two grades | Fast inside/outside without duplicate windows |

---

## Common Pitfalls & Fixes

| Symptom | Cause | Fix |
|---------|-------|-----|
| Grade affects wrong area | Used Serial when needed Parallel | Insert Parallel Mixer for zone isolation |
| Blend mode not working | Used Parallel instead of Layer Mixer | Swap to Layer Mixer for blend modes |
| Outside Node grades nothing | Predecessor has no Key Output | Enable Key Output on mask node |
| Order confusion in Layer Mixer | Forgot bottom→top = back→front | Label inputs: Base, Look, Texture, Vignette |
| Parallel branches affect each other | Accidentally serial-chained inside branch | Each branch must start fresh from Parallel Mixer input |

---

## Verification Checklist

- [ ] Can explain Serial vs Parallel vs Layer Mixer vs Outside in one sentence each
- [ ] Build a tree: Serial (WB→Exp) → Parallel (Skin/Sky/BG) → Layer Mixer (Grain/Vignette)
- [ ] Use Outside Node to grade background after Power Window on subject
- [ ] Debug a broken grade by tracing node types upstream
- [ ] Save 4-node template as Compound Node → PowerGrade for new projects

---

## References

- Source: Instagram @marcoherbst.work — "4 wichtigsten Node-Typen in DaVinci Resolve" (30 weeks ago)
- Hashtags: #DaVinciResolve #ColorGrading #NodeTree #DaVinciResolveTutorial #Colorist
- Type: Carousel post (multi-slide educational, German caption)
- Call to action: Comment "NODETREE" for free Future Proof Nodetree PDF

---

## Tags

```markdown
#davinci-resolve #node-types #serial-node #parallel-node #layer-mixer #outside-node #node-structures #workflow #educational #color-grading #marco-herbst #foundation
```