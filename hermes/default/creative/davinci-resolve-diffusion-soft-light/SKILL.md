---
name: davinci-resolve-diffusion-soft-light
description: "DaVinci Resolve diffusion/halation: Blur + Soft Light composite mode for optical glass look from @yancolorist."
version: 0.1.0
author: Hermes
metadata:
  hermes:
    tags: [DaVinci Resolve, Color Grading, Diffusion, Halation, Soft Light, Film Aesthetics]
---

# DaVinci Resolve — Diffusion / Halation via Blur + Soft Light

Learn the **Soft Light Diffusion** technique from @yancolorist — creating dreamy, ethereal highlight diffusion using blur tools and Soft Light composite modes to mimic optical glass filters in post (technique 8/10 in their most-used Resolve techniques).

## When to Use
- Adding romantic, nostalgic, surreal film aesthetics
- Softening digital sharpness from modern sensors
- Mimicking Pro-Mist, Glimmerglass, or Black Pro-Mist filters
- Highlight diffusion for poetic visual storytelling
- Reducing "perceived reality" for film aesthetics

## Prerequisites
- DaVinci Resolve (Free or Studio)
- Footage with good highlight detail
- Basic node graph and composite modes familiarity

## How to Run
Build the diffusion node chain in DaVinci Resolve Color page as described in **Procedure**.

## Quick Reference
| Step | Node | Tool | Key Setting |
|------|------|------|-------------|
| 1 | Node 01 | Blur (Box/Gaussian) | Radius: 10-50px |
| 2 | Node 02 | Composite Mode | **Soft Light** |
| 3 | Node 03 | Gain/Contrast | Control diffusion intensity |
| 4 | Optional | Qualifier | Protect shadows/skin |

## Procedure

### 1. Base Grade (Node 01)
- Complete your primary grade first (WB, exposure, contrast)
- Label: `BASE_GRADE`

### 2. Diffusion Blur (Node 02)
- **Serial Node** after base, label: `DIFFUSION_BLUR`
- **Blur OFX** (Resolve FX Blur → Box Blur or Gaussian Blur):
  - **Blur Radius:** 10-50 pixels (depends on resolution/desired strength)
  - **Aspect Ratio:** 1.0 (circular) or match lens
- **Composite Mode (Node 02):** **Soft Light**
  - This blends the blurred highlights into the image naturally
  - Soft Light = Screen on highlights + Multiply on shadows

### 3. Intensity Control (Node 03)
- **Serial Node** after Node 02, label: `DIFFUSION_INTENSITY`
- **Gain/Contrast** to control diffusion strength:
  - **Gain ↓** reduces highlight bloom
  - **Contrast ↑** increases diffusion pop
  - **Pivot** at 0.335 for filmic control

### 4. Shadow/Skin Protection (Optional)
- **Parallel Node** from Base Grade (bypass diffusion):
  - **Qualifier** on skin/shadows
  - **Alpha Output** → Layer Mixer to composite clean skin OVER diffusion
- Or: **Layer Mixer** with diffusion at reduced opacity on shadows

## Creative Variations

### A. Halation-Style (Red Highlight Bloom)
- Add **Color Wheels** on Diffusion Blur node:
  - **Gain:** Push **Red** slightly
  - **Gamma:** Slight **Red** lift
- Mimics film halation (red fringe on highlights)

### B. Glow + Diffusion Combo
- **Node 02a:** Blur (Large radius) → Soft Light
- **Node 02b:** Glow OFX (Threshold low, Size large) → Add
- Layer both for bloom + diffusion

### C. Anamorphic-Style (Horizontal Blur)
- **Blur OFX** → **Aspect Ratio:** 0.5 (horizontal only)
- Mimics anamorphic lens flare diffusion

### D. Pro-Mist Strength Grades
| Strength | Blur Radius | Soft Light Opacity | Use Case |
|----------|-------------|-------------------|----------|
| 1/8 (Subtle) | 5-10px | 30% | Natural, slight glow |
| 1/4 (Standard) | 15-25px | 50% | Classic Pro-Mist |
| 1/2 (Strong) | 30-50px | 70% | Dreamy, surreal |
| 1 (Heavy) | 50-100px | 100% | Surreal, music video |

## Pitfalls
| Issue | Cause | Fix |
|-------|-------|-----|
| Too much contrast/saturation | Soft Light adds contrast | Reduce diffusion opacity; add Contrast node ↓ |
| Skin looks soft/blurry | Diffusion affects entire frame | Qualifier + Layer Mixer to protect skin |
| Highlights blow out | Soft Light screens highlights | Lower Gain on diffusion node; add Soft Clip |
| Looks "digital filter" not optical | Uniform blur radius | Vary blur by luminance (qualifier on highlights only) |
| Color shift | Soft Light affects color | Desaturate diffusion node slightly (-10 to -20) |

## Verification
1. **Toggle diffusion nodes** — subtle highlight bloom, not overall blur
2. **Check scopes** — Waveform highlights bloom naturally, no clipping
3. **Skin check** — Talent sharp, not diffused
4. **Compare to optical** — Matches Pro-Mist/Glimmerglass look

## References
- Source: Instagram @yancolorist — "8/10 My most used techniques... Creating a dreamy, ethereal atmosphere... By using blur tools and Soft Light composite modes, we create highlight diffusion that mimics optical glass." (5 weeks ago at capture)
- Caption: "Do you prefer using physical filters on lens or creating the diffusion effect in post?"
- Hashtags: #davinciresolve #colorgrading #filmaesthetics

## Related Skills
- `davinci-resolve-cinematic-haze-effect` (Atmospheric haze via Lift/Gamma)
- `davinci-resolve-complementary-color-grading` (Creative looks)
- `davinci-resolve-cinematic-grading-3-mistakes` (Layer structure)