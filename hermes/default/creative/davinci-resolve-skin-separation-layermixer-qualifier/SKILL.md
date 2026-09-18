---
name: davinci-resolve-skin-separation-layermixer-qualifier
description: "DaVinci Resolve Skin Separation: Layer Mixer + Qualifier for clean skin isolation & protected grading"
version: 0.1.0
author: Hermes
metadata:
  hermes:
    tags: [DaVinci Resolve, Color Grading, Skin Tones, Layer Mixer, Qualifier, Masking & Power Windows]
---

# DaVinci Resolve Skin Separation — Layer Mixer + Qualifier

Learn the **Skin Separation** technique from @marcoherbst.work — clean skin isolation using Layer Mixer + Qualifier for protected High-End grading.

## When to Use
- Commercial/beauty work where skin tones must remain natural while background gets creative look
- Narrative grading where skin protection is critical across varying lighting
- Any project needing precise skin/hue isolation without Power Windows

## Prerequisites
- DaVinci Resolve (Free or Studio) 18+
- Basic node graph understanding
- Familiarity with Qualifier and Layer Mixer

## Quick Reference
| Step | Node | Tool | Key Action |
|------|------|------|------------|
| 1 | Node 01 — Skin | Qualifier | Select skin tones in Highlight Mode |
| 2 | Node 01 — Skin | Qualifier > Matte Finesse | Clean Black/White, Blur, Denoise |
| 3 | Node 01 — Skin | Hue vs Hue | Refine skin hue for natural tone |
| 4 | Layer Mixer | Layer Mixer | Composite: Skin (bottom) + Look (top) |
| 5 | Node 02 — Look | Color Wheels/Curves | Build creative grade on background only |

## Procedure

### 1. Node Setup — Create Layer Mixer Structure
- Add a new **Node** → right-click → **Add Layer Mixer**
- **Bottom input (Node 01)**: Label **"Skin"** — this isolates & protects skin
- **Top input (Node 02)**: Label **"Look"** — this carries your creative grade
- **Why**: Separates structure (skin protection) from creativity (look) from the start

### 2. Skin Selection — Qualifier in Highlight Mode
- On **Node 01 (Skin)**: Open **Qualifier** panel
- Enable **Highlight Mode** (eyeball icon) — shows exactly what mask captures
- Use **HSL qualifier** (pipette + drag) to select skin tones
- Hold mouse while selecting to see real-time highlight preview
- **Goal**: Capture all skin, exclude background/clothing

### 3. Matte Finesse — Clean the Mask
On Node 01 Qualifier > **Matte Finesse**:
| Setting | Typical Value | Purpose |
|---------|---------------|---------|
| **Clean Black** | 5–15 | Crush near-black noise in mask |
| **Clean White** | 5–15 | Clip near-white fringe |
| **Blur Radius** | 1–3 px | Soften mask edges |
| **Denoise** | 1–5 | Remove flicker/micro-noise |
| **In/Out Ratio** | Adjust | Fine-tune edge roll-off |

**Iterate** until mask is clean — no flicker, no halos, skin only.

### 4. Skin Tone Refinement — Hue vs Hue
- On Node 01: Open **Hue vs Hue** curve
- Target the **skin hue band** (~25–45° on vectorscope skin-tone line)
- Nudge curve to correct any magenta/green shift
- **Result**: Natural, consistent skin hue regardless of lighting

### 5. Build the Look — Node 02 (Look Input)
- Switch to **Node 02 (Look)** — this feeds Layer Mixer **top** input
- Apply your creative grade: Color Wheels, Curves, Color Slice, LUTs, etc.
- **Skin is untouched** because Layer Mixer composites Node 01 (clean skin) **under** Node 02 (look)
- Adjust Layer Mixer **Composite Mode** if needed (default = Normal works for most)

## Key Principles
| Principle | Application | Why It Works |
|-----------|-------------|--------------|
| **Structure before creativity** | Skin node first, then Layer Mixer, then Look | Guarantees skin protection isn't an afterthought |
| **Qualifier + Matte Finesse > Power Window** | Precise hue-based selection with cleanup | Tracks skin automatically; no manual tracking needed |
| **Hue vs Hue for skin fidelity** | Micro-adjust skin hue post-mask | Fixes qualifier spill without affecting look |
| **Layer Mixer = non-destructive composite** | Skin (bottom) + Look (top) | Look changes never touch skin node |

## Common Pitfalls & Fixes
| Symptom | Cause | Fix |
|---------|-------|-----|
| Mask flickers on movement | Denoise too low / Clean Black/White off | Increase Denoise 2–5; nudge Clean Black/White |
| Halo around face/ears | Blur Radius too high / Matte edge hard | Reduce Blur to 1–2; adjust In/Out Ratio |
| Skin looks gray/desaturated | Qualifier pulled too wide (includes shadows) | Narrow HSL range; use Highlight Mode to verify |
| Look bleeds into skin | Layer Mixer inputs swapped | Ensure Skin = bottom, Look = top |
| Hue vs Hue shifts wrong colors | Curve affects non-skin hues | Limit curve to skin-tone band only (25–45°) |

## Verification Checklist
- [ ] Toggle Node 01 ON/OFF → skin changes, background stable
- [ ] Toggle Node 02 ON/OFF → background changes, skin stable
- [ ] Scopes: Waveform 64–940 (legal), Parade balanced, Vectorscope skin on line
- [ ] Shot match: Apply template to 3+ clips — only Node 01 Qualifier needs per-shot tweak

## References
- Source: Instagram @marcoherbst.work — "Skin Separation in DaVinci Resolve – so isolierst du deine Hauttöne perfekt" (29 weeks ago)
- Hashtags: #DaVinciResolve #ColorGrading #SkinTones #Colorist #Filmmaking
- Type: Carousel post (multi-slide educational)

## Tags
```markdown
#davinci-resolve #skin-separation #layer-mixer #qualifier #matte-finesse #hue-vs-hue #masking-power-windows #color-grading #creative-grading #workflow
```