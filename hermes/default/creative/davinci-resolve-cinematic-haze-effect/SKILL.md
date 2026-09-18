---
name: davinci-resolve-cinematic-haze-effect
description: "DaVinci Resolve Cinematic Haze Effect: Native tools only - glow, lift, contrast for atmospheric haze look from @3rdvisionfilm."
version: 0.1.0
author: Hermes
metadata:
  hermes:
    tags: [DaVinci Resolve, Color Grading, Haze Effect, Atmospheric, Glow, Native Tools, Cinematic]
---

# DaVinci Resolve — Cinematic Haze Effect

Learn the **Cinematic Haze Effect** technique from @3rdvisionfilm — creating atmospheric, dreamy haze/glow using **only native DaVinci Resolve tools** (no plugins, no LUTs).

## When to Use
- Adding atmospheric haze/fog look to footage
- Dreamy, ethereal, cinematic mood
- Music videos, fashion, narrative scenes needing "magic hour" feel
- Learning native Resolve glow/lift techniques
- Softening digital sharpness for filmic texture

## Prerequisites
- DaVinci Resolve (Free or Studio)
- Footage with good highlight detail (log/RAW preferred)
- Basic node graph, curves, and OFX familiarity

## How to Run
Build the node tree in DaVinci Resolve Color page as described in **Procedure**.

## Quick Reference
| Step | Node | Tool | Key Action |
|------|------|------|------------|
| 1 | Node 01 | Lift/Gamma | Lift ↑ (raise blacks), Gamma ↓ (lower midtones) |
| 2 | Node 02 | Contrast/Pivot | Low contrast, Pivot high (soft look) |
| 3 | Node 03 | Curves | Gentle S-curve, lift shadow point |
| 4 | Node 04 | Glow OFX | Threshold low, size large, intensity subtle |
| 5 | Node 05 | Color Wheels | Temp → warm (golden hour), slight magenta |
| 6 | Node 06 | Vignette | Soft oval, inverted → focus center |

## Procedure

### 1. Node 01 — Lift & Gamma (The Haze Base)
- **Serial Node**, label: `01_HAZE_BASE`
- **Lift:** **Raise significantly** (+0.1 to +0.3) — lifts blacks to "milky" gray
- **Gamma:** **Lower slightly** (-0.05 to -0.1) — compresses midtones
- **Gain:** Slight negative or neutral
- **Result:** Image looks "foggy" — reduced contrast, lifted shadows

### 2. Node 02 — Low Contrast / High Pivot
- **Serial Node** after Node 01, label: `02_LOW_CONTRAST`
- **Contrast:** **Negative or very low** (-10 to +5)
- **Pivot:** **High** (0.5 to 0.7) — anchors at highlights
- **Why:** High pivot + low contrast = soft, hazy transition

### 3. Node 03 — Curves (Shadow Lift + Highlight Roll)
- **Serial Node** after Node 02, label: `03_CURVES_HAZE`
- **RGB Curve:**
  - **Lift shadow point (bottom-left) UP** — raises blacks
  - **Gentle S-curve** for some separation
  - **Pull highlight point DOWN slightly** — soft highlight rolloff
- **Result:** Compressed dynamic range = hazy film look

### 4. Node 04 — Glow OFX (The "Magic")
- **Serial Node** after Node 03, label: `04_GLOW`
- **OpenFX → Glow** (native Resolve OFX):
  - **Threshold:** **Low** (0.2-0.4) — glows even midtones
  - **Size:** **Large** (50-100) — big, soft bloom
  - **Intensity:** **Subtle** (0.2-0.4) — don't overdo
  - **Quality:** High (Studio) / Normal (Free)
- **Optional:** Glow on separate Layer Node with qualifier for highlights only

### 5. Node 05 — Color Temperature (Golden Hour Feel)
- **Serial Node** after Node 04, label: `05_COLOR_MOOD`
- **Gain (Highlights):** Push **Warm/Orange** (golden hour)
- **Lift (Shadows):** Push **Cool/Teal** slightly (complementary) OR warm
- **Saturation:** Slightly **reduced** (-10 to -20) — haze desaturates
- **Tint:** Slight **Magenta** (dreamy)

### 6. Node 06 — Vignette & Final Polish
- **Serial Node**, label: `06_VIGNETTE_POLISH`
- **Power Window → Oval, Inverted:**
  - Center on subject
  - Softness: **0.7-0.9** (very soft)
  - Exposure: **-0.1 to -0.2** (gentle edge darkening)
- **Optional OFX (Studio):** Film Grain (0.1-0.2) for texture

## Pitfalls
| Issue | Cause | Fix |
|-------|-------|-----|
| Looks "foggy/bad" not "cinematic" | Too much lift, no color mood | Add Node 05 warm/cool split; reduce lift |
| Glow blows out highlights | Threshold too low / intensity too high | Raise threshold (0.5+), lower intensity |
| Image too flat | Contrast too low | Slight contrast boost (+5 to +10); check scopes |
| Color cast weird | Temp/Tint imbalance | Balance warm highlights + cool shadows |
| Noise amplified | Lift raises noise floor | Shoot log/RAW; add grain to mask; don't over-lift |

## Verification
1. **Toggle Test:** Nodes 01-06 ON = dreamy haze, OFF = normal
2. **Waveform:** Blacks raised (15-30 IRE), highlights soft (<90 IRE)
3. **Vectorscope:** Low saturation, warm highlight cluster
4. **Visual:** Atmospheric, not just "washed out"

## References
- Source:Source: Instagram @3rdvisionfilm — "THE CINEMATIC HAZE EFFECT... Using only Davinci Resolve native tool, no plugins." (3 weeks ago at capture)
 Caption: #tutorial #learn #diy
- Engagement: Requests for LUTs, "amazing", "goated"

## Related Skills
- `davinci-resolve-day-to-night-grade` (native tools workflow)
- `davinci-resolve-cinematic-grading-3-mistakes` (contrast/pivot theory)
- `davinci-resolve-complementary-color-grading` (warm/cool split)