---
name: davinci-resolve-day-to-night-grade
description: "DaVinci Resolve Day-for-Night grading: Native tools only - exposure drop, blue shift, shadow crush, power windows for artificial lights."
version: 0.1.0
author: Hermes
metadata:
  hermes:
    tags: [DaVinci Resolve, Color Grading, Day for Night, Native Tools, Qualifier, Power Windows]
---

# DaVinci Resolve — Day-for-Night (Day to Night) Grading

Learn the **Day-for-Night** transformation technique from @3rdvisionfilm — converting daytime footage to nighttime using **only native DaVinci Resolve tools** (no plugins, no LUTs).

## When to Use
- Converting day footage to night for narrative/story needs
- Budget/time constraints preventing night shoots
- Learning native Resolve grading depth
- Creating moody, cinematic night looks from scratch

## Prerequisites
- DaVinci Resolve (Free or Studio)
- Daytime footage with good dynamic range (log/RAW preferred)
- Basic node graph, qualifier, and power window familiarity

## How to Run
Build the node tree in DaVinci Resolve Color page as described in **Procedure**.

## Quick Reference
| Step | Node | Tool | Key Action |
|------|------|------|------------|
| 1 | Node 01 | Primary Wheels | Exposure ↓↓↓, Temp → Blue, Tint → Magenta |
| 2 | Node 02 | Contrast/Pivot | Contrast ↑, Pivot → left (crush shadows) |
| 3 | Node 03 | Curves | S-curve + pull highlight point down |
| 4 | Node 04 | Qualifier | Select "light" areas (windows, lamps) → lower exposure |
| 5 | Node 05 | Power Windows | Circular masks for artificial lights → add glow/warmth |
| 6 | Node 06 | Vignette | Soft oval, inverted → darken edges |

## Procedure

### 1. Node 01 — Global Exposure & Color Shift (The Base)
- **Serial Node**, label: `01_DAY_TO_NIGHT_BASE`
- **Primary Wheels:**
  - **Exposure:** Lower significantly (-1.5 to -3.0 stops) — kills daylight brightness
  - **Temperature:** Push heavily toward **Blue** (cool, moonlight feel)
  - **Tint:** Slight **Magenta** (removes green cast from blue push)
- **Scopes:** Waveform should show overall level drop; Vectorscope trace moves to blue sector

### 2. Node 02 — Shadow Crush & Contrast (The Night Feel)
- **Serial Node** after Node 01, label: `02_CONTRAST_PIVOT`
- **Contrast:** Increase (+20 to +50)
- **Pivot:** Move **left** (toward 0.1-0.2) — anchors crush at deep shadows
- **Result:** Deep blacks, high contrast ratio (night = high contrast)
- **Waveform:** Blacks at 5-10 IRE, midtones compressed

### 3. Node 03 — Curve Refinement (Highlight Control)
- **Serial Node** after Node 02, label: `03_CURVES`
- **RGB Curve:**
  - Create **S-curve** for contrast
  - **Critical:** Pull **highlight point (top right) DOWN** significantly
  - This prevents sky/bright surfaces from looking like "dim day"
- **Optional:** Separate R/G/B curves for color shift fine-tune

### 4. Node 04 — Artificial Lights via Qualifier (Practical Lights)
- **Serial Node** after Node 03, label: `04_PRACTICAL_LIGHTS`
- **Qualifier Tool:**
  - Pick bright areas that should be "lit" (windows, lamp posts, signs, building lights)
  - Refine: Hue/Sat/Lum ranges, Softness, Clean Black/White
- **Grade on Qualified Selection:**
  - **Exposure:** Lower (makes them pop as light sources)
  - **Temperature:** Push **Warm/Orange** (street lamps, windows)
  - **Saturation:** Boost for color pop
- **Invert Qualifier?** No — grade ONLY the selected light sources

### 5. Node 05 — Artificial Light Pools via Power Windows
- **Serial Node** (or Layer from Node 04), label: `05_LIGHT_POOLS`
- **Power Windows → Circle/Custom:**
  - Place on ground/areas where light would fall
  - Multiple windows for multiple light sources
- **Grade inside windows:**
  - Exposure ↑ (creates light pool)
  - Temp → Orange/Amber
  - Softness: High (0.5-0.8) for natural falloff
- **Track** if camera/light moves

### 6. Node 06 — Vignette & Final Polish
- **Serial Node**, label: `06_VIGNETTE_POLISH`
- **Power Window → Oval, Inverted:**
  - Center on subject/action
  - Softness: 0.6-0.8
  - Exposure ↓ (darkens edges naturally)
- **Optional OFX (Studio):** Glow on light sources, Film Grain for texture

## Pitfalls
| Issue | Cause | Fix |
|-------|-------|-----|
| Looks like "dark day" not night | Not enough blue shift / shadows not crushed | More Temp→Blue; Pivot left for deep blacks |
| Sky still looks like day | Highlights not pulled down enough | Curve: pull highlight point down; add sky qualifier |
| Artificial lights look fake | Wrong color temp / too uniform | Qualifier + Power Windows: vary warmth per source |
| Subject too dark | Global exposure dropped too much | Use Power Window on subject to lift slightly |
| Flat/low contrast | Contrast/Pivot not aggressive | Increase Contrast, Pivot→0.1 |

## Verification
1. **Toggle all nodes OFF→ON** — clear day→night transformation
2. **Waveform:** Deep blacks (5-10 IRE), controlled highlights (<60 IRE)
3. **Vectorscope:** Dominant blue/cyan trace, warm spots at 30° (lights)
4. **Visual:** Believable night — not just darkened day

## References
- Source: Instagram @3rdvisionfilm — "Day to Night color transformation... No plugins, no luts, Just davinci resolve native tools" (3 weeks ago at capture)
- Technique: Day-for-Night via native Primary, Curves, Qualifier, Power Windows
- Engagement: High positive response ("cold", "beautiful", "thank you boss")

## Related Skills
- `davinci-resolve-cinematic-grading-3-mistakes` (Pivot/Contrast theory)
- `davinci-resolve-masking-power-masking-power-masking` (Power Windows)
- `davinci-resolve-white-balance-luma-mix` (Base balance)