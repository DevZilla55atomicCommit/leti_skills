---
name: davinci-resolve-20-2-cinematic-haze
description: "DaVinci Resolve 20.2 Cinematic Haze — new native OFX tool for atmospheric haze/glow effects, presented by Blackmagic Design at IBC"
version: 0.1.0
author: Hermes
metadata:
  hermes:
    tags: [DaVinci Resolve 20.2, Cinematic Haze, OFX, Blackmagic Design, IBC, Atmospheric Effects, Native Tools, Free Version]
---

# DaVinci Resolve 20.2 — Cinematic Haze (New OFX)

Learn the **new Cinematic Haze OFX** introduced in DaVinci Resolve 20.2 — a native atmospheric haze/glow tool presented by Mike from Blackmagic Design at IBC. Works in **Free version**.

## When to Use
- Adding atmospheric depth/haze to any shot
- Creating "golden hour" or "magic hour" feel
- Simulating lens diffusion/halation organically
- Free-version atmospheric grading (no plugins needed)

## Prerequisites
- DaVinci Resolve **20.2+** (Free or Studio)
- Basic Color Page / OFX navigation

## Quick Reference

| Feature | Detail |
|---------|--------|
| **Tool Name** | Cinematic Haze (OFX) |
| **Category** | Resolve FX / OpenFX |
| **Version Introduced** | 20.2 |
| **Presented By** | Mike (Blackmagic Design) at IBC |
| **Free Version** | ✅ Yes |
| **Key Controls** | Amount, Size, Softness, Color, Blend Mode |

---

## Procedure

### 1. Find & Apply the Effect
1. Open **Effects Library** → **OpenFX** → **Resolve FX**
2. Search **"Cinematic Haze"** (new in 20.2)
3. Drag onto node (or create new serial node for it)

### 2. Key Controls & Settings

| Control | Range | Purpose | Starting Point |
|---------|-------|---------|----------------|
| **Amount** | 0–1+ | Overall haze intensity | 0.15–0.30 |
| **Size** | 0–100 | Spread/falloff of haze | 30–60 |
| **Softness** | 0–1 | Edge feathering | 0.5–0.8 |
| **Color** | Color picker | Haze tint (warm/cool) | Warm gold / cool blue |
| **Blend Mode** | Dropdown | Composite method | Screen / Add / Overlay |

### 3. Typical Workflows

#### A. Subtle Atmospheric Depth (Documentary/Narrative)
| Setting | Value |
|---------|-------|
| Amount | 0.10–0.20 |
| Size | 40–60 |
| Softness | 0.7 |
| Color | Neutral/warm (slight gold) |
| Blend | Screen |

#### B. Golden Hour / Magic Hour Enhancement
| Setting | Value |
|---------|-------|
| Amount | 0.25–0.40 |
| Size | 50–80 |
| Softness | 0.6 |
| Color | Warm gold (45–55° hue, 60–80% sat) |
| Blend | Overlay / Soft Light |

#### C. Cool Cinematic Haze (Sci-Fi/Thriller)
| Setting | Value |
|---------|-------|
| Amount | 0.15–0.30 |
| Size | 30–50 |
| Softness | 0.8 |
| Color | Cool teal (180–200° hue, 40–60% sat) |
| Blend | Screen / Add |

#### D. Lens Diffusion / Halation Mimic
| Setting | Value |
|---------|-------|
| Amount | 0.05–0.15 |
| Size | 20–40 |
| Softness | 0.9 |
| Color | Match highlight color |
| Blend | Add |

---

## Node Placement Strategy

| Position | Use Case |
|----------|----------|
| **After Creative, Before Output CST** | Standard — haze in working space |
| **Inside Parallel/Layer Mixer branch** | Isolate haze to specific zones (sky, background) |
| **Timeline Grade** | Global atmospheric look for entire scene |
| **Group Pre-Clip** | Consistent haze across scene |

---

## Pro Tips (from Blackmagic Demo)

| Tip | Detail |
|-----|--------|
| **Less is more** | Start at 0.1 Amount; build gradually |
| **Color matches light** | Warm haze for sun, cool for shade/moon |
| **Combine with Glow** | Cinematic Haze + Glow OFX = rich atmosphere |
| **Mask if needed** | Power Window on haze node = local atmosphere |
| **Animate Amount** | Keyframe for "haze rolling in" transitions |
| **Free version = full access** | No Studio-only restrictions on this OFX |

---

## Comparison: Cinematic Haze vs. Manual Methods

| Aspect | Cinematic Haze (20.2) | Manual (Blur + Soft Light) | Glow OFX |
|--------|----------------------|---------------------------|----------|
| **Speed** | ⚡ One node | 🐢 2–3 nodes | ⚡ One node |
| **Control** | Dedicated params | Full curve control | Threshold-based |
| **Naturalism** | High (purpose-built) | High (custom) | Medium (bloom-focused) |
| **Animation** | Native keyframes | Keyframe multiple | Native keyframes |
| **Free Version** | ✅ | ✅ | ✅ |

---

## Common Issues & Fixes

| Issue | Cause | Fix |
|-------|-------|-----|
| Haze looks "foggy/milky" | Amount too high | Reduce Amount; increase Softness |
| Color doesn't match scene | Wrong hue for light source | Match haze color to dominant light |
| Affects shadows too much | Blend mode = Screen | Try Overlay/Soft Light; or mask shadows |
| Banding in smooth gradients | 8-bit monitoring / compression | Work in DWG; add subtle grain after |
| Not in Effects Library | Resolve < 20.2 | Update to 20.2+ |

---

## Verification Checklist

- [ ] Locate Cinematic Haze in Resolve FX (OpenFX)
- [ ] Apply to node, adjust Amount 0.1→0.3 — see immediate effect
- [ ] Match haze Color to scene light source (warm/cool)
- [ ] Test Blend modes: Screen vs Overlay vs Add
- [ ] Combine with Glow OFX for richer atmosphere
- [ ] Mask haze to sky/background only via Power Window
- [ ] Keyframe Amount for dynamic transition

---

## References

- Source: Instagram @creatorsergeant — "Cinematic Haze in DaVinci Resolve 20.2" (41 weeks ago)
- Presented by: Mike (Blackmagic Design) at IBC
- Hashtags: #davinciresolve #davinciresolve20 #cinematichaze #ibc #blackmagicdesign #colorgrading #filmmaking
- Type: Reel (video demo with Mike from BMD)

---

## Tags

```markdown
#davinci-resolve #davinci-resolve-20-2 #cinematic-haze #ofx #resolve-fx #blackmagic-design #ibc #atmospheric-effects #haze #glow #diffusion #free-version #native-tools #creatorsergeant #color-grading
```