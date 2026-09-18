---
name: davinci-resolve-fast-preset-creation-creatorsergeant
description: How to create fast presets in DaVinci Resolve — reusable node trees, PowerGrades, and keyboard shortcuts for efficient workflow
category: creative
tags: [davinci-resolve, presets, powergrade, workflow, efficiency, node-tree, templates, creatorsergeant]
source_url: https://www.instagram.com/reel/DKe-2y6tIYq/
author: creatorsergeant
---

# DaVinci Resolve: Fast Preset Creation

> **"How to create a fast preset in DaVinci Resolve"** — creatorsergeant

## Core Concept

Build **reusable, one-click presets** that encapsulate your common grading workflows — node structure, settings, and even keyframes — for instant recall across projects.

## Preset Types in Resolve

| Type | Scope | Best For |
|------|-------|----------|
| **PowerGrade** | Global (all projects) | Full node trees, complex looks, LUT pipelines |
| **Still** | Project-specific | Single-frame reference grades, shot matching |
| **Macro** | Single node | Repeated node settings (e.g., specific CST, curve) |
| **Keyboard Shortcut** | Global | Instant node creation, view toggles, panel switching |

## Creating a Fast Preset (PowerGrade Workflow)

### 1. Build Your Template Node Tree

```
Node 01: CST (Input)          ← Camera-specific (leave as placeholder)
Node 02: Primary Balance      ← Lift/Gamma/Gain + Temp/Tint
Node 03: Contrast/Pivot       ← Gain + Pivot method
Node 04: Creative Look        ← Curves / Color Wheels / LUT
Node 05: Skin Protection      ← Qualifier → Layer Mixer
Node 06: Grain/Halation       ← Film texture (optional)
Node 07: CST (Output)         ← Target delivery space
```

### 2. Save as PowerGrade

1. Right-click node graph → **Grab Still** (or `Ctrl/Cmd + G`)
2. In Gallery: Right-click still → **Export** → **PowerGrade** (`.dpx` + `.dpx.grd`)
3. Save to: `~/Library/Application Support/Blackmagic Design/DaVinci Resolve/PowerGrades/` (macOS)
   Or: `%APPDATA%\Blackmagic Design\DaVinci Relsolve\PowerGrades\` (Windows)

### 3. Organize PowerGrade Library

```
PowerGrades/
├── CAMERA_SPECIFIC/
│   ├── SONY_S-Log3_Cineon.dpx.grd
│   ├── CANON_C-Log_Cineon.dpx.grd
│   └── FUJIFILM_F-Log_Cineon.dpx.grd
├── CREATIVE_LOOKS/
│   ├── TEAL_ORANGE_Blockbuster.dpx.grd
│   ├── KODAK_2383_Film.dpx.grd
│   └── FUJIFILM_Eterna.dpx.grd
├── DELIVERY/
│   ├── REC709_G24_Web.dpx.grd
│   ├── REC709_G24_Broadcast.dpx.grd
│   └── P3_D65_DCI.dpx.grd
└── UTILITY/
    ├── SKIN_PROTECTION.dpx.grd
    ├── GRAIN_HALATION.dpx.grd
    └── SHARPENING_Final.dpx.grd
```

### 4. Apply with One Click

- **Gallery panel** → Drag PowerGrade onto node graph
- **Right-click node** → **Apply Grade** → Select PowerGrade
- **Keyboard shortcut** (custom): Map to `Apply Grade from Gallery`

## Pro Tips from Comments

> **@suchy_bagnet:** *"DaVinci Resolve ❌❌❌ Vintage result ✅✅✅"*
> 
> → **Lesson:** Presets ≠ Magic. Build presets that **start from correct color management**, not crushed/contrasty "looks."

> **@__tayyab.khan:** *"But we can only do this for one effect right?"*
> 
> → **No.** PowerGrades can contain **entire node trees** (10+ nodes). The preset applies the full tree structure.

> **@clickkmemories:** *"How do you create this subtitle style... single word highlighted yellow?"*
> 
> → **Different feature:** That's **Fusion Titles / Text+** with per-word animation, not a grading preset.

## Keyboard Shortcuts for Speed

| Action | Default | Recommended Custom |
|--------|---------|-------------------|
| Grab Still | `Ctrl/Cmd + G` | Keep |
| Apply Grade | None | `Ctrl/Cmd + Shift + G` |
| New Serial Node | `Alt/Option + S` | Keep |
| New Layer Node | `Alt/Option + L` | Keep |
| Toggle Gallery | `Ctrl/Cmd + 9` | Keep |

## Integration with Versioning

1. Create **Timeline Grade** version for each look variant
2. Use **Group Pre-Clip / Post-Clip** for project-wide preset application
3. **PowerGrade + Timeline Grade** = Instant project consistency

## Related Skills

- `davinci-resolve-grading-systems-cdvc-day19` — Group Pre/Post-Clip, Timeline Grades
- `davinci-resolve-magicgrade-workflow-blueprint` — 4-step keyboard-driven template
- `davinci-resolve-node-tree-river-analogy` — Mental model for node order

## Hashtags

#davinciresolve #colorgrading #workflow #presets #powergrade #efficiency