---
name: davinci-resolve-smooth-contrast-marco-herbst
description: Smooth Contrast in DaVinci Resolve — S-Curve in Custom Curves + Middle Gray DCTL for precise 18% gray anchoring, prevents crushing while achieving cinematic contrast
category: creative
tags: [davinci-resolve, contrast, curves, s-curve, middle-gray, dctl, marco-herbst, cinematic-look]
source_url: https://www.instagram.com/reel/DLNll2psFum/
author: marcoherbst.work
---

# DaVinci Resolve: Smooth Contrast — Marco Herbst

> **"Smooth Contrast in DaVinci Resolve – so geht's richtig!"** — marcoherbst.work
>
> *"Du willst diesen soften, cineastischen Look? Hier zeig ich dir, wie ich mit einer S-Curve und meinem Middle Gray DCTL einen perfekt ausbalancierten Kontrast erstelle – ohne das Bild zu 'crushen'."*

## Core Technique: S-Curve + Middle Gray Anchor

Traditional contrast crushes blacks and clips whites. Marco's method uses **Custom Curves S-Curve** anchored to **18% Middle Gray** via a DCTL for perfect tonal balance.

---

## Step-by-Step

### 1. Create Gentle S-Curve (Custom Curves)

```
Custom Curves → Master (RGB) / Luma:
    
    Output
    1.0 ┤           ╭─────
        │         ╱
    0.5 ┤───────╱        ← Middle Gray (18%) ANCHOR POINT
        │     ╱
    0.0 ┤____╱___________
        0.0   0.18  1.0
        Input (Luminance)
```

**Key:** The curve **must pass through 18% gray (0.18)** at the same output value — this preserves middle gray while expanding contrast above/below.

### 2. Check Before/After — Image Looks Darker?

After S-Curve, midtones often **appear darker** because contrast expanded around middle gray.

### 3. Middle Gray DCTL — The Fix

**Marco's Free DCTL** shows exactly where 18% gray sits on scopes.

```
DCTL: Middle Gray Reference
    ├── Overlays 18% gray line on Waveform
    ├── Overlays 18% gray point on Parade RGB
    └── Visual anchor for curve adjustment
```

**Get it:** Comment "Gray" on his post for free download.

### 4. Re-Anchor: Bring White Line Back to Origin

With DCTL visible:
1. See where middle gray shifted
2. **Adjust curve** so 18% gray input = 18% gray output
3. **Result:** Contrast expanded, middle gray preserved, no crush

---

## Why Middle Gray Matters

| Without Anchor | With 18% Gray Anchor |
|----------------|---------------------|
| Midtones shift unpredictably | Middle gray locked — consistent exposure |
| Skin tones drift | Skin (typically 40–60 IRE) stable |
| Hard to match shots | Shot matching via gray reference |
| "Crushed" look | **Smooth, cinematic contrast** |

---

## Node Structure

```
Node 01: CST (Log → Linear) + WB
    │
    ▼
Node 02: SMOOTH CONTRAST (Custom Curves)
    ├── S-Curve anchored at 0.18 in/out
    ├── Gentle roll-off highlights (0.8–1.0)
    ├── Gentle lift shadows (0.0–0.15)
    └── Middle Gray DCTL (guide only, disable for render)
    │
    ▼
Node 03: Creative Grade / LUT
    │
    ▼
Node 04: Output CST → Rec.709
```

---

## Pro Tips

| Tip | Why |
|-----|-----|
| **Use Luma-only curve** | Prevents color shifts (RGB curves can hue-shift) |
| **DCTL as guide only** | Disable/bypass before render — it's a visual tool |
| **Test on waveform** | Verify 18% gray line stays fixed pre/post curve |
| **Combine with Gain/Pivot** | For global exposure after contrast shape |

---

## Related Skills

- `davinci-resolve-primary-color-correction-workflow-linear` — Gain+Pivot contrast method (Waqas Qazi)
- `davinci-resolve-cinematic-grading-3-mistakes` — CST→DWG, Gain+Pivot, CST last (ey_cinema)
- `davinci-resolve-tone-curve-basics` — Tone curve fundamentals (huggyyx)

---

## Hashtags

#colorgrading #davinciresolve #coloristlife #gradingworkflow #contrastcurve #smoothcontrast #filmlook #resolveediting #filmmakingtips #colorgradingtools #davinciresolvetutorial #middlegray #customcurves #cinematiclook #reelcolorgrading #cinematographertools