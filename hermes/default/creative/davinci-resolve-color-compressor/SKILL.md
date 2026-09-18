---
name: davinci-resolve-color-compressor
category: creative
description: "Color Compressor OFX in DaVinci Resolve 20+ Studio — unified gamut mapping and highlight compression with built-in skin tone protection"
tags:
  - davinci-resolve
  - color-grading
  - color-compressor
  - gamut-mapping
  - highlight-compression
  - hdr-tools
  - resolve-20
  - studio-only
  - skin-tone-protection
version: "1.0"
author: "Hermes Agent"
source_url: "https://www.instagram.com/reel/DKAAH6VvR7H/"
creator: "@davinciresolved"
vault_file: "Color Correction Fundamentals/18-Color-Compressor_davinciresolved_Gamut-Highlight-Compression.md"
---

# Color Compressor in DaVinci Resolve

## Overview
Resolve 20+ Studio OFX that combines gamut mapping, highlight compression, and skin tone protection in a single node — essential for wide-gamut → Rec.709 and HDR → SDR workflows.

## When to Use
- Camera wide gamut → Rec.709/P3 delivery (S-Gamut3, DWG, etc.)
- HDR → SDR tone mapping with highlight rolloff
- Any gamut compression where skin tones must survive
- **Studio only** — not in Free version
- **Before creative grade** — compress technical, then grade artistically

## Prerequisites
- DaVinci Resolve **Studio 20+**
- Color Managed pipeline (DaVinci YRGB CM) or manual CST to DWG
- Basic scope reading (Vectorscope, Waveform, Parade)

## Node Structure

```
Node 01: Input CST → DaVinci Wide Gamut (DWG)
Node 02: Primary Balance (Exposure, WB, Contrast)
Node 03: [COLOR COMPRESSOR OFX] ← Single node does it all
Node 04: Creative Grade (in compressed space)
Node 05: Output CST (if not color managed)
```

## Step-by-Step Procedure

### 1. Project Color Management Setup
```
Project Settings → Color Management:
├── Mode: DaVinci YRGB Color Managed
├── Input: [Camera - S-Log3/S-Gamut3.Cine, etc.]
├── Timeline: DaVinci Wide Gamut (DWG)
├── Output: [Target - Rec.709, P3, Rec.2020]
└── Tone Mapping: None (Color Compressor handles)
```

### 2. Add Color Compressor OFX (Node 03)
- Effects Library → **Resolve FX Color** → **Color Compressor**
- Drag to Node 03 (serial after primary balance)

### 3. Configure Gamut Compression
| Parameter | Recommended | Notes |
|-----------|-------------|-------|
| **Enable Gamut** | ✅ On | |
| **Source Gamut** | Timeline (DWG) | Auto from CM |
| **Target Gamut** | Output (Rec.709/P3) | Auto from CM |
| **Method** | **Perceptual** | Preserves hue, best for skin |
| **Strength** | 0.5-1.0 | 0.7 typical; 1.0 = full compress |

**Methods:**
- **Perceptual**: Hue-preserving, compresses saturation (RECOMMENDED)
- **Saturation**: Saturation-only, may shift hue
- **Luminance**: Luminance compression (rare)

### 4. Configure Highlight Compression
| Parameter | SDR (Rec.709) | HDR (P3/2020) | Notes |
|-----------|---------------|---------------|-------|
| **Enable HL** | ✅ On | ✅ On | |
| **Threshold** | 0.85-0.95 | 100-300 nits | Start of rolloff |
| **Strength** | 0.5-0.8 | 0.5-0.8 | Aggressiveness |
| **Shape** | **Soft** | Soft/Medium | Soft = filmic |

### 5. Enable Skin Tone Protection (CRITICAL)
| Parameter | Setting | Why |
|-----------|---------|-----|
| **Enable Skin** | ✅ On | |
| **Hue Center** | 35° (default) | Adjust to your talent |
| **Hue Range** | ±25° | Cover skin variation |
| **Sat Range** | 0.2-0.6 | Mid-sat skin tones |
| **Lum Range** | 0.2-0.8 | Mid-luminance skin |
| **Protection** | 0.8-1.0 | High = skin untouched |

### 6. Verify on Scopes
- **Vectorscope**: Skin on skin-tone line (±2°)
- **Waveform**: Smooth highlight rolloff, no hard clip at 1023/940
- **Parade RGB**: Channels compress together (no color shift)
- **CIE Diagram**: Visual gamut compression (if available)

## Parameter Presets

| Workflow | Gamut Method | Strength | HL Thresh | HL Strength | HL Shape | Skin Protect |
|----------|--------------|----------|-----------|-------------|----------|--------------|
| **S-Gamut3 → Rec.709** | Perceptual | 0.8 | 0.90 | 0.7 | Soft | 0.9 |
| **DWG → Rec.709 SDR** | Perceptual | 0.7 | 0.85 | 0.6 | Soft | 0.8 |
| **DWG → P3 HDR** | Perceptual | 0.5 | 200 nits | 0.5 | Medium | 0.7 |
| **Rec.2020 → Rec.709** | Perceptual | 1.0 | 0.90 | 0.8 | Soft | 1.0 |
| **Aggressive** | Saturation | 1.0 | 0.80 | 1.0 | Hard | 0.5 |
| **Skin Priority** | Perceptual | 0.6 | 0.90 | 0.5 | Soft | 1.0 |

## Advanced Workflows

### Dual Color Compressor (Separate Control)
```
Node 03a: Color Compressor — Gamut ONLY (HL disabled)
Node 03b: Color Compressor — HL ONLY (Gamut disabled)
```
Independent tuning for each compression type.

### Pre-Compression Saturation Boost
```
Node 02a: Primary Balance
Node 02b: Saturation +15-20% (expand gamut)
Node 03: Color Compressor (compresses expanded range naturally)
```
Richer colors that survive compression better.

### HDR → SDR Complete (Studio)
```
Timeline: DWG / ST.2084 / 1000 nits
Node 03: Color Compressor
  ├── Gamut: DWG → Rec.709 (Perceptual, 0.7)
  ├── Highlights: On, Threshold 200 nits, Soft, 0.7
  └── Skin Protect: On, 0.9
Node 04: Creative Grade (SDR space)
Output: Rec.709 / Gamma 2.4
```

### Non-Color-Managed with CST
```
Node 01: CST Camera → DWG
Node 02: Balance
Node 03: Color Compressor (DWG → Rec.709)
Node 04: Creative
Node 05: CST DWG → Rec.709 (or skip if CC did output)
```

## Comparison Matrix

| Feature | Color Compressor | CST Gamut Map | Manual Curves | HDR Wheels |
|---------|------------------|---------------|---------------|------------|
| Gamut Compression | ✅ Perceptual | ✅ Basic | ❌ | ❌ |
| Highlight Compression | ✅ Integrated | ❌ | ✅ Curves | ✅ HDR Wheels |
| Skin Protection | ✅ Built-in | ❌ | ❌ Manual | ❌ |
| Unified Control | ✅ Single OFX | ❌ Separate | ❌ Multiple | ❌ |
| Free Version | ❌ Studio | ✅ | ✅ | ✅ |
| HDR→SDR | ✅ Excellent | ⚠️ Basic | ⚠️ Complex | ✅ Good |

## Common Pitfalls

| Issue | Cause | Fix |
|-------|-------|-----|
| Skin desaturated | Gamut strength high, skin protect off | Lower strength, enable skin protect |
| Highlights clipping | Threshold too high / strength low | Lower threshold, increase strength |
| Hue shifts | Method = Saturation | Use **Perceptual** |
| Flat/milky image | Over-compression (both) | Reduce strengths, check waveform |
| OFX not found | Free version / Resolve < 20 | Requires **Studio 20+** |
| Double compression | CC + CST both gamut map | Disable CST gamut, let CC handle |

## Pro Tips from Community

- **@charliejamesrobertson**: "Qualifying in rec709?" → Qualify in **wide gamut (DWG)** before compression for cleaner mattes
- **@waynetaylormadethese**: "Lifesaver, had no idea this was in DaVinci" — Resolve 20 hidden gem
- **@marcusg490**: "Never heard of this" — Even pros miss new OFX
- **@mert.creative**: "You're insane" — Workflow efficiency praise

## Related Skills
- `davinci-resolve-auto-balance-ivarbrauer` — Initial WB before compression
- `davinci-resolve-white-balance-luma-mix` — Precision WB
- `davinci-resolve-cinematic-haze-20-2` — Resolve 20.2 features
- `davinci-resolve-gamut-io-fix-banding-luts` — LUT gamut issues

## References
- Source: @davinciresolved Instagram Reel (May 23, 2025)
- Hashtags: #davinci #davinciresolve #videoediting
- Requires: DaVinci Resolve Studio 20+