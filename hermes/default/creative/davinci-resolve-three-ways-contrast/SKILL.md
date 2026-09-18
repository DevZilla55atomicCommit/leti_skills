---
name: davinci-resolve-three-ways-contrast
description: "DaVinci Resolve 3 Ways to Build Contrast: Contrast/Pivot, Lift/Gamma/Gain, Custom Curves with Middle Gray DCTL"
version: 0.1.0
author: Hermes
metadata:
  hermes:
    tags: [DaVinci Resolve, Color Grading, Contrast, Pivot, Lift Gamma Gain, Custom Curves, Middle Gray, DCTL, Creative Grading]
---

# DaVinci Resolve — 3 Ways to Build Contrast

Learn **3 professional contrast methods** from @marcoherbst.work — Contrast/Pivot (technical), Lift/Gamma/Gain (visual/filmic), Custom Curves with Middle Gray DCTL (maximum control).

## When to Use
- Any grading session needing contrast structure
- Choosing the right contrast tool for the job
- Understanding how each method affects image differently
- DWG (DaVinci Wide Gamut) workflow optimization

## Prerequisites
- DaVinci Resolve (Free or Studio) 18+
- Basic Color Page navigation
- Understanding of tonal ranges (shadows/midtones/highlights)

## Quick Reference

| Method | Tool | Best For | Control Level |
|--------|------|----------|---------------|
| **1. Contrast & Pivot** | Primaries → Contrast + Pivot | Fast, technically clean contrast | Medium |
| **2. Lift / Gamma / Gain** | Primaries Wheels | Visual, filmic look design | High (artistic) |
| **3. Custom Curves + Middle Gray DCTL** | Curves + DCTL | Maximum precision, separation | Maximum |

---

## Procedure

### Method 1: Contrast & Pivot (Primaries Panel)
**Technically clean, fast contrast control**

| Setting | Value | Why |
|---------|-------|-----|
| **Working Space** | DaVinci Wide Gamut (DWG) | Required for correct pivot |
| **Pivot** | **0.336** | Middle Gray point in DWG (not 0.5!) |
| **Contrast** | Adjust to taste | Expands around pivot |

**Marco's Insight:** *"Wenn du im DaVinci Wide Gamut arbeitest, stell den Pivot auf 0.336 – der korrekte Middle-Gray-Punkt für DWG. Danach kannst du über den Contrast-Slider den grundsätzlichen Punch setzen."*

**Why 0.336?** DWG encodes middle gray at ~0.336 (not 0.5 like Rec.709). Pivot at 0.5 in DWG shifts midtones incorrectly.

---

### Method 2: Lift / Gamma / Gain (Primaries Wheels)
**Visual, filmic contrast — shape the look by feel**

| Wheel | Tonal Range | Creative Control |
|-------|-------------|------------------|
| **Lift** | Shadows (0–25%) | Crush blacks, add color tint to darks |
| **Gamma** | Midtones (25–75%) | Core contrast, skin tone brightness |
| **Gain** | Highlights (75–100%) | Protect/sculpt highlights, add specular pop |

**Workflow:**
1. Set **Gamma** first — establishes midtone contrast
2. Adjust **Lift** — shadow depth/tint
3. Adjust **Gain** — highlight rolloff/protection
4. Iterate — three wheels interact organically

**Marco's Insight:** *"Das Zusammenspiel der drei Wheels erzeugt einen organischen, cineastischen Look. Ideal, wenn du Look & Feeling bewusst gestalten willst."*

---

### Method 3: Custom Curves + Middle Gray DCTL
**Maximum control, perfect tonal separation**

**Step 1: Middle Gray DCTL**
- Apply **Middle Gray DCTL** (free, available online)
- Sets **exact mid-gray reference** (0.336 in DWG, 0.5 in Rec.709)
- Visual confirmation: middle gray sits at correct IRE

**Step 2: Custom Curves (Editable Spline)**
- Open **Custom Curves** → Master (or Luma)
- Create **S-curve** with precise control points:
  - Shadow point (~10–15%): pull down for depth
  - Mid-gray anchor (33.6% in DWG): **lock to DCTL reference**
  - Highlight point (~85–90%): pull up for separation
- **Editable Spline** = smooth, natural rolloff

**Marco's Insight:** *"Über einen Middle Gray DCTL bestimmst du zuerst den exakten Mid-Gray-Punkt. Dann passt du den Kontrast über die Custom Curves an oder erstellst mit Editable Spline eine saubere S-Curve. Maximale Kontrolle und perfekte Separation zwischen Light & Dark."*

---

## Comparison & When to Use Which

| Scenario | Recommended Method | Why |
|----------|-------------------|-----|
| **Quick technical balance** | Contrast & Pivot (Pivot=0.336) | Fast, mathematically correct in DWG |
| **Creative look development** | Lift/Gamma/Gain | Organic interaction, filmic feel |
| **Precision grading / HDR** | Custom Curves + Middle Gray DCTL | Frame-accurate, repeatable, maximum separation |
| **Matching shots** | Custom Curves | Copy/paste curve points for consistency |
| **Teaching/learning** | All three | Understand how each shapes tone differently |

---

## Key Principles

| Principle | Application |
|-----------|-------------|
| **Pivot = Middle Gray** | In DWG, middle gray ≠ 0.5 — it's 0.336. Wrong pivot = tonal shift |
| **Three wheels = organic** | Lift/Gamma/Gain interact like film response curves |
| **Curves = surgical** | Every point adjustable; anchor mid-gray for stability |
| **DCTL = reference** | Middle Gray DCTL removes guesswork from curve anchor |

---

## Common Pitfalls & Fixes

| Symptom | Cause | Fix |
|---------|-------|-----|
| Midtones shift weird with Contrast | Pivot at 0.5 in DWG | Set Pivot = **0.336** for DWG |
| Shadows crushed / highlights blown | Contrast slider too aggressive | Use Curves for gradual rolloff |
| Look feels "video" not "film" | Only used Contrast slider | Add Lift/Gamma/Gain shaping |
| Can't match shot-to-shot | Contrast slider values don't translate | Use Custom Curves — copy point values |
| Middle gray unknown | No reference | Apply **Middle Gray DCTL** first |

---

## Verification Checklist

- [ ] In DWG project: Contrast Pivot set to **0.336** (not 0.5)
- [ ] Can build contrast with each method independently
- [ ] Middle Gray DCTL shows correct mid-gray IRE
- [ ] Custom Curve S-curve anchored at mid-gray reference
- [ ] Shot match: Copy curve points → consistent contrast across clips
- [ ] Toggle each method → see distinct "character" of contrast

---

## References

- Source: Instagram @marcoherbst.work — "3 Wege, wie du perfekten Kontrast in DaVinci Resolve aufbaust" (34 weeks ago)
- Hashtags: #davinciresolve #davinciresolvetutorial #davinciresolveediting #colorgrading #colorist #colorgradingtips #colorgradingtutorial #filmlook #cinematiclook #cinematiccolor #colorgradingworkflow #filmmaking #filmmakersworld #gradingworkflow #learncolorgrading #hdrgrading #creativegrading #filmmaker #filmmakersworld #gradeSociety #marcoherbst #colorgradingreels #dslrvideos #editorlife #resolvecommunity
- Type: Carousel post (multi-slide educational, German caption)

---

## Tags

```markdown
#davinci-resolve #contrast #pivot #lift-gamma-gain #custom-curves #middle-gray #dctl #davinci-wide-gamut #creative-grading #color-grading #marco-herbst #workflow #educational
```