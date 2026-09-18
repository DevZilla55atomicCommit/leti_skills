---
name: tone-curve-mastery-retouching
description: "Tone Curve Mastery — comprehensive guide to tone curves for exposure and color control, from retouchingpanels/retouchingacademy"
version: 0.1.0
author: Hermes
metadata:
  hermes:
    tags: [Tone Curve, Color Grading, Exposure, Retouching, Photoshop, Lightroom, Educational, Photography]
---

# Tone Curve Mastery — Retouching Panels / Retouching Academy

Comprehensive educational content on **Tone Curve mastery** from @retouchingpanels (featuring @mypicturesbox and @retouchingacademy) — the most powerful tool for exposure and color control in photo/video editing.

## When to Use
- Learning tone curve fundamentals (beginner to advanced)
- Understanding RGB channel curves for color grading
- Translating curve knowledge across tools (PS, LR, Resolve)
- Professional retouching workflow integration

## Prerequisites
- Basic exposure/contrast understanding
- Photoshop, Lightroom, or DaVinci Resolve
- Willingness to practice curve manipulation

## Quick Reference

| Curve Type | Tool | Best For |
|------------|------|----------|
| **Master/Composite** | All | Global contrast, brightness |
| **Red Channel** | PS/LR/Resolve | Cyan/Red balance, skin tones |
| **Green Channel** | PS/LR/Resolve | Magenta/Green balance |
| **Blue Channel** | PS/LR/Resolve | Yellow/Blue balance, mood |
| **Parametric (LR)** | Lightroom | Regional (Highlights/Lights/Darks/Shadows) |
| **Point Curve (LR/PS)** | LR/PS/Resolve | Custom shapes, precise control |

---

## Core Concepts

### 1. The Curve Graph
- **X-axis:** Input (original tones: Shadows → Midtones → Highlights)
- **Y-axis:** Output (result tones: Darker → Brighter)
- **Diagonal line:** Neutral (no change)
- **Above diagonal:** Brightening
- **Below diagonal:** Darkening

### 2. Standard Curve Shapes

| Shape | Name | Effect | Use Case |
|-------|------|--------|----------|
| **S-curve** | Contrast | Deepen shadows, brighten highlights | Most grades |
| **Inverted S** | Flat/Log | Lift shadows, lower highlights | HDR prep, film scan |
| **Single hump** | Midtone contrast | Boost midtone separation | Portraits, product |
| **Double hump** | Complex | Targeted tonal regions | Creative, cross-process |

### 3. RGB Channel Curves (Color Grading)

| Channel | Pull UP → | Pull DOWN → |
|---------|-----------|-------------|
| **Red** | Red / Warm | Cyan / Cool |
| **Green** | Green | Magenta |
| **Blue** | Blue / Cool | Yellow / Warm |

**Classic Combinations:**
- **Teal & Orange:** Blue up (shadows) + Red up (highlights)
- **Cinematic Cool:** Blue up shadows, Green down midtones
- **Warm Nostalgia:** Red up highlights, Blue down shadows
- **Cross Process:** Green up midtones, Red down highlights

---

## Procedure: Mastering the Tone Curve

### Phase 1: Master Curve (Global Contrast)
1. Open Curves adjustment
2. **Add 2 points:** ~25% (shadows) and ~75% (highlights)
3. **Pull shadows down** slightly (deepen blacks)
4. **Pull highlights up** slightly (brighten whites)
5. **Result:** Clean S-curve = professional contrast

### Phase 2: RGB Channels (Color Grading)
1. Switch to **Red channel**
2. Add point in shadows → pull toward **Cyan** (cool shadows)
3. Add point in highlights → pull toward **Red** (warm highlights)
4. Repeat for **Green** (subtle) and **Blue** channels
5. **Result:** Color separation, cinematic look

### Phase 3: Targeted Adjustments
| Target | Channel | Region | Direction |
|--------|---------|--------|-----------|
| Fix green skin | Green | Midtones | Down (Magenta) |
| Warm highlights | Red | Highlights | Up (Red) |
| Cool shadows | Blue | Shadows | Up (Blue) |
| Remove color cast | All | Neutral gray | Balance RGB |

### Phase 4: Luminosity Blending (Advanced)
1. Apply Curves adjustment layer
2. Set **Blend Mode: Luminosity**
3. Curve now affects **only brightness**, not color
4. Perfect for contrast without saturation shifts

---

## Lightroom Specifics

### Parametric Curve (Region Sliders)
| Slider | Tonal Range | Best For |
|--------|-------------|----------|
| **Highlights** | 75–100% | Highlight recovery |
| **Lights** | 50–75% | Mid-high brightness |
| **Darks** | 25–50% | Mid-shadow depth |
| **Shadows** | 0–25% | Shadow lift/detail |

### Point Curve (Custom)
- Click curve → add points
- **RGB tabs** for channel curves
- **Targeted Adjustment Tool** (circle icon) → click image → adds point at that tone

---

## DaVinci Resolve Translation

| Lightroom/Photoshop | DaVinci Resolve | Notes |
|---------------------|-----------------|-------|
| Parametric Regions | **Log Wheels** / Custom Curves | Log wheels target similar regions |
| Point Curve (Master) | **Custom Curves → Master** | Identical concept |
| RGB Channel Tabs | **Custom Curves → Red/Green/Blue** | Identical |
| Targeted Adjustment | **Qualifier / Curves picker** | More powerful in Resolve |
| Luminosity Blend | **Layer Mixer → Luminosity** | Or Compound Node → Luminosity |

---

## Pro Tips from Retouching Academy

| Tip | Detail |
|-----|--------|
| **Less points = smoother** | 2–4 points max for natural results |
| **Anchor midtones** | Lock middle point (50/50) for stability |
| **Check histogram** | Avoid clipping; watch for gaps |
| **Use adjustment layers** | Non-destructive, maskable, adjustable |
| **Match across images** | Save/load curve presets (.acv / .cube) |
| **Curves > Sliders** | Curves give precision sliders can't |

---

## Common Mistakes & Fixes

| Mistake | Symptom | Fix |
|---------|---------|-----|
| Too many points | Jagged, unnatural transitions | Max 3–4 points; use smooth curves |
| Ignoring RGB channels | Flat color, no separation | Always grade in RGB channels |
| Overdoing contrast | Crushed blacks, blown highlights | Subtle S-curve; check histogram |
| No midtone anchor | Global brightness drift | Lock center point or add anchor |
| Single curve for all | Inconsistent look | Save presets per lighting scenario |

---

## Verification Checklist

- [ ] Draw S-curve from memory; explain what it does
- [ ] Create Teal/Orange using only RGB channel curves
- [ ] Fix a green color cast using Green channel curve
- [ ] Use Luminosity blend for contrast without saturation shift
- [ ] Translate a LR curve grade to Resolve Custom Curves
- [ ] Save curve preset; load on 3 different images

---

## References

- Source: Instagram @retouchingpanels — "The Tone Curve is one of the most powerful tools..." (44 weeks ago)
- Featuring: @mypicturesbox (artist), @retouchingacademy (education)
- Links: retouchingacademylab.com, retouchingacademy.com
- Type: Carousel post (multi-slide educational)
- Community: Lightroom verified account commented "Let's gooo👏"

---

## Tags

```markdown
#tone-curve #color-grading #exposure #retouching #photoshop #lightroom #davinci-resolve #rgb-curves #master-curve #parametric-curve #point-curve #educational #photography #retouchingpanels #retouchingacademy
```