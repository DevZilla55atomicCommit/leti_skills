---
name: davinci-resolve-gamma-2-2-vs-2-4-cdvc
description: "CDVC Day 34: Gamma 2.2 vs Gamma 2.4 — understanding output gamma standards, display calibration, and when to use each for color grading delivery."
version: 0.1.0
author: Hermes
metadata:
  hermes:
    tags: [DaVinci Resolve, Color Grading, Gamma, Output, Delivery, Display Calibration]
    source_url: "https://www.instagram.com/reel/DWNldJnjTG3/"
    source_creator: "@flynn.on.film"
    source_date: "2025-04-20"
    vault_category: "Color Correction Fundamentals"
    skill_level: "Intermediate"
    tags: [Gamma, Gamma 2.2, Gamma 2.4, Output Gamma, Display Calibration, CDVC, Color Grading Delivery, Flynn on Film]
---

# DaVinci Resolve: Gamma 2.2 vs Gamma 2.4 — CDVC Day 34

**Source:** [@flynn.on.film Instagram Reel](https://www.instagram.com/reel/DWNldJnjTG3/) — "CDVC | Day 34: Gamma 2.2 vs Gamma 2.4"

## Technique Overview

Understanding the difference between **Gamma 2.2** and **Gamma 2.4** for output delivery — critical for consistent viewing across different displays and platforms.

> **Series:** CDVC (Color Grading Daily Video Course?) — Day 34
> **Comments highlight:** Confusion about gamma standards, export settings, display P3 vs Rec.709

---

## Gamma Standards Explained

| Gamma | Standard | Typical Use | Display Target |
|-------|----------|-------------|----------------|
| **2.2** | sRGB / Rec.709 (legacy) | Web, computer monitors, mobile | Standard office/consumer displays |
| **2.4** | Rec.709 / BT.1886 (modern) | Broadcast, TV, cinema, streaming | Reference monitors, calibrated TVs |

---

## Why It Matters

| Aspect | Gamma 2.2 | Gamma 2.4 |
|--------|-----------|-----------|
| **Midtone Brightness** | Brighter midtones | Darker midtones |
| **Shadow Detail** | More visible | Compressed |
| **Highlight Roll-off** | Gentler | Steeper |
| **Perceived Contrast** | Lower | Higher |
| **Standard** | sRGB (computers) | BT.1886 (TV/broadcast) |

---

## When to Use Which

### Use **Gamma 2.2** when:
- Delivering for **web/social media** (YouTube, Instagram, Vimeo)
- Target is **computer monitors, phones, tablets**
- Working in **sRGB** color space
- Client views on **standard office displays**

### Use **Gamma 2.4** when:
- Delivering for **broadcast/TV/streaming** (Netflix, broadcast)
- Target is **calibrated reference monitors** or **consumer TVs**
- Working in **Rec.709** with **BT.1886** compliance
- **Cinema/DCP** workflows (often 2.6, but 2.4 for Rec.709 trim)

---

## DaVinci Resolve Settings

### Project Settings → Color Management
| Setting | Value |
|---------|-------|
| **Timeline Color Space** | Rec.709 Gamma 2.4 (or 2.2) |
| **Output Color Space** | Match timeline |
| **Use Mac Display Color Profile** | OFF (for accurate grading) |

### Delivery Page → Advanced Settings
| Format | Gamma Setting |
|--------|---------------|
| **H.264/H.265 (Web)** | **2.2** (or leave auto) |
| **ProRes/DNx (Broadcast)** | **2.4** |
| **DCP** | 2.6 (XYZ) |

---

## Common Confusion (Per Comments)

**@mmczwski:** *"How tf do you know all of this? Like where can we find a table that just shows the standard output for these channels?"*
→ **Answer:** BT.1886 / BT.2100 standards documents; Resolve manual; ICC profiles

**@seynoia:** *"I just use display P3, I find that when I use 2.2 or 2.4 my grades are gone when I view it on my phone"*
→ **Explanation:** Display P3 uses ~2.2 gamma. If you grade in 2.4 but view on phone (2.2), image looks darker/muddy. **Match grading gamma to delivery gamma.**

**@alexius_ide:** *"Or just set it in the export page"*
→ **Partial truth:** Export gamma tag helps, but **grading monitor must match** for accurate decisions.

---

## Best Practice Workflow

1. **Grade on calibrated reference monitor** at target gamma (2.4 for broadcast, 2.2 for web)
2. **Set Project → Timeline Color Space** to match delivery gamma
3. **Grade in that gamma** — don't grade 2.2 and export 2.4
4. **Delivery Page → Advanced → Gamma** = match timeline
5. **Tag metadata correctly** in export (Rec.709 + gamma tag)

---

## Gamma 2.2 vs 2.4 Visual Difference

```
Luminance Response:
1.0 ┤              Gamma 2.2 (brighter mids)
    │            ╱
0.5 ┤          ╱    Gamma 2.4 (darker mids)
    │        ╱
0.0 ┼──────╱─────────────────
    0.0   0.5   1.0
        Input Signal
```

---

## Related Techniques

- `davinci-resolve-cst-gamut-mapping-color-spill` — Output CST with gamut mapping
- `davinci-resolve-white-balance-luma-mix` — Linear grading foundation
- `davinci-resolve-cinematic-look-post-production-philosophy` — Full pipeline

---

## Tags

`#davinciresolve` `#colorgrading` `#gamma` `#gamma-2-2` `#gamma-2-4` `#output-gamma` `#display-calibration` `#delivery` `#broadcast` `#web-delivery` `#cdvc` `#flynn-on-film`