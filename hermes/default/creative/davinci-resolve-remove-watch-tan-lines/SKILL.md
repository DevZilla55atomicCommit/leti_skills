---
name: davinci-resolve-remove-watch-tan-lines
description: "Remove watch tan lines in DaVinci Resolve — Power Window + Qualifier + Blur technique for wedding video cleanup."
version: 0.1.0
author: Hermes
metadata:
  hermes:
    tags: [DaVinci Resolve, Color Grading, Watch Tan Lines, Power Window, Wedding, Object Removal]
    source_url: "https://www.instagram.com/reel/DVY_NkCETox/"
    source_creator: "@brattphotoandfilm"
    source_date: "2025-03-02"
    vault_category: "Creative Grading & Looks"
    skill_level: "Beginner to Intermediate"
    tags: [Watch Tan Lines, Power Window, Qualifier, Blur, Wedding Video, Object Removal, Bratt Photo & Film]
---

# DaVinci Resolve: Remove Watch Tan Lines — @brattphotoandfilm

**Source:** [@brattphotoandfilm Instagram Reel](https://www.instagram.com/reel/DVY_NkCETox/) — "Here's a quick tutorial on how to remove watch tan line lines in DaVinci Resolve"

## Technique Overview

Quick cleanup technique for removing watch tan lines on wrists in wedding videos using **Power Window + Qualifier + Blur** — simple, effective, wedding-specific.

> "If you told me when I first started that I'd be able to remove things like this out of wedding videos this easy I'd call you crazy" — @brattphotoandfilm

---

## Node Structure

```
Node 01: Base Grade (Corrected)
Node 02: **TAN LINE REMOVAL** (Serial)
  ├── Power Window (Circle on wrist)
  ├── Qualifier (Skin tone within window)
  ├── Blur OFX (Radius 15-25)
  └── Composite: Normal
Node 03: Optional — Skin Protection (Layer Mixer)
Node 04: Output CST + Gamut Map
```

---

## Step-by-Step

### 1. Create Tan Line Removal Node (Node 02)
- Add Serial Node after base grade
- Label: **"WATCH TAN REMOVAL"**

### 2. Power Window (Circle on Wrist)
| Setting | Value |
|---------|-------|
| **Shape** | Circle |
| **Position** | Over watch tan line on wrist |
| **Size** | Slightly larger than tan line |
| **Softness** | **0.6-0.8** (feathered edge) |

### 3. Qualifier (Within Power Window)
- Switch to **Qualifier** panel (eyedropper)
- **Pick skin tone** within the circle
- **Luma Range:** Mid-tones (avoid highlights/shadows)
- **Sat Range:** Wide (capture all skin)
- **Hue Range:** Narrow around skin hue (~30-40°)

### 4. Blur OFX (Inside Qualified Area)
| Setting | Value |
|---------|-------|
| **Radius** | **15-25** (resolution dependent) |
| **HV Ratio** | 1.0 |
| **Border** | Replicate |

### 5. Optional: Layer Mixer for Skin Protection
```
Layer Mixer
├── Input 1: Grade + Tan Removal
└── Input 2: Skin Protection
    └── Qualifier: Skin tones (Hue 25-45°)
    └── Composite: Normal, Opacity 50%
```

---

## Pro Tips

| Tip | Description |
|-----|-------------|
| **Track the window** | If wrist moves, use Tracker → Track Forward |
| **Softness 0.7+** | Prevents hard edge on wrist |
| **Blur 20-30** | Smooth blend, adjust per resolution |
| **Per-shot adjust** | Tan line intensity varies — tweak blur radius |
| **Qualifier first** | Isolates skin, prevents background blur |

---

## When to Use

| Scenario | Recommended |
|----------|-------------|
| **Groom prep shots** | ✅ Perfect |
| **Bride getting ready** | ✅ Common |
| **Ceremony close-ups** | ⚠️ May be visible |
| **Reception dancing** | ⚠️ Motion blur issues |
| **Detail rings shots** | ✅ Often needed |

---

## Community Discussion

Post also sparked Premiere Pro vs DaVinci Resolve debate in comments — creator switched from Premiere to DaVinci "couple years back because DaVinci obviously blew premiere pro out of the water at the time."

---

## Related Techniques

- `davinci-resolve-masking-power-masking` — Power Masking with Magic Mask
- `davinci-resolve-realistic-wall-shadows-power-window` — Power Window tracking
- `davinci-resolve-wedding-film-look` — Wedding film look LUT

---

## Tags

`#davinciresolve` `#colorgrading` `#watch-tan-lines` `#power-window` `#qualifier` `#blur` `#wedding-video` `#object-removal` `#brattphotoandfilm`