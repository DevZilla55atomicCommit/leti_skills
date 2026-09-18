---
name: videographer-camera-theory-sony-picture-profile-slog3-deith
description: "Sony Picture Profile settings for S-Log3/S-Gamut3.Cine cinematic workflow on FX3/A7IV — maximizes dynamic range, protects highlights, provides flat flexible base for DaVinci Resolve grading"
version: 1.0.0
author: Hermes Agent
metadata:
  hermes:
    tags: [Sony, Picture Profile, S-Log3, S-Gamut3.Cine, Camera Theory, Color Science, Dynamic Range, DaVinci Resolve, Color Grading, FX3, A7IV]
---

# Sony Picture Profile Explained — S-Log3 / S-Gamut3.Cine Settings

> **Source:** [@deith__ — Sony Picture Profile Explained](https://www.instagram.com/p/DRwi6KPjMqo/)
> **Creator:** @deith__ (Verified)
> **Date Processed:** 2025-07-18
> **Instagram Post Code:** DRwi6KPjMqo
> **Content Type:** Post (Single Image with Detailed Caption)
> **Technique Category:** Camera Theory / Color Science / Log Workflow

---

## 🎯 Technique Summary

Complete Sony Picture Profile setup for cinematic footage on FX3/A7IV. This profile maximizes dynamic range, protects highlights, and provides a flat, flexible image with natural skin tones and smooth highlight rolloff — ideal for serious color grading in DaVinci Resolve.

---

## 📋 Complete Picture Profile Settings

| Parameter | Value | Purpose |
|-----------|-------|---------|
| **Gamma** | **S-Log3** | Maximizes dynamic range and protects highlights |
| **Color Mode** | **S-Gamut3.Cine** | Softer, film-like colors for easier grading |
| **Black Level** | **0** | Keeps shadows neutral without crushing detail |
| **Black Gamma** | **Middle / Level 0** | Controls contrast in dark areas with natural roll-off |
| **Knee** | **Auto** | Prevents highlight clipping in bright scenes |
| **Saturation** | **0** | Clean, low-contrast base that grades better than oversaturated footage |
| **Color Phase** | **0** | Keeps color tones accurate and consistent |
| **Color Depth** | **Default** | Ensures natural color balance before grading |
| **Detail** | **–5** | Reduces digital sharpness for cinematic, less "video" look |

---

## 🏗️ Why This Works

| Setting | Technical Rationale |
|---------|---------------------|
| S-Log3 | Logarithmic curve captures ~14 stops DR; better highlight protection than S-Log2 |
| S-Gamut3.Cine | Slightly smaller gamut than S-Gamut3; maps better to Rec.709/Display P3; easier grading |
| Black Level 0 | Neutral black point; avoids crushing shadows (unlike +1 which lifts blacks) |
| Black Gamma Middle/0 | Natural shadow contrast without artificial lift or crush |
| Knee Auto | Dynamic highlight compression; manual knee requires scene-by-scene adjustment |
| Saturation 0 | Zero saturation in log = cleanest separation; oversaturation bakes in color casts |
| Detail –5 | Digital sharpening creates ringing artifacts; soft in-camera = better Resolve sharpening |

---

## 🎬 DaVinci Resolve Grading Pipeline

```text
Node 01 — Input CST (S-Log3/S-Gamut3.Cine → DaVinci WG/Intermediate)
    │
    ▼
Node 02 — Primary Balance (Lift/Gamma/Gain + Temp/Tint)
    │  • Establish neutral gray reference
    │  • Skin tone line on vectorscope
    ▼
Node 03 — Contrast & Density (Custom Curves)
    │  • S-curve: raise midtones, protect highlights
    │  • Pivot at 0.4 for natural rolloff
    ▼
Node 04 — Color Separation (Parallel Node)
    │  • Hue vs Hue: shift shadows cyan, highlights orange
    │  • Hue vs Sat: targeted saturation per hue
    ▼
Node 05 — Skin Tone Refinement (Qualifier + Parallel)
    │  • Isolate skin tones (H: 25-45, S: 20-60)
    │  • Smooth + glow for natural texture
    ▼
Node 06 — Creative Look (LUT / Film Emulation / PowerGrades)
    │  • Kodak 2383 / Fujifilm 3513 / Custom
    ▼
Node 07 — Vignette & Texture (Power Window + Film Grain OFX)
    │  • Subtle edge vignette
    │  • 35mm grain @ 15% opacity
    ▼
OUTPUT — Output CST (DaVinci WG → Rec.709/Display P3)
```

---

## 📸 Shot Recipe (Reproducible Workflow)

### Pre-Production
- [ ] Camera: Sony FX3 / A7IV / FX6 / FX9
- [ ] Lens: Any (profile is lens-agnostic)
- [ ] Location: Controlled lighting preferred for S-Log3
- [ ] Time: Any (S-Log3 handles mixed lighting)

### Production
- [ ] Set Picture Profile to **PP8** (or custom PP slot)
- [ ] Apply all 9 settings from table above
- [ ] **Expose to the right (ETTR)**: +1.0 to +1.7 stops over middle gray
- [ ] Use **Waveform/False Color/Zebras** — protect highlights
- [ ] White Balance: **Manual Kelvin** (match scene, e.g., 5600K day / 3200K tungsten)
- [ ] ISO: **Base ISO** (FX3: 640 / A7IV: 800) — never go below base in S-Log3

### Post-Production (DaVinci Resolve)
1. **Clip Attributes** → Input Color Space: S-Log3 / S-Gamut3.Cine
2. **Project Settings** → Color Management: DaVinci YRGB Color Managed
3. **Timeline Color Space**: DaVinci Wide Gamut Intermediate
4. **Output Color Space**: Rec.709 (web) / Display P3 (monitor) / DCI-P3 (DCP)
5. Apply node pipeline above
6. **Verify** on calibrated Display P3 / Rec.709 monitor

---

## ⚠️ Common Pitfalls & Fixes

| Problem | Root Cause | Solution |
|---------|------------|----------|
| **Crushed blacks** | Black Level > 0 or Black Gamma > 0 | Set Black Level=0, Black Gamma=Middle/Level 0 |
| **Clipped highlights** | Knee=Manual/Off or underexposure | Knee=Auto; expose +1.0 to +1.7 stops |
| **Color casts in shadows** | Saturation > 0 | Saturation=0; add saturation in Resolve only |
| **Digital "video" look** | Detail ≥ 0 | Detail=–5; add sharpening in Resolve (Spatial NR) |
| **Muddy skin tones** | Wrong Color Mode (S-Gamut3 not .Cine) | Use S-Gamut3.Cine; apply CST to DaVinci WG |
| **Noise in shadows** | Underexposed S-Log3 (noise floor at -6 to -8 stops) | ETTR +1.0 to +1.7 stops; use NR in Resolve |

---

## ✅ Verification Checklist

- [ ] PP slot saved and labeled "S-Log3 Cine"
- [ ] All 9 parameters match table exactly
- [ ] Waveform shows highlights at 85-95% (not clipping)
- [ ] False color shows skin at 50-55 IRE (pink)
- [ ] Zebras at 95% show only specular highlights
- [ ] ISO at base (640 FX3 / 800 A7IV)
- [ ] White Balance set manually per scene
- [ ] Clip attributes correct in Resolve (S-Log3/S-Gamut3.Cine)
- [ ] CST node first in pipeline (Input → DaVinci WG)

---

## 🔗 Cross-References

| Topic | Vault Location |
|-------|----------------|
| S-Log3 vs S-Log2 comparison | `Camera Theory/01-RAW-vs-LOG_Camera-Theory_Fundamentals.md` |
| DaVinci Wide Gamut workflow | `Color Grading & Looks/Node Structures & Templates/` |
| Kodak 2383 LUT application | `Color Grading & Looks/Kodak 2383/` |
| Sony FX3/A7IV base ISO | `Camera Theory/04-Sony-Picture-Profile-Settings_deith_Camera-Theory.md` |
| ETTR methodology | `Camera Theory/01-RAW-vs-LOG_Camera-Theory_Fundamentals.md` |

---

## 🏷️ Tags

`#videographer` `#camera-theory` `#sony-picture-profile` `#slog3` `#sgamut3cine` `#fx3` `#a7iv` `#davinci-resolve` `#color-grading` `#dynamic-range` `#log-workflow` `#ettr` `#cinematic-look`

---

*Skill generated by `instagram-videographer-learning-pipeline` on 2025-07-18 from Instagram Post DRwi6KPjMqo by @deith__*