---
name: reel_DDmkIadTSKM
description: "Reel technique from Instagram — Sony S-Log2 vs S-Log3 vs HLG from @borisforeal"
version: 1.0.0
author: Hermes Agent
metadata:
  hermes:
    tags: [videographer, reel, sony, slog2, slog3, hlg, picture-profiles, camera-settings, 8bit-vs-10bit, borisforeal, instagram-learning, camera-theory]
---

# Sony S-Log2 vs S-Log3 vs HLG — Reel Technique

> **Source:** [Instagram Reel](https://www.instagram.com/reel/DDmkIadTSKM/)
> **Creator:** @borisforeal
> **Date Processed:** 2026-07-19
> **Instagram Post Code:** DDmkIadTSKM
> **Content Type:** Reel
> **Technique Category:** Camera Theory / Sony Picture Profiles / Exposure

---

## 🎯 Technique Summary

**Sony picture profile selection is a trade-off between dynamic range, bit depth, and workflow.** This reel shares the creator's personal settings and sparks a rich community discussion on S-Log2 vs S-Log3 vs HLG for 8-bit Sony cameras (A7III, A6400, etc.). Key insight: **S-Log3 requires overexposure (+1.7 to +2 stops) to lift shadows out of noise floor — but 8-bit codecs fall apart when pushed that far.** HLG3 is often the practical sweet spot for 8-bit: no overexposure needed, broadcast-ready, decent latitude.

---

## 📋 Complete Technique Details

| Parameter | Value | Purpose |
|-----------|-------|---------|
| Technique | Sony Picture Profile Selection & Exposure | Core technique |
| Creator | @borisforeal | Source |
| Discipline | Camera Theory / Sony Ecosystem | Knowledge domain |
| Application | Production / Pre-Production | Where used |
| Cameras | A7III, A7IV, A6400, A6600, FX3, FX30 | Applicable models |

---

## 🏗️ Core Principles

| Principle | Description |
|-----------|-------------|
| **S-Log2 = 13 stops, designed for 8-bit** | Native 8-bit curve; less aggressive than S-Log3; +1 stop over native ISO recommended |
| **S-Log3 = 14+ stops, designed for 10-bit+** | Cine-style curve; demands +1.7 to +2 stops over; 8-bit = banding/noise in shadows |
| **HLG (Hybrid Log-Gamma) = Broadcast/Immediate** | No grading required for HDR display; 10-bit preferred but usable in 8-bit; no overexposure needed |
| **ISO Base = Noise Floor** | Sony A7III/A6400: Base ISO 640 (S-Log2/3); Base ISO 100 (HLG) — never go below |
| **8-bit = 256 levels per channel** | Aggressive log curves stretch those levels thin → posterization in gradients |

---

## 🎬 Picture Profile Decision Tree

```
START: What is your codec bit depth?
  │
  ├─► 10-bit 4:2:2 (A7IV, FX3, FX30, A7SIII)
  │     │
  │     ├─► Need max latitude, will grade → S-Log3 @ Base ISO +1.7 to +2 stops
  │     │
  │     ├─► Quick turnaround, HDR delivery → HLG3 @ Base ISO
  │     │
  │     └─► Matching legacy S-Log2 footage → S-Log2 @ Base ISO +1 stop
  │
  └─► 8-bit 4:2:0 (A7III, A6400, A6600, A7RIII/IV)
        │
        ├─► Will grade carefully, accept noise risk → S-Log2 @ ISO 640 +1 stop
        │
        ├─► Want usable SOOC + grading flexibility → HLG3 @ ISO 100 (no over-exposure)
        │
        └─► S-Log3 in 8-bit → ONLY if exposing to right (+2 stops) AND using external 10-bit recorder
```

---

## 🔧 Recommended Settings by Camera-Shoot: Creator's Shared Settings (from caption)

| Setting | Value | Notes |
|---------|-------|-------|
| **Profile** | S-Log2 (creator's choice) | "These are my settings" |
| **Gamma** | S-Log2 | 13 stops, 8-bit friendly |
| **Color Mode** | S-Gamut3.Cine | Slightly smaller than S-Gamut3; easier grade |
| **ISO** | 640 (Base for S-Log2/3) | Never lower |
| **Exposure** | +1 stop over (via ND/aperture) | Lifts shadows above noise |
| **White Balance** | Kelvin (fixed) | No AWB drift |
| **Focus** | DMF / Focus Peaking | Manual assist |

---

## 💬 Community Wisdom (Top Comments)

| Insight | Source | Verdict |
|---------|--------|---------|
| **S-Log3 in 8-bit = pain** | @guru.filmz, @mang.raw, @sir.mohsen.ch | Confirmed: HLG3 better for 8-bit |
| **HLG3 = best 8-bit profile** | @guru.filmz (A7III veteran) | "Only captures 8-bit; S-Log destroys it" |
| **S-Log2 needs +1, S-Log3 needs +2** | @mang.raw, @peymanshirpoor | Standard exposure offsets |
| **S-Gamut3.Cine > S-Gamut3** | Implied by creator's choice | Smaller gamut = less hue shift in 8-bit |
| **A7III 4K 25-100Mbps ✅** | @media_arc | Bitrate sufficient for S-Log2 |

---

## ✅ Verification Checklist

- [ ] Know your camera's **base ISO** for each gamma (640 for S-Log2/3, 100 for HLG)
- [ ] Match **exposure offset** to profile (+1 S-Log2, +1.7-2 S-Log3, 0 HLG)
- [ ] Use **ND filters** to maintain aperture/shutter while overexposing
- [ ] Set **Color Mode** to S-Gamut3.Cine (easier grade than S-Gamut3)
- [ ] **Never shoot below base ISO** — raises noise floor
- [ ] Test **grading pipeline** before commit (CST: S-Log3/S-Gamut3.Cine → DWG)

---

## 🔗 Cross-References

| Topic | Vault Location |
|-------|----------------|
| Sony S-Log3/S-Gamut3.Cine CST | `DaVinci_Knowledge_Base/Videographer/Camera_Theory/Sony-SLog3-CST.md` |
| HLG Workflow in DaVinci | `DaVinci_Knowledge_Base/Videographer/Color_Grading_&_Looks/HLG-Workflow.md` |
| 8-bit vs 10-bit Grading Limits | `DaVinci_Knowledge_Base/Videographer/Camera_Theory/8bit-vs-10bit-Grading.md` |
| Exposure for Log (ETTR) | `DaVinci_Knowledge_Base/Videographer/Camera_Theory/ETTR-Log-Exposure.md` |
| Sony Picture Profile Deep Dive | `DaVinci_Knowledge_Base/Videographer/Camera_Theory/Sony-Picture-Profiles.md` |

---

## 🏷️ Tags

`#videographer` `#reel` `#sony` `#slog2` `#slog3` `#hlg` `#picture-profiles` `#camera-settings` `#8bit-vs-10bit` `#borisforeal` `#instagram-learning` `#camera-theory`

---

*Skill generated by `instagram-videographer-learning-pipeline` on 2026-07-19 from Instagram Reel*