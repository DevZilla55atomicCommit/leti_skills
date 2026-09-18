---
name: davinci-resolve-auto-balance-ivarbrauer
description: "Auto Balance in DaVinci Resolve — is it any good? Testing Auto Balance vs manual WB (Temp/Tint, Linear Gain, Gray Card) on Sony A7IV footage."
version: 0.1.0
author: Hermes
metadata:
  hermes:
    tags: [DaVinci Resolve, Color Grading, Auto Balance, White Balance, Testing]
    source_url: "https://www.instagram.com/reel/DTd8JMDAiNc/"
    source_creator: "@ivarbrauer"
    source_date: "2025-01-15"
    vault_category: "Color Correction Fundamentals"
    skill_level: "Beginner to Intermediate"
    tags: [Auto Balance, White Balance, Ivar Brauer, Sony A7IV, Testing, Color Grading]
---

# DaVinci Resolve: Auto Balance — Is It Any Good? — @ivarbrauer

**Source:** [@ivarbrauer Instagram Reel](https://www.instagram.com/reel/DTd8JMDAiNc/) — "Auto Balance - is it any good?"

## Technique Overview

Testing **DaVinci Resolve's Auto Balance** feature vs manual white balance methods (Temp/Tint, Linear Gain/Luma Mix=0, Gray Card) on Sony A7IV footage with 100mm macro, DJI Mic 2, Aputure lights, Manfrotto.

> *"Auto Balance - is it any good?"* — Testing Resolve's one-click WB

---

## Auto Balance in DaVinci Resolve

### Where to Find
- Color Page → Primary Wheels → **Auto Balance** (eyedropper with "A" icon)
- Or: Right-click clip → **Auto Balance**

### What It Does
- Analyzes frame for neutral reference (gray/white)
- Applies Temp/Tint adjustment automatically
- **Single-click** white balance

---

## Test Setup (from post)
| Equipment | Details |
|-----------|---------|
| **Camera** | Sony A7IV |
| **Lens** | 100mm Macro |
| **Audio** | DJI Mic 2 |
| **Lights** | Aputure |
| **Support** | Manfrotto |

---

## Auto Balance vs Manual Methods

| Method | Pros | Cons | Best For |
|--------|------|------|----------|
| **Auto Balance** | Fast, one-click, decent starting point | Can be fooled by dominant colors, no creative control | Quick turnaround, dailies, reference |
| **Temp/Tint** | Full control, familiar | Couples luminance & chrominance | General use, beginners |
| **Linear Gain (Luma Mix=0)** | Photometric accuracy, decoupled | Learning curve, needs scopes | Pro workflow, critical work |
| **Gray Card / ColorChecker** | Reference accuracy | Extra step on set | Controlled environments, product |

---

## When Auto Balance Works Well

| Scenario | Result |
|----------|--------|
| **Neutral gray/white in frame** | ✅ Good |
| **Even lighting, no strong color cast** | ✅ Good |
| **Quick dailies/rough cut** | ✅ Acceptable |
| **Strong color cast (sunset, neon)** | ❌ Often wrong |
| **Dominant single color (green screen, red wall)** | ❌ Biased toward that color |
| **Mixed lighting** | ⚠️ Unpredictable |

---

## Comment Insights

| Comment | Insight |
|---------|---------|
| @simon.kirketerp | *"How about using CST before changing anything?"* → **Yes, CST first, then WB in correct color space** |
| @uunweybasico | *"Trust the veriscope"* → **Scopes (Vectorscope) over auto tools** |
| @rohitravidirector | *"Change normal eyes to blind white cloudy iris... power window not getting best results"* → Different technique (Qualifier + Hue shift) |
| @francheska_sketch | *"You're brilliant 🤩"* | |
| @v.i.n.t.y_eddits | *"You are the best 🔥 really needed to hear this"* | |

---

## Pro Workflow Recommendation

```
1. CST (Log → Working Space)
2. Manual WB (Linear Gain / Luma Mix=0) using scopes
3. Verify on Vectorscope (skin tone line, neutral axis)
4. Auto Balance ONLY as starting reference, then refine manually
```

---

## Related Techniques

- `davinci-resolve-white-balance-3-methods` — Temp/Tint, Linear Gain, Gray Card
- `davinci-resolve-white-balance-luma-mix` — Luma Mix=0, RGB Gain = printer lights
- `davinci-resolve-rgb-mixer-white-balance` — RGB Mixer 3-axis surgical WB
- `davinci-resolve-qualifier-picker-measurement-tool` — Qualifier for precise measurement

---

## Tags

`#davinciresolve` `#colorgrading` `#auto-balance` `#white-balance` `#ivarbrauer` `#sony-a7iv` `#testing` `#color-correction`