---
name: davinci-resolve-depth-map-tutorial-gabelomotey
description: "How to use Depth Map in DaVinci Resolve — FG/MG/BG layer isolation via Layer Mixer, atmospheric perspective by distance. Studio feature for depth-based grading."
version: 0.1.0
author: Hermes
metadata:
  hermes:
    tags: [DaVinci Resolve, Color Grading, Depth Map, Layer Mixer, Studio Feature]
    source_url: "https://www.instagram.com/reel/DSlhZfZEclo/"
    source_creator: "@gabelomoteycreative"
    source_date: "2025-12-22"
    vault_category: "Creative Grading & Looks"
    skill_level: "Intermediate"
    tags: [Depth Map, Layer Mixer, Foreground, Midground, Background, Atmospheric Perspective, Gabelomotey]
---

# DaVinci Resolve: Depth Map Tutorial — @gabelomoteycreative

**Source:** [@gabelomoteycreative Instagram Reel](https://www.instagram.com/reel/DSlhZfZEclo/) — "How to use Depth Map in DaVinci Resolve"

## Technique Overview

**Depth Map in DaVinci Resolve (Studio feature)** — Foreground/Midground/Background layer isolation via Layer Mixer, atmospheric perspective by distance. "Not just focus, shape emotion."

> *"How to use Depth Map in DaVinci Resolve 🎨✨"*

---

## What is Depth Map?

| Feature | Details |
|---------|---------|
| **Availability** | DaVinci Resolve **Studio** only |
| **Source** | Depth from focus / LiDAR / stereo / AI |
| **Output** | Grayscale map: White = Close, Black = Far |
| **Use** | Layer isolation by distance |

---

## Node Structure with Layer Mixer

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    DEPTH MAP GRADING (Studio)                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────┐  ┌────────────────────────────────────────────────────────┐  │
│  │  INPUT   │──▶│              LAYER MIXER                               │  │
│  │  (Clip)  │   │                                                       │  │
│  └──────────┘   │  ┌─────────┐  ┌─────────┐  ┌─────────┐               │  │
│                 │  │ INPUT 1 │  │ INPUT 2 │  │ INPUT 3 │               │  │
│                 │  │   FG    │  │   MG    │  │   BG    │               │  │
│                 │  │ (Near)  │  │ (Mid)   │  │ (Far)   │               │  │
│                 │  │         │  │         │  │         │               │  │
│                 │  │ Qual:   │  │ Qual:   │  │ Qual:   │               │  │
│                 │  │ Depth   │  │ Depth   │  │ Depth   │               │  │
│                 │  │ Map     │  │ Map     │  │ Map     │               │  │
│                 │  │ White   │  │ Gray    │  │ Black   │               │  │
│                 │  └────┬────┘  └────┬────┘  └────┬────┘               │  │
│                 │       │           │           │                       │  │
│                 │       ▼           ▼           ▼                       │  │
│                 │  ┌─────────────────────────────────────┐              │  │
│                 │  │        COMPOSITE: Normal            │              │  │
│                 │  └─────────────────────────────────────┘              │  │
│                 └────────────────────────────────────────────────────────┘  │
│                                     │                                       │
│                                     ▼                                       │
│                              ┌────────────┐                                │
│                              │  OUTPUT    │                                │
│                              └────────────┘                                │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Depth Map Qualifier Settings

| Layer | Depth Range | Qualifier Settings |
|-------|-------------|-------------------|
| **Foreground** | Near (0-30%) | **Luma High:** ~0.3, **Luma Low:** 0.0 |
| **Midground** | Middle (30-70%) | **Luma High:** ~0.7, **Luma Low:** ~0.3 |
| **Background** | Far (70-100%) | **Luma High:** 1.0, **Luma Low:** ~0.7 |

> **Tip:** Use soft transitions (Blur on Qualifier) for natural blending

---

## Grading Each Layer

| Layer | Typical Adjustments |
|-------|---------------------|
| **Foreground** | Contrast ↑, Saturation ↑, Sharpness ↑, Warmth ↑ |
| **Midground** | Balanced, subject focus, skin tones |
| **Background** | Contrast ↓, Saturation ↓, Cool shift, Haze/Glow |

### Atmospheric Perspective
- **FG:** High contrast, warm, saturated
- **MG:** Neutral, natural
- **BG:** Low contrast, cool, desaturated, hazy

---

## Comment Insights

| Comment | Insight |
|---------|---------|
| @capturedbysadiq | *"🔥🔥"* |
| @swans_production | *"Are you making it on youtube?"* |
| @athletic.aperture | *"Using depth map as stylized look, using Xbox Kinect"* → Creative reuse |
| @levi_kovach | *"Woah, def saving this for later!"* |
| @eyeofty.za | *"Make it a compound node to clean up node tree... simplifying your tree is easiest way to get started"* → **Pro tip: Compound Node** |
| @way.2b.me | *"Good explanation, now let's see if my laptop can even run it"* → Studio + GPU heavy |

---

## Pro Tips

1. **Compound Node** — Wrap Layer Mixer + Qualifiers for clean tree
2. **Soft Transitions** — Blur Qualifier masks (radius 10-20)
3. **Atmospheric Grading** — Cool/desaturate BG for depth
4. **Keyframe Depth** — Animate focus pull in post
5. **Save as PowerGrade** — Reusable depth grading template

---

## Related Techniques

- `davinci-resolve-depth-map-grading` — @mastermotion depth map grading
- `davinci-resolve-cinematic-haze-effect` — Native haze for BG
- `davinci-resolve-soft-light-glow-cinematic-emotion` — Glow for atmospheric depth

---

## Tags

`#davinciresolve` `#colorgrading` `#depth-map` `#layer-mixer` `#foreground` `#midground` `#background` `#atmospheric-perspective` `#studio` `#gabelomoteycreative`