---
name: davinci-resolve-custom-kodak-2383-lut-design
description: "Custom Kodak 2383 LUT Design — Print Film Emulation with Deep Blue Shadows in DaVinci Resolve"
version: 1.0.0
author: Hermes
metadata:
  hermes:
    tags: [DaVinci Resolve, Color Grading, LUT Design, Kodak 2383, Film Emulation, Creative Grading]
---

# Custom Kodak 2383 LUT Design

Learn to design a **custom Kodak 2383 Print Film Emulation LUT** with traditional print film characteristics + deep blue shadows for cinematic movie look — all inside DaVinci Resolve.

## When to Use
- Creating signature film looks for projects/branding
- Wedding/cinematic work needing consistent film emulation
- Building LUT packs for sale/distribution
- Matching footage to specific print film aesthetic

## Prerequisites
- DaVinci Resolve Studio (for 3D LUT export)
- Understanding of CST pipeline (Camera → DWG → Film LUT → Output)
- Reference footage or stills of actual Kodak 2383 print

## Quick Reference

| Stage | Node | Tools | Key Settings |
|-------|------|-------|--------------|
| 1 | Camera CST | Color Space Transform | Input: Camera (S-Log3/S-Gamut3) → DWG |
| 2 | Base Contrast | Custom Curves / LGG | Print film contrast curve (toe + shoulder) |
| 3 | Color Density | Hue vs Hue / Hue vs Sat | Film color separation: skin protection, cyan, foliage, sky |
| 4 | Shadow Tint | Custom Curves (Blue) | **Deep blues in shadows** (signature look) |
| 5 | Highlight Roll | Custom Curves / Color Warper | Soft highlight knee, no clipping |
| 6 | Film LUT | 3D LUT (export) | 33×33×33 or 65×65×65 |
| 7 | Output CST | Color Space Transform | DWG → Rec.709 / P3 |

## Procedure

### 1. Set Up Pipeline (DWG Working Space)
```
Node 01: CST — Camera → DaVinci Wide Gamut (DWG)
    Input: S-Log3 / S-Gamut3 (or your camera)
    Output: DWG / DaVinci Intermediate
```

### 2. Build Print Film Contrast (Node 02)
| Tool | Setting |
|------|---------|
| Custom Curves | **Master**: Gentle S-curve (print film density) |
| Custom Curves | **Red**: Slight lift in shadows |
| Custom Curves | **Green**: Neutral midtones |
| Custom Curves | **Blue**: **Deep lift in shadows (0.0-0.2)** ← Signature |

> **Print Film Curve:** Toe (shadows lift) → Linear mid → Shoulder (highlight roll-off)

### 3. Color Density & Separation (Node 03)
| Tool | Target | Adjustment |
|------|--------|------------|
| Hue vs Hue | Skin (0.05-0.12) | Lock → 0.0 (protect skin) |
| Hue vs Hue | Foliage (0.25-0.35) | Shift → Cyan (0.02) |
| Hue vs Hue | Sky (0.55-0.65) | Deepen → Blue (0.03) |
| Hue vs Sat | Skin | -10% (natural) |
| Hue vs Sat | Foliage | +15% (rich) |
| Hue vs Sat | Sky/Blue | +20% (cinematic) |

### 4. **Deep Blue Shadows** (Node 04 — Signature)
| Channel | Curve Shape |
|---------|-------------|
| **Blue** | **Lift shadows (0.0-0.2) +0.15 to +0.25** |
| Red | Slight opposite (-0.05 in shadows) |
| Green | Slight opposite (-0.03 in shadows) |

> **Why:** Real print film has cyan/blue shadow dye density. This creates the "movie theater" look.

### 5. Highlight Knee & Roll-Off (Node 05)
| Tool | Setting |
|------|---------|
| Color Warper / Custom Curves | Soft knee at 0.85-0.9 |
| Highlight Sat | Desaturate >0.95 (film highlight behavior) |
| Glow (optional) | Subtle halation on specular |

### 6. Export 3D LUT
```
Right-click Node 06 → **Export LUT** → **3D LUT**
Format: .cube
Size: 33×33×33 (standard) or 65×65×65 (premium)
Name: Custom_Kodak_2383_DeepBlue_v01.cube
```

### 7. Verify Pipeline
```
Test Clip → CST (Camera→DWG) → Your LUT → CST (DWG→Rec.709)
```
Compare to: Real 2383 print scan / Arri LUT / Kodak 2383 DCTL

## Pitfalls

| Issue | Cause | Fix |
|-------|-------|-----|
| LUT looks different on other footage | No input CST | **Always CST to DWG first** |
| Shadows block up / crush | Blue lift too aggressive | Reduce blue shadow lift to +0.10 |
| Skin tones turn magenta | Hue vs Hue skin not locked | Lock skin at 0.05-0.12 |
| Highlights clip | No soft knee | Add Color Warper highlight roll-off |
| Green/magenta color cast | Unbalanced RGB curves | Balance R/G/B shadow lifts |

## Verification

- [ ] Input CST matches camera native
- [ ] Print film contrast curve (toe + shoulder)
- [ ] Skin tones protected (Hue vs Hue lock)
- [ ] **Deep blue shadows visible** (Blue channel lift 0.0-0.2)
- [ ] Highlight roll-off soft (no clipping)
- [ ] 3D LUT exports clean (.cube, 33³ or 65³)
- [ ] Round-trip: Camera→DWG→LUT→Rec.709 = correct

## Cross-References

| Skill | Topic |
|-------|-------|
| `davinci-resolve-kodak-2383-film-emulation` | Standard 2383 application |
| `davinci-resolve-kodak-2383-breakdown-gabelomotey` | S-Log3 pipeline breakdown |
| `davinci-resolve-cst-gamut-mapping-color-spill` | Gamut mapping for LUTs |
| `davinci-resolve-color-compressor-ofx` | Alternative: Color Compressor for gamut |

## References

- Source: Instagram @shotbysammy_ — "Comment 'LUT' for my own designed 2383 LUT... designed the LUT to have characteristics of traditional print film but also with some deep blues in the shadows, just like in the movies." (Reel: DDzf-sTNsVk)
- Vault Note: `DaVinci_Knowledge_Base/Color Grading & Looks/Kodak 2383/03-Custom-Kodak-2383-LUT-Design_ShotBySammy_Print-Film-Deep-Blues.md`