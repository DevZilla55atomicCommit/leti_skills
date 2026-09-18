---
name: davinci-resolve-cst-gamut-mapping-color-spill
description: "Fix color spill/oversaturation using CST Out node Gamut Mapping (Saturation method) — lower Saturation Max and Saturation Knee to tame oversaturated colors while preserving grade integrity."
version: 0.1.0
author: Hermes
metadata:
  hermes:
    tags: [DaVinci Resolve, Color Grading, CST, Gamut Mapping, Color Spill, Color Science]
    source_url: "https://www.instagram.com/reel/DZA2xswowAI/"
    source_creator: "@williamsamehfilm"
    source_date: "2025-05-31"
    vault_category: "Color Correction Fundamentals"
    skill_level: "Intermediate"
    tags: [CST, Gamut Mapping, Saturation, Color Spill, Color Science, Sony FX3]
---

# DaVinci Resolve: CST Gamut Mapping for Color Spill Control

**Source:** [@williamsamehfilm Instagram Reel](https://www.instagram.com/reel/DZA2xswowAI/) — "Here's a better approach to fixing color spill in your image."

## Technique Overview

Instead of globally reducing saturation (which affects the entire image), use the **CST Out node's Gamut Mapping** feature with the **Saturation method** to surgically tame oversaturated/out-of-gamut colors while preserving the overall grade integrity.

## Node Structure

```
Node 1: Primary Correction (Balance, Contrast, etc.)
Node 2: Creative Grade (Look, LUT, etc.)
Node 3: CST (Color Space Transform) — **OUTPUT node**
  → Input Color Space: Camera/Source (e.g., S-Log3/S-Gamut3.Cine)
  → Output Color Space: Timeline/Target (e.g., Rec.709/Rec.709)
  → **Gamut Mapping: ENABLED**
  → **Method: Saturation**
  → **Saturation Max: Lowered** (e.g., 0.8–0.95)
  → **Saturation Knee: Slightly below Saturation Max** (e.g., 0.75–0.9)
```

## Step-by-Step Workflow

### 1. Add CST as Final Output Node
Place a **Color Space Transform** node at the end of your node tree (after all creative grades).

### 2. Configure CST for Your Pipeline
- **Input Color Space:** Match your source footage (e.g., Sony S-Log3/S-Gamut3.Cine for FX3)
- **Output Color Space:** Match your timeline/delivery (e.g., Rec.709 Gamma 2.4)

### 3. Enable Gamut Mapping → Saturation Method
In the CST OFX panel, scroll to **Gamut Mapping** section:
- **Enable:** ✓ On
- **Method:** `Saturation` (not "Clip" or "Scale")

### 4. Adjust Saturation Max
- **Default:** 1.0 (no clamping)
- **Reduce to:** ~0.85–0.95 depending on severity of spill
- **Effect:** Hard-clips saturation values above this threshold

### 5. Fine-Tune Saturation Knee
- **Default:** Matches Saturation Max
- **Set slightly BELOW Saturation Max:** e.g., if Max=0.9, Knee=0.85
- **Effect:** Creates a soft rolloff *before* the hard clip, preventing harsh transitions
- **Rule:** Knee should always be ≤ Max

## Why This Works Better Than Global Saturation Reduction

| Approach | Pros | Cons |
|----------|------|------|
| **Global Saturation (Gain/Offset)** | Simple, one slider | Desaturates *entire image* — skin tones, shadows, everything |
| **CST Gamut Mapping (Saturation)** | Targets *only* out-of-gamut/oversaturated colors | Requires CST at end of pipeline |
| **Qualifier + Saturation** | Precise isolation | Manual tracking, edge artifacts, time-consuming |

## Parameter Guidelines by Scenario

| Scenario | Saturation Max | Saturation Knee | Notes |
|----------|----------------|-----------------|-------|
| Mild spill (skin tones slightly hot) | 0.95 | 0.90 | Subtle, transparent |
| Moderate spill (neon signs, saturated wardrobe) | 0.90 | 0.80 | Visible but natural |
| Severe spill (LED walls, extreme lighting) | 0.80–0.85 | 0.70–0.75 | Aggressive — check skin tones |
| HDR → SDR tone mapping | 0.90–0.95 | 0.85–0.90 | Pair with Tone Mapping OFX |

## Pro Tips

1. **Always place CST at the END** — after all creative grades, before output
2. **Scope it:** Use **CIE Chromaticity** or **Saturation vs. Lum** scope to visualize gamut clipping
3. **Test on skin tones:** Disable/enable Gamut Mapping to verify skin isn't desaturated
4. **Pair with Highlight Rolloff:** In CST, enable *Highlight Rolloff* for smoother specular handling
5. **S-Log3/Sony specific:** For FX3/A7SIII, use S-Gamut3.Cine → Rec.709 with Saturation mapping for cleanest results

## DaVinci Resolve Version Notes

- **Gamut Mapping** added in **DaVinci Resolve 18.5+**
- **Saturation Knee** control refined in **Resolve 19**
- Available in **Free and Studio** versions

## Related Techniques

- `davinci-resolve-white-balance-luma-mix` — Luma Mix = 0 white balance technique
- `davinci-resolve-cinematic-grading-3-mistakes` — Node structure & color management mistakes
- `davinci-resolve-depth-map-grading` — Layer-based isolation alternative

## Tags

`#davinciresolve` `#colorgrading` `#cst` `#gamutmapping` `#colorspill` `#colorscience` `#sonyfx3` `#williamsamehfilm`