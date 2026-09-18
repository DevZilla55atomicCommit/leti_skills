# Apple Log / Apple Log 2 Tutorial Markdown Template

Copy this structure when creating markdown from iPhone Apple Log color grading video transcripts.

---

# [Descriptive Title] — [Creator] (iPhone [Model], Apple Log / Apple Log 2, DaVinci [Version])

**Source:** [YouTube URL]
**Channel:** [Channel Name]
**Duration:** [X:XX]
**Views:** [X]
**Date:** [Relative/absolute]
**DaVinci Resolve Version:** [18+/19/20/21]
**Camera/Log:** [e.g., iPhone 15 Pro Max, Apple Log 2 / ProRes Log]

---

## 🎯 Overview

2-3 sentence summary. Note the workflow type:
- **Group Pre/Post-Clip Dual CST** (DWG Intermediate grading space)
- **Single CST → Rec.709** (Direct conversion)
- **One-Click LUT** (Baked CST + Grade)
- **Film Look Path** (ST2084 + Kodak 2383 LUT)

---

## 📋 Node Structure ([X] Nodes)

| Order | Label | Purpose | Key Settings |
|-------|-------|---------|--------------|
| 1 | NODE_LABEL | Brief purpose | Critical parameter: value |

---

## ⚙️ Step-by-Step Workflow

### **Step 1: [Name]**
1. Action with shortcut
2. Parameter settings
3. Why this step matters

> **Pro Tip:** Key insight from creator

---

## 🧠 Key Principles

| Principle | Detail |
|-----------|--------|
| **Apple Log = Rec.2020 + Apple Log Gamma** | Not Rec.709 — must set Input correctly |
| **DWG Intermediate for Grading** | Wider gamut than Rec.709; more latitude for look |
| **Group Pre/Post for Batch** | Pre-Clip = Input CST, Post-Clip = Output CST |
| **HDR Wheels for Log Exposure** | More precise than Primaries for log footage |
| **ST2084 Output for Film LUTs** | PQ curve preserves highlight latitude |

---

## 📊 CST Settings Reference (Apple Log / Apple Log 2)

### **Apple Log 2 (iPhone 15/17 Pro Max)**
| Parameter | DWG Intermediate Path | Direct Rec.709 Path | Film Path |
|-----------|----------------------|---------------------|-----------|
| Input Color Space | Apple Log 2 | Apple Log 2 | Apple Log 2 |
| Input Gamma | Apple Log | Apple Log | Apple Log |
| Output Color Space | DaVinci Wide Gamut | Rec.709 | Rec.709 |
| Output Gamma | DaVinci Intermediate | Rec.709 (Gamma 2.4) | ST2084 (PQ) |

### **Apple Log (Original, Pre-Log 2)**
| Parameter | Commercial Path | Film Path |
|-----------|-----------------|-----------|
| Input Color Space | Rec.2020 | Rec.2020 |
| Input Gamma | Apple Log | Apple Log |
| Output Color Space | Rec.709 | Rec.709 |
| Output Gamma | Gamma 2.4 | ST2084 |

---

## 🔗 Cross-References

- **DaVinci Master Map:** `../Memory.md` → Core Workflows → Proper Balancing
- **Related Apple Log Tutorial:** `[Other-Apple-Log-Tutorial.md]`
- **Technical Doc:** `../../DaVinci Resolve 20/LUT_and_Technical_Accuracy.md`
- **S-Log3 Comparison:** `../S-Log3/S-Log3_Danny-Gan_3-Node-CST-Workflow.md` (similar upstream philosophy)

---

## 🏷️ Tags

`#Apple-Log` `#Apple-Log-2` `#iPhone-15-Pro` `#iPhone-17-Pro` `#ProRes-Log` `#Rec2020` `#DaVinci-Wide-Gamut` `#DWG-Intermediate` `#ColorSpaceTransform` `#CST` `#Group-Pre-Clip` `#Group-Post-Clip` `#Kodak-2383` `#ST2084` `#Film-Look` `#HDR-Wheels`

---

*Transcript fetched via youtube-content skill • Saved to `Color Grading & Looks/Apple Log 2/` • Mapped in `../Memory.md`*