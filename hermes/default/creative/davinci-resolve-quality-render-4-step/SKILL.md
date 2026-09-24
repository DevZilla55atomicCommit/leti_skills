---
name: davinci-resolve-quality-render-4-step
description: "DaVinci Resolve Quality Render in 4 Steps: CST → Film Emulation + Primaries → DCTL & Glow → Magic Mask. Loris Marie's Ultimate PowerGrade workflow."
version: 0.1.0
author: Hermes
metadata:
  hermes:
    tags: [DaVinci Resolve, Color Grading, Workflow, CST, Film Emulation, DCTL, Glow, Magic Mask, PowerGrade, Loris Marie]
---

# DaVinci Resolve — Quality Render in 4 Steps (Loris Marie)

Learn the **4-step quality render workflow** from @loris_marie — CST conversion, film emulation with primaries, DCTL + Glow, and Magic Mask refinement. Part of her "Ultimate PowerGrade" system.

## When to Use
- Complete grading workflow from log to final look
- Learning professional pipeline structure
- Applying film emulation correctly
- Using Magic Mask for selective refinement

## Prerequisites
- DaVinci Resolve Studio 18+ (Magic Mask requires Studio)
- Basic Color Page navigation
- Understanding of CST and node structures

## Quick Reference

| Step | Operation | Tools | Purpose |
|------|-----------|-------|---------|
| **1** | CST Convert | Color Space Transform | Log → Working Space (DWG) |
| **2** | Film Emulation + Primaries | LUT + Color Wheels | Creative look foundation |
| **3** | DCTL & Glow | Custom DCTL + Glow OFX | Texture, halation, atmosphere |
| **4** | Magic Mask | Neural Engine (Studio) | Selective refinement, isolation |

---

## Procedure

### Step 1: CST Convert — Log to Working Space
```
Node 01: CST
  Input: Camera Log (S-Log3, Apple Log, BRAW, etc.)
  Output: DaVinci Wide Gamut (DWG) / ACEScc
  ★ NO creative grade before this!
```

| Camera | Input Space | Output Space |
|--------|-------------|--------------|
| Sony S-Log3 | S-Log3/S-Gamut3.Cine | DWG |
| Apple Log | Apple Log / Wide Gamut | DWG |
| Blackmagic BRAW | Blackmagic Design Film / Gen 5 | DWG |
| Canon C-Log | Canon Log / Cinema Gamut | DWG |
| ARRI | LogC / Alexa Wide Gamut | DWG |

---

### Step 2: Film Emulation + Primaries — Creative Foundation
```
Node 02: Film Emulation LUT (Kodak 2383, Fuji, etc.)
Node 03: Primaries (Lift/Gamma/Gain) — balance after LUT
Node 04: Contrast/Pivot or Curves — tonal shape
```

| Element | Settings | Purpose |
|---------|----------|---------|
| **Film LUT** | Kodak 2383 / Fuji 3513 / Custom | Base look, highlight rolloff, color response |
| **Primaries** | Adjust WB, Exposure, Contrast | Balance LUT to shot |
| **Contrast** | Pivot 0.336 (DWG) or Curves | Cinematic tonal separation |

**Key Insight:** *Film LUT first, then Primaries to balance — not the reverse.*

---

### Step 3: DCTL & Glow — Texture & Atmosphere
```
Node 05: DCTL (Film Print Emulation / Halation / Gate Weave)
Node 06: Glow OFX — Soft Light / Screen blend
```

| DCTL Type | Effect | Typical Use |
|-----------|--------|-------------|
| **Print Film Emulation** | Density, halation, gate weave | Authentic film texture |
| **Halation** | Highlight bloom around bright edges | Specular highlights, practicals |
| **Grain** | Film grain structure | Organic texture |
| **Gate Weave** | Subtle frame movement | Film projector feel |

| Glow Setting | Value | Purpose |
|--------------|-------|---------|
| **Threshold** | Low (0.1–0.3) | Catch highlights only |
| **Size** | Medium (30–60) | Natural falloff |
| **Intensity** | Subtle (0.1–0.3) | Atmosphere, not fog |
| **Blend** | Soft Light / Screen | Organic integration |

---

### Step 4: Magic Mask — Selective Refinement (Studio Only)
```
Node 07: Magic Mask → Person/Object isolation
Node 08: Refinement grade (skin, sky, subject)
```

| Magic Mask Target | Refinement |
|-------------------|------------|
| **Person** | Skin tone polish, exposure, separation |
| **Sky** | Graduated filter, color, drama |
| **Foreground** | Depth, contrast, focus pull |
| **Custom Object** | Product, vehicle, specific element |

**Workflow:**
1. Add **Magic Mask** on new node (or use Magic Mask OFX)
2. Select **Object** → **Person** (or Sky, Custom)
3. **Track** forward/backward
4. **Refine** grade inside mask (separate node after mask)

---

## Complete Node Tree

```
┌─────────────────────────────────────────────────────────────────┐
│  NODE 01: CST — Camera Log → DWG                               │
├─────────────────────────────────────────────────────────────────┤
│  NODE 02: Film LUT (Kodak 2383 / Fuji / Custom)               │
│  NODE 03: Primaries — WB, Exposure, Balance                    │
│  NODE 04: Contrast/Pivot (0.336) or Custom Curves             │
├─────────────────────────────────────────────────────────────────┤
│  NODE 05: DCTL — Print Film Emulation / Halation / Grain      │
│  NODE 06: Glow OFX — Soft Light, Low Threshold                │
├─────────────────────────────────────────────────────────────────┤
│  NODE 07: Magic Mask — Person/Sky/Object Isolation            │
│  NODE 08: Inside Mask — Skin polish / Sky drama / Depth       │
├─────────────────────────────────────────────────────────────────┤
│  NODE 09: CST — DWG → Output (Rec.709/P3/HDR) + Gamut Map     │
│  NODE 10: Legalizer / Soft Clip                                │
└─────────────────────────────────────────────────────────────────┘
```

---

## Pro Tips (Loris Marie)

| Tip | Detail |
|-----|--------|
| **CST first, always** | Never grade in camera log space |
| **LUT before Primaries** | Film LUT sets response; Primaries balance to shot |
| **DWG Pivot = 0.336** | Middle gray in DWG, not 0.5 |
| **DCTL = Texture** | Not "effect" — authentic film character |
| **Glow = Atmosphere** | Subtle; threshold low, blend Soft Light |
| **Magic Mask = Precision** | Studio only; isolates for final polish |
| **PowerGrade = Template** | Save as PowerGrade; swap LUT per project |

---

## Free vs Studio Version

| Step | Free Version | Studio Version |
|------|--------------|----------------|
| 1. CST | ✅ | ✅ |
| 2. Film LUT + Primaries | ✅ | ✅ |
| 3. DCTL + Glow | ✅ (DCTL works) | ✅ |
| 4. Magic Mask | ❌ (Neural Engine) | ✅ |
| **Alternative Free** | Qualifier + Power Window | Magic Mask |

---

## Verification Checklist

- [ ] CST Node 01: Correct camera log → DWG
- [ ] Film LUT applied before Primaries
- [ ] Contrast Pivot = 0.336 in DWG
- [ ] DCTL adds film texture (not digital look)
- [ ] Glow threshold low, blend Soft Light
- [ ] Magic Mask tracks cleanly (Studio)
- [ ] Output CST with Gamut Mapping ON
- [ ] Legalizer prevents broadcast illegal levels

---

## References

- Source: Instagram @loris_marie — "Quality render in 4 step 🎨" (42 weeks ago)
- Hashtags: #colorgrading #colorgrade #cinematography #colorgradingfilms #filmmkrs #fx3 #sonyalpha
- Type: Carousel post (4-slide educational)
- CTA: "All these steps are available in the Ultimate powergrade available in the shop linked in my bio"
- Related: @loris_marie Color Science Guide, Ultimate PowerGrade

---

## Tags

```markdown
#davinci-resolve #workflow #cst #film-emulation #dctl #glow #magic-mask #powergrade #loris-marie #color-grading #cinematic #studio-version #free-version-compatible
```