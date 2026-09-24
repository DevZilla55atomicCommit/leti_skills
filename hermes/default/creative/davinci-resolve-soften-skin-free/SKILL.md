---
name: davinci-resolve-soften-skin-free
description: "Free skin softening technique in DaVinci Resolve — Face Refinement + Circle Mask + Blur for smooth, natural skin without plugins."
version: 0.1.0
author: Hermes
metadata:
  hermes:
    tags: [DaVinci Resolve, Color Grading, Skin Softening, Face Refinement, Free Tools]
    source_url: "https://www.instagram.com/reel/DVKrbWNDThu/"
    source_creator: "@flynn.on.film"
    source_date: "2025-03-25"
    vault_category: "Creative Grading & Looks"
    skill_level: "Beginner"
    tags: [Skin Softening, Face Refinement, Circle Mask, Blur, Free, CDVC, Color Grading, Flynn on Film]
---

# DaVinci Resolve: Soften Skin for Free — @flynn.on.film (CDVC Day 23)

**Source:** [@flynn.on.film Instagram Reel](https://www.instagram.com/reel/DVKrbWNDThu/) — "CDVC | Day 23: How to Soften Skin (free)"

## Technique Overview

Free skin softening using **Face Refinement** + **Circle Mask** + **Blur** — no plugins required, works in Free version.

> **Series:** CDVC — Day 23 of color grading daily video course

---

## Node Structure

```
Node 01: Base Grade (Corrected)
Node 02: **SKIN SOFTEN** (Parallel via Layer Mixer)
  ├── Face Refinement OFX
  │   ├── Skin Smoothing: 0.3-0.5
  │   ├── Skin Tone: Auto/Manual
  │   └── Blur Radius: 5-10
  └── Circle Mask (on face)
      └── Blur OFX: Radius 8-15
Node 03: Layer Mixer
  ├── Input 1: Base Grade
  └── Input 2: Skin Soften (Composite: Normal, Opacity 50-70%)
Node 04: Output CST + Gamut Map
```

---

## Step-by-Step

### 1. Base Grade Complete (Node 01)
- Primary correction, creative grade done
- Skin tones verified on Vectorscope (11° line)

### 2. Create Skin Soften Layer (Node 02)
**Add Layer Mixer:**
- Right-click → **Add Layer Mixer** (parallel)
- Label: **"SKIN SOFTEN"**

**In Layer Mixer Input 2 (Top):**

#### A. Face Refinement OFX
| Setting | Value |
|---------|-------|
| **Skin Smoothing** | 0.3-0.5 |
| **Skin Tone** | Auto (or Manual pick) |
| **Blur Radius** | 5-10 |
| **Other settings** | Default |

#### B. Circle Mask (on Face Refinement node)
- Add **Circle Power Window** on Face Refinement node
- Position over face
- **Softness:** 0.8-0.9 (very feathered)
- **Size:** Cover face + neck

#### C. Blur OFX (on same node, after Face Refinement)
| Setting | Value |
|---------|-------|
| **Radius** | 8-15 (depends on resolution) |
| **HV Ratio** | 1.0 |

### 3. Layer Mixer Composite (Node 03)
| Setting | Value |
|---------|-------|
| **Composite Mode** | Normal |
| **Opacity** | 50-70% (start 60%) |
| **Layer Order** | Input 1 (Base) bottom, Input 2 (Soft) top |

### 4. Output CST + Gamut Map (Node 04)
- DWG → Rec.709 + Gamut Map (Sat, Max 0.92)

---

## Pro Tips

| Tip | Description |
|-----|-------------|
| **Circle Mask > Face Refinement alone** | Mask limits effect to face only, prevents background blur |
| **Opacity 50-70%** | Natural look — 100% looks plastic |
| **Face Refinement = Free** | Works in Free version (Studio has more features) |
| **Per-shot mask adjustment** | Track mask if subject moves |
| **Protect eyes/mouth** | Add small inverted mask on eyes/lips if needed |

---

## Comment Insights

| Comment | Insight |
|---------|---------|
| @cinemaddict_by_stsa | *"Oh my god I wasn't utilizing the circle mask while using color. Fudge that would've saved me weeks of work"* |
| @g_m_d_three | *"Entirely free??? Is your computer free, is the electric bill free..."* → **Free = no plugin cost** |
| @odee.film | *"Wow this is the solution to those Real Estate Agent Videos who wants their face smoother and cleaner"* |
| @cinemaddict_by_stsa | *"Saved me weeks of work"* |

---

## When to Use

| Scenario | Recommended |
|----------|-------------|
| **Interviews/Talking Heads** | ✅ Perfect |
| **Wedding Prep/Portraits** | ✅ Natural |
| **Beauty/Fashion** | ⚠️ May need more control |
| **Narrative/Drama** | ⚠️ May look too "smooth" |
| **Documentary** | ✅ Subtle cleanup |

---

## Related Techniques

- `davinci-resolve-masking-power-masking` — Power Masking with Magic Mask
- `davinci-resolve-color-warper-saturation-balance` — Color Warper for skin saturation
- `davinci-resolve-white-balance-helper-window-technique` — WB for skin tones

---

## Tags

`#davinciresolve` `#colorgrading` `#skin-softening` `#face-refinement` `#circle-mask` `#blur` `#free` `#cdvc` `#flynn-on-film` `#skin-retouching`