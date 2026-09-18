---
name: davinci-color-correction-grading-fundamentals
description: Master DaVinci Resolve color correction and grading fundamentals — serial node workflows, lift/gamma/gain, saturation, contrast, temperature, and creative grading techniques from 24 Instagram Reel analyses.
category: davinci-resolve
tags: [color-correction, grading, color-grading, davinci-resolve, serial-nodes, lift-gamma-gain, saturation, contrast, temperature]
trigger: Use when user wants to learn or apply color correction/grading fundamentals in DaVinci Resolve
parameters:
  - name: technique
    description: Specific technique to apply (lift-gamma-gain, saturation-contrast, temperature-tint, serial-node-workflow, creative-grading)
    type: string
    default: serial-node-workflow
  - name: footage_type
    description: Type of footage being graded
    type: string
    enum: [log, rec709, raw, mixed]
    default: log
  - name: target_look
    description: Desired creative look
    type: string
    enum: [natural, cinematic, vintage, teal-orange, high-contrast, custom]
    default: natural
steps:
  - step: Set up serial node structure (Node 1: Primary Correction, Node 2: Creative Grade, Node 3: LUT/Output)
    description: Create 3-node serial graph on Color page
  - step: Primary correction on Node 1
    description: Balance lift/gamma/gain using parade RGB scopes; set white balance with temp/tint
  - step: Creative grade on Node 2
    description: Adjust saturation, contrast, hue vs saturation curves for target look
  - step: Apply LUT or output transform on Node 3
    description: Add CST/LUT for final output space (Rec.709, P3, etc.)
  - step: Match grades across clips
    description: Use still gallery or color match to unify look across timeline
---

# DaVinci Resolve Color Correction & Grading Fundamentals

**Cluster:** 24 techniques from vision_batch_2.json tagged with "color correction", "grading", "color grading"

## Core Techniques Covered

| Technique | Reels | Key Nodes | Parameters |
|-----------|-------|-----------|------------|
| Serial Node Workflow (Primary → Creative → Output) | C_tGXsGPIwQ, C_YaaTkPIaU, C-0Q0FUtEkQ, C93Ef02BTJV, C962pSMvohG, C8E_bWsuEOx, C9gAsyJx204, C9XGErCo7nK, C9L5b-7Ppnb, C9BB0vtxdWK, C8e4UkvoT7E, C8zcAmnvxT9, C6bSKc5AtaF, C6PXEmLpPjU, C6HzBePg764, C5zHQrqp3Rx, C5oyKYTpxHz, C2z8_PVSa17, C5HQfcCJc-9, C4cD8eXPJxq, C4Ykzo6sUF8, C4q_btGp1yN, C4nzM9hgcbb, C4jZ4etJES2 | 3 serial nodes | Lift/Gamma/Gain, Saturation, Contrast, Temp/Tint |

## Node Graph Structure

```
Node 1 (Primary Correction) → Node 2 (Creative Grade) → Node 3 (Output Transform/LUT)
     │                            │                          │
     ├─ Balance RGB Parade       ├─ Saturation/Contrast     ├─ CST to Rec.709
     ├─ White Balance (Temp/Tint) ├─ Hue vs Sat Curves      └─ OR Creative LUT
     └─ Exposure (Lift/Gamma/Gain)└─ Contrast/Pivot
```

## Key Parameters by Technique

### Primary Correction (Node 1)
- **Lift/Gamma/Gain**: Balance shadows/midtones/highlights using Parade RGB scope
- **Temperature/Tint**: Set white balance (5000K–6500K typical, adjust tint for green/magenta)
- **Exposure**: Offset overall brightness; use pivot for contrast center

### Creative Grade (Node 2)
- **Saturation**: 50–150% depending on look (natural ~100%, cinematic 80–120%)
- **Contrast/Pivot**: Build contrast with S-curve or contrast+pivot controls
- **Hue vs Sat**: Selective saturation per hue (skin tones protected, skies enhanced)
- **Hue vs Hue**: Shift specific hues (e.g., greens→teal for cinematic)

### Output Transform (Node 3)
- **CST (Color Space Transform)**: Input: Camera Log → Output: Rec.709/Gamma 2.4
- **Creative LUT**: .cube file applied at 50–100% intensity

## Step-by-Step: Serial Node Workflow (Beginner → Intermediate)

1. **Open Color page**, select clip on timeline
2. **Add 3 serial nodes** (Alt+S ×3): Label "Primary", "Creative", "Output"
3. **Node 1 - Primary**: Open Parade RGB scope. Adjust Lift/Gamma/Gain until RGB channels align at neutral grays. Set Temp/Tint for white balance.
4. **Node 2 - Creative**: Increase Saturation 10–20%. Add Contrast 10–15 with Pivot ~0.4. Use Hue vs Sat to protect skin tones (reduce saturation at ~30° hue).
5. **Node 3 - Output**: Add CST (Color Space Transform) OFX. Input: Camera Log (e.g., S-Log3, V-Log). Output: Rec.709 Gamma 2.4. Or drop LUT at 75% strength.
6. **Match across clips**: Grab still (Gallery → Grab Still), apply to other clips via right-click → Apply Grade.

## Difficulty Progression

| Level | Techniques | Reels |
|-------|------------|-------|
| Beginner | Primary correction only (Node 1), basic CST | C9L5b-7Ppnb, C962pSMvohG |
| Intermediate | 3-node serial, creative curves, LUT blending | C_tGXsGPIwQ, C93Ef02BTJV, C6PXEmLpPjU, C4cD8eXPJxq |
| Advanced | Hue vs Hue/Hue vs Sat curves, skin tone isolation, group pre-clip | C5zHQrqp3Rx, C4Ykzo6sUF8, C2z8_PVSa17 |

## Pro Tips from Reels

- **C_tGXsGPIwQ**: "Apply color correction node first, then grading node — never skip primary"
- **C93Ef02BTJV**: "LUT on Node 3, not Node 1 — preserves grading flexibility"
- **C5zHQrqp3Rx**: "Grade node for overall tone, LUT for look — separate concerns"
- **C4Ykzo6sUF8**: "Contrast via pivot at 0.4 protects midtones better than pure contrast slider"
- **C6HzBePg764**: "Adjust color balance and saturation for desired look BEFORE applying LUT"

## Common Pitfalls

| Pitfall | Fix |
|---------|-----|
| LUT on Node 1 | Move LUT to Node 3 (output) |
| Crushing blacks in primary | Use Lift for shadows, not Offset |
| Over-saturating skin tones | Qualifier → Hue vs Sat → desaturate ~30° hue range |
| Inconsistent white balance | Use Color Match (Color page toolbar) against reference still |

## Related Skills

- `davinci-lut-based-color-grading` — Deep dive on LUT workflows
- `davinci-creative-grading-workflows` — Advanced parallel/layer mixer structures
- `davinci-color-management-cst` — Color Space Transform deep dive