---
name: davinci-resolve-rgb-mixer-white-balance
description: "RGB Mixer technique for precise white balance in DaVinci Resolve — isolate R/G/B channels independently for surgical color correction vs Temp/Tint sliders."
version: 0.1.0
author: Hermes
metadata:
  hermes:
    tags: [DaVinci Resolve, Color Grading, RGB Mixer, White Balance, Color Correction]
    source_url: "https://www.instagram.com/reel/DV_-uWtggWd/"
    source_creator: "@ivarbrauer"
    source_date: "2025-03-15"
    vault_category: "Color Correction Fundamentals"
    skill_level: "Intermediate"
    tags: [RGB Mixer, White Balance, Color Correction, Channel Isolation, Ivar Brauer]
---

# DaVinci Resolve: RGB Mixer for Precision White Balance

**Source:** [@ivarbrauer Instagram Reel](https://www.instagram.com/reel/DV_-uWtggWd/) — "RGB Mixer"

## Technique Overview

**Problem:** Temp/Tint sliders affect all channels simultaneously — crude, 2-axis control.

**Solution:** **RGB Mixer** — independent per-channel gain control for surgical white balance and color correction.

> "Is this entirely different than WB? Or is it somehow the same?" — Comment by @ichester.fit
> **Answer:** RGB Mixer IS white balance, but with 3 independent channels instead of 2-axis Temp/Tint.

---

## RGB Mixer vs Temp/Tint

| Aspect | Temp/Tint | RGB Mixer |
|--------|-----------|-----------|
| **Control** | 2 axes (Blue↔Orange, Green↔Magenta) | 3 independent channels (R, G, B) |
| **Precision** | Coarse — shifts all colors | Surgical — isolate specific channel |
| **Color Science** | Display-referred | Scene-referred (when in Linear) |
| **Use Case** | Quick WB, creative warming/cooling | Technical balance, shot matching |

---

## Node Setup

```
Node 01: INPUT CST (Camera Log → Linear)
Node 02: **RGB MIXER** (WB Node)
Node 03: Creative Grade
Node 04: Output CST + Gamut Mapping
```

---

## RGB Mixer Settings for White Balance

### In Linear Space (Recommended)
| Mixer Tab | Output Red | Output Green | Output Blue |
|-----------|------------|--------------|-------------|
| **Red** | **1.0 + WB_R** | 0 | 0 |
| **Green** | 0 | **1.0 + WB_G** | 0 |
| **Blue** | 0 | 0 | **1.0 + WB_B** |

**Where WB_R, WB_G, WB_B are small adjustments (±0.02–0.10)**

### Step-by-Step WB with RGB Mixer

1. **CST to Linear** (Node 01) — Critical for photometric accuracy
2. **Open RGB Mixer** on Node 02
3. **Parade RGB** — Find neutral reference (gray card, white shirt, etc.)
4. **Adjust per channel:**
   - Red trace high? → Lower **Output Red → Red Input**
   - Green trace high? → Lower **Output Green → Green Input**
   - Blue trace high? → Lower **Output Blue → Blue Input**
5. **Goal:** R=G=B perfectly aligned on Parade for neutral target
6. **Verify:** Vectorscope → trace at dead center

---

## Advanced: Cross-Channel Mixing (Color Correction)

| Goal | Mixer Adjustment |
|------|------------------|
| **Remove green spill** | Output Red → Green: +0.02; Output Blue → Green: +0.01 |
| **Warm shadows only** | Output Red → Red: +0.03 (in Lift/Shadows via Qualifier) |
| **Cool highlights** | Output Blue → Blue: +0.02 (in Gain/Highlights via Qualifier) |
| **Fix magenta cast** | Output Green → Red: -0.01; Output Green → Blue: -0.01 |

---

## Pro Tips from Comments

**@ichester.fit:** *"Is this entirely different than WB? Or is it somehow the same?"*
→ **Answer:** RGB Mixer IS white balance — just 3-axis vs 2-axis. Use Linear space for true printer-light behavior.

**@outcookingx:** *"How the hell Instagram now's I am doing hardcore video editing"*
→ Algorithm knows your interests 🎯

---

## When to Use RGB Mixer vs Temp/Tint

| Scenario | Tool |
|----------|------|
| **Quick client preview** | Temp/Tint |
| **Technical shot matching** | RGB Mixer (Linear) |
| **Mixed lighting correction** | RGB Mixer + Qualifiers |
| **Skin tone rescue** | RGB Mixer + Skin Qualifier |
| **Creative warming/cooling** | Temp/Tint or Offset |
| **Vintage/film emulation** | RGB Mixer for channel response curves |

---

## Verification Checklist

- [ ] **Node 01:** CST correct (Camera Log → Linear)
- [ ] **Node 02:** RGB Mixer adjustments ≤ ±0.10 per channel
- [ ] **Parade RGB:** Neutral reference = R=G=B aligned
- [ ] **Vectorscope:** Neutral reference = centered
- [ ] **Skin tones:** On/near 11° Skin Tone Line
- [ ] **A/B (Cmd+D):** Natural, no channel clipping

---

## Related Techniques

- `davinci-resolve-white-balance-luma-mix` — @rolling.shuttermedia Luma Mix=0 + RGB Gain
- `davinci-resolve-white-balance-3-methods` — @ivarbrauer Temp/Tint, Linear Gain, Gray Card
- `davinci-resolve-white-balance-helper-window-technique` — @marcoherbst.work Power Window + Highlight Mode
- `davinci-resolve-primary-color-correction-linear` — Waqas Qazi Linear workflow

---

## Tags

`#davinciresolve` `#rgb-mixer` `#whitebalance` `#colorcorrection` `#linear` `#printer-lights` `#parade-rgb` `#ivarbrauer`