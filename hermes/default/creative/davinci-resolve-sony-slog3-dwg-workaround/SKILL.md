---
name: davinci-resolve-sony-slog3-dwg-workaround
description: "Sony S-Log3 Workaround in DaVinci Resolve — CST round-trip (S-Log3→DWG→S-Log3→Rec.709) fixes yellow/red color casts in highlights and skin tones when grading in DaVinci Wide Gamut. Grade between Node 1 & 2 in DWG."
version: 0.1.0
author: Hermes
metadata:
  hermes:
    tags: [DaVinci Resolve, Color Grading, Sony S-Log3, DaVinci Wide Gamut, CST, Workaround]
    source_url: "https://www.instagram.com/p/DSg1MJGDBVh/"
    source_creator: "@marcoherbst.work"
    source_date: "2025-01-10"
    vault_category: "S-Log3 / Sony Workflows"
    skill_level: "Intermediate"
    tags: [Sony S-Log3, DWG, CST, Color Cast, Workaround, PowerGrade, Marco Herbst]
---

# DaVinci Resolve: Sony S-Log3 DWG Workaround — @marcoherbst.work

**Source:** [@marcoherbst.work Instagram Post](https://www.instagram.com/p/DSg1MJGDBVh/) — "Wichtiger Sony S-Log3 Workaround in DaVinci Resolve!"

## Technique Overview

**Sony S-Log3 Workaround** for DaVinci Resolve — CST round-trip (S-Log3→DWG→S-Log3→Rec.709) fixes **yellow/red color casts in highlights and skin tones** when grading in DaVinci Wide Gamut. Grade between Node 1 & 2 in DWG.

> *"Wenn du in S-Log3 filmst und in DaVinci Wide Gamut graden willst, solltest du das hier wissen... Viele Sony-Shooter haben aktuell Probleme mit falschen Gelb- und Rot-Tönen, sobald sie ihr Material in DWG bringen und danach nach Rec.709 ausgeben."*

> **Language:** German (translated below)
> **Offer:** Comment "SONY" for PowerGrade

---

## The Problem

| Symptom | Cause |
|---------|-------|
| **False yellow tones** | S-Log3 + DWG interaction issue |
| **Red shift in highlights** | Warm light sources, skin tones turn reddish |
| **Washed out skin tones** | Unstable color in DWG → Rec.709 path |
| **Highlight color cast** | Gamut mapping instability |

---

## The Solution: CST Round-Trip

### Node Structure

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    SONY S-LOG3 DWG WORKAROUND                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐                │
│  │   NODE 01      │  │   NODE 02      │  │   NODE 03      │                │
│  │ "Slog3toDWG"   │──▶│ "DWGtoSlog3"   │──▶│ "Slog3toRec709"│                │
│  │                │  │                │  │                │                │
│  │ CST:           │  │ CST:           │  │ CST:           │                │
│  │ S-Log3 /       │  │ DWG /          │  │ S-Log3 /       │                │
│  │ S-Gamut3.cine  │  │ Intermediate   │  │ S-Gamut3.cine  │                │
│  │ → DWG /        │  │ → S-Log3 /     │  │ → Rec.709      │                │
│  │ Intermediate   │  │ S-Gamut3.cine  │  │ Gamma 2.4      │                │
│  └────────────────┘  └────────────────┘  └────────────────┘                │
│        │                    │                    │                          │
│        │         GRADE HERE (in DWG)           │                          │
│        │         between Node 1 & 2            │                          │
│        ▼                    ▼                    ▼                          │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Step-by-Step

| Step | Node | Label | CST Settings |
|------|------|-------|--------------|
| **1** | 01 | "Slog3toDWG" | **Input:** S-Log3 / S-Gamut3.cine → **Output:** DaVinci Wide Gamut / Intermediate |
| **2** | 02 | "DWGtoSlog3" | **Input:** DWG / Intermediate → **Output:** S-Log3 / S-Gamut3.cine |
| **3** | 03 | "Slog3toRec709" | **Input:** S-Log3 / S-Gamut3.cine → **Output:** Rec.709 / Gamma 2.4 |

### Critical Rule
> **Do ALL grading between Node 1 & Node 2** — in DaVinci Wide Gamut space

---

## Why It Works

| Mechanism | Explanation |
|-----------|-------------|
| **Forward CST** | S-Log3 → DWG (enters wide gamut) |
| **Grade in DWG** | Large gamut, full creative control |
| **Reverse CST** | DWG → S-Log3 (stabilizes color science) |
| **Output CST** | S-Log3 → Rec.709 (clean delivery transform) |

> *"Sony S-Log3 verhält sich aktuell in Kombination mit DWG problematisch – vor allem bei Gelb- und Rottönen. Durch die Hin- und Rückkonvertierung wird das Material erst korrekt in DWG 'stabilisiert', bevor es am Ende sauber nach Rec.709 transformiert wird."*

---

## Results

| Before Workaround | After Workaround |
|-------------------|------------------|
| ❌ False yellow tones | ✅ Clean, stable colors |
| ❌ Red shift in highlights | ✅ Natural highlight rendering |
| ❌ Washed out skin tones | ✅ Stable, natural skin tones |
| ❌ Unpredictable gamut map | ✅ Reliable Rec.709 output |

---

## Offer

> *"Du filmst mit Sony und willst den Workaround als PowerGrade? Kommentiere mit SONY – dann schicke ich dir das Powergrade!"*

---

## Related Techniques

- `davinci-resolve-slog3-cinematic-node-tree` — Kyle White 7-node S-Log3 workflow
- `davinci-resolve-slog3-3-node-cst-workflow` — Danny Gan minimal 3-node
- `davinci-resolve-apple-log2-workflow` — Dual-CST for Apple Log 2
- `davinci-resolve-cinematic-grading-3-mistakes` — CST pipeline mistakes

---

## Tags

`#davinciresolve` `#colorgrading` `#sony-slog3` `#dwg` `#cst` `#color-cast` `#workaround` `#powergrade` `#marcoherbst`