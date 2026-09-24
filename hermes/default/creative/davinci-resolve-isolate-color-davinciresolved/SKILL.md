---
name: davinci-resolve-isolate-color-davinciresolved
description: Isolate a color in DaVinci Resolve — Qualifier/HSL techniques for precise color selection, hue/saturation/luminance refinement, cleanup
category: creative
tags: [davinciresolve, qualifier, hsl, color-isolation, color-grading, davinciresolved]
source_url: https://www.instagram.com/reel/DLm-NySJl26/
author: davinciresolved
---

# DaVinci Resolve: Isolate a Color

> **"Isolate a color in DaVinci Resolve"** — davinciresolved

## Core Technique: Qualifier (HSL) for Precise Color Isolation

The Qualifier tool is the primary method for isolating specific colors in DaVinci Resolve for secondary grading, color replacement, or targeted adjustments.

---

## Qualifier Workflow

### 1. Open Qualifier Panel
**Color Page → Qualifier** (eyedropper icon) or `Shift + H` to toggle highlight

### 2. Select Target Color
```
Qualifier Panel:
├── Mode: HSL (Hue, Saturation, Luminance) — default
├── Eyedropper: Click on target color in viewer
├── Add to selection: Shift + Click (multiple samples)
└── Subtract: Option/Alt + Click
```

### 3. Refine Selection (Critical Step)

| Parameter | Function | Typical Range |
|-----------|----------|---------------|
| **Hue Width** | Range of hues selected | Start wide (30–60), narrow to 10–20 |
| **Hue Softness** | Feather edges of hue range | 5–15 |
| **Sat Low/High** | Min/max saturation | Exclude desaturated (noise) |
| **Sat Softness** | Feather saturation edges | 5–15 |
| **Lum Low/High** | Min/max luminance | Exclude crushed blacks/clipped whites |
| **Lum Softness** | Feather luminance edges | 5–15 |

### 4. Clean Up Selection

```
Qualifier Refinement Tools:
├── **Erode/Dilate** — Shrink/grow matte (1–3 pixels)
├── **Blur Radius** — Soften matte edges (0.5–2.0)
├── **Clean Black/White** — Remove noise in shadows/highlights
└── **Invert** — Select everything EXCEPT target color
```

### 5. View Matte
- **Highlight Mode** (`Shift + H`): Shows selection as grayscale matte
- **White = Selected** — Adjust until clean
- **Gray = Partial** — Increase softness or widen range

---

## Common Use Cases

### 1. Color Replacement (e.g., Red Car → Blue)
```
Node 01: Balance
    │
    ▼
Node 02: Qualifier (Select Red)
    ├── Hue: ~0° (red), Width: 20, Soft: 10
    ├── Sat: 0.3–1.0, Lum: 0.2–0.8
    ├── Clean: Erode 1, Blur 0.5
    └── Output: Alpha → Node 03 Key Input
    │
    ▼
Node 03: Color Wheels / Curves (Keyed)
    ├── Hue Shift: 0° → 240° (Blue)
    ├── Sat/Lum: Match target
    └── Mix: 100%
```

### 2. Sky Enhancement (Blue Isolation)
```
Qualifier Settings:
├── Hue: ~210° (blue), Width: 30
├── Sat: 0.2–0.8 (exclude white clouds)
├── Lum: 0.3–0.9 (exclude dark shadows)
└── Grade: Sat boost, Lum adjust, Gradient
```

### 3. Skin Tone Protection (Invert)
```
Node 01: Creative Grade (Teal/Orange, etc.)
    │
    ▼
Node 02: Qualifier (Select Skin)
    ├── Hue: ~30°, Width: 20
    ├── Sat: 0.1–0.5, Lum: 0.3–0.7
    ├── Invert: ON (select NON-skin)
    └── Output: Alpha → Layer Mixer
    │
    ▼
Node 03: Layer Mixer
    ├── A: Node 01 (Full creative grade)
    ├── B: Node 01 (Original, via bypass)
    └── Mix: Alpha from Node 02 (protect skin)
```

---

## Pro Tips

| Tip | Why |
|-----|-----|
| **Sample multiple points** | Shift+Click across color variations (shadows, highlights) |
| **Use 3D Qualifier view** | Toggle 3D scope — see selection in HSL space |
| **Clean Black/White** | Essential for noisy footage — removes matte speckles |
| **Blur before Erode** | Blur 0.5 → Erode 1 = clean edge without chatter |
| **Save as Still** | Grab Still → Gallery → Reuse qualifier settings |

---

## Qualifier vs. Other Isolation Methods

| Method | Best For | Precision | Speed |
|--------|----------|-----------|-------|
| **Qualifier (HSL)** | Single color, memory colors | High | Fast |
| **Power Window** | Geometric shapes, position-based | Medium | Fast |
| **Magic Mask (Studio)** | Organic shapes, moving subjects | Very High | Medium |
| **Depth Map (Studio)** | Distance-based (FG/MG/BG) | High | Slow |
| **Color Warper** | Creative color pushing | Medium | Fast |

---

## Related Skills

- `davinci-resolve-masking-power-masking` — Magic Mask + Power Window combo
- `davinci-resolve-skin-tones-qualifier-noisy` — Clean skin isolation (Ivar Brauer)
- `davinci-resolve-chroma-warp-davinciresolved` — 3D color warping alternative
- `davinci-resolve-split-toning-danny-gan` — Split tone without qualifiers

---

## Hashtags

#davinciresolve #colorgrading #videoediting #qualifier #hsl #colorisolation #davinciresolved