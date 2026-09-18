# S-Log3 Tutorial Markdown Template

Copy this structure when creating markdown from S-Log3 (Sony) color grading video transcripts.

---

# [Descriptive Title] — [Creator] (Sony [Camera], S-Log3/S-Gamut3, DaVinci [Version])

**Source:** [YouTube URL]
**Channel:** [Channel Name]
**Duration:** [X:XX]
**Views:** [X]
**Date:** [Relative/absolute]
**DaVinci Resolve Version:** [19/20/21]
**Camera/Log:** [e.g., Sony FX3, S-Log3 / S-Gamut3.Cine]

---

## 🎯 Overview

2-3 sentence summary of the tutorial's core value proposition and workflow philosophy. Note whether it's minimalist (3-node), comprehensive (7+ node), or pro-techniques focused.

---

## 📋 Node Structure ([X] Nodes)

| Order | Label | Purpose | Key Settings |
|-------|-------|---------|--------------|
| 1 | NODE_LABEL | Brief purpose | Critical parameter: value |

---

## ⚙️ Step-by-Step Workflow

### **Step 1: [Name]**
1. Action with shortcut (Option+S / Alt+S)
2. Parameter settings (CST Input/Output, HDR wheels, etc.)
3. Why this step matters

> **Pro Tip:** Key insight from creator

---

## 🧠 Key Principles

| Principle | Detail |
|-----------|--------|
| **Upstream Grading** | All corrections before CST in native S-Gamut3/S-Log3 space |
| **CST at End** | Single transform to delivery space (Rec.709/Gamma 2.4) |
| **ETTR (Expose Right)** | +1-2 stops over "correct" for Sony noise floor management |
| **Lum vs Sat Highlights** | Desaturate extreme highlights for filmic roll-off |

---

## 📊 CST Settings Reference (S-Log3)

| Parameter | Standard (FX3/A7IV) | Venice/Pro | Notes |
|-----------|---------------------|------------|-------|
| Input Color Space | Sony S-Gamut3.Cine | Sony S-Gamut3 | Check camera model |
| Input Gamma | Sony S-Log3 | Sony S-Log3 | |
| Output Color Space | Rec.709 | Rec.709 / DWG Intermediate | |
| Output Gamma | Gamma 2.4 | Gamma 2.4 / DWG Intermediate | 2.2 web, 2.6 cinema |
| Tone Mapping | DaVinci | DaVinci | Try Luminance Mapping for yellow/orange |
| Gamut Mapping | None | None | Or Saturation Compression |

---

## 🔗 Cross-References

- **DaVinci Master Map:** `../Memory.md` → Core Workflows → Proper Balancing
- **Related S-Log3 Tutorial:** `[Other-Slog3-Tutorial.md]`
- **Technical Doc:** `../../DaVinci Resolve 20/LUT_and_Technical_Accuracy.md`
- **Upstream vs Downstream:** `../../DaVinci Resolve 20/davinci_guide_part_016.md`

---

## 🏷️ Tags

`#S-Log3` `#S-Gamut3` `#ColorSpaceTransform` `#CST` `#DaVinciResolve` `#SonyFX3` `#A7SIII` `#A7IV` `#UpstreamGrading` `#ETTR` `#LumVsSat` `#NoiseReduction`

---

*Transcript fetched via youtube-content skill • Saved to `Color Grading & Looks/S-Log3/` • Mapped in `../Memory.md`*