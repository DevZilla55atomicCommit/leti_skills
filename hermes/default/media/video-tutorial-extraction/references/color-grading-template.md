# Color Grading Tutorial Markdown Template

Use this template when extracting DaVinci Resolve color grading tutorials from YouTube. Replace all `[BRACKETED]` sections.

---

# [Tutorial Title] — [Channel Name] ([Camera/Log], [DaVinci Version])

**Source:** [YouTube URL]  
**Channel:** [Channel Name]  
**Duration:** [X:XX]  
**Views:** [X]  
**Date:** [Relative/absolute]  
**DaVinci Resolve Version:** [18+/19/20/21]  
**Camera/Log:** [e.g., Sony FX3, S-Log3 / S-Gamut3]

---

## 🎯 Overview

2-3 sentence summary of the tutorial's core value proposition and workflow philosophy.

---

## 📋 Complete Node Tree

| Order | Node Label | Node Label | Type | Purpose | Key Settings |
|-------|------------|------|---------|--------------|
| 1 | [LABEL] | Serial/Parallel | [Purpose] | [Key params] |
| 2 | [LABEL] | Serial/Parallel | [Purpose] | [Key params] |

> **Node Order (Left → Right):** `NODE1` → `NODE2` → ...

---

## ⚙️ Step-by-Step Workflow

### **Step 1: [Phase Name]**
1. [Action]
2. [Action with specific values]

#### **Settings Reference**
| Parameter | Value | Context |
|-----------|-------|---------|
| [Setting] | [Value] | [Why/When] |

---

## 🧠 Key Techniques & Principles

| Technique | Why It Works |
|-----------|--------------|
| [Name] | [Explanation] |

---

## 🎬 Camera/Log Specific Notes

| Aspect | [Camera A] | [Camera B] |
|--------|------------|------------|
| **CST Input** | [e.g., Sony S-Gamut3/S-Log3] | [e.g., Apple Log 2] |
| **CST Output** | [e.g., Rec.709/Gamma 2.4] | [e.g., DWG Intermediate] |
| **Typical Issue** | [e.g., Green skin cast] | [e.g., Underexposure] |
| **Fix** | [e.g., Temp +2, Tint +3] | [e.g., HDR Offset] |

---

## 📊 Critical Settings Reference

| Parameter | Value | Context |
|-----------|-------|---------|
| [CST Input Color Space] | [Value] | [Camera-specific] |
| [CST Input Gamma] | [Value] | [Camera-specific] |
| [CST Output Color Space] | [Value] | [Delivery target] |
| [CST Output Gamma] | [Value] | [Delivery target] |
| [Contrast Pivot] | [Value] | [Middle gray lock] |
| [Skin Midtone Detail] | [Value] | [Skin softening] |
| [Key Output Gain] | [Value] | [LUT blending] |

---

## 💡 Pro Tips from Tutorial

1. **[Tip]** — [Why it matters]
2. **[Tip]** — [Why it matters]

---

## 🔗 Cross-References

- **DaVinci Master Map:** `../../Memory.md` → Core Workflows → [Reference]
- **Complementary Tutorial:** `[Other Tutorial Name]` (`../[Folder]/[file].md`)
- **Technical Foundation:** `../../DaVinci Resolve 20/[doc].md`

---

## 🏷️ Tags

`#[Camera]` `#S-Log3` `#Apple-Log2` `#ColorSpaceTransform` `#CST` `#Kodak-2383` `#Film-Emulation` `#Node-Tree` `#DaVinciResolve` `#Color-Grading` `#Skin-Tones`

---

*Transcript fetched via youtube-content skill • Saved to `[Folder]/` • Mapped in `../Memory.md`*