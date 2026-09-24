---
name: davinci-resolve-density-saturation-hue-vs-luminance
description: "Create rich cinematic density by lowering luminance of saturated colors via Hue vs Luminance curves — 'subtractive saturation' technique avoids fake oversaturated look."
version: 0.1.0
author: Hermes
metadata:
  hermes:
    tags: [DaVinci Resolve, Color Grading, Creative Looks, Hue vs Luminance, Density, Saturation, Color Warper]
    source_url: "https://www.instagram.com/reel/DZCqY6CBzQA/"
    source_creator: "@ulterior_visuals"
    source_date: "2025-06-15"
    vault_category: "Creative Grading & Looks"
    skill_level: "Intermediate"
    tags: [Hue vs Luminance, Density, Saturation, Cinematic Look, Color Warper, HSV, Subtractive Saturation, Creative Grading]
---

# DaVinci Resolve: Density-Based Saturation via Hue vs Luminance Curves

**Source:** [@ulterior_visuals Instagram Reel](https://www.instagram.com/reel/DZCqY6CBzQA/) — "This is the saturation hack that helps create those rich, cinematic colours..."

## Technique Overview

**Problem:** Standard Saturation slider increases chroma *and* shifts luminance — colors get brighter, image feels "thin," fake, oversaturated.

**Solution:** **Subtractive Saturation / Density technique** — Lower the *luminance* of saturated hues (via Hue vs Luminance curve) to create perceived saturation/density without actual chroma boost. Result: deeper, richer, more "filmic" color separation.

> "Reduce the luminance of the colours relative to their saturation. This creates a richer, denser image that feels more saturated without pushing the image into that fake, oversaturated look."

---

## Node Structure

```
Node 01: Balance/Primary (Linear workflow)
Node 02: Creative Grade / LUT (Optional)
Node 03: **DENSITY NODE** — Custom Curve → Hue vs Luminance
  └─ Pull DOWN luminance on key saturated hues (skin-safe)
Node 04: Output CST (Rec.709)
```

---

## Step-by-Step Procedure

### 1. Add Custom Curve Node (or Color Warper)
- Right-click node graph → **Add Node** → **Custom Curve** (or use Color Warper panel)
- Label: **"DENSITY / Hue vs Lum"**

### 2. Open Hue vs Luminance Curve
- **Custom Curve panel** → **Hue vs Luminance** tab (icon: hue ring with vertical axis)
- **Color Warper** → **Hue vs Luminance** grid mode

### 3. Identify Target Hues
Use **Qualifier** (eyedropper) on saturated colors in your image:
- Foliage/greens (~100-140°)
- Sky/cyans (~180-220°)
- Warm wardrobe/reds (~0-30°, 330-360°)
- Avoid skin tones (~25-45°) — protect these!

### 4. Pull Down Luminance on Saturated Hues
| Hue Range | Typical Target | Luma Reduction | Effect |
|-----------|----------------|----------------|--------|
| **Reds** (0-30°, 330-360°) | Wardrobe, lips, neon | -5% to -15% | Richer reds, less "neon" |
| **Oranges/Skin** (25-45°) | **SKIN — PROTECT** | 0% (anchor point) | Lock with control points |
| **Yellows** (45-65°) | Golden hour, practicals | -3% to -10% | Density without mud |
| **Greens** (100-140°) | Foliage, grass | -8% to -20% | Deep cinematic greens |
| **Cyans/Teals** (180-220°) | Sky, water, teal grade | -5% to -15% | Dense teal separation |
| **Blues** (220-260°) | Night, mood lighting | -5% to -12% | Cinematic blue depth |
| **Magentas** (280-330°) | Creative accents | -5% to -10% | Controlled pop |

### 5. Anchor Skin Tones (Critical!)
- Add **control points** at ~30° and ~40° (skin hue range)
- Lock luminance at **0% change** (horizontal line through center)
- This prevents skin from darkening/green-shifting

### 6. Smooth the Curve
- Use **fewer points** (4-8 max) for smooth transitions
- Avoid sharp V-shapes — causes hue banding
- Test: toggle node ON/OFF — skin should be identical

---

## Alternative Methods (Mentioned in Comments)

### Method A: Color Slicer (HSV) — @lucasamarinho22
```
Node: Color Warper → HSV Slicer
1. Select Hue range (exclude skin)
2. Lower Luminance (V channel) for selection
3. Keep Saturation (S) at 0 change
```
> "Subtractive saturation — go right into color slicer tool, same logic same result, always make sure luminance is defaulted to zero"

### Method B: HSL Qualifier + Layer Mixer
```
Node A: Grade
Node B: HSL Qualifier (select saturated hues, EXCLUDE skin)
  → Key Output: Gain 1.0, Saturation 1.0, **Luminance -0.1 to -0.2**
Node C: Layer Mixer → Composite Mode: **Luminance** (or Overlay at low opacity)
```

### Method C: Custom DCTL / LUT
- Build a 3D LUT that maps high saturation → lower luminance
- Apply as Creative LUT at low mix (20-30%)

---

## Why This Works: Color Science

| Standard Saturation | Density (Hue vs Lum) |
|---------------------|----------------------|
| Increases *chroma* (distance from gray axis) | Decreases *luminance* of chromatic colors |
| Shifts colors toward brighter values | Shifts colors toward darker values |
| **Result:** Brighter, "thinner," video-ish | **Result:** Deeper, "denser," filmic |
| Skin tones often oversaturate | Skin protected via anchor points |
| Global affect | Targeted per-hue control |

**Perceptual principle:** Human vision associates *lower luminance at same chroma* with *higher colorfulness/density*. This mimics film's natural saturation-to-density relationship (D-log-E curve).

---

## Parameter Quick Reference

| Control | Range | Starting Point | Adjust By |
|---------|-------|----------------|-----------|
| **Max Luma Reduction** (foliage/sky) | -5% to -20% | -10% | Taste + scope check |
| **Skin Anchor Width** | ±5-10° around 35° | 2 points at 30°/40° | Widen if skin shifts |
| **Transition Smoothness** | Curve tension | Auto-smooth | Fewer points = smoother |
| **Node Gain/Opacity** | 50-100% | 100% | Lower for subtle |

---

## Scope Verification

| Scope | What to Watch | Target |
|-------|---------------|--------|
| **Waveform (Y)** | Overall luminance drop | < 3-5 IRE average change |
| **Parade RGB** | Channel separation on saturated objects | Channels separate cleanly, no clipping |
| **Vectorscope** | Saturation distance from center | **Should NOT increase** (chroma same) |
| **Hue vs Lum Curve** | Curve shape | Smooth, skin flat, saturated hues pulled down |
| **CIE Graph** | Gamut coverage | Stays within Rec.709, denser distribution |

---

## Common Pitfalls

| Symptom | Cause | Fix |
|---------|-------|-----|
| Skin looks gray/green | Skin anchors missing or wrong hue | Add points at 30° & 40°, lock to 0 |
| Image too dark overall | Too aggressive on too many hues | Reduce max reduction, fewer hues |
| Hue banding / posterization | Sharp curve angles | Use fewer points, enable spline smoothing |
| Shadows get muddy | Affects low-luma saturated colors | Add Lum vs Sat qualifier: only affect mid/high luma |
| Highlights clip weirdly | Bright saturated speculars darkened | Add highlight protection: Lum vs Lum curve up |
| "Nothing changed" | Curve too subtle or wrong hues | Verify with Qualifier → check actual hue angles |

---

## Pro Tips from Comments

1. **@niwo.colour:** *"That is literally the saturation channel though? You are increasing saturation in a different colour model"* → **Response:** No, this *lowers luminance*, doesn't raise chroma. Different vector in color space.

2. **@ulterior_visuals reply:** *"Subtractive saturation... color slicer tool... same logic same result, always make sure luminance is defaulted to zero"* — Color Slicer alternative confirmed.

3. **@brandsyoudontknow:** *"Why don't you deselect channel 1 and channel 3 for hsv?"* — In HSV slicer, modify only Channel 2 (Saturation) and Channel 3 (Value/Luma), leave Hue (Ch 1) alone.

4. **Protect skin FIRST** — Add skin anchor points *before* pulling other hues.

5. **Shot match** — Copy Density node across scene, tweak per-shot (foliage density varies).

---

## Related Techniques

- `davinci-resolve-complementary-color-grading` — Teal/Orange split-toning (often pairs with density)
- `davinci-resolve-cinematic-haze-effect` — Luma-vs-Sat curve for glow
- `davinci-resolve-depth-map-grading` — Layer-based density by depth
- `davinci-resolve-cst-gamut-mapping-color-spill` — Output gamut control (pair with density)

---

## Tags

`#davinciresolve` `#colorgrading` `#creativelooks` `#huevsluminance` `#density` `#subtractivesaturation` `#cinematiclook` `#colorwarper` `#customcurves` `#filmic` `#ulterior_visuals`