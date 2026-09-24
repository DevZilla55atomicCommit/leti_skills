---
name: davinci-resolve-gamut-io-fix-banding-luts
description: "Fix Banding with LUTs using Tetrahedral Interpolation — Gamut.io technical deep dive on LUT interpolation methods"
version: 0.1.0
author: Hermes
metadata:
  hermes:
    tags: [DaVinci Resolve, LUT, Banding, Tetrahedral Interpolation, Gamut.io, Technical, Color Science]
---

# Fix Banding with LUTs — Tetrahedral Interpolation (Gamut.io)

Technical deep dive from @gamut.io on fixing banding artifacts in LUTs using **tetrahedral interpolation** vs. trilinear interpolation.

## When to Use
- Applying LUTs that show banding/posterization
- Understanding LUT interpolation methods
- Technical color science deep dive
- Choosing LUT application settings

## Prerequisites
- DaVinci Resolve (Free or Studio)
- Basic LUT workflow understanding
- Interest in color science

## Quick Reference

| Interpolation Method | Quality | Speed | Banding Risk |
|---------------------|---------|-------|--------------|
| **Trilinear** | Lower | Faster | High |
| **Tetrahedral** | Higher | Slower | Low |
| **Pyramidal** | Highest | Slowest | Lowest |

---

## Core Concept

**LUTs are 3D lookup tables** — sparse grids of color transforms. When input values fall between grid points, Resolve must **interpolate**.

### Trilinear Interpolation (Default in many apps)
- Simple linear interpolation along 3 axes
- Creates "blocky" transitions between grid points
- **Visible banding** in smooth gradients (skies, skin)

### Tetrahedral Interpolation (Better)
- Divides each cube into **6 tetrahedra**
- Interpolates within tetrahedron containing the point
- **Smoother transitions**, less banding
- DaVinci Resolve uses this by default for 3D LUTs

---

## Procedure

### In DaVinci Resolve
1. **LUT Settings** → **Interpolation: Tetrahedral** (default)
2. For 1D LUTs: **Interpolation: Linear** (only option)
3. For 3D LUTs: **Tetrahedral** = best quality

### When Banding Persists
| Fix | How |
|-----|-----|
| **Increase LUT size** | 65³ → 129³ grid (more points = less interpolation) |
| **Add dithering** | Project Settings → Dithering ON |
| **Work in higher bit depth** | DWG/ACES 32-bit float pipeline |
| **Smooth source** | Slight noise/grain before LUT |

---

## Gamut.io's Technical Insight

> **Tetrahedral interpolation** splits each cube in the 3D LUT grid into 6 tetrahedra. The point falls in exactly one tetrahedron, and barycentric coordinates give smooth weights. This is mathematically superior to trilinear for color transforms.

**Key Takeaway:** Resolve's default tetrahedral interpolation is why LUTs look cleaner in Resolve than in other apps.

---

## Verification Checklist

- [ ] Confirm Resolve LUT interpolation = Tetrahedral (3D LUTs)
- [ ] Test problematic LUT: toggle Trilinear vs Tetrahedral
- [ ] Enable Project Dithering for 8/10-bit output
- [ ] Use 65³ or 129³ LUTs for critical work
- [ ] Grade in DWG (32-bit float) before LUT application

---

## References

- Source: Instagram @gamut.io — "Fix Banding with LUTs (Tetrahedral Interpolation)" (44 weeks ago)
- Hashtags: #davinciresolve #colortonediffuser #malaysiancolorist #filmcolorist #colourgrading #colorgrading #davinciresolve20
- Type: Technical carousel/video
- Community: High engagement from colorists

---

## Tags

```markdown
#davinci-resolve #lut #banding #tetrahedral-interpolation #gamut-io #color-science #interpolation #3d-lut #technical #color-grading
```