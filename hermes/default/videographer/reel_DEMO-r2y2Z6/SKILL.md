---
name: reel_DEMO-r2y2Z6
description: "Reel technique from Instagram — Cinematic Cloudy Day Travel (Sony A7IV) from @jaysonrobertson"
version: 1.0.0
author: Hermes Agent
metadata:
  hermes:
    tags: [videographer, reel, cinematic, travel, sony-a7iv, cloudy-day, color-grading, run-and-gun, jaysonrobertson, instagram-learning]
---

# Cinematic Travel on a Cloudy Day (Sony A7IV) — Reel Technique

> **Source:** [Instagram Reel](https://www.instagram.com/reel/DEMO-r2y2Z6/)
> **Creator:** @jaysonrobertson (Verified)
> **Date Processed:** 2026-07-19
> **Instagram Post Code:** DEMO-r2y2Z6
> **Content Type:** Reel
> **Technique Category:** Cinematography / Travel / Run-and-Gun / Color Grading

---

## 🎯 Technique Summary

**"Making Sydney look like a movie on a cloudy day"** — flat, overcast light becomes a creative asset. Cloudy skies = giant natural softbox. The reel demonstrates: shooting in S-Log3 for latitude, exposing for highlights (protecting sky), using ND to maintain wide aperture for shallow DOF, and grading to cinematic teal-orange with lifted blacks for "film look." Sound design (ambient city audio) completes the mood.

---

## 📋 Complete Technique Details

| Parameter | Value | Purpose |
|-----------|-------|---------|
| Technique | Cloudy Day Cinematic Travel | Core technique |
| Creator | @jaysonrobertson | Source |
| Discipline | Cinematography / Travel / Color Grading | Knowledge domain |
| Application | Production / Post / Run-and-Gun | Where used |
| Camera | Sony A7IV | Gear |
| Profile | S-Log3 / S-Cinetone (likely) | Picture Profile |

---

## 🏗️ Core Principles

| Principle | Description |
|-----------|-------------|
| **Overcast = Softbox** | Cloud cover = massive, even, wrap-around light — no harsh shadows, beautiful skin |
| **Protect Highlights (Sky)** | Expose for sky (ETTR for log) — pull shadows in grade; sky detail = production value |
| **Wide Aperture + ND = Separation** | f/1.8-f/2.8 on 35mm/50mm + variable ND = shallow DOF in bright daylight |
| **S-Log3 = Latitude for Grade** | 14+ stops → push teal shadows, warm highlights, lift blacks for film emulation |
| **Sound = Half the Picture** | Ambient city audio (trams, voices, footsteps) grounds the visual mood |

---

## 🎬 Production Workflow (Run-and-Gun)

### Gear (Minimal)
```
Sony A7IV + 35mm f/1.8 (or 24mm f/1.4 GM)
Variable ND (2-5 stops)
No rig, no gimbal — handheld/IBIS
```

### Camera Settings
| Setting | Value | Why |
|---------|-------|-----|
| **Profile** | S-Log3 / S-Gamut3.Cine | Max latitude for grade |
| **ISO** | 640 (Base for S-Log3) | Cleanest noise floor |
| **Shutter** | 1/50s (180° @ 24fps) | Natural motion blur |
| **Aperture** | f/1.8-f/2.8 | Subject separation |
| **ND** | Variable (dial for exposure) | Maintains aperture/shutter |
| **WB** | 5600K (fixed) / Auto (if consistent) | No color shift mid-shot |

### Shooting Technique
```
1. Find pockets of light (windows, reflections, open shade)
2. Expose for highlights (zebras at 95%+ / waveform sky ~80 IRE)
3. Handheld with IBIS + wide lens = stable enough
4. Shoot "coverage" — wide/medium/close of same moment
5. Capture clean audio separately (phone/recorder) for layer
```

---

## 🎬 DaVinci Resolve Grade: "Cloudy Cinematic"

```
Node 01 — CST (S-Log3/S-Gamut3.Cine → DWG)
Node 02 — Primary Balance
  | Temp +50 (warmth), Tint -5 (green counter)
  | Lift +0.08 (lifted blacks = film feel)
  | Gamma -0.05 (mid contrast)
  | Gain -0.05 (protect highlights)
Node 03 — Creative Look (Parallel Node)
  | Serial: Teal Shadows (Lift → Cyan/Teal)
  | Serial: Warm Highlights (Gain → Orange/Amber)
  | Parallel Mix: 60-70% opacity
Node 04 — Film Emulation
  | Halation (Glow OFX, subtle)
  | Film Grain (16mm/35mm, 30-40% opacity)
  | LUT: Kodak 2383 / Fuji Eterna (20-30%)
Node 05 — Vignette + Cleanup
  | Power Window (circle, feather 0.8) → Exposure -0.1
  | Skin cleanup if needed
Node 06 — Output CST (DWG → Rec.709/sRGB)
```

### Key Grade Decisions
| Decision | Reason |
|----------|--------|
| **Lifted Blacks (+0.08)** | Mimics film base fog; cloudy day has no true black |
| **Teal Shadows / Warm Highlights** | Classic cinematic contrast; works on flat light |
| **Halation + Grain** | Sells "film" on digital; hides sensor cleanliness |
| **Highlight Protection** | Sky detail retained → no blown windows |

---

## ✅ Verification Checklist

- [ ] Overcast day = soft light advantage (no harsh shadows)
- [ ] S-Log3 @ Base ISO 640 + ND for aperture control
- [ ] Expose for highlights (sky detail critical)
- [ ] Handheld IBIS + wide lens = stable enough
- [ ] Grade: lifted blacks, teal-orange split, halation/grain
- [ ] Sound design: layered ambient + music bed

---

## 🔗 Cross-References

| Topic | Vault Location |
|-------|----------------|
| S-Log3 Exposure (ETTR) | `DaVinci_Knowledge_Base/Videographer/Camera_Theory/ETTR-Log-Exposure.md` |
| Run-and-Gun Travel Kit | `DaVinci_Knowledge_Base/Videographer/Production/Run-and-Gun-Kit.md` |
| Teal-Orange Grade Breakdown | `DaVinci_Knowledge_Base/Videographer/Color_Grading_&_Looks/Teal-Orange-Deep-Dive.md` |
| Film Emulation in Resolve | `DaVinci_Knowledge_Base/Videographer/Color_Grading_&_Looks/Film-Emulation-Workflow.md` |
| Sound Design for Travel | `DaVinci_Knowledge_Base/Videographer/Audio_&_Sound/Travel-Sound-Design.md` |

---

## 🏷️ Tags

`#videographer` `#reel` `#cinematic` `#travel` `#sony-a7iv` `#cloudy-day` `#color-grading` `#run-and-gun` `#jaysonrobertson` `#instagram-learning`

---

*Skill generated by `instagram-videographer-learning-pipeline` on 2026-07-19 from Instagram Reel*