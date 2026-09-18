---
name: davinci-edit-speed-ramp
description: Edit page workflows — speed ramping with curve smoothing, ripple cut shortcuts, multi-cam triptych layout, timeline editing
trigger: Use when editing on the Edit/Cut page: speed ramps, ripple cuts, multi-cam layouts, thumbnail creation
steps:
  - name: Dynamic Speed Ramping with Curve Smoothing
    description: Variable speed changes with Bezier easing for cinematic slow-mo/speed-up
    resolve_page: Edit
    difficulty: intermediate
    key_nodes: [Inspector, Curve Editor, Keyframe Editor]
    parameters:
      Speed Change: "Variable"
      Curve Type: "Ease-in/Ease-out"
      Keyframes: "Active"
    steps:
      - Drag the clip onto the Edit timeline
      - Right-click the clip and select "Retime Speed" or click the Retime Curve icon on the clip
      - Change the dropdown in the Curve Editor window to "Retime Speed"
      - Add keyframes at points where you want the speed to change
      - Drag the segments between keyframes to speed up or slow down the footage
      - Select keyframes and use the Bezier tool to smooth the transitions
    tags: [speed-ramp, cinematic, keyframing, davinci-resolve, retime]

  - name: Ripple Cut / Smart Trim Shortcut
    description: Delete at playhead and close gap instantly (Cmd+/ / Ctrl+/)
    resolve_page: Edit
    difficulty: beginner
    key_nodes: [Timeline, Playhead]
    parameters:
      shortcut: "Cmd + / (Mac) | Ctrl + / (Windows)"
      action: "Delete at playhead and close gap"
    steps:
      - Place the playhead at the start of the segment you wish to remove
      - Press Command + / (Mac) or Ctrl + / (Windows)
      - Observe how the clip is deleted and subsequent clips shift left automatically
    tags: [davinci resolve, video-editing, shortcuts, workflow, productivity, ripple cut]

  - name: Sunset Beach Montage — Triptych Layout
    description: Three-panel vertical split-screen layout using Transform controls
    resolve_page: Edit
    difficulty: beginner
    key_nodes: [Timeline, Clip, Transform]
    parameters:
      scaling: "Zoom in/out to frame each panel"
      positioning: "Adjust X/Y position to create the triptych layout"
      cropping: "Crop to create distinct panels if needed"
    steps:
      - Import the video clip into DaVinci Resolve
      - Place the clip on the timeline
      - Duplicate the clip two times to create three identical clips stacked on top of each other
      - On the first clip (top panel), use the Transform controls in the Inspector to scale and position it to fill the top third of the frame
      - On the second clip (middle panel), use the Transform controls to scale and position it to fill the middle third
      - On the third clip (bottom panel), use the Transform controls to scale and position it to fill the bottom third
      - Adjust the scaling and positioning of each clip until the desired triptych layout is achieved
    tags: [montage, triptych, sunset, beach, editing, layout]

  - name: Cinematic Drone Thumbnail Creation
    description: Create YouTube/social thumbnails with Text+ and color correction
    resolve_page: Edit
    difficulty: beginner
    key_nodes: [Text+, Color Correction]
    parameters:
      Text+:
        font: "Impact"
        size: "100"
        color: "yellow"
        outline_color: "black"
        outline_width: "2"
      Color Correction:
        contrast: "1.2"
        saturation: "1.1"
        gamma: "0.9"
    steps:
      - Import the drone footage into DaVinci Resolve
      - Add a Text+ node to the timeline
      - Type "3 CINEMATIC DRONE MOVES PART 6" into the Text+ node
      - Adjust the font, size, color, and outline of the text to match the example
      - Apply color correction to the footage to enhance the colors and contrast
      - Position the text and drone footage to create a compelling thumbnail
    tags: [thumbnail, text overlay, drone footage, tutorial, cinematic]

  - name: Multi-Cam Sync & Angle Editing
    description: Sync multiple camera angles and cut between them
    resolve_page: Edit
    difficulty: intermediate
    key_nodes: [Timeline, Multi-Cam Clip]
    parameters:
      sync_mode: "Timecode | Audio Waveform | Markers"
      angle_names: "Cam A, Cam B, Cam C"
    steps:
      - Select all camera angle clips in Media Pool
      - Right-click → Create Multi-Cam Clip Using Selected Clips
      - Choose sync method (Timecode, Audio, or Markers)
      - Drag multi-cam clip to timeline
      - Open Multi-Cam Viewer (Shift+F11)
      - Click angles during playback to cut live
      - Refine cuts with Blade tool (B)
    tags: [multi-cam, sync, editing, angles, live switching]

  - name: Timeline Markers & Notes Workflow
    description: Use markers for organization, notes, and chapter points
    resolve_page: Edit|Color
    difficulty: beginner
    key_nodes: [Timeline Markers]
    parameters:
      marker_colors: ["Red", "Green", "Blue", "Purple", "Yellow", "Cyan"]
      marker_types: ["Note", "Chapter", "Web Link", "Compression"]
    steps:
      - Move playhead to desired frame
      - Press M to add marker (or Option+M for marker dialog)
      - Double-click marker to edit name, note, color, duration
      - Use marker colors for coding: Red=VFX, Green=Approved, Blue=Audio, Purple=Graphics
      - Export markers to CSV for editorial notes
      - Use Chapter markers for YouTube chapters on Deliver
    tags: [markers, timeline, organization, notes, chapters, workflow]

parameters:
  - name: retime_curve_type
    type: string
    description: Curve interpolation for speed ramps
    default: "Bezier"
  - name: ripple_shortcut
    type: string
    description: Ripple cut keyboard shortcut
    default: "Cmd+/ (Mac) | Ctrl+/ (Win)"
  - name: triptych_panels
    type: integer
    description: Number of panels in triptych
    default: 3

tags: [editing, speed ramp, ripple cut, triptych, thumbnail, multi-cam, markers, davinci resolve, edit page, retime]
category: davinci-resolve-edit
---

# DaVinci Resolve Edit Page — Speed Ramps, Shortcuts & Layouts

Core Edit page workflows: variable speed ramping with curve smoothing, productivity shortcuts (ripple cut), multi-panel layouts, thumbnail creation, and multi-cam editing.

## Skills Included

1. **Dynamic Speed Ramping with Curve Smoothing** — Bezier-eased variable speed
2. **Ripple Cut / Smart Trim Shortcut** — Cmd+/ (Mac) / Ctrl+/ (Win) instant gap-close
3. **Sunset Beach Montage — Triptych Layout** — 3-panel vertical split-screen
4. **Cinematic Drone Thumbnail Creation** — Text+ overlay + color grade for social
5. **Multi-Cam Sync & Angle Editing** — Sync by audio/timecode, live switching
6. **Timeline Markers & Notes Workflow** — Color-coded markers, chapter points

## Quick Reference

| Task | Page | Shortcut/Method | Difficulty |
|------|------|-----------------|------------|
| Speed ramp | Edit | Retime Curve → Bezier | Intermediate |
| Ripple cut | Edit | Cmd+/ / Ctrl+/ | Beginner |
| Triptych layout | Edit | Transform (scale/position) | Beginner |
| Thumbnail | Edit | Text+ + Color Correct | Beginner |
| Multi-cam sync | Edit | Right-click → Create Multi-Cam | Intermediate |
| Add marker | Edit/Color | M (Option+M for dialog) | Beginner |

## Tips

- **Speed Ramp**: Use "Retime Curve" (not "Retime Frame") for smooth curves; add keyframes at change points
- **Ripple Cut**: Works on single clip or selection; Shift+Cmd+/ = Ripple Delete (removes gap AND selection)
- **Triptych**: Use Transform inspector (not Crop) for cleaner scaling; hold Shift while dragging to constrain proportions
- **Thumbnails**: Export frame (Right-click → Export Frame) → open in Fusion for advanced graphics
- **Multi-Cam**: Use audio sync for DSLR/mirrorless without timecode; assign angle names before creating clip
- **Markers**: Green=Approved, Red=Needs VFX, Blue=Audio Fix, Purple=Graphics, Yellow=Color Note

## Keyboard Shortcuts (Edit Page)

| Action | Mac | Windows |
|--------|-----|---------|
| Ripple Cut | Cmd+/ | Ctrl+/ |
| Ripple Delete | Shift+Cmd+/ | Shift+Ctrl+/ |
| Blade | B | B |
| Selection Mode | A | A |
| Trim Mode | T | T |
| Retime Curve | Option+R | Alt+R |
| Add Marker | M | M |
| Marker Dialog | Option+M | Alt+M |
| Multi-Cam Viewer | Shift+F11 | Shift+F11 |

## Related Skills

- `davinci-resolve-techniques/davinci-cut-page-workflow` — Cut page fast editing
- `davinci-resolve-techniques/davinci-fusion-fairlight-vfx` — Fusion comps from Edit timeline
- `davinci-resolve-techniques/davinci-color-grading-fundamentals` — Color after edit lock