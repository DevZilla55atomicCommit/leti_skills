---
name: davinci-resolve-color-grading-umbrella
title: DaVinci Resolve Color Grading Techniques (Class-Level Umbrella)
description: Central hub for organized color grading workflows, node structures, and advanced techniques. Contains references, templates, and scripts for professional-grade workflows.
version: 0.1.0
author: Hermes
metadata:
  hermes:
    tags: [DaVinci Resolve, Color Grading, Color Correction, Creative Look, Node Structures, Templates]
    source: "Internal Knowledge Base Consolidation"
    vault_category: "Color Grading & Looks"
    skill_level: "Professional"
    cross_reference: "See also: davinci-resolve-split-tone-studio-free, davinci-resolve-cst-gamut-mapping-color-spill, davinci-resolve-density-saturation-hue-vs-luminance, davinci-resolve-parallel-density-layer-mixer, davinci-resolve-rgb-crosstalk-color-correction"
---

# 🎨 DaVinci Resolve Color Grading Umbrella

This is the **class-level umbrella skill** that consolidates all professional color grading techniques extracted from Instagram learning sessions. It serves as the central entry point for:

- **Core color correction** (white balance, scopes, linear workflow)
- **Creative looks** (teal-orange, bleach bypass, cross process)
- **Advanced node structures** (parallel density, HDR zones, magic mask)
- **Specialized workflows** (automotive, day-for-night, film emulation)
- **Troubleshooting** (crosstalk, RGB mixer, qualifier precision)

## 📚 Organization

The corresponding vault directory structure is mirrored here:

```
Color Grading & Looks/
├── 00-MASTER-INDEX.md                 ← Master index of all techniques
├── Creative Grading & Looks/            ← Creative looks and effects
│   ├── 01-Complementary-Color-Grading_Teal-Orange_Magimir-Guide.md
│   ├── 02-Day-for-Night_Transformation_3rdvisionfilm_Native-Tools-Only.md
│   ├── 03-Cinematic-Haze-Effect_3rdvisionfilm_Native-Tools-Only.md
│   └── ...
├── Color Correction Fundamentals/       ← Core correction workflows
│   ├── 05-White-Balance_Luma-Mix-Zero_RGB-Gain_Rolling-Shutter-Media.md
│   ├── 06-CST-Gamut-Mapping_Color-Spill-Control_williamsamehfilm.md
│   ├── 07-White-Balance-3-Methods_Ivar-Brauer_Linear-Gain-Gray-Card.md
│   ├── 08-WB-Helper-Power-Window-Highlight-Mode_marco-herbst.md
│   ├── 09-RGB-Crosstalk-Correction_harmony_color60_davinciresolved.md
│   ├── 10-RGB-Mixer-White-Balance_Ivar-Brauer_Precision-Channel-Control.md
│   └── ...
├── Masking & Power Windows/             ← Masking and power window techniques
│   ├── 01-Power-Masking_Loris-Marie_Radial-MagicMask-InvertedBG-Workflow.md
│   └── 02-Realistic-Wall-Shadows_Power-Window-Tracking_harmony_color60.md
├── Automotive & Specialty/              ← Vehicle-specific grading
│   └── 01-Automotive-Cinematic-Grading_BWD-Motorsports_CST-EndNode-PowerWindow-Tracking.md
└── Node Structures & Templates/         ← Reusable node templates
    └── 01-MagicGrade-4-Step-Workflow_Blueprint_Summy-Dean_MrAlexTech.md
```

## 🔗 Linked Skills & Vault Files

This umbrella references all previously created sub-skills:

- `davinci-resolve-split-tone-studio-free` → [Split Tone Built-In](Creative Grading & Looks/13-Split-Tone-Built-In_Free-Studio_Ivar-Brauer.md)
- `davinci-resolve-cst-gamut-mapping-color-spill` → [CST Gamut Mapping](Color Correction Fundamentals/06-CST-Gamut-Mapping_Color-Spill-Control_williamsamehfilm.md)
- `davinci-resolve-density-saturation-hue-vs-luminance` → [Density & Saturation](Creative Grading & Looks/06-Hue-vs-Luminance-Density-Subtractive-Saturation_ulterior-visuals_Cinematic-Color-Density.md)
- `davinci-resolve-parallel-density-layer-mixer` → [Parallel Density](Creative Grading & Looks/12-Parallel-Density-Layer-Mixer_harmony_color60_davinciresolved.md)
- `davinci-resolve-rgb-crosstalk-color-correction` → [RGB Crosstalk](Color Correction Fundamentals/09-RGB-Crosstalk-Correction_harmony_color60_davinciresolved.md)
- `davinci-resolve-rgb-mixer-white-balance` → [RGB Mixer WB](Color Correction Fundamentals/10-RGB-Mixer-White-Balance_Ivar-Brauer_Precision-Channel-Control.md)
- `davinci-resolve-white-balance-3-methods` → [White Balance Methods](Color Correction Fundamentals/07-White-Balance-3-Methods_Ivar-Brauer_Linear-Gain-Gray-Card.md)
- `davinci-resolve-white-balance-helper-window-technique` → [WB Helper Technique](Color Correction Fundamentals/08-WB-Helper-Power-Window-Highlight-Mode_marco-herbst.md)
- `davinci-resolve-magicgrade-workflow-blueprint` → [MagicGrade Blueprint](Node Structures & Templates/01-MagicGrade-4-Step-Workflow_Blueprint_Summy-Dean_MrAlexTech.md)
- `davinci-resolve-masking-power-masking` → [Power Masking](Masking & Power Windows/01-Power-Masking_Loris-Marie_Radial-MagicMask-InvertedBG-Workflow.md)
- `davinci-resolve-realistic-wall-shadows-power-window` → [Realistic Wall Shadows](Masking & Power Windows/02-Realistic-Wall-Shadows_Power-Window-Tracking_harmony_color60.md)

## 📖 References

Each technique has a dedicated reference file in the `references/` directory that contains:

- Error transcripts and reproduction recipes
- Provider API documentation excerpts
- Research citations and authoritative external sources
- Condensed knowledge banks for quick review

## 🛠️ Usage

1. **Discover techniques** via `graphify query "<topic>"` or `graphify explain "<concept>"`
2. **Load specific sub-skills** with `skill_view(name='<skill-name>')`
3. **Access templates** via `references/` files for implementation details
4. **Run verification scripts** from `scripts/` for reproducible workflows

## 🔄 Update Protocol

When new techniques are discovered:
- A new sub-file is added to the appropriate category
- The `00-MASTER-INDEX.md` is updated to reflect new entries
- This umbrella skill is patched to include new cross-references
- Supporting reference files are created or updated
- All changes are committed to maintain synchronization

---

*Last Updated: 2025-07-11 — Consolidated 48 processed techniques (including new Sharpening, Masking Matters, Halation, Relight Effect, Fast Preset Creation, Fujifilm Look, Relight Scene, Match Color Grade, Cinematic Saturation, Depth Map Relight, Chroma Warp, Split Toning, Smooth Contrast, Isolate Color, Advanced White Balance, Kodak Film Look, Advanced Skin Tones) into umbrella structure.*