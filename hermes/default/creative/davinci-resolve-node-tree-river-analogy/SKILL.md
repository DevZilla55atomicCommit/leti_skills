---
name: davinci-resolve-node-tree-river-analogy
description: "DaVinci Resolve node tree explained as a river — everything flows downstream, upstream changes affect downstream, nothing flows back up. Mental model for understanding node order."
version: 0.1.0
author: Hermes
metadata:
  hermes:
    tags: [DaVinci Resolve, Color Grading, Node Tree, Workflow, Mental Model]
    source_url: "https://www.instagram.com/reel/DTIgsSaDbEK/"
    source_creator: "@chrisbrockhurst"
    source_date: "2025-01-08"
    vault_category: "Node Structures & Templates"
    skill_level: "Beginner"
    tags: [Node Tree, River Analogy, Serial Nodes, Workflow, Chris Brockhurst]
---

# DaVinci Resolve: Node Tree as River — @chrisbrockhurst

**Source:** [@chrisbrockhurst Instagram Reel](https://www.instagram.com/reel/DTIgsSaDbEK/) — "If DaVinci Resolve nodes have ever felt confusing, think of them like a river."

## Technique Overview

**Mental model for understanding DaVinci Resolve node trees:** Think of nodes like a **river** — everything flows downstream. Changes upstream affect everything downstream; nothing flows back upstream.

> *"If DaVinci Resolve nodes have ever felt confusing, think of them like a river. Everything flows downstream. Any change you make upstream affects everything after it... But nothing flows back up the river."*

---

## The River Analogy

| River Concept | Node Tree Equivalent |
|---------------|---------------------|
| **Source** | Original footage (Log/raw) |
| **Upstream** | Early nodes (01, 02, 03...) |
| **Downstream** | Later nodes (05, 06, 07...) |
| **Current** | Image data flowing through nodes |
| **Tributary** | Parallel nodes (Layer/Parallel Mixer) |
| **Dam** | Node bypass / disable |
| **Delta** | Final output |

---

## Key Principles

### 1. Serial = Downstream Flow
```
Node 01 (CST) → Node 02 (WB) → Node 03 (Exposure) → Node 04 (Creative)
     ↑              ↑              ↑              ↑
   Source       Affects         Affects        Final
   (Log)        Node 02-04      Node 03-04     Look
```

### 2. Upstream Changes Propagate Down
- Change **Node 02 (WB)** → Affects Node 03, 04, 05...
- Change **Node 01 (CST)** → Affects **entire tree**
- Order matters: CST → WB → Exposure → Creative

### 3. Nothing Flows Upstream
- Node 04 creative **cannot** affect Node 02 WB
- Node 03 exposure **cannot** affect Node 01 CST
- To fix upstream: go back to that node

### 4. Each Node = Independent Adjustment
- Turn on/off to isolate effect
- No "stacking" like layers in Photoshop
- Clean, reversible, non-destructive

---

## Practical Application: Correct Order

| Order | Node | Purpose | Why This Order |
|-------|------|---------|----------------|
| **1st** | **CST** | Log → Working Space | All downstream ops in correct space |
| **2nd** | **WB/Exposure** | Primary balance | Clean base for creative |
| **3rd** | **Contrast/Sat** | Image structure | Foundation for look |
| **4th** | **Creative** | Split tone, LUT, look | On balanced foundation |
| **5th** | **Polish** | Grain, halation, vignette | Final touches |
| **Last** | **Output CST** | Working → Delivery | After all grading |

---

## Parallel Nodes = Tributaries

```
Main River (Serial):  01→02→03→04→05→Output
                         │
                    ┌────┴────┐
                    ▼         ▼
              Tributary   Tributary
            (Parallel)  (Parallel)
            Skin Grade  BG Grade
                    │         │
                    └────┬────┘
                         ▼
                   Layer Mixer
                    (Confluence)
                         │
                       Output
```

---

## Common Beginner Mistakes

| Mistake | River Analogy | Fix |
|---------|---------------|-----|
| Creative before CST | Building dam before source | CST first |
| WB after creative | Changing water color at delta | WB early |
| Fixing upstream by tweaking downstream | Digging downstream to fix source | Go to source node |
| Too many serial nodes | River too long, loses clarity | Use parallel/layer mixers |

---

## Why This Mental Model Works

| Concept | Without Model | With River Model |
|---------|---------------|------------------|
| **Node Order** | Confusing, arbitrary | Logical: upstream→downstream |
| **Troubleshooting** | Random tweaking | Trace upstream to source |
| **Parallel Nodes** | "What's a layer mixer?" | Tributaries joining main river |
| **Non-Destructive** | "How undo works?" | Water always from source |

---

## Comments Insights

| Comment | Insight |
|---------|---------|
| @not_joros: *"In any order?"* | **No — order matters** (upstream→downstream) |
| @cerocta: *"This always confuses me"* | Common pain point — river model clarifies |
| @trav_inspire: *"Why nodes? I grade without them"* | Layers = destructive; Nodes = river = non-destructive |
| @dd_khan889: *"Watched alot of videos but this one helped"* | Simple analogies beat technical jargon |
| @stevewisepark: *"Detailed ✅"* | |

---

## Related Techniques

- `davinci-resolve-cinematic-grading-3-mistakes` — Node structure, exposure order, color management
- `davinci-resolve-magicgrade-workflow-blueprint` — F-key keyboard-driven node template
- `davinci-resolve-simple-4-step-workflow` — 4-step balance workflow

---

## Tags

`#davinciresolve` `#colorgrading` `#node-tree` `#river-analogy` `#serial-nodes` `#workflow` `#chrisbrockhurst` `#mental-model`