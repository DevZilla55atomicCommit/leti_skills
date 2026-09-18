---
name: davinci-resolve-qualifier-picker-measurement-tool
description: "Qualifier Picker as measurement tool in DaVinci Resolve — precise WB, exposure, skin tone, and color value readings via eyedropper + scopes."
version: 0.1.0
author: Hermes
metadata:
  hermes:
    tags: [DaVinci Resolve, Color Grading, Qualifier, Eyedropper, Measurement, Scopes]
    source_url: "https://www.instagram.com/reel/DXH7U22xmta/"
    source_creator: "@ivarbrauer"
    source_date: "2025-04-15"
    vault_category: "Color Correction Fundamentals"
    skill_level: "Beginner to Intermediate"
    tags: [Qualifier, Eyedropper, White Balance, Exposure, Skin Tones, Measurement, Ivar Brauer]
---

# DaVinci Resolve: Qualifier Picker as Measurement Tool

**Source:** [@ivarbrauer Instagram Reel](https://www.instagram.com/reel/DXH7U22xmta/) — "Qualifier Picker for measuring all kinds of things"

## Technique Overview

The **Qualifier Picker (Eyedropper)** in DaVinci Resolve isn't just for creating keys — it's a **precision measurement instrument** when combined with scopes.

> "Most people don't realize the Qualifier picker can measure WB, exposure, skin tones, and color values directly on the scopes." — @ivarbrauer

---

## What the Qualifier Picker Measures

| Measurement | Scope | How to Read |
|-------------|-------|-------------|
| **White Balance** | Vectorscope | Trace position = hue offset from neutral |
| **Exposure** | Waveform (Y) | IRE value at picker point |
| **Skin Tones** | Vectorscope + Skin Tone Line | Distance from 11° line |
| **Color Values** | Parade RGB | R/G/B alignment on neutral |
| **Saturation** | Vectorscope | Distance from center |

---

## Step-by-Step: Using Qualifier as Meter

### 1. Open Qualifier Panel
- Color Page → **Qualifier** tab (eyedropper icon)
- **Mode:** HSL or 3D (both work)

### 2. Enable Display Qualifier Focus (Critical!)
- **Vectorscope Settings** (gear icon) → **Display Qualifier Focus: ON**
- **Waveform/Parade Settings** → **Display Qualifier Focus: ON**

### 3. Pick Target Area
- Click **Eyedropper** in Qualifier
- Click on image area to measure (white card, skin, gray card, etc.)

### 4. Read Scopes
| Target | Scope | What to Look For |
|--------|-------|------------------|
| **Gray Card / White** | Vectorscope | Trace at **dead center** = neutral |
| **Gray Card / White** | Parade RGB | R=G=B perfectly aligned |
| **Skin Tone** | Vectorscope | Trace on/near **11° Skin Tone Line** |
| **Exposure Check** | Waveform Y | IRE value at pick point |

---

## Practical Use Cases

### Use Case 1: White Balance Verification
```
1. Pick neutral reference (gray card, white shirt)
2. Vectorscope → trace at center? = WB correct
3. Parade RGB → R=G=B aligned? = WB correct
4. If off-center: adjust WB node until centered
```

### Use Case 2: Shot Matching
```
1. Pick same reference on Shot A (note Parade RGB values)
2. Pick same reference on Shot B
3. Adjust Shot B WB until Parade RGB matches Shot A
```

### Use Case 3: Skin Tone Consistency
```
1. Pick skin on hero shot → note Vectorscope angle
3. Pick skin on other shots
4. Adjust until all sit on 11° Skin Tone Line
```

### Use Case 4: Exposure Spot-Meter
```
1. Pick highlight → Waveform Y reads ~90-95 IRE (not clipped)
2. Pick shadow → Waveform Y reads ~5-10 IRE (not crushed)
3. Pick mid-gray (18%) → Waveform Y reads ~40-50 IRE
```

---

## Pro Tips

| Tip | Description |
|-----|-------------|
| **Shift+Click** | Add to selection (multiple samples) |
| **Option/Alt+Click** | Subtract from selection |
| **Display Qualifier Focus** | **Must be ON** for scope accuracy |
| **Luma Range** | Adjust in Qualifier to isolate specific brightness |
| **Save Presets** | Save common picks (skin, gray, foliage) as Qualifier presets |

---

## Related Techniques

- `davinci-resolve-white-balance-helper-window-technique` — Power Window + Highlight Mode WB
- `davinci-resolve-rgb-mixer-white-balance` — RGB Mixer 3-axis WB
- `davinci-resolve-white-balance-3-methods` — @ivarbrauer 3 WB methods
- `davinci-resolve-white-balance-luma-mix` — Luma Mix=0 + RGB Gain

---

## Tags

`#davinciresolve` `#qualifier` `#eyedropper` `#measurement` `#whitebalance` `#exposure` `#skintones` `#vectorscope` `#parade` `#waveform` `#ivarbrauer`