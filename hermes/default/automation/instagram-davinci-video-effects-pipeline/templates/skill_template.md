---
name: davinci-resolve-{{TECHNIQUE_SLUG}}
description: "{{EFFECT_NAME}} technique using {{KEY_TOOLS}} in DaVinci Resolve. Learned from @{{SOURCE_HANDLE}} Instagram reel."
version: 1.0.0
author: Hermes Agent (from Instagram @{{SOURCE_HANDLE}})
tags: [davinci-resolve, video-effects, {{EFFECT_CATEGORY}}, {{KEY_TAGS}}, {{SOURCE_HANDLE}}]
---

# DaVinci Resolve: {{EFFECT_NAME}}

> **Technique:** {{TECHNIQUE_NAME}}
> **Source:** Instagram @{{SOURCE_HANDLE}} — "{{CAPTION_EXCERPT}}"
> **Reel:** [{{REEL_CODE}}](https://www.instagram.com/reel/{{REEL_CODE}}/)
> **Hashtags:** {{HASHTAGS}}
> **DaVinci Pages:** {{DAVINCI_PAGES}}
> **Difficulty:** {{DIFFICULTY}}
> **Time:** {{ESTIMATED_TIME}}

---

## 🎬 Technique Overview

{{2-3 sentences: what it does, when to use it, key insight}}

---

## 🏗️ Complete Node Graph / Fusion Flow

### Method A: Fusion Page (Best Results)

```
NODE 01 — MediaIn (Source Footage)
    │
    ▼
NODE 02 — {{MASK_TOOL}} ⭐
    │  • {{MASK_PARAM_1}}
    │  • {{MASK_PARAM_2}}
    │  • Tracker: {{TRACKER_SETTINGS}}
    │
    ▼
NODE 03 — AlphaDivide (Unpremultiply)
    │  • Fixes dark halos on high-contrast edges
    │
    ▼
NODE 04 — Merge (Over)
    │  • Foreground: AlphaDivide output
    │  • Background: MediaIn2 (New Scene)
    │  • Apply Mask: {{MASK_TOOL}}
    │
    ▼
NODE 05 — MediaOut (Final Composite)
```

### Method B: Color Page (Faster for Simple Motion)

```
NODE 01 — Source Clip
    │
    ▼
NODE 02 — Power Window ({{WINDOW_TYPE}}) ⭐
    │  • Shape: {{SHAPE_DETAILS}}
    │  • Tracker: {{TRACKER_SETTINGS}}
    │  • Softness: {{SOFTNESS}}
    │  • Invert: OFF
    │
    ▼
NODE 03 — Alpha Output (Enable in Node Inspector)
    │  • Outputs mask as transparency
    │
    ▼
NODE 04 — Composite (Timeline)
    │  • Video Track 2: New Background Clip
    │  • Composite Mode: Normal
    │  • Alpha from Node 03
    │
    ▼
OUTPUT
```

---

## ⚙️ Step-by-Step Procedure

### Method A: Fusion Page (Best Results)

#### Step 1: Import & Setup
| Tool | Action | Why |
|------|--------|-----|
| MediaIn1 | Drag source clip to Node Editor | Base footage |
| MediaIn2 | Drag new background clip | Replacement scene |
| Background | Match resolution/framerate | Prevent scaling artifacts |

#### Step 2: Create Mask (Node 02) ⭐
| Parameter | Value | Why |
|-----------|-------|-----|
| **Tool** | {{MASK_TOOL}} | {{MASK_REASON}} |
| **Points** | {{NUM_POINTS}} around subject | Tight fit = clean edge |
| **Soft Edge** | {{SOFTNESS}}px | Optical feather |
| **Tracker** | Position + Rotation + Scale | Full transform tracking |
| **Track Direction** | Forward | Standard workflow |
| **Reference Frame** | First transition frame | Clean starting shape |

#### Step 3: Track & Refine
1. Click **Track Forward** on mask
2. Review — scrub timeline for drift
3. **Add Keyframes** every 2-3 frames where mask slips
4. **Adjust Points** manually on keyframes
5. **Smooth** tracker data if jittery (right-click → Smooth)

#### Step 4: Alpha Correction (Node 03)
| Tool | Setting | Why |
|------|---------|-----|
| AlphaDivide | Connect to mask output | Unpremultiply alpha |
| Mode | "Unpremultiply" | Remove dark fringes |

#### Step 5: Composite (Node 04)
| Tool | Setting | Why |
|------|---------|-----|
| Merge | Operation: Over | Standard composite |
| Merge | Foreground: AlphaDivide | Subject + alpha |
| Merge | Background: MediaIn2 | New scene |
| Merge | Apply Mask: {{MASK_TOOL}} | Clean edge enforcement |

#### Step 6: Output
| Tool | Action |
|------|--------|
| MediaOut | Connect to Merge output |

---

### Method B: Color Page (Quick Turnaround)

#### Step 1: Power Window Mask (Node 02) ⭐
| Parameter | Value | Why |
|-----------|-------|-----|
| **Window Type** | {{WINDOW_TYPE}} | {{SHAPE_REASON}} |
| **Points** | {{NUM_POINTS}} around subject | Balance detail/speed |
| **Tracker** | Position + Rotation + Scale | Auto-track motion |
| **Softness** | {{SOFTNESS}}px | Natural feather |
| **Invert** | OFF | Keep subject |

#### Step 2: Track & Refine
1. **Track Forward** from first transition frame
2. **Add Keyframes** at drift points (every 2-3 frames)
3. **Adjust Points** manually on keyframes
4. **Smooth** if jittery (right-click tracker → Smooth)

#### Step 3: Enable Alpha Output (Node 03)
- Open **Node Inspector** (top-right)
- Check **"Alpha Output"**
- This outputs the mask as transparency

#### Step 4: Timeline Composite
1. Place **new background** on **Video Track 2** (above source)
2. Set Track 2 **Composite Mode: Normal**
3. Track 2 shows through Node 02's alpha

---

## 🎯 Key Principles

| Principle | Application |
|-----------|-------------|
| **Tight Mask = Clean Composite** | Draw 1-2px inside subject edge; expand via Softness, not mask size |
| **Track First, Refine Later** | Let tracker do 80%; keyframe only problem frames |
| **Feather for Reality** | 3-5px soft edge mimics lens falloff; hard edges look "CGI" |
| **Premultiply Correction** | AlphaDivide prevents dark halos on high-contrast edges |
| **Motion Blur Match** | Enable Motion Blur on mask (Fusion) if subject has blur |
| **Perspective Consistency** | New background must match camera angle/focal length of source |

---

## ⚠️ Common Pitfalls

| Symptom | Cause | Fix |
|---------|-------|-----|
| **Mask drifts off subject** | Tracker lost reference | Increase search area; add manual keyframes at drift points |
| **Dark halo around subject** | Premultiplication error | Add AlphaDivide after mask; set "Unpremultiply" in Merge |
| **Jittery mask edges** | Over-keyframing / over-correction | Reduce keyframe frequency; use Tracker Smoothing (Fusion) |
| **Background perspective wrong** | Mismatched focal length/angle | Re-shoot background or use Camera Tracker to match |
| **Hair/fabric shows old background** | Mask too tight on fine detail | Expand mask 2-3px; increase Softness to 8-10px; use EdgeExtend (Fusion) |
| **Alpha channel not working** | Alpha Output disabled | Enable "Alpha Output" in Node Inspector (Color) or check MediaOut alpha (Fusion) |

---

## ✅ Verification Checklist

- [ ] Mask tracks subject cleanly for entire transition duration
- [ ] No visible edge artifacts (halos, chatter, gaps)
- [ ] Soft edge feathering looks natural (not glowing)
- [ ] New background perspective matches source footage
- [ ] Motion blur on subject matches composite (if applicable)
- [ ] Alpha channel exports correctly (test with Checkerboard background)
- [ ] Transition timing feels natural (not rushed, not dragging)

---

## 🔗 Cross-References

| Topic | File |
|-------|------|
| Power Window Tracking | `../Masking & Power Windows/02-Realistic-Wall-Shadows_Power-Window-Tracking_harmony_color60.md` |
| Magic Mask (AI Alternative) | `../Masking & Power Windows/01-Power-Masking_Loris-Marie_Radial-MagicMask-InvertedBG-Workflow.md` |
| Alpha Channel Compositing | `../Creative Grading & Looks/06-Diffusion-Halation_Soft-Light_YanColorist_Optical-Glass-Mimic.md` |
| Fusion Compositing Basics | `../../DaVinci Resolve 20/` |
| Keyframe Animation | `../Node Structures & Templates/` (Parallel node keyframing) |

---

## 🏷️ Obsidian Tags

```markdown
#davinci-resolve #video-effects #{{EFFECT_CATEGORY}} #{{KEY_TAGS}} #{{SOURCE_HANDLE}}
```

---

## 📸 Visual Assets

| Asset | Description | Location |
|-------|-------------|----------|
| **Demo GIF** | Full reel demonstration | `assets/demo.gif` |
| **Transition Loop** | 3-second effect loop | `assets/transition_demo.gif` |
| **Frame Before** | Frame before effect starts | `assets/frame_before.png` |
| **Frame During** | Frame mid-effect | `assets/frame_during.png` |
| **Frame After** | Frame after effect completes | `assets/frame_after.png` |
| **Before/After Comparison** | Side-by-side comparison | `assets/before_after_comparison.png` |

---

## 📅 Revision Log

| Date | Version | Notes |
|------|---------|-------|
| {{DATE}} | 1.0 | Created from Instagram @{{SOURCE_HANDLE}} reel {{REEL_CODE}} |

---

*Part of the **DaVinci Knowledge Base → Video Effects → {{EFFECT_CATEGORY}}** collection.*  
*Curated for professional video effects workflows using DaVinci Resolve.*