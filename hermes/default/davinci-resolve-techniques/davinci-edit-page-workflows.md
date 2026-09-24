---
name: davinci-edit-page-workflows
description: Edit page editing workflows - speed ramping, ripple cuts, montage layouts, time-lapse, shortcuts
category: davinci-resolve
tags: [edit-page, speed-ramping, ripple-cut, montage, time-lapse, shortcuts, keyframing, retime, timeline]
trigger: Use when user asks about Edit page editing, speed ramps, ripple cuts, montage layouts, time-lapse, editing shortcuts, or retime curves
---

# DaVinci Resolve Edit Page Workflows

Core editing techniques on the Edit page including speed manipulation, cutting shortcuts, timeline layouts, and creative pacing.

## Techniques Included

### 1. Dynamic Speed Ramping with Curve Smoothing
**Video ID:** `C-FvSX-piqT` | **Difficulty:** Intermediate | **Page:** Edit | **Node Graph:** Serial
- **Key Nodes:** Inspector, Curve Editor, Keyframe Editor
- **Parameters:** Speed Change: Variable, Curve Type: Ease-in/Ease-out, Keyframes: Active
- **Steps:**
  1. Drag the clip onto the Edit timeline
  2. Right-click the clip and select 'Retime Speed' or click the Retime Curve icon on the clip
  3. Change the dropdown in the Curve Editor window to 'Retime Speed'
  4. Add keyframes at points where you want the speed to change
  5. Drag the segments between keyframes to speed up or slow down the footage
  6. Select keyframes and use the Bezier tool to smooth the transitions
- **Tags:** speed-ramp, cinematic, keyframing, davinci-resolve

### 2. Ripple Cut / Smart Trim Shortcut
**Video ID:** `DAMFEaWyaJg` | **Difficulty:** Beginner | **Page:** Edit | **Node Graph:** Serial
- **Key Nodes:** Timeline, Playhead
- **Parameters:** Shortcut: Cmd + / (Mac) / Ctrl + / (Windows), Action: Delete at playhead and close gap
- **Steps:**
  1. Place the playhead at the start of the segment you wish to remove
  2. Press Command + / (Mac) or Ctrl + / (Windows)
  3. Observe how the clip is deleted and subsequent clips shift left automatically
- **Tags:** DaVinci Resolve, video-editing, shortcuts, workflow, productivity

### 3. Sunset Beach Montage (Triptych Layout)
**Video ID:** `DAQ30GGP5tj` | **Difficulty:** Beginner | **Page:** Edit | **Node Graph:** Serial
- **Key Nodes:** Timeline, Clip, Transform
- **Parameters:** Scaling: Zoom in/out to frame each panel, Positioning: Adjust X/Y position to create the triptych layout, Cropping: Crop to create distinct panels if needed
- **Steps:**
  1. Import the video clip into DaVinci Resolve
  2. Place the clip on the timeline
  3. Duplicate the clip two times to create three identical clips stacked on top of each other
  4. On the first clip (top panel), use the Transform controls in the Inspector to scale and position it to fill the top third of the frame
  5. On the second clip (middle panel), use the Transform controls to scale and position it to fill the middle third of the frame
  6. On the third clip (bottom panel), use the Transform controls to scale and position it to fill the bottom third of the frame
  7. Adjust the scaling and positioning of each clip until the desired triptych layout is achieved
- **Tags:** montage, triptych, sunset, beach, editing, layout

### 4. Dramatic Time-Lapse
**Video ID:** `C1cQyyuLv5k` | **Difficulty:** Intermediate | **Page:** Color|Edit|Fusion|Fairlight | **Node Graph:** Serial
- **Key Nodes:** Speed Ramp
- **Parameters:** Frame Rate: 25 fps
- **Steps:**
  1. Import footage
  2. Set up speed ramp
- **Tags:** time-lapse, speed, fusion

---

## Edit Page Speed Manipulation

### Retime Controls Overview

| Method | Access | Best For |
|--------|--------|----------|
| **Retime Speed** | Right-click clip → Retime Speed | Quick constant speed changes |
| **Retime Curve** | Clip → Retime Curve icon (or Ctrl+R) | Variable speed, ramps |
| **Speed Editor** | Cut page / Speed Editor hardware | Tactile shuttle/jog |
| **Optical Flow** | Retime Process → Optical Flow | Smooth slow-mo from normal footage |

### Retime Curve (Speed Ramping) Deep Dive

#### Interface
```
Timeline Clip
    │
    ▼
┌─────────────────────────────────────┐
│ Retime Curve Panel                  │
├─────────────────────────────────────┤
│ Dropdown: [Retime Speed ▼]          │
│                                     │
│ Graph:                              │
│  Y-axis: Speed % (0-1000+)          │
│  X-axis: Timeline frames            │
│  White line: Speed curve            │
│  Keyframes: Diamond markers         │
│                                     │
│ Tools: [Selection] [Pen] [Bezier]   │
└─────────────────────────────────────┘
```

#### Curve Types
| Type | Behavior | Use Case |
|------|----------|----------|
| **Linear** | Constant speed between keyframes | Mechanical, precise |
| **Ease In** | Slow start, fast end | Entering slow-mo |
| **Ease Out** | Fast start, slow end | Exiting slow-mo |
| **Ease In/Out** | Smooth both sides | Natural ramps |
| **Bezier** | Custom handles | Organic, custom feel |

#### Speed Ramp Workflow
1. **Enable Retime Curve** on clip (Ctrl+R / Cmd+R)
2. **Set Dropdown** to "Retime Speed"
3. **Add Keyframes** (Pen tool or Opt/Alt+Click on curve)
   - At ramp start: 100%
   - At ramp peak: 500% (fast) or 25% (slow)
   - At ramp end: 100%
4. **Smooth Transitions** (Bezier tool)
   - Drag handles for gradual acceleration
   - Match handle angles for symmetry
5. **Set Retime Process** (Right-click clip)
   - **Nearest Neighbor:** Fast, blocky (draft)
   - **Frame Blend:** Dissolves frames (good for 2x)
   - **Optical Flow:** AI interpolation (best for slow-mo)

#### Common Speed Ramp Patterns
```
Action Sequence:     100% ──╮       ╭── 100%
                     500%  ╰───────╯    (Speed burst)

Dramatic Reveal:     100% ──╮
                     25%   ╰──────────  (Slow pull)

Whip Pan:            100% ──╮    ╭── 100%
                     800%  ╰────╯       (Invisible cut)
```

---

## Ripple Cut & Trim Shortcuts

### Essential Edit Page Shortcuts (Mac / Windows)

| Action | Mac | Windows | Description |
|--------|-----|---------|-------------|
| **Ripple Delete** | Cmd+/ | Ctrl+/ | Delete at playhead, close gap |
| **Ripple Trim Start** | Opt+[ | Alt+[ | Trim clip start to playhead |
| **Ripple Trim End** | Opt+] | Alt+] | Trim clip end to playhead |
| **Roll Edit** | Cmd+Opt+Drag | Ctrl+Alt+Drag | Roll between two clips |
| **Slip Edit** | Opt+Drag | Alt+Drag | Move content within clip |
| **Slide Edit** | Cmd+Opt+Drag | Ctrl+Alt+Drag | Move clip, trim neighbors |
| **Extend Edit** | Shift+[ / ] | Shift+[ / ] | Extend to playhead |
| **Add Edit (Cut)** | Cmd+B | Ctrl+B | Cut at playhead |
| **Join Clips** | Cmd+J | Ctrl+J | Join through cuts |

### Ripple Delete Variants
```
Standard:     [Clip A][Clip B][Clip C]  → Playhead in B → Ripple Delete → [Clip A][Clip C]

With Gap:     [Clip A][  GAP  ][Clip C]  → Ripple Delete GAP → [Clip A][Clip C]

Multi-track:  V1: [A][B][C]     → Ripple Delete B (all tracks) → [A][C]
              V2: [X][Y][Z]                          → [X][Z]
              A1: [M][N][O]                          → [M][O]
```

---

## Montage & Multi-Panel Layouts

### Triptych / Split Screen (Sunset Beach Technique)

#### Manual Transform Method
```
Timeline:
V3: [Clip Top]    → Inspector → Transform → Position Y: -33%, Zoom: 0.5
V2: [Clip Mid]    → Inspector → Transform → Position Y: 0%, Zoom: 0.5
V1: [Clip Bot]    → Inspector → Transform → Position Y: +33%, Zoom: 0.5
```

#### Using Fusion Composition (More Flexible)
```
Right-click clips → New Fusion Clip
Fusion Page:
MediaIn1 (Top) → Transform → Merge → MediaOut
MediaIn2 (Mid) → Transform → Merge
MediaIn3 (Bot) → Transform → Merge
```
**Advantages:** Animate panel transitions, add dividers, shadows, 3D layout

#### Aspect Ratio Considerations
| Layout | Frame | Panel AR | Use Case |
|--------|-------|----------|----------|
| **Triptych Vertical** | 16:9 | 16:27 each | Social (Reels/TikTok) |
| **Triptych Horizontal** | 16:9 | 48:9 each | Cinematic wide |
| **Quad Split** | 16:9 | 16:9 each | Security, comparison |
| **Diptych** | 16:9 | 8:9 each | Before/After |

---

## Time-Lapse Workflow

### In-Camera vs Post Time-Lapse
| Method | Pros | Cons |
|--------|------|------|
| **In-Camera (Interval)** | Small files, baked look | Fixed interval, no ramping |
| **Post (Speed Up)** | Flexible speed, ramping | Large files, storage |

### Post Time-Lapse Steps
1. **Import** full-res footage (or proxy)
2. **Cut** to desired range (Mark In/Out)
3. **Retime Speed** → 500-3000% (adjust for final duration)
4. **Retime Process** → Optical Flow (smooth) or Frame Blend
5. **Add Motion Blur** (Fusion → Motion Blur OFX) for cinematic feel
6. **Deflicker** (Color → Deflicker OFX or Fusion → Flicker Remover)

### Speed Ramp in Time-Lapse (Hyperlapse)
```
Normal:    [──────────── 100% ────────────]
Ramped:    [100%] [╲500%╱] [100%] [╲2000%╱] [100%]
           Start   Fast     Slow    Fast    End
```

### Holy Grail Time-Lapse (Day to Night)
- **Exposure Ramping:** Blend multiple exposures
- **DaVinci:** Use Color → Keyframes on Exposure/ISO
- **LR Timelapse** (external) → Import graded sequence

---

## Edit Page Workflow Tips

### Timeline Management
```
Project Structure:
├── Timelines
│   ├── SELECTS (All good takes)
│   ├── ASSEMBLY (Rough cut, long)
│   ├── ROUGH_CUT_v1
│   ├── FINE_CUT_v1
│   ├── LOCKED_CUT
│   └── DELIVERABLES (Versions)
```

### Pancake Timeline (Selects → Assembly)
```
Top Timeline:  SELECTS (Source monitor style)
Bottom Timeline: ASSEMBLY (Build edit)
→ Drag from top to bottom
```

### Keyboard Customization (DaVinci → Keyboard Shortcuts)
```
Search: "Retime" → Map to single key (e.g., 'R')
Search: "Ripple Delete" → Verify Cmd+/
Search: "Add Edit" → Verify Cmd+B
```

### Proxy Workflow for Speed
```
Project Settings → Master Settings → Proxy Resolution: Half
Media Pool → Right-click → Generate Proxy Media
Playback → Proxy Preference: Prefer Proxies
```

---

## Common Issues & Fixes

| Issue | Cause | Fix |
|-------|-------|-----|
| **Ripple Delete deletes wrong clip** | Playhead not on clip | Park playhead *on* clip, not between |
| **Speed ramp stutters** | Wrong Retime Process | Use Optical Flow for slow, Frame Blend for fast |
| **Optical Flow artifacts** | Complex motion | Reduce speed %, add Motion Blur, or mask problem areas |
| **Montage panels misaligned** | Transform anchor point | Set Anchor to Center (0.5, 0.5) before scaling |
| **Time-lapse flicker** | Auto exposure changes | Deflicker OFX, or manual exposure keyframes |

---

## Skill Trigger Examples

- "How to speed ramp in DaVinci Resolve"
- "Ripple cut shortcut DaVinci"
- "Create triptych split screen"
- "Time-lapse workflow Edit page"
- "Retime curve Bezier handles"
- "Optical Flow vs Frame Blend"
- "Edit page keyboard shortcuts"
- "Pancake timeline workflow"
- "Montage editing DaVinci"
- "Variable speed clip"