---
name: davinci-resolve-rgb-crosstalk-color-correction
description: "RGB Crosstalk / Channel Cross-Talk correction in DaVinci Resolve — fixing color contamination between R/G/B channels for clean color separation and accurate hue reproduction."
version: 0.1.0
author: Hermes
metadata:
  hermes:
    tags: [DaVinci Resolve, Color Grading, RGB Crosstalk, Channel Separation, Color Correction, Color Science]
    source_url: "https://www.instagram.com/reel/DXzpBYLIFkv/"
    source_creator: "@harmony_the_artistic_colorist / @davinciresolved"
    source_date: "2025-05-01"
    vault_category: "Color Correction Fundamentals"
    skill_level: "Intermediate"
    tags: [RGB Crosstalk, Channel Cross-Talk, Color Separation, Color Science, DaVinci Resolve, COLOR60, Harmony, davinciresolved]
---

# DaVinci Resolve: RGB Crosstalk / Channel Cross-Talk Correction

**Source:** [@harmony_the_artistic_colorist Instagram Reel](https://www.instagram.com/reel/DXzpBYLIFkv/) — "Day 18/60: COLOR60 — RGB Crosstalk in DaVinci Resolve"

**Original Credit:** @davinciresolved (original video/visuals/content)

## Technique Overview

**Problem:** RGB Crosstalk (Channel Cross-Talk) — signal bleed between Red, Green, Blue channels causing:
- Impure hues (colors contaminated by other channels)
- Incorrect skin tones (green/magenta shifts)
- Poor color separation
- Difficult grading (tools affect multiple channels)

**Solution:** Identify and correct crosstalk using Parade RGB + Custom Curves / RGB Mixer for clean channel separation.

> **Series:** COLOR60 — Day 18 of 60 color grading challenge

---

## What is RGB Crosstalk?

| Ideal Sensor | Real Sensor (with Crosstalk) |
|--------------|------------------------------|
| Red channel = ONLY red photons | Red channel = Red + some Green + some Blue |
| Green channel = ONLY green photons | Green channel = Green + some Red + some Blue |
| Blue channel = ONLY blue photons | Blue channel = Blue + some Red + some Green |

**Result:** Colors never fully saturate to pure hue; "muddy" color science.

---

## Detection: Parade RGB

| Scope View | Clean Channels | Crosstalk Present |
|------------|----------------|-------------------|
| **Neutral Gray** | R=G=B perfectly aligned | R/G/B traces separated on gray |
| **Pure Red** | Only Red trace high; G/B at zero | G/B traces show signal on red object |
| **Pure Green** | Only Green trace high | R/B traces show signal on green object |
| **Pure Blue** | Only Blue trace high | R/G traces show signal on blue object |

**Test:** Shoot ColorChecker / Gray Card → Check Parade RGB on neutral patches.

---

## Correction Methods

### Method 1: RGB Mixer (Global Channel Rebalancing)
**Node:** Serial after base balance

| Mixer Tab | Adjustment |
|-----------|------------|
| **Output Red** | Red: 1.0, Green: -0.02 to -0.05, Blue: -0.01 to -0.03 |
| **Output Green** | Red: -0.01 to -0.03, Green: 1.0, Blue: -0.02 to -0.05 |
| **Output Blue** | Red: -0.01 to -0.03, Green: -0.02 to -0.05, Blue: 1.0 |

> **Principle:** Subtract bleed from each channel. Values are small (1-5%).

### Method 2: Custom Curves → RGB Channel Isolation
**Node:** Serial after base balance

| Curve | Adjustment |
|-------|------------|
| **Red Channel** | Pull down Green/Blue contribution in shadows/mids |
| **Green Channel** | Pull down Red/Blue contribution |
| **Blue Channel** | Pull down Red/Green contribution |

**Technique:** Use **Hue vs Sat** or **Hue vs Lum** to target specific hue ranges where crosstalk is worst (often skin tones, foliage).

### Method 3: 3x3 Matrix (DCTL / LUT) — Most Accurate
**Best for:** Camera-specific correction profiles

```python
# Example 3x3 Correction Matrix (conceptual)
# [R_out]   [ 1.02  -0.03  -0.01 ] [R_in]
# [G_out] = [ -0.02  1.01  -0.04 ] [G_in]
# [B_out]   [ -0.01  -0.03  1.03 ] [B_in]
```

**In Resolve:** Use **Color Space Transform** with custom matrix, or **DCTL** for per-pixel math.

---

## Step-by-Step Workflow (Method 1: RGB Mixer)

### 1. Shoot Test Chart
- ColorChecker Classic / Video
- Even illumination, proper exposure (gray ~50 IRE)

### 2. Analyze in Resolve
```
Node 01: Input CST (Camera Log → Linear)
Node 02: **CROSSTALK CORRECTION** (RGB Mixer)
Node 03: Output CST (Linear → Rec.709)
```

### 3. Measure & Adjust
| Step | Action |
|------|--------|
| 1 | Open **Parade RGB** |
| 2 | Select neutral gray patch (Qualifier) |
| 3 | Read R/G/B values on Parade |
| 4 | In **RGB Mixer**, subtract bleed |
| 5 | Verify: Neutral patch = R=G=B aligned |
| 6 | Check ColorChecker skin/color patches on Vectorscope |

### 4. Save as PowerGrade / DCTL
- **PowerGrade:** Save Node 02 as template
- **DCTL:** Write 3x3 matrix for camera model
- **Apply:** Per camera, per ISO if needed

---

## Camera-Specific Notes

| Camera | Typical Crosstalk | Correction Approach |
|--------|-------------------|---------------------|
| **Sony (S-Log3)** | Green→Red, Blue→Green | RGB Mixer per ISO |
| **ARRI (LogC)** | Minimal (factory calibrated) | Rarely needed |
| **RED (Log3G10)** | Moderate, varies by OLPF | DCTL per sensor |
| **Blackmagic (BRAW)** | Low (BRAW panel handles) | Check per ISO |
| **Canon (C-Log3)** | Red→Blue in shadows | RGB Mixer + Curves |
| **Panasonic (V-Log)** | Blue→Green in low light | Per-ISO matrix |

---

## Verification Checklist

- [ ] **Parade RGB:** Neutral grays = perfect R=G=B alignment
- [ ] **Vectorscope:** ColorChecker patches hit target boxes
- [ ] **Skin Tones:** No green/magenta shift in midtones
- [ ] **Pure Colors:** Red/Green/Blue patches isolated on Parade
- [ ] **A/B Toggle:** Crosstalk correction ON/OFF → cleaner separation
- [ ] **Saved:** PowerGrade / DCTL for reuse

---

## Pro Tips

1. **Per-ISO:** Crosstalk often changes with gain — create matrix per ISO
2. **In Camera First:** Use camera's built-in matrix if available (Sony Matrix, RED Color Science)
3. **DCTL > Mixer:** 3x3 matrix is mathematically cleaner than sequential mixer ops
4. **Test Footage:** Shoot ColorChecker at start of every shoot day
5. **Document:** Save matrix values in project metadata / LUT library

---

## Related Techniques

- `davinci-resolve-primary-color-correction-linear` — Clean base before crosstalk fix
- `davinci-resolve-white-balance-3-methods` — WB after crosstalk = accurate
- `davinci-resolve-cst-gamut-mapping-color-spill` — Output gamut control
- `davinci-resolve-cinematic-grading-3-mistakes` — Node structure for technical fixes

---

## Tags

`#davinciresolve` `#colorgrading` `#rgb-crosstalk` `#channel-crosstalk` `#color-science` `#color-correction` `#parade-rgb` `#rgb-mixer` `#dctl` `#matrix` `#colorchecker` `#color60` `#harmony` `#davinciresolved`