---
name: davinci-resolve-moody-cinematic-greens
description: "Deep Moody Cinematic Greens Grade — Hue vs Hue, Hue vs Sat, Color Warper, Custom Curves in DaVinci Resolve"
version: 1.0.0
author: Hermes
metadata:
  hermes:
    tags: [DaVinci Resolve, Color Grading, Creative Grading, Moody Greens, Hue vs Hue, Color Warper]
---

# Moody Cinematic Greens

Create **deep, moody cinematic greens** — a signature atmospheric look for nature, thriller, and mystery narratives. Pushes foliage/shadows into rich teal-green while protecting skin tones.

## When to Use
- Nature documentaries, outdoor narratives
- Thriller/mystery/horror mood establishment
- Music videos with green/forest aesthetics
- Any project where "greens tell the story"

## Prerequisites
- DaVinci Resolve (Free/Studio) 18+
- CST pipeline knowledge (Camera → DWG)
- Hue vs Hue, Hue vs Sat, Color Warper familiarity

## Quick Reference

| Node | Tool | Key Action |
|------|------|------------|
| 01 | CST | S-Log3/S-Gamut3 → DWG |
| 02 | Primary | Balance, WB, mild S-curve |
| 03 | **Hue vs Hue** | **Yellow (0.15) → Green (0.30); Skin locked** |
| 04 | **Hue vs Sat** | **Desat non-greens; Green +15%** |
| 05 | **Custom Curves** | **Green channel shadow lift +0.15** |
| 06 | **Color Warper** | **Sat vs Sat: Green density up** |
| 07 | Power Window | Inverted vignette, green edge tint |
| 08 | CST | DWG → Rec.709/P3 |

## Procedure

### 1. Pipeline Setup (Node 01-02)
```
Node 01: CST — Sony S-Log3/S-Gamut3 → DWG / DaVinci Intermediate
Node 02: Primary — Exposure normalize, WB neutral (RGB Mixer, Luma Mix=0), Contrast 1.1
```

### 2. **Hue vs Hue — Yellow → Green Shift (Node 03)**
| Control Point | Input Hue | Output Hue | Purpose |
|---------------|-----------|------------|---------|
| 1 | 0.15 (Yellow) | 0.30 (Green) | Shift warm foliage → cinematic green |
| 2 | 0.05 (Skin) | 0.05 (Locked) | **Protect skin** |
| 3 | 0.08 (Skin edge) | 0.08 (Locked) | **Protect skin** |
| 4 | 0.12 (Skin edge) | 0.12 (Locked) | **Protect skin** |

### 3. **Hue vs Sat — Desaturate Competing Hues (Node 04)**
| Hue | Sat Change |
|-----|------------|
| Red (0.0) | -40% |
| Orange (0.08) | -30% |
| **Green (0.30)** | **+15%** |
| Cyan (0.50) | -10% |
| Blue (0.65) | -20% |
| Magenta (0.85) | -50% |

### 4. **Custom Curves — Green Shadow Lift (Node 05)**
| Channel | Action |
|---------|--------|
| **Green** | **Lift shadows (0.0-0.3) +0.12 to +0.15** |
| Red | Slight lift +0.03 (warmth separation) |
| Blue | Slight drop -0.03 (cool separation) |

### 5. **Color Warper — Green Saturation Density (Node 06)**
| Tool | Setting |
|------|---------|
| **Sat vs Sat** | Green region (0.25-0.40): Curve **up** |
| Effect | "Subtractive saturation" — richer, not neon |
| Skin Protection | Qualifier mask on input (inverted) |

### 6. **Power Window — Green Vignette (Node 07)**
| Parameter | Value |
|-----------|-------|
| Shape | Circle / Ellipse, Center |
| Softness | 0.85 (very soft) |
| **Inverted** | **Yes** |
| Offset (Lift) | Green +0.05, Blue -0.02 |
| Opacity | 30-50% |

### 7. Output CST (Node 08)
```
DWG / DaVinci Intermediate → Rec.709 Gamma 2.4 (or P3)
```

## Pitfalls

| Symptom | Cause | Fix |
|---------|-------|-----|
| Skin turns green | Hue vs Hue skin lock loose | Lock 0.05, 0.08, 0.12 tightly |
| Neon/artificial greens | Over-saturation Node 4+6 | Reduce Hue vs Sat; use Warper Sat vs Sat |
| Shadows block up | Green lift too high | Reduce to +0.08; add highlight knee |
| Highlights clip green | No rolloff | Custom Curves soft knee >0.9 |
| Grade fails on other footage | No CST / wrong input | **Always CST from camera native** |

## Verification

- [ ] CST: S-Log3/S-Gamut3 → DWG
- [ ] Hue vs Hue: Skin locked 0.05/0.08/0.12; Yellow→Green
- [ ] Hue vs Sat: Non-greens down; Green +15%
- [ ] Curves: Green shadow lift +0.12 to +0.15
- [ ] Warper: Sat vs Sat green density up
- [ ] Window: Inverted, soft 0.85, green edge
- [ ] Output CST: DWG → Rec.709/P3
- [ ] Vectorscope: Skin ±2°; Green cluster at 0.30
- [ ] Parade: No clipping; green lifted in shadows

## Cross-References

| Skill | Topic |
|-------|-------|
| `davinci-resolve-hue-vs-luminance-density-saturation` | Subtractive saturation technique |
| `davinci-resolve-color-warper-saturation-balance` | Sat vs Sat density |
| `davinci-resolve-power-windows-parallel-nodes` | Power window techniques |
| `davinci-resolve-sony-slog3-dwg-workaround` | S-Log3 pipeline |

## References

- Source: Instagram @caleboshi — "💥Get DEEP moody cinematic greens for your next video!! Created In: DaVinci Resolve | Camera: Sony a7S III | Lens: Tamron 17-28mm f2.8 | Location: Singapore" (Reel: DEks7VbRH97)
- Vault Note: `DaVinci_Knowledge_Base/Color Grading & Looks/Creative Grading & Looks/46-Moody-Cinematic-Greens_Caleboshi_Deep-Green-Grade.md`