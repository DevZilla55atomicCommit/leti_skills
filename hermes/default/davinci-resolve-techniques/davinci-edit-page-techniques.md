---
name: davinci-edit-page-techniques
description: Edit page editing techniques - speed ramping, ripple cuts, timeline layouts, multicam, thumbnails
category: davinci-resolve
tags: [edit-page, speed-ramping, ripple-cut, timeline, editing, shortcuts, keyframing, retime]
trigger: Use when user asks about Edit page editing, speed ramps, ripple cuts, timeline management, shortcuts, or multicam workflows
---

# DaVinci Resolve Edit Page Techniques

Core editing workflows on the Edit page including speed manipulation, cutting shortcuts, timeline layouts, and creative editing techniques.

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

### 3. Sunset Beach Montage - Triptych Layout
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

### 4. Cinematic Drone Moves Tutorial Thumbnail
**Video ID:** `C11pkkePnC4` | **Difficulty:** Beginner | **Page:** Edit | **Node Graph:** Serial
- **Key Nodes:** Text+, Color Correction
- **Parameters:** Text+: Font: Impact, Size: 100, Color: Yellow, Outline Color: Black, Outline Width: 2; Color Correction: Contrast: 1.2, Saturation: 1.1, Gamma: 0.9
- **Steps:**
  1. Import the drone footage into DaVinci Resolve
  2. Add a Text+ node to the timeline
  3. Type "3 CINEMATIC DRONE MOVES PART 6" into the Text+ node
  4. Adjust the font, size, color, and outline of the text to match the example
  5. Apply color correction to the footage to enhance the colors and contrast
  6. Position the text and drone footage to create a compelling thumbnail
- **Tags:** thumbnail, text overlay, drone footage, tutorial, cinematic

### 5. Dramatic Time-Lapse
**Video ID:** `C1cQyyuLv5k` | **Difficulty:** Intermediate | **Page:** Color|Edit|Fusion|Fairlight | **Node Graph:** Serial
- **Key Nodes:** Speed Ramp
- **Parameters:** Frame Rate: 25 fps
- **Steps:**
  1. Import footage
  2. Set up speed ramp
- **Tags:** time-lapse, speed, fusion

---

## Speed Ramping Deep Dive

### Retime Curve Editor Workflow
```
Clip → Right-click → "Retime Controls" → Curve Editor icon
     → Change dropdown to "Retime Speed"
     → Add keyframes (Opt+Click / Alt+Click on curve)
     → Drag curve up/down for speed changes
     → Select keyframes → Press "S" for smooth/Bezier
```

### Common Speed Ramp Patterns
| Pattern | Curve Shape | Use Case |
|---------|-------------|----------|
| Speed Up | ↗ Ramp up | Action moments, punch-ins |
| Slow Down | ↘ Ramp down | Impact moments, reveals |
| Speed → Freeze → Speed | ↗ → Flat → ↗ | "Time freeze" effect |
| S-Curve | Smooth S | Natural acceleration/deceleration |

### Pro Tips
- **Optical Flow:** For extreme slow-mo, enable Optical Flow in Retime Process (Inspector → Retime Process → Optical Flow)
- **Frame Blending:** Faster preview, lower quality - good for drafts
- **Nearest Neighbor:** Sharp but juddery - avoid for slow-mo
- **Keyframe Density:** More keyframes = more control but harder to smooth

---

## Ripple Cut Workflow

### Essential Shortcuts (Mac / Windows)
| Action | Shortcut (Mac) | Shortcut (Win) |
|--------|----------------|----------------|
| Ripple Delete | Cmd + / | Ctrl + / |
| Ripple Trim Start | Opt + [ | Alt + [ |
| Ripple Trim End | Opt + ] | Alt + ] |
| Insert Clip | F9 | F9 |
| Overwrite Clip | F10 | F10 |

### When to Use Ripple vs Roll vs Slip
- **Ripple:** Delete/trim and close gap - changes timeline duration
- **Roll:** Adjust edit point between two clips - keeps duration
- **Slip:** Move clip content within its boundaries - keeps edit points
- **Slide:** Move clip position, adjust neighbors - keeps clip duration

---

## Timeline Layout Techniques

### Triptych / Split Screen
```
Track 3: Clip A (Top Third)     → Transform: Scale ~33%, Y = -33%
Track 2: Clip B (Middle Third)  → Transform: Scale ~33%, Y = 0%
Track 1: Clip C (Bottom Third)  → Transform: Scale ~33%, Y = +33%
```

### Picture-in-Picture
```
Track 2: Main footage (100%)
Track 1: B-roll (Scale 25-40%, Position corner)
```

### Text Overlay for Thumbnails
- Use **Text+** (Fusion title) for outline/stroke control
- **Impact** font + **Yellow** + **Black Outline** = YouTube thumbnail standard
- Position using Safe Margins (View → Show Safe Margins)

---

## Skill Trigger Examples

- "How do I do a speed ramp in DaVinci Resolve?"
- "Ripple cut shortcut not working"
- "Create a triptych split screen layout"
- "Make a YouTube thumbnail in DaVinci Resolve"
- "Time-lapse speed ramping tutorial"
- "Edit page workflow tips and shortcuts"