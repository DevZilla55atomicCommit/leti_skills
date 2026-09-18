---
name: reel_DDlqRrfRkTI
description: "Reel technique from Instagram — Frame Rate Selection Guide from @cobikrumholz"
version: 1.0.0
author: Hermes Agent
metadata:
  hermes:
    tags: [videographer, reel, frame-rate, cinematography, camera-settings, slow-motion, davinci-resolve, cobikrumholz, instagram-learning]
---

# Frame Rate Selection Guide — Reel Technique

> **Source:** [Instagram Reel](https://www.instagram.com/reel/DDlqRrfRkTI/)
> **Creator:** @cobikrumholz
> **Date Processed:** 2026-07-19
> **Instagram Post Code:** DDlqRrfRkTI
> **Content Type:** Reel
> **Technique Category:** Cinematography / Camera Settings / Frame Rate

---

## 🎯 Technique Summary

**Frame rate is a creative decision, not a default.** This reel breaks down how to choose between 24fps, 30fps, and 60fps (and higher) based on the *intent* of the shot — not just "what the camera does." Key insight: your **project timeline frame rate** dictates how footage plays back; shooting at a different rate creates slow-motion or fast-motion by design.

---

## 📋 Complete Technique Details

| Parameter | Value | Purpose |
|-----------|-------|---------|
| Technique | Frame Rate Selection Strategy | Core technique |
| Creator | @cobikrumholz | Source |
| Discipline | Cinematography / Camera Settings | Knowledge domain |
| Application | Pre-Production / Production | Where used |

---

## 🏗️ Core Principles

| Principle | Description |
|-----------|-------------|
| **Timeline FPS = Playback Reality** | Project timeline frame rate determines "real time" — everything else is relative |
| **24fps = Cinematic Standard** | Motion cadence audiences associate with "film" — slight judder = emotional texture |
| **30fps = Broadcast/Reality Feel** | Smoother motion; associated with TV, news, live events — less "cinematic" |
| **60fps+ = Slow-Motion Source** | Shoot high, play back at timeline rate (24/30) for clean slow-mo |
| **Shutter Angle = Motion Blur Match** | 180° shutter (1/48s @ 24fps, 1/60s @ 30fps, 1/120s @ 60fps) for natural motion |

---

## 🎬 Frame Rate Decision Matrix

| Shooting Scenario | Recommended FPS | Timeline FPS | Playback Effect | Shutter Speed |
|-------------------|-----------------|--------------|-----------------|---------------|
| Narrative/Dialogue | 24fps | 24fps | Real-time cinematic | 1/48s (180°) |
| Documentary/Run-and-Gun | 24fps or 30fps | Match | Real-time | 1/48s or 1/60s |
| Action/Sports (normal) | 60fps | 24fps | 2.5x slow-mo | 1/120s |
| Action/Sports (extreme) | 120fps | 24fps | 5x slow-mo | 1/240s |
| B-Roll/Atmospheric | 60fps | 24fps | 2.5x slow-mo (optional) | 1/120s |
| Vlog/Social (talking head) | 30fps | 30fps | Real-time smooth | 1/60s |
| Timelapse Source | 1-2fps (interval) | 24fps | Hyper-speed | N/A |

---

## 📐 The Math: Converting Frame Rates

```
Slow-Motion Factor = Shooting FPS / Timeline FPS

Examples @ 24fps timeline:
  30fps → 1.25x slow (subtle)
  48fps → 2x slow
  60fps → 2.5x slow
  120fps → 5x slow
  240fps → 10x slow

% Speed in NLE = (Timeline FPS / Shooting FPS) × 100
  60fps → 24fps timeline = 40% speed
  120fps → 24fps timeline = 20% speed
```

---

## 🎬 DaVinci Resolve Workflow

### Project Setup
```
Project Settings → Master Settings → Timeline Frame Rate: 24 (or 30)
  → "Mismatched Frame Rate" → "Scale Entire Image to Fit" (or crop)
```

### Clip Interpretation (Media Pool)
```
Right-click clip(s) → Clip Attributes → Video Frame Rate:
  - Set to SHOOTING frame rate (not timeline rate)
  - Resolve now knows: "this clip is 60fps, play at 24fps = slow-mo"
```

### Retime Curve (Fine Control)
```
Right-click clip on timeline → Retime Curve → Speed Warp (Optical Flow)
  - For non-integer conversions (e.g., 30fps → 24fps = 80% speed)
  - Enable "Speed Warp" for AI frame interpolation
```

---

## ⚠️ Common Pitfalls & Fixes

| Problem | Root Cause | Solution |
|---------|------------|----------|
| "My 60fps looks choppy at 24fps" | Clip interpreted as 24fps (not 60fps) | Fix Clip Attributes → Video Frame Rate = 60 |
| "Motion blur looks wrong" | Shutter speed not matched to frame rate | 180° rule: 1/(2×FPS) — 1/48s@24, 1/120s@60 |
| "Mixed fps timeline looks weird" | Clips not interpreted before editing | Batch-set Clip Attributes in Media Pool first |
| "Can't get 24fps look at 1/50s shutter" | 1/50s ≠ 180° @ 24fps (that's ~173°) | Use 1/48s for true 180°; 1/50s = slight stutter |
| "Bright outdoor + 24fps + wide aperture" | Over-exposed at 1/48s | ND filters (variable or fixed) — not higher shutter |

---

## ✅ Verification Checklist

- [ ] Project timeline frame rate SET before import
- [ ] All clips: Clip Attributes → Video Frame Rate = SHOOTING rate
- [ ] Shutter speed matched to shooting frame rate (180° rule)
- [ ] ND filters used for exposure control (not shutter speed)
- [ ] Retime Curve / Speed Warp used for non-integer conversions
- [ ] Test export: verify motion cadence looks intended

---

## 🔗 Cross-References

| Topic | Vault Location |
|-------|----------------|
| Shutter Angle & Motion Blur | `DaVinci_Knowledge_Base/Videographer/Camera_Theory/Shutter-Angle-Guide.md` |
| DaVinci Resolve Clip Attributes | `DaVinci_Knowledge_Base/Videographer/Post-Production/Clip-Attributes.md` |
| Retime Curve & Speed Warp | `DaVinci_Knowledge_Base/Videographer/Post-Production/Retime-Curve.md` |
| ND Filter Guide | `DaVinci_Knowledge_Base/Videographer/Lenses_&_Optics/ND-Filters.md` |
| Slow-Motion Workflow | `DaVinci_Knowledge_Base/Videographer/Post-Production/Slow-Motion-Workflow.md` |

---

## 🏷️ Tags

`#videographer` `#reel` `#frame-rate` `#cinematography` `#camera-settings` `#slow-motion` `#davinci-resolve` `#cobikrumholz` `#instagram-learning`

---

*Skill generated by `instagram-videographer-learning-pipeline` on 2026-07-19 from Instagram Reel*