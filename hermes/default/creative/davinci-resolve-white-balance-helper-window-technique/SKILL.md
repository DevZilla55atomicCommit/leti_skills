---
name: davinci-resolve-white-balance-helper-window-technique
description: "White Balance Helper technique using Source Window + Highlight Mode in DaVinci Resolve — isolate neutral reference with Power Window, connect Alpha Output to WB node, Gamma Linear + Luma Mix=0 for precision."
version: 0.1.0
author: Hermes
metadata:
  hermes:
    tags: [DaVinci Resolve, White Balance, Power Window, Highlight Mode, Color Correction, Workflow]
    source_url: "https://www.instagram.com/p/DX_WbKvjHDW/"
    source_creator: "@marcoherbst.work"
    source_date: "2025-05-12"
    vault_category: "Color Correction Fundamentals"
    skill_level: "Intermediate"
    tags: [White Balance, Power Window, Highlight Mode, Alpha Output, LOG Footage, Gamma Linear, Luma Mix, Shot Matching, Marco Herbst]
---

# DaVinci Resolve: White Balance Helper — Power Window + Highlight Mode

**Source:** [@marcoherbst.work Instagram Post](https://www.instagram.com/p/DX_WbKvjHDW/) — "White balance Hack for you Creator..."

## Technique Overview

Traditional WB in LOG: Difficult because scopes are log-encoded, WB tools work in display space.

**Solution:** **WB Helper Node** — Add Source → Create Corrector Node → Power Window over neutral reference → Highlight Mode (Shift+H) → Connect Alpha Output → WB Node (Gamma Linear, Luma Mix=0) → Vectorscope center → Delete Helper.

> "Many make White Balance in LOG Footage significantly more complicated than necessary. You can work extremely precisely with a simple Window + Highlight Mode and neutralize your image perfectly in DaVinci Resolve."

---

## Step-by-Step Workflow

### 1. Create WB Helper Node
| Action | Details |
|--------|---------|
| Right-click Node Tree | **Add Source** |
| New Corrector Node | Rename: **"WB Helper"** |
| Purpose | Temporary isolation node |

### 2. Isolate Neutral Reference (Power Window)
| Step | Action |
|------|--------|
| 1 | On WB Helper Node: **Add Power Window** |
| 2 | **Shape:** Circle / Custom over **white/gray reference** (white card, gray card, neutral surface) |
| 3 | **Softness:** Low (0.1-0.2) — precise isolation |
| 4 | **Shift+H** → **Highlight Mode ON** (only window area visible) |
| 5 | Verify: Vectorscope shows ONLY reference point |

### 3. Connect Alpha Output to WB Node
| Connection | Purpose |
|------------|---------|
| **WB Helper Node → Alpha Output** | Feed window mask to WB node |
| **Target WB Node → Alpha Input** | WB correction ONLY affects windowed area |

### 4. Precise White Balance (Target WB Node)
| Setting | Value | Why |
|---------|-------|-----|
| **Mode** | **Gamma Linear** | Linear response = printer lights |
| **Luma Mix** | **0** | Pure Gain, no Lift/Gamma contamination |
| **Tool** | **Gamma Wheel** (not Temp/Tint) | Precise vector control |
| **Scope** | **Vectorscope** (Display Qualifier Focus) | Center the isolated trace |

**Action:** Rotate **Gamma** until isolated point hits **dead center** of Vectorscope (both axes).

### 5. Clean Up
| Step | Action |
|------|--------|
| 1 | **Shift+H** → Highlight Mode OFF |
| 2 | **Delete WB Helper Node** (with window) |
| 3 | Result: Perfectly neutralized LOG image, clean node tree |

---

## Why This Works

| Traditional LOG WB | WB Helper Method |
|--------------------|------------------|
| Scopes in log = hard to read | Window isolates reference in linear light |
| Temp/Tint = crude | Gamma wheel = surgical vector control |
| Affects whole image | Alpha restricts to reference only |
| Guessing on scopes | Vectorscope center = mathematical neutral |

---

## Ideal Use Cases

| Scenario | Why Helper Wins |
|----------|-----------------|
| **LOG Footage** (S-Log3, BRAW, LogC) | Scopes unreadable without LUT |
| **Mixed Lighting** | Isolate ONE clean reference |
| **Difficult Color Casts** | Precision > broad strokes |
| **Fast Shot Matching** | Copy WB node across scene |
| **Pro Workflows** | Repeatable, teachable, scope-verified |

---

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| **Shift+H** | Toggle Highlight Mode |
| **Option+S / Alt+S** | Add Serial Node |
| **Right-click Node** | Add Source |
| **Alpha Output** | Drag from node ► to node ▼ |

---

## Related Techniques

- `davinci-resolve-white-balance-luma-mix` — @rolling.shuttermedia Luma Mix=0 deep dive
- `davinci-resolve-white-balance-3-methods` — @ivarbrauer 3 WB methods
- `davinci-resolve-primary-color-correction-linear` — Waqas Qazi linear workflow

---

## Tags

`#davinciresolve` `#whitebalance` `#powerwindow` `#highlightmode` `#alphaoutput` `#logfootage` `#gammalinear` `#lumamix` `#vectorscope` `#shotmatching` `#marcoherbst` `#colorcorrection`