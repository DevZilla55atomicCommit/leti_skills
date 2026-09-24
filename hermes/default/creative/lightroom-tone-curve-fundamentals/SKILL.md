---
name: lightroom-tone-curve-fundamentals
description: "Lightroom Tone Curve Fundamentals for beginners — understanding RGB curves, parametric vs point curve, color grading basics"
version: 0.1.0
author: Hermes
metadata:
  hermes:
    tags: [Lightroom, Tone Curve, Color Grading, Educational, Photography, RGB Curves, Beginner]
---

# Lightroom Tone Curve Fundamentals — @travelbugraphy

Beginner-friendly introduction to the **Tone Curve** in Adobe Lightroom — the foundation of color grading and contrast control. While Lightroom-specific, the curve concepts transfer directly to DaVinci Resolve Curves, Color Wheels, and Custom Curves.

## When to Use
- Learning tone curve basics (first time)
- Understanding RGB channel curves vs composite
- Translating Lightroom curve knowledge to Resolve
- Photography post-processing workflow

## Prerequisites
- Adobe Lightroom (Classic or CC)
- Basic exposure/contrast slider familiarity

## Quick Reference

| Curve Type | Access | Best For |
|------------|--------|----------|
| **Parametric** | Region sliders (Highlights, Lights, Darks, Shadows) | Quick adjustments, beginners |
| **Point Curve** | Click curve to add points | Precision, custom shapes, color grading |
| **RGB Channels** | Red/Green/Blue tabs in Point Curve | Color grading, cross-processing, film looks |

---

## Core Concepts

### 1. The Tone Curve Graph
- **X-axis:** Input tones (Shadows → Midtones → Highlights)
- **Y-axis:** Output tones (Darker → Brighter)
- **Diagonal line:** Neutral (input = output)
- **Above diagonal:** Brightening
- **Below diagonal:** Darkening

### 2. Parametric Curve (Region Sliders)
| Region | Tonal Range | Typical Use |
|--------|-------------|-------------|
| **Highlights** | ~75–100% | Recover blown highlights, add sparkle |
| **Lights** | ~50–75% | Brighten mid-high tones, skin glow |
| **Darks** | ~25–50% | Deepen mid-shadows, add contrast |
| **Shadows** | ~0–25% | Lift crushed blacks, reveal detail |

**Interaction:** Sliders create smooth S-curves automatically. Good for global contrast.

### 3. Point Curve (Custom Points)
- Click anywhere on curve → adds **control point**
- Drag point → reshapes curve locally
- **S-curve** = Contrast (lift highlights, lower shadows)
- **Inverted S** = Flat/low contrast (lift shadows, lower highlights)
- **Multiple points** = Complex shaping (cross-process, film emulation)

### 4. RGB Channel Curves (Color Grading)
| Channel | Pull Up → | Pull Down → |
|---------|-----------|-------------|
| **Red** | Red / Cyan shift | Cyan / Red shift |
| **Green** | Green / Magenta shift | Magenta / Green shift |
| **Blue** | Blue / Yellow shift | Yellow / Blue shift |

**Classic Film Looks:**
- **Teal & Orange:** Blue up in shadows, Red up in highlights
- **Cross-process:** Green up in midtones, Red down in highlights
- **Cinematic:** S-curve on RGB + Blue lift in shadows + Red lift in highlights

---

## Step-by-Step: First Tone Curve Grade

### 1. Start with Parametric (Global Contrast)
- **Highlights:** -10 to -20 (recover detail)
- **Shadows:** +10 to +20 (lift crushed blacks)
- **Result:** Subtle S-curve, natural contrast

### 2. Switch to Point Curve → RGB Channels
**For Cinematic Teal/Orange:**
| Channel | Shadows (left) | Midtones (center) | Highlights (right) |
|---------|----------------|-------------------|-------------------|
| **Red** | — | — | **Pull up** (+10–20) |
| **Green** | — | Slight down | — |
| **Blue** | **Pull up** (+15–25) | — | Slight down |

### 3. Refine with Point Curve (Master)
- Add point at 25% → pull down slightly (deepen shadows)
- Add point at 75% → pull up slightly (brighten highlights)
- **Result:** Custom contrast + color grade combined

### 4. Before/After (Backslash \ key)
- Toggle to verify grade is intentional, not accidental
- Check histogram for clipping

---

## Translating to DaVinci Resolve

| Lightroom | DaVinci Resolve | Notes |
|-----------|-----------------|-------|
| Parametric Regions | **Custom Curves → Master/Luma** | Resolve: more precise control points |
| Point Curve (Master) | **Custom Curves → Master** | Identical concept |
| RGB Channel Tabs | **Custom Curves → Red/Green/Blue** | Identical concept |
| Region Sliders | **Log Wheels / Color Wheels** | Different UI, same tonal targeting |
| Tone Curve Panel | **Color Page → Curves** | Resolve has Hue vs Sat, Hue vs Hue, Hue vs Lum too |

**Key Insight:** *Curve theory is universal. Lightroom = entry point; Resolve = professional depth.*

---

## Common Mistakes & Fixes

| Mistake | Symptom | Fix |
|---------|---------|-----|
| Overdoing S-curve | Crushed blacks, blown highlights | Reduce point displacement; use parametric for safety |
| Ignoring RGB channels | Color casts, unnatural skin | Always check R/G/B channels separately |
| Point curve on JPEG | Banding, posterization | Shoot RAW; curves need bit depth |
| No before/after | Drift from intent | Tap `\` (backslash) constantly |
| Single global curve | Can't isolate tones | Use masks (Lightroom) / Power Windows/Qualifiers (Resolve) |

---

## Verification Checklist

- [ ] Can draw S-curve from memory and explain what it does
- [ ] Switch between Parametric and Point curve fluently
- [ ] Create teal/orange look using only RGB channel curves
- [ ] Identify crushed blacks / blown highlights on histogram
- [ ] Translate a Lightroom curve grade to Resolve Curves panel
- [ ] Explain why curves > sliders for color grading

---

## References

- Source: Instagram @travelbugraphy — "The Art of Color Grading [Lightroom Tutorial for beginners, Tone Curve]" (31 weeks ago)
- Hashtags: #lightroom #tonecurve #colorgrading #photography #tutorial
- Type: Reel (video tutorial, educational)
- CTA: "Comment ❤️ I'll send you the link"

---

## Tags

```markdown
#lightroom #tone-curve #color-grading #rgb-curves #parametric-curve #point-curve #beginner #educational #photography #post-processing #travelbugraphy #davinci-resolve-transferable
```