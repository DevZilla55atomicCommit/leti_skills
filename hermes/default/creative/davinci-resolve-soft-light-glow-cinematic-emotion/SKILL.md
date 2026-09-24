---
name: davinci-resolve-soft-light-glow-cinematic-emotion
description: "Soft Light glow technique in DaVinci Resolve — small glow, massive cinematic impact. Blur + Soft Light composite for mood, depth, and emotion."
version: 0.1.0
author: Hermes
metadata:
  hermes:
    tags: [DaVinci Resolve, Color Grading, Glow, Soft Light, Cinematic Look, Creative Grading]
    source_url: "https://www.instagram.com/reel/DY4iuOIMad2/"
    source_creator: "@mastermotion__cinematographer"
    source_date: "2025-05-28"
    vault_category: "Creative Grading & Looks"
    skill_level: "Beginner to Intermediate"
    tags: [Soft Light, Glow, Blur, Cinematic Emotion, Mood, Depth, Halation, Bloom, Mastermotion]
---

# DaVinci Resolve: Soft Light Glow for Cinematic Emotion

**Source:** [@mastermotion__cinematographer Instagram Reel](https://www.instagram.com/reel/DY4iuOIMad2/) — "Glow isn't just light… it's mood, depth, and cinematic emotion. Soft Light in DaVinci Resolve can turn a normal shot into a scene that feels alive. Small glow. Massive impact."

## Technique Overview

Using **Blur + Soft Light composite** to create organic, emotional glow that adds mood and depth — not just "bloom" but cinematic atmosphere.

> "Glow isn't just light… it's mood, depth, and cinematic emotion. Small glow. Massive impact."

---

## Node Structure

```
Node 01: Base Grade (Corrected, Balanced)
Node 02: **GLOW NODE** — Serial or Layer
  ├── Blur OFX (Radius: 30-80, depending on resolution)
  ├── Gain: 0.5-1.0 (controls glow intensity)
  └── Composite Mode: **Soft Light**
Node 03: Optional — Color Warper / Hue vs Sat to tint glow
Node 04: Output CST + Gamut Mapping
```

---

## Step-by-Step

### 1. Create Glow Node (Serial Node after base grade)
- Right-click node graph → **Add Node** → **Add Serial Node**
- Label: **"GLOW / Soft Light"**

### 2. Add Blur OFX
- Open Effects → **Blur** (or **Gaussian Blur**)
- **Radius:** 40-60 (HD), 60-100 (4K), 100+ (6K/8K)
- **HV Ratio:** 1.0 (uniform)
- **Border:** Replicate (prevents edge darkening)

### 3. Set Composite Mode to Soft Light
- In Node keyframe/composite controls (or Layer Mixer if using parallel)
- **Composite Mode: Soft Light**
- **Why Soft Light?** 
  - Brightens highlights, darkens shadows
  - Preserves midtone contrast
  - More organic than Add/Screen — doesn't wash out

### 4. Fine-Tune Intensity
| Control | Range | Effect |
|---------|-------|--------|
| **Gain (Key Output)** | 0.3–0.8 | Overall glow strength |
| **Blur Radius** | 30–100+ | Glow spread / "size" |
| **Blur HV Ratio** | 1.0 (circle) / 1.5 (anamorphic) | Shape |

### 5. Color the Glow (Optional, Advanced)
**Method A: Color Warper on Glow Node**
- Shift glow hue: Warm (30°) for golden hour, Cool (220°) for moonlight
- Desaturate slightly (-10 to -20) for natural feel

**Method B: Hue vs Sat Curve on Glow Node**
- Target glow hue range → adjust saturation independently

**Method C: Parallel Node + Layer Mixer**
```
Layer Mixer
├── Input 1: Main Grade
└── Input 2: Glow Node (Blur + Soft Light)
    └── Qualifier: Isolate highlights only (Luma > 0.7)
    └── Composite: Soft Light
```

---

## Parameter Presets

| Look | Blur Radius | Gain | Hue Tint | Vibe |
|------|-------------|------|----------|------|
| **Golden Hour Warmth** | 50 (HD) / 80 (4K) | 0.5 | +15° (warm) | Nostalgic, romantic |
| **Moonlight Cool** | 40 / 70 | 0.4 | -15° (cool) | Mystery, night |
| **Dreamy/Ethereal** | 80 / 120 | 0.6 | 0 (neutral) | Fantasy, memory |
| **Subtle Atmosphere** | 30 / 50 | 0.25 | +5° | Documentary, natural |
| **Anamorphic Bloom** | 60 / 100 (HV 1.5) | 0.45 | +10° | Cinematic, lens character |

---

## Pro Tips

1. **Isolate to Highlights:** Use **Qualifier (Luma > 0.75)** on glow node so only bright areas bloom
2. **Protect Skin:** Layer Mixer → Skin qualifier → bypass glow on faces
3. **Anamorphic Feel:** Blur HV Ratio = 1.5 (horizontal stretch)
4. **Animate:** Keyframe Gain for "breathing" glow (emotional beats)
5. **Combine with Halation:** Add separate Glow OFX (threshold 0.9) for specular halation

---

## Comment Insight

**@cinexmotiv:** *"Did you set the first node to CST or not? Do you even use CST in this?"*
→ **Implied Answer:** Yes, base grade should include proper CST pipeline. Glow is creative layer ON TOP of color-managed base.

---

## Related Techniques

- `davinci-resolve-diffusion-soft-light` — @yancolorist Blur + Soft Light for optical diffusion (Pro-Mist mimic)
- `davinci-resolve-cinematic-haze-effect` — @3rdvisionfilm Lift/Gamma + Glow OFX for atmospheric haze
- `davinci-resolve-hue-vs-luminance-density-saturation` — @ulterior_visuals density for color separation
- `davinci-resolve-cst-gamut-mapping-color-spill` — Output gamut safety

---

## Tags

`#davinciresolve` `#colorgrading` `#softlight` `#glow` `#blur` `#cinematic` `#mood` `#emotion` `#mastermotion` `#creativegrading` `#halation` `#bloom`