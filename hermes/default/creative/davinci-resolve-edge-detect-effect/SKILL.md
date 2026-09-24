---
name: davinci-resolve-edge-detect-effect
description: "DaVinci Resolve Edge Detect effect: Native OFX for stylized edges, outlines, and creative compositing from @caleboshi."
version: 0.1.0
author: Hermes
metadata:
  hermes:
    tags: [DaVinci Resolve, Color Grading, Edge Detect, OFX, Stylized, Compositing, Free Version]
---

# DaVinci Resolve — Edge Detect Effect

Learn the **Edge Detect** effect technique from @caleboshi (Caleb) — a powerful native OFX in DaVinci Resolve (works in Free version) for creating stylized edge detection, outlines, and creative compositing effects.

## When to Use
- Stylized edge outlines on footage
- Motion graphics / title sequences
- Creative compositing (edge maps for masking)
- "Pencil sketch" / "line art" looks
- Technical visualization (edge detection for VFX)
- Free version compatible creative effects

## Prerequisites
- DaVinci Resolve (Free or Studio)
- Footage with good contrast/edges
- Basic OFX and composite modes familiarity

## How to Run
Apply Edge Detect OFX in DaVinci Resolve Color page or Fusion page as described in **Procedure**.

## Quick Reference
| Step | Location | Tool | Key Action |
|------|----------|------|------------|
| 1 | Color Page / Fusion | OpenFX → Edge Detect | Apply to node/clip |
| 2 | Edge Detect Panel | Mode | Choose: Sobel, Prewitt, Roberts, etc. |
| 3 | Edge Detect Panel | Threshold | Adjust edge sensitivity |
| 4 | Edge Detect Panel | Invert | ON for white lines on black |
| 5 | Composite | Composite Mode | Add/Screen for overlay on original |

## Procedure

### 1. Color Page Application (Simple)
1. Add **Serial Node** (label: `EDGE_DETECT`)
2. Open **Effects Library** → **OpenFX** → **Resolve FX Stylize** → **Edge Detect**
3. Drag onto node
4. **Edge Detect Settings:**
   - **Mode:** Sobel (classic), Prewitt, Roberts, Laplacian
   - **Threshold:** 0.1-0.5 (lower = more edges)
   - **Invert:** ON (white edges on black) or OFF
   - **Mix:** 0.5-1.0 (blend with original)

### 2. Fusion Page Application (Advanced)
1. Switch to **Fusion Page**
2. **MediaIn** → **Edge Detect** (Tools → Stylize → Edge Detect) → **MediaOut**
3. **Edge Detect Settings:**
   - **Filter:** Sobel, Prewitt, Roberts, Kirsch, Robinson
   - **Threshold:** Edge sensitivity
   - **Gain:** Edge strength
   - **Output:** Edges Only / Edges + Source
4. **Composite:** Merge (Add/Screen) over original

### 3. Creative Composite Techniques

#### A. Edge Overlay (Pencil Sketch)
```
Original → Edge Detect (Invert ON) → Composite: Multiply
```
- Creates white line drawing on original

#### B. Edge Map for Masking
```
Edge Detect → Threshold/Contrast → Use as Mask → Color Grade
```
- Grade only edges, or only non-edges

#### C. Glow on Edges
```
Edge Detect → Blur → Glow → Add over Original
```
- Edge highlight glow effect

#### D. Color Separation
```
Edge Detect (Red) + Edge Detect (Green, offset) → 3D Anaglyph
```
- Chromatic aberration style

### 4. Flicker Reduction (Comment Issue)
**Problem:** Flickering on detailed areas (hats, hair, textures)
**Fixes:**
- **Temporal NR:** Add Temporal Noise Reduction before Edge Detect
- **Blur Pre-Filter:** Slight blur (0.5-1px) before Edge Detect
- **Threshold Keyframe:** Animate threshold per shot
- **Motion Blur:** Enable in Fusion if motion causes flicker

## Pitfalls
| Issue | Cause | Fix |
|-------|-------|-----|
| Flickering on fine detail | Frame-to-frame edge changes | Temporal NR; Blur pre-filter; Higher threshold |
| Too many edges (noise) | Low threshold / noisy footage | Increase threshold; Denoise first |
| Edges too thin | Default settings | Increase Gain; Lower threshold |
| Color fringes | RGB edge detection separate | Use Luminance-only mode; or desaturate first |
| Performance slow | High-res + Fusion | Use Color Page OFX; Proxy mode |

## Verification
1. **Toggle Effect:** Clear edge outline visible
2. **Scrub Timeline:** No excessive flicker (or controlled)
3. **Composite Modes:** Test Add, Screen, Multiply, Overlay
4. **Free Version:** Confirmed working in Free

## References
- Source: Instagram @caleboshi (Verified) — "Edge Detect can be used for a lot of things... works in the free version of DaVinci Resolve as well" (3 weeks ago at capture)
- Caption: "Download this clip & 50 more! In my bio" — provides assets
- Comments: Flicker issue on hats; Glow vs Edge Detect comparison
- Hashtags: #davinciresolve

## Related Skills
- `davinci-resolve-cinematic-haze-effect` (Glow OFX native)
- `davinci-resolve-complementary-color-grading` (Creative compositing)
- `davinci-resolve-day-to-night-grade` (Native tools workflow)