---
name: davinci-resolve-qualifier-focus-color-page
description: "DaVinci Resolve Qualifier Focus Mode — Precise HSL Selection Visualization for Clean Color Keys"
version: 1.0.0
author: Hermes
metadata:
  hermes:
    tags: [DaVinci Resolve, Color Grading, Qualifier, Color Correction, HSL Selection, Workflow]
---

# DaVinci Resolve Qualifier Focus Mode

Learn the **Qualifier Focus** feature in DaVinci Resolve's Color Page — a precision HSL selection visualization that shows ONLY qualified pixels in the viewer, eliminating guesswork from color keying.

## When to Use
- Precise color isolation for skin tones, skies, foliage, products
- Cleaning up noisy/bleeding qualifier selections
- Real-time HSL range adjustment with visual feedback
- Professional color grading workflows requiring precision

## Prerequisites
- DaVinci Resolve (Free or Studio) 17+
- Basic Color Page navigation
- Understanding of HSL color space

## Quick Reference

| Step | Action | Shortcut/Location |
|------|--------|-------------------|
| 1 | Add Qualifier Node | Right-click graph → Add Node → Serial |
| 2 | Open Qualifier Panel | Color Page → Bottom Right |
| 3 | **Enable Qualifier Focus** | **Viewer Toolbar → Magnifying Glass Icon** or **`Shift + F`** |
| 4 | Adjust HSL Ranges | Watch viewer = ONLY selection shows |
| 5 | Refine Edges | Clean Black / Clean White / Blur Radius |
| 6 | Disable Focus & Grade | `Shift + F` → Apply corrections |

## Procedure

### 1. Enable Qualifier Focus
Click the **Qualifier Focus icon** (magnifying glass with crosshair) in the **Viewer Toolbar** (top of viewer), or press **`Shift + F`**.

**Result:** Viewer shows **ONLY qualified pixels** in full color; everything else = pure black.

### 2. Dial HSL Selection (Real-Time)
With Focus ON, adjust sliders while watching viewer:
- **Hue:** Narrow range around target (Skin: 0.05-0.12)
- **Saturation:** Exclude low (shadows) + high (specular)
- **Luminance:** Target midtones (0.2-0.8)

### 3. Refine Matte
| Control | Purpose | Range |
|---------|---------|-------|
| Clean Black | Remove noise/shrink | 2-8 |
| Clean White | Fill gaps/expand | 1-5 |
| Blur Radius | Feather edges | 3-10 |
| Denoise | Temporal cleanup | 0.5-1.0 |

### 4. Exit Focus → Grade
Press `Shift + F` again → Normal viewer. Apply corrections to this node.

## Pitfalls

| Issue | Cause | Fix |
|-------|-------|-----|
| Flickering selection | No temporal denoise | Enable Denoise or keyframe |
| Hard edges | Blur = 0 | Add 3-8 Blur Radius |
| Wrong colors selected | Hue too wide | Narrow Hue; use Lum to exclude |
| Banding in matte | 8-bit + heavy qual | Blur 5+; 32-bit float project |

## Verification

- [ ] Focus enabled (`Shift + F`)
- [ ] Hue narrow (±0.02-0.05)
- [ ] Sat excludes shadows/highlights
- [ ] Lum targets midtones
- [ ] Clean Black/White/Blur set
- [ ] Focus disabled → grade applied
- [ ] Node toggle = clean selection

## Cross-References

| Skill | Topic |
|-------|-------|
| `davinci-resolve-skin-separation-layermixer-qualifier` | Skin isolation with Layer Mixer |
| `davinci-resolve-three-color-fundamentals-chrisseinn` | 3 pillars including subject isolation |
| `davinci-resolve-power-windows-parallel-nodes` | Power Window + Qualifier combo |

## References

- Source: Instagram @creatorsergeant — "Turn on the qualifier focus in the color page of DaVinci Resolve." (Reel: DFagthrsgkF)
- Vault Note: `DaVinci_Knowledge_Base/Color Correction Fundamentals/23-Qualifier-Focus-Color-Page_CreatorSergeant_Precise-Selection.md`