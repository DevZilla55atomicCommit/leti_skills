---
name: davinci-resolve-orange-teal-parallel-nodes
description: "DaVinci Resolve Orange & Teal: Parallel nodes for split-tone with skin protection via Hue vs Sat/Hue"
version: 0.1.0
author: Hermes
metadata:
  hermes:
    tags: [DaVinci Resolve, Color Grading, Creative Grading & Looks, Orange & Teal, Parallel Nodes, Skin Protection]
---

# DaVinci Resolve Orange & Teal — Parallel Nodes Split-Tone

Learn the **Quick Orange & Teal** technique from @mansourmelouli — parallel nodes for background teal grade + skin recovery via Hue vs Sat/Hue curves.

## When to Use
- Fast cinematic look for narrative/commercial/social content
- When you need teal shadows/midtones but natural skin tones
- Free-version compatible (no Studio required)
- Shot-to-shot consistency via parallel node template

## Prerequisites
- DaVinci Resolve (Free or Studio) 18+
- Basic node graph understanding
- Familiarity with Color Wheels, Curves, Qualifier

## Quick Reference
| Step | Node | Tool | Key Action |
|------|------|------|------------|
| 1 | Node 01 | Parallel Node | Add parallel mixer (2 inputs) |
| 2 | Top (BG) | Lift Wheel | Push Teal into shadows/midtones |
| 3 | Top (BG) | Log Wheels | Warmth in black point for depth |
| 4 | Top (BG) | Waveform | Verify blacks clean, not crushed |
| 5 | Bottom (Skin) | Hue vs Sat | Qualifier pick skin → boost saturation |
| 6 | Bottom (Skin) | Hue vs Hue | Fine-tune skin to vectorscope skin-tone line |
| 7 | Mixer | Key Output | Adjust blend strength if needed |

## Procedure

### 1. Create Parallel Node Structure
- On Color Page: Right-click a node → **Add Parallel Node**
- Creates **Parallel Mixer** with 2 inputs:
  - **Top Input** = Background grade (gets the teal look)
  - **Bottom Input** = Skin recovery (protects subject)

### 2. Top Node — Background Teal Grade
**Goal**: Cool teal shadows/midtones for cinematic "blockbuster" palette

| Tool | Setting | Why |
|------|---------|-----|
| **Lift Wheel** | Push toward **Teal** (cyan-blue) | Cools shadows & midtones |
| **Gamma Wheel** | Slight Teal push (optional) | Extends teal into midtones |
| **Log Wheels — Shadows** | Small **Warm** push (orange/red) | Keeps black point depth, prevents flatness |
| **Waveform** | Monitor | Blacks stay clean (above 64), no crush from tint |

**Mansour's Tip:** *"Use the Log wheels to add a touch of warmth back into your black point, keeping depth."*

### 3. Bottom Node — Skin Recovery
**Goal**: Restore natural skin saturation & hue after teal contamination

| Tool | Action | Detail |
|------|--------|--------|
| **Hue vs Sat Curve** | Qualifier picker → click skin | Widens selection slightly around skin tones |
| **Hue vs Sat** | Boost curve at skin hue (~30–40°) | Brings life back to skin |
| **Hue vs Hue Curve** | Qualifier picker → skin | Fine-tune hue toward **Vectorscope skin-tone line** |
| **Vectorscope** | Skin tone line reference | Pull skin hue to sit on line |

### 4. Blend Control
- If teal too strong on skin: Lower **Key Output Gain** on Top (BG) node
- If skin recovery too strong: Reduce **Hue vs Sat** boost on Bottom node
- **Parallel Mixer** defaults to Normal composite — adjust opacity per node if needed

## Key Principles
| Principle | Application | Why It Works |
|-----------|-------------|--------------|
| **Parallel = Independent** | BG grade & Skin recovery run simultaneously | Neither affects the other's source pixels |
| **Teal in Lift/Gamma** | Shadows/midtones get cinematic cool | Highlights stay clean for skin recovery |
| **Warmth in Log Shadows** | Black point retains depth | Prevents "muddy" crushed blacks from teal tint |
| **Hue vs Hue for skin fidelity** | Micro-adjust hue post-saturation | Vectorscope skin-tone line = perceptual anchor |

## Common Pitfalls & Fixes
| Symptom | Cause | Fix |
|---------|-------|-----|
| Skin looks green/sickly | Teal bleed into skin tones | Increase Hue vs Sat boost; verify Hue vs Hue on skin-tone line |
| Blacks crushed / noisy | Lift push too far + Log Shadows cold | Pull back Lift; add warmth via Log Shadows |
| Look too flat | No contrast separation | Add S-curve on Master or per-node Contrast |
| Skin oversaturated | Hue vs Sat boost too high | Lower curve; reduce Key Output on BG node |
| Inconsistent across shots | Manual per-shot tweaks | Save Parallel structure as **Compound Node → PowerGrade** |

## Verification Checklist
- [ ] Toggle Top node ON/OFF → BG changes, skin stable
- [ ] Toggle Bottom node ON/OFF → Skin changes, BG stable
- [ ] Vectorscope: Skin tones sit on skin-tone line (±2°)
- [ ] Waveform: Legal range 64–940, no crush in blacks
- [ ] Parade: RGB balanced in neutrals, teal bias in shadows only
- [ ] Shot match: Apply template to 3+ clips — only Hue vs Sat/Hue need per-shot tweak

## References
- Source: Instagram @mansourmelouli — "Quick and Easy Orange & Teal look in DaVinci Resolve" (28 weeks ago)
- Hashtags: #colorgrading #DaVinciResolve #colorist #videographer #photographer
- Type: Reel (video tutorial with on-screen text steps)

## Tags
```markdown
#davinci-resolve #orange-teal #parallel-nodes #split-tone #skin-protection #hue-vs-sat #hue-vs-hue #creative-grading #color-grading #mansourmelouli #free-version-compatible
```