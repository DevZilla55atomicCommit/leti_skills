---
name: davinci-resolve-hue-vs-luminance-density-saturation
description: "Create cinematic color density via Hue vs Luminance curves — lower luminance of saturated hues for 'subtractive saturation' effect: richer, denser colors without oversaturation artifacts."
version: 0.1.0
author: Hermes
metadata:
  hermes:
    tags: [DaVinci Resolve, Color Grading, Hue vs Luminance, Density, Saturation, Creative Looks, Color Science]
    source_url: "https://www.instagram.com/reel/DZCqY6CBzQA/"
    source_creator: "@ulterior_visuals"
    source_date: "2025-05-31"
    vault_category: "Creative Grading & Looks"
    skill_level: "Intermediate"
    tags: [Hue vs Luminance, Density, Subtractive Saturation, Color Density, Cinematic Look, Creative Grading, Ulterior Visuals]
---

# DaVinci Resolve: Hue vs Luminance for Cinematic Color Density

**Source:** [@ulterior_visuals Instagram Reel](https://www.instagram.com/reel/DZCqY6CBzQA/) — "This is the saturation hack that helps create those rich, cinematic colours..."

## Technique Overview

**Problem:** Global Saturation slider increases *both* chroma AND luminance of colors → image feels "brighter," "thinner," "fake/oversaturated."

**Solution:** **Hue vs Luminance curves** — selectively *lower luminance* of saturated hues → "subtractive saturation" / "density" → richer, deeper, more cinematic color separation without brightness increase.

> "As you increase saturation, you're also changing the luminance of the colours, which can make the image feel brighter and less dense. Instead... reduce the luminance of the colours relative to their saturation. This creates a richer, denser image that feels more saturated without pushing the image into that fake, oversaturated look."

## Node Structure

```
Node 01: Primary Correction (Balance, Exposure, WB) — SCOPES VERIFIED
Node 02: Creative Base Grade (LUT, Look, Split Toning) — OPTIONAL
Node 03: **HUE vs LUMINANCE — DENSITY CURVE** ← KEY NODE
Node 04: Final Polish (Contrast, Global Sat, Grain) — LIGHT TOUCH
Node 05: Output CST (Rec.709) + Gamut Mapping
```

## Step-by-Step Procedure

### 1. Complete Base Correction First
- Node 01: Linear balance, proper exposure, white balance
- **Scopes verified:** Waveform (exposure), Parade (balance), Vectorscope (skin tones)
- *Creative density only works on technically correct base*

### 2. Add Creative Base Grade (Optional)
- Node 02: LUT, Teal/Orange, Bleach Bypass, etc.
- Keep it moderate — density curve will enhance perceived saturation

### 3. Create Hue vs Luminance Density Curve (Node 03)

**Open Curves Panel → Hue vs Luminance (H vs L)**

#### The "Density Curve" Shape:
```
Luminance (Y)
  1.0 ┤                         ●
      │                       ╱
  0.8 ┤                     ╱
      │                   ╱
  0.6 ┤                 ╱
      │               ╱
  0.4 ┤             ╱
      │           ╱
  0.2 ┤         ╱
      │       ╱
  0.0 ┼───────╱───────────────────────
      │     ╱
      │   ╱
 -0.2 ┤ ╱
      ╱
      └───────────────────────────────
        0°    60°   120°  180°  240°  300°  360°
              Hue (H)
```

#### Target Hue Ranges & Luminance Reduction:

| Hue Range | Colors | Luma Reduction | Why |
|-----------|--------|----------------|-----|
| **20°–50°** | Skin tones, warm highlights | **-0.02 to -0.05** | Subtle — protect skin naturalness |
| **50°–80°** | Yellows, golds, warm mids | **-0.05 to -0.10** | Gold/orange density for cinematic warmth |
| **80°–140°** | Greens, foliage | **-0.05 to -0.15** | Deep forest greens, avoid "video green" |
| **140°–220°** | Cyans, teals, blues | **-0.10 to -0.20** | **Strongest** — teal/orange complement, cinematic blues |
| **220°–280°** | Blues, purples, magentas | **-0.08 to -0.15** | Deep movie blues, avoid purple fringe |
| **280°–340°** | Magentas, reds | **-0.05 to -0.10** | Rich reds, skin-adjacent caution |
| **340°–20°** | Reds, skin adjacent | **-0.02 to -0.05** | Protect skin, subtle red density |

> **Key Principle:** Push *complementary hues* (teal/cyan 180°–220°) hardest for Teal & Orange looks. Skin-adjacent hues (20°–50°, 340°–20°) lightest touch.

### 4. Alternative: Color Slice (Resolve 18.5+) for "Subtractive Saturation"
As noted in comments by @lucasamarinho22: *"Go right into the Color Slice tool and use it there, same logic same result, and always make sure luminance is defaulted to zero"*

**Color Slice Workflow:**
1. Open **Color Slice** OFX (or Panel in Color page)
2. For each hue slice (Red, Yellow, Green, Cyan, Blue, Magenta):
   - **Saturation:** Increase slightly (+5 to +15)
   - **Luminance:** **Decrease** (-5 to -20) ← THE KEY
   - **Hue:** Shift slightly if needed
3. **Global Luminance Offset:** Keep at 0 (default)

### 5. Final Polish (Node 04)
| Setting | Value | Why |
|---------|-------|-----|
| Contrast / Pivot | +5–10 / 0.335 | Compensate for density darkness |
| Global Saturation | +2 to +5 | Fine-tune after density |
| Film Grain / Halation | Light | Organic texture masks curve transitions |

### 6. Output CST + Gamut Mapping (Node 05)
- Ensures broadcast legal, manages any gamut shifts from density curve

---

## Why This Works: Color Science

### Additive vs. Subtractive Saturation

| Property | **Additive (Saturation Slider)** | **Subtractive (Hue vs Lum / Color Slice)** |
|----------|----------------------------------|--------------------------------------------|
| **Luminance** | Increases with saturation | **Decreases** with saturation |
| **Perceived Density** | Thinner, brighter | **Richer, deeper** |
| **Highlight Behavior** | Blows out, loses detail | **Preserves** highlight texture |
| **Skin Tones** | Orange/red, unhealthy | **Natural**, controllable |
| **Print Film Analogy** | Digital push processing | **Photochemical density** (D-max) |

### The "Density" Concept (from Photochemistry)
- **Film density (D):** Optical density = -log10(transmittance)
- **Higher density = darker, richer color**
- **Saturation + Density = "Colorfulness" without "Brightness"**
- This technique mimics **photographic paper response** — darker, more saturated dyes

---

## Parameter Quick Reference

### Hue vs Luminance Curve Presets

| Look | Key Hue Reductions | Vibe |
|------|-------------------|------|
| **Cinematic Teal/Orange** | Cyan 180°: -0.15, Teal 200°: -0.18, Orange 30°: -0.03 | Blockbuster, separation |
| **Moody/Noir** | Blue 240°: -0.20, Cyan 180°: -0.15, Green 120°: -0.10 | Dark, atmospheric |
| **Warm/Golden Hour** | Yellow 60°: -0.08, Orange 30°: -0.05, Red 0°: -0.03 | Golden, nostalgic |
| **Natural/Documentary** | All hues: -0.02 to -0.05 | Subtle, transparent |
| **Green-Magenta Split** | Green 120°: -0.12, Magenta 300°: -0.10 | Fashion, editorial |

---

## Pro Tips & Variations

1. **Animate for Transitions:** Keyframe curve intensity for scene transitions
2. **Per-Shot Tweaks:** Copy Node 03, adjust 1-2 control points per shot
3. **Layer Node Blend:** Use Layer Mixer → Density curve in parallel → Key Output Gain 50–70% for subtle blend
4. **Combine with Hue vs Sat:** After lowering luminance, *slightly* raise saturation on same hues for "double density"
5. **Protect Skin:** Always qualify skin tones (Hue 20°–50°) → Layer Mixer → bypass density on skin
6. **HDR Workflow:** In HDR (ST2084), density curve more aggressive — PQ curve compresses highlights naturally

---

## Common Pitfalls

| Symptom | Cause | Fix |
|---------|-------|-----|
| Image too dark overall | Curve pulls *all* hues down | Anchor neutral hues (0/360, 120, 240) at 0; only pull saturated hues |
| Skin looks gray/green | Red/Orange luminance pulled too much | Lighten curve at 20°–50°; add skin qualifier Layer Node |
| Banding/posterization | Too many control points, steep slopes | Fewer points (6–8 max), smoother Bezier curves |
| Colors shift hue | Hue vs Lum interacts with Hue vs Sat | Order: Hue vs Sat → Hue vs Lum, or use Color Slice |
| Highlights lose detail | Luminance reduction affects highlights | Use **Luma vs Sat** curve instead: lower sat only in high luma |

---

## Verification Checklist

- [ ] Base correction complete (scopes verified)
- [ ] Hue vs Luminance curve: 6–8 control points max, smooth Bezier
- [ ] Skin tones (20°–50°) reduction ≤ -0.05
- [ ] Complementary hues (180°–220°) reduction -0.10 to -0.20
- [ ] **Vectorscope:** Saturation *feels* higher but trace not dramatically wider
- [ ] **Waveform:** Overall level slightly lower (compensate with Contrast/Pivot)
- [ ] **CIE Graph:** Colors move radially inward (lower L*) not outward
- [ ] A/B (Cmd+D): Image feels "richer," "denser," more "filmic" — not "more saturated"
- [ ] Skin tones natural, no gray/green cast

---

## Related Techniques

- `davinci-resolve-complementary-color-grading` — Teal & Orange split-toning (pair with density)
- `davinci-resolve-diffusion-soft-light` — Optical diffusion + density = film look
- `davinci-resolve-cst-gamut-mapping-color-spill` — Gamut mapping handles spill from saturation
- `davinci-resolve-white-balance-luma-mix` — Luma Mix=0 for clean density foundation

## Tags

`#davinciresolve` `#colorgrading` `#hue-vs-luminance` `#density` `#subtractive-saturation` `#color-science` `#cinematic-look` `#creative-grading` `#ulterior_visuals` `#colorslice` `#film-look`