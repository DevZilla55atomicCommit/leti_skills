---
name: davinci-resolve-color-compressor_davinciresolved
category: creative
description: "Color Compressor OFX in DaVinci Resolve 20+ Studio — Gamut mapping for smooth out-of-gamut compression, hue/lightness preservation, color spill fix"
tags:
  - davinci-resolve
  - color-grading
  - color-compressor
  - ofx
  - gamut-mapping
  - studio-only
  - davinci-resolve-20
  - color-spill
  - oversaturation
version: "1.0"
author: "Hermes Agent"
source_url: "https://www.instagram.com/reel/DKAAH6VvR7H/"
creator: "@davinciresolved"
vault_file: "Color Management & Pipeline/60-Color-Compressor_davinciresolved_OFX-Gamut-Mapping.md"
---

# Color Compressor OFX — DaVinci Resolve 20+ Studio Gamut Mapping

## Overview
Resolve 20+ Studio exclusive OFX for **smooth gamut mapping** — compresses out-of-gamut colors into target space preserving hue and lightness. Replaces hard clipping with filmic rolloff.

## When to Use
- Creative grades pushing beyond Rec.709/P3
- LUT application creating out-of-gamut colors
- HDR→SDR trim pass gamut mapping
- Mixed footage gamut normalization
- Color spill/contamination cleanup
- **Requires**: Resolve 20+ Studio (not Free)

## Prerequisites
- DaVinci Resolve 20+ Studio
- Color managed or manual CST pipeline
- CIE Diagram scope familiarity
- Basic gamut/color space understanding

## Core Concept

> **Compress, don't clip** — Smooth rolloff at gamut boundary preserves hue relationships and luminance.

---

## Node Placement

```
Node 01: CST / Input Transform
Node 02: Primary Balance
Node 03: Creative Grade (may push out of gamut)
Node 04: [COLOR COMPRESSOR OFX] — Gamut Mapping
Node 05: Output Transform / Final Polish
```

**Critical**: After creative grade, before output transform.

---

## Parameters

| Parameter | Options | Recommended | Function |
|-----------|---------|-------------|----------|
| **Mode** | Clip / Compress | **Compress** | Clip=hard; Compress=smooth |
| **Target Gamut** | Rec.709 / P3 / Rec.2020 / Custom | **Match Output** | Destination space |
| **Compression Strength** | 0-1 | 0.5-1.0 | Aggressiveness |
| **Preserve Lightness** | On/Off | **ON** | Lock luminance |
| **Preserve Hue** | On/Off | **ON** | Lock hue angle |
| **Roll-off** | Soft/Hard | **Soft** | Transition quality |

---

## Setup by Delivery

### SDR (Rec.709)
```
Target Gamut: Rec.709
Mode: Compress
Strength: 0.7-1.0
Preserve Lightness: ON
Preserve Hue: ON
Roll-off: Soft
```

### HDR (P3-D65 / Rec.2020)
```
Target Gamut: P3-D65 or Rec.2020
Mode: Compress
Strength: 0.5-0.8
Preserve Lightness: ON
Preserve Hue: ON
Roll-off: Soft
```

### Custom (VFX/Archival)
```
Target Gamut: Custom (.cube/.icc)
Mode: Compress
Strength: Per project
Preserve Lightness: ON
Preserve Hue: ON
```

---

## Verification (Scopes)

1. **CIE Diagram** — Watch gamut boundary, no hard corners
2. **Parade RGB** — No hard clip at 1.0
3. **Vectorscope** — Saturation compressed, hue stable
4. **Waveform** — Luminance flat (Preserve Lightness ON)

---

## Use Cases

| Scenario | Why Compressor |
|----------|----------------|
| Heavy creative grade | Saturation pushes beyond Rec.709 |
| Film LUT application | LUTs often exceed output gamut |
| HDR→SDR trim | Gamut mapping step |
| Mixed camera gamuts | Normalize to target |
| Green spill / reflections | Targeted hue compression |

---

## vs Alternatives

| Method | Pros | Cons |
|--------|------|------|
| **Color Compressor** | Smooth, hue-preserving, luminance-aware | Studio 20+ only |
| CST Gamut Mapping | Free, built-in | Less control, per-clip |
| Saturation Reduction | Simple | Dulls all, hue shifts |
| Soft Clip (Curves) | Free, flexible | Manual, per-channel |
| LUT with Gamut Map | Baked | Not adjustable |

---

## Pro Tips

1. **Qualify in DWG/Working Space** — Not Rec.709 (per @charliejamesrobertson)
2. **After Creative Grade** — Compress result, not source
3. **CIE Scope Active** — Visualize boundary real-time
4. **Strength by Eye** — Start 0.5, increase until clipping gone
5. **Save PowerGrade** — Reusable across projects
6. **HDR→SDR Trim** — Use in trim pass

---

## Common Pitfalls

| Mistake | Symptom | Fix |
|---------|---------|-----|
| Before creative grade | Compresses source | **After creative grade** |
| Wrong Target Gamut | Double mapping | **Match output space** |
| Strength always 1.0 | Over-compressed, flat | **Dial 0.5-0.8** |
| Preserve Lightness OFF | Luminance shifts | **Keep ON** |
| On Free version | Effect missing | **Studio 20+ required** |

---

## Community Insights

- **@charliejamesrobertson**: "Qualify in rec709?" → **Qualify in working space (DWG)**
- **@waynetaylormadethese**: "Lifesaver... had no idea this was in DaVinci"
- **@cj_dadd**: "You're insane" — High impact
- **Community**: "Goat resolver" — Trusted source

---

## Related Skills
- `davinci-resolve-cst-gamut-mapping-color-spill` — CST-based (Free)
- `davinci-resolve-gamut-io-fix-banding-luts` — Tetrahedral LUT interp
- `davinci-resolve-color-management-timeline_caleboshi` — Timeline CM
- `davinci-resolve-cst-gamut-mapping-williamsamehfilm` — CST saturation method

---

## References
- Source: @davinciresolved Instagram Reel (May 23, 2025)
- Hashtags: #davinci #davinciresolve #videoediting
- Engagement: 2,893 likes, 24 comments
- Resolve Version: 20+ Studio only