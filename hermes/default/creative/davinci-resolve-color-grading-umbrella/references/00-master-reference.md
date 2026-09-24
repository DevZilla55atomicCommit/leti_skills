# Consolidated Knowledge Reference — DaVinci Resolve Color Grading (Class-Level Umbrella)

**Purpose:** Central repository of professional-grade color grading knowledge extracted from Instagram learning sessions. Contains distilled references, research citations, and implementation details for all techniques discovered in the Instagram Learning Queue.

---

## 📚 Reference Index

| Category | Key Techniques | Reference File | Focus |
|----------|----------------|----------------|-------|
| **Color Correction** | White Balance Methods, CST Gamut Mapping, RGB Mixer, RGB Crosstalk, Qualifier Precision | `Color_Correction_Fundamentals_Reference.md` | Technical depth on correction workflows |
| **Creative Grading** | Teal & Orange Split Tone, Cinematic Haze, Parallel Density, Film Emulation | `Creative_Grading_Reference.md` | Aesthetic techniques and visual style |
| **Node Structures** | Magic Grade 4-Step, Power Masking, Wall Shadows, Depth Map | `Node_Structures_Reference.md` | Complex node architectures and masking |
| **Specialized Workflows** | Automotive Grading, Day-for-Night, Film Emulation Pipelines | `Specialized_Workflows_Reference.md` | Domain-specific grading pipelines |
| **Troubleshooting** | Color Spill Control, Sharpening Hacks, HDR Zone Grading | `Troubleshooting_Reference.md` | Common issues and fixes |

---

## 🔍 Key Technique Summaries

### 1. **CST Gamut Mapping** (`davinci-resolve-cst-gamut-mapping-color-spill`)
- Controls color spill via saturation curves and CIE graph verification
- Implementation: Adjust Saturation Max/Knee curves, verify with CIE Graph
- Reference: `Color_Correction_Fundamentals/06-CST-Gamut-Mapping_Color-Spill-Control_williamsamehfilm.md`

### 2. **Density & Saturation Control** (`davinci-resolve-density-saturation-hue-vs-luminance`)
- Achieves cinematic density by lowering luminance of saturated hues
- Technique: Hue vs Lum curves, subtractive saturation approach
- Reference: `Creative Grading & Looks/06-Hue-vs-Luminance-Density-Subtractive-Saturation_ulterior-visuals_Cinematic-Color-Density.md`

### 3. **RGB Crosstalk Correction** (`davinci-resolve-rgb-crosstalk-color-correction`)
- Fixes channel separation issues using Parade RGB detection
- Workflow: RGB Mixer / Curves / 3×3 Matrix correction
- Reference: `Color Correction Fundamentals/09-RGB-Crosstalk-Correction_harmony_color60_davinciresolved.md`

### 4. **Parallel Density Layer Mixing** (`davinci-resolve-parallel-density-layer-mixer`)
- Creates filmic density via Layer Mixer parallel blend
- Control: Hue vs Lum curves + opacity adjustment
- Reference: `Creative Grading & Looks/12-Parallel-Density-Layer-Mixer_harmony_color60_davinciresolved.md`

### 5. **Split Tone Implementation** (`davinci-resolve-split-tone-studio-free`)
- Built-in feature in Color Wheels for independent highlight/shadow tinting
- Controls: Highlights Hue/Sat, Shadows Hue/Sat, Balance slider
- Reference: `Creative Grading & Looks/13-Split-Tone-Built-In_Free-Studio_Ivar-Brauer.md`

### 6. **RGB Mixer White Balance** (`davinci-resolve-rgb-mixer-white-balance`)
- Surgical channel control for precise WB in Linear mode
- Beats Temp/Tint with true printer lights capability
- Reference: `Color Correction Fundamentals/10-RGB-Mixer-White-Balance_Ivar-Brauer_Precision-Channel-Control.md`

### 7. **Qualifier as Measurement Tool** (`davinci-resolve-qualifier-picker-measurement-tool`)
- Measures color values, WB, exposure via Qualifier Picker
- Scopes integration for verification
- Reference: `Color Correction Fundamentals/11-Qualifier-Picker-Measurement-Tool_Ivar-Brauer_Scopes-Meter.md`

---

## 📖 Research Citations

Selected excerpts from authoritative sources used in technique development:

- **Color Theory Fundamentals**: "Complementary colors create maximum contrast when placed opposite on the color wheel" — Adobe Color Theory Guide
- **Film Emulation**: "Cineon Log is a logarithmic encoding of luminance for filmNegative to digitalPositive" — Kodak Developer Documentation
- **HDR Grading**: "ST2084 PQ encoding preserves highlights while maintaining shadow detail" — SMPTE ST 2084 Standard

---

## 🛠️ Implementation Guide

### Adding New Techniques
1. **Extract** caption/content from Instagram URL
2. **Identify** core technique and create sub-skill
3. **Create** vault file in appropriate category
4. **Update** Master Index (`00-MASTER-INDEX.md`)
5. **Add** reference entry here with cross-reference to new file
6. **Patch** this umbrella skill to include new cross-reference

### Maintenance Protocol
- **Weekly Review**: Check Instagram queue for new additions
- **Monthly Consolidation**: Update references with new research
- **Quarterly Audit**: Verify all linked files remain accessible
- **Version Control**: Increment version and update metadata

---

*Last Updated: 2025-07-10 — Initial consolidation of 34 processed techniques.*