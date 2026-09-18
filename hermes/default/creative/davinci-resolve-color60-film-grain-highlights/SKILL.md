---
name: davinci-resolve-color60-film-grain-highlights
description: "COLOR60 Day 11/60: Film grain technique — grain strongest in highlights, less in midtones, least in shadows. Advanced grain controls for cinematic film emulation."
version: 0.1.0
author: Hermes
metadata:
  hermes:
    tags: [DaVinci Resolve, Color Grading, Film Grain, Film Emulation, COLOR60]
    source_url: "https://www.instagram.com/reel/DTcRb3kjrMf/"
    source_creator: "@officialjonathankim"
    source_date: "2025-01-15"
    vault_category: "Creative Grading & Looks"
    skill_level: "Intermediate"
    tags: [Film Grain, Film Emulation, COLOR60, Highlights, Midtones, Shadows, Jonathan Kim]
---

# DaVinci Resolve: COLOR60 Day 11 — Film Grain Distribution — @officialjonathankim

**Source:** [@officialjonathankim Instagram Reel](https://www.instagram.com/reel/DTcRb3kjrMf/) — "DAY 11/60: COLOR60"

## Technique Overview

Film grain technique for cinematic emulation — **grain is usually strongest in highlights, less in midtones, and least in shadows** for movies shot on film. Advanced grain controls in DaVinci Resolve for per-project fine-tuning.

> *"Today's video is about film grain. It's hard to really see grain on YouTube or Instagram, so next time you're in a theater watching a movie shot on film, pay attention to where the grain is strongest."*

> **Series:** COLOR60 — Day 11 of 60

---

## Film Grain Distribution (Real Film Behavior)

| Region | Grain Amount | Reason |
|--------|--------------|--------|
| **Highlights** | **Strongest** | Highlight detail + grain most visible |
| **Midtones** | **Medium** | Balanced grain presence |
| **Shadows** | **Least** | Shadow grain less visible, crushed |

> *"For movies shot on film, grain is usually strongest in the highlights, less in the midtones, and the least in the shadows."*

---

## DaVinci Resolve Film Grain OFX Settings

### Location
OpenFX → **Film Grain** (Studio version) or **Grain** (Free version)

### Recommended Settings for Filmic Distribution

| Parameter | Value | Effect |
|-----------|-------|--------|
| **Type** | Kodak / Fuji / Custom | Film stock emulation |
| **Size** | 0.8-1.2 | Grain particle size |
| **Strength (Highlights)** | **Higher** (e.g., 0.6-0.8) | Strongest grain in highlights |
| **Strength (Midtones)** | **Medium** (e.g., 0.4-0.6) | Balanced grain |
| **Strength (Shadows)** | **Lower** (e.g., 0.2-0.4) | Minimal grain in shadows |
| **Color/Gray** | Color | Chromatic grain (more filmic) |
| **ISO** | 400-800 | Film speed equivalent |

---

## Advanced Controls (Per Project Fine-Tuning)

| Control | Use Case |
|---------|----------|
| **Highlight Grain** | Boost for bright scenes, reduce for night |
| **Midtone Grain** | Balance overall texture |
| **Shadow Grain** | Keep clean for low-light |
| **Red/Green/Blue channels** | Color-specific grain (Kodak = more blue grain) |
| **Roughness** | Grain sharpness vs softness |
| **Seed** | Different grain pattern per shot |

---

## Node Placement

```
Node 01: CST (Log → DWG)
Node 02: Primary Balance
Node 03: Creative Look
...
Node N-1: **FILM GRAIN OFX** (last creative node)
Node N: Output CST (DWG → Rec.709)
```

> **Critical:** Apply grain **after** creative grade, **before** output CST
> - Grain in working space (DWG) = correct scaling
> - Grain after output CST = wrong size/distribution

---

## Comment Debates (Scientific Accuracy)

| Comment | Claim | Reality |
|---------|-------|---------|
| @lucas_arnaud | *"Shadows have more grain, highlights less — literally opposite"* | **Debate exists** — varies by film stock, exposure, development |
| @sh4.mil__ | *"Isn't it the opposite? Shadows have more grains"* | **Kodak Vision3**: Highlights show more grain due to photon statistics |
| @jonathankim | *"Pay attention in theater — highlights show most grain"* | **Practical observation** from theatrical projection |

**Consensus:** Test per stock. Jonathan Kim's observation = **theatrical projection experience** (Kodak Vision3 print film).

---

## Export Settings for Social Media (Reels/IG)

| Setting | Recommendation |
|---------|----------------|
| **Bitrate** | High (50-100 Mbps) |
| **Codec** | H.265/HEVC if supported |
| **Grain Preservation** | Disable platform compression preview |
| **Sharpening** | Minimal (grain provides texture) |

> **Comment @sh4.mil__:** *"Can you teach grain & export settings for reels? IG compressed my reel but I've seen reels with crisp grain."*

---

## Related Techniques

- `davinci-resolve-ivarbrauer-film-look-lut-powergrade` — Film LUT pack includes grain
- `davinci-resolve-kodak-2383-gabe-lomotey` — DWG + DCTLs + Dehancer grain workflow
- `davinci-resolve-cinematic-look-post-production-philosophy` — 9-node template includes grain

---

## Tags

`#davinciresolve` `#colorgrading` `#film-grain` `#film-emulation` `#color60` `#officialjonathankim` `#highlights` `#midtone` `#shadows`