---
name: davinci-text-compositing
description: Text behind subject effects, depth masking, text+ overlays, title design, masking overlays, compositing text with footage
trigger: Use when creating text-behind-subject effects, depth masking with Magic Mask, Text+ animations, or compositing text over footage
steps:
  - name: Text Behind Subject (Depth Masking) — Fusion Method
    description: Place text behind a subject using Magic Mask in Fusion for depth compositing
    resolve_page: Fusion
    difficulty: intermediate
    key_nodes: [Text+, Alpha Output, Magic Mask]
    parameters:
      font_style: "Bold Serif"
      tracking: "wide"
      mask_softness: "low-to-medium"
    steps:
      - Import the clip to the Fusion page
      - Add a Text+ node and type the desired text (e.g., "GLOW TEXT EFFECT")
      - Use the Magic Mask tool or a manual Polygon mask to select the subject (the person)
      - Connect the mask to the Alpha channel of the Text+ node
      - Adjust the text position so the subject overlaps with the letters
      - Merge the masked text over the original background footage
    tags: [vfx, text-effect, masking, fusion, davinci-resolve]

  - name: Text Behind Subject (Masking Overlay) — Edit/Color Method
    description: Place text behind subject using Power Window/Magic Mask on Color page with track matte
    resolve_page: Edit
    difficulty: intermediate
    key_nodes: [Background Clip, Duplicate Clip, Text+]
    parameters:
      mask_method: "Power Window or Magic Mask"
      feathering: "Soft"
      blend_mode: "Normal"
    steps:
      - Place your video clip on the timeline
      - Duplicate the clip (Alt+Drag) to create a second layer directly above
      - Add a Text+ title on a layer between the two video clips
      - Select the top video clip and go to Color page
      - Use the Power Window or Magic Mask to isolate the subject
      - Track the mask across the clip to follow the movement
      - Adjust the text layer position so it appears behind the masked subject
    tags: [masking, text effect, motion tracking, compositing]

  - name: Text+ Title Design & Animation
    description: Create professional titles with Text+ including outlines, shadows, animations
    resolve_page: Edit|Fusion
    difficulty: beginner
    key_nodes: [Text+]
    parameters:
      font: "Impact"
      size: "100"
      color: "yellow"
      outline_color: "black"
      outline_width: "2"
    steps:
      - Add a Text+ title to the timeline (Edit page) or Text+ node (Fusion page)
      - Type your title text
      - In Inspector: set Font, Size, Color
      - Enable Outline: set Color (black) and Width (2-5)
      - Enable Drop Shadow for depth
      - Animate: add keyframes to Position/Scale/Rotation for entrance/exit
      - Use "Write On" effect for typewriter animation
    tags: [text+, title, animation, outline, shadow, write on, davinci resolve]

  - name: Instagram Reel Thumbnail Creation
    description: Create click-worthy thumbnails with Text+ overlay and color grade
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
      - Import the footage into DaVinci Resolve
      - Add a Text+ node to the timeline
      - Type the title text (e.g., "3 CINEMATIC DRONE MOVES PART 6")
      - Adjust font, size, color, and outline to match branding
      - Apply color correction to the footage to enhance colors and contrast
      - Position the text and footage to create a compelling thumbnail composition
      - Export frame (Right-click clip → Export Frame) for YouTube/IG thumbnail
    tags: [thumbnail, text overlay, drone footage, tutorial, cinematic]

  - name: Lower Thirds & Name Supers
    description: Professional lower third graphics with background plate and animation
    resolve_page: Fusion
    difficulty: beginner
    key_nodes: [Text+, Background, Merge, Transform]
    parameters:
      Background:
        Width: "1920"
        Height: "150"
        Color: "0.0, 0.0, 0.0, 0.7"
      Text+: "Name | Title"
    steps:
      - Add Background node → set to semi-transparent dark rectangle
      - Add Text+ node → type name and title on separate lines
      - Merge Text+ over Background (Background=Foreground in Merge)
      - Add Transform for animation (slide in from left)
      - Keyframe Transform Center X for entrance/exit
      - Save as Macro (.setting) for reuse
    tags: [lower third, name super, title, animation, fusion, macro]

  - name: Text on Path / Curved Text
    description: Animate text along a custom path using Text+ Following modifier
    resolve_page: Fusion
    difficulty: intermediate
    key_nodes: [Text+, Path, Following Modifier]
    parameters:
      Path Type: "B-Spline"
      Write On: "0 to 1"
    steps:
      - Add Text+ node
      - In Text+ Inspector: click "Following" button → add Path modifier
      - Draw path with Polyline/B-Spline tool in viewer
      - Animate "Write On" from 0 to 1 for text reveal along path
      - Add Transform for additional position/scale animation
    tags: [text on path, curved text, following, animation, fusion]

  - name: Kinetic Typography — Beat-Synced Text
    description: Text animation synced to music beats using keyframes or expressions
    resolve_page: Fusion
    difficulty: intermediate
    key_nodes: [Text+, Transform, Audio Waveform]
    parameters:
      Beat Sync: "Manual keyframes or Audio-driven expressions"
    steps:
      - Import music track to timeline
      - Add Text+ for each phrase/word
      - Use Blade tool (B) to cut text clips on beats
      - Animate each: Scale 0→100 on beat, Opacity 0→1, Position offset
      - Or use Fusion: Audio → Expression → drive Scale/Opacity
      - Add Motion Blur (Transform → Motion Blur) for smoothness
    tags: [kinetic typography, beat sync, music video, text animation, fusion]

parameters:
  - name: text_font
    type: string
    description: Default font for titles
    default: "Impact"
  - name: text_outline_width
    type: number
    description: Outline width for Text+
    default: 2
  - name: mask_feather
    type: string
    description: Mask feather for text behind subject
    default: "Soft"

tags: [text behind subject, depth masking, magic mask, text+, fusion, compositing, title design, lower thirds, kinetic typography, thumbnails]
category: davinci-resolve-text-compositing
---

# DaVinci Resolve Text Effects & Compositing

Text-behind-subject effects, depth masking with Magic Mask, Text+ title design, thumbnails, lower thirds, and kinetic typography.

## Skills Included

1. **Text Behind Subject (Fusion)** — Magic Mask → Alpha channel on Text+
2. **Text Behind Subject (Edit/Color)** — Track matte with Power Window/Magic Mask
3. **Text+ Title Design & Animation** — Outlines, shadows, write-on, keyframes
4. **Instagram Reel Thumbnail Creation** — Text+ + Color grade for social
5. **Lower Thirds & Name Supers** — Background plate + animation + macro save
6. **Text on Path / Curved Text** — Following modifier + B-Spline path
7. **Kinetic Typography (Beat-Synced)** — Music-driven text animation

## Quick Reference

| Effect | Page | Nodes/Tools | Difficulty |
|--------|------|-------------|------------|
| Text behind subject (Fusion) | Fusion | Text+, Magic Mask, Merge | Intermediate |
| Text behind subject (Edit) | Edit/Color | Alt+Drag duplicate, Text+, Mask | Intermediate |
| Title design | Edit/Fusion | Text+ | Beginner |
| Thumbnail | Edit | Text+, Color Correct | Beginner |
| Lower thirds | Fusion | Background, Text+, Merge, Transform | Beginner |
| Text on path | Fusion | Text+, Following, Path | Intermediate |
| Kinetic typography | Fusion | Text+, Transform, Audio | Intermediate |

## Text+ Essentials

| Feature | Location | Use Case |
|---------|----------|----------|
| Font/Size/Color | Inspector → Text | Basic styling |
| Outline | Inspector → Text → Outline | Contrast on busy footage |
| Drop Shadow | Inspector → Text → Shadow | Depth/readability |
| Write On | Inspector → Text → Write On | Typewriter effect |
| Following | Inspector → Text → Following | Text on path |
| Character/Line Spacing | Inspector → Text → Layout | Multi-line titles |
| Transform | Inspector → Transform | Position/Scale/Rotation/Anchor |

## Text Behind Subject: Fusion vs Edit

| Method | Pros | Cons |
|--------|------|------|
| **Fusion (Magic Mask→Alpha)** | Clean, nodal, reusable, handles complex motion | Steeper learning curve |
| **Edit/Color (Track Matte)** | Familiar timeline workflow, real-time | Track matte can be finicky, less flexible |

**Recommendation**: Use Fusion for complex shots; Edit page for quick social content.

## Magic Mask Tips (for Depth Masking)

- **Mode**: "F" (Forward), "B" (Backward), "BI" (Bidirectional) — use BI for best tracking
- **Refine**: After initial mask, use "Refine" brush to add/subtract
- **Softness**: 2-5 pixels for natural edge; 0 for hard cutout
- **Invert**: Connect inverted mask to background blur for fake DOF
- **Cache**: Enable Fusion Cache (Playback menu) for smooth playback

## Lower Third Template Structure (Fusion)

```
MediaIn1 (BG footage)
    |
Background (dark semi-transparent rect)
    |
Text+ (Name)
    |
Text+ (Title)
    |
Merge (Text over Background)
    |
Merge (over MediaIn1)
    |
MediaOut1
```

Save as `.setting` file: Right-click comp → Save Macro → use in any project.

## Keyboard Shortcuts (Text Workflow)

| Action | Mac | Windows |
|--------|-----|---------|
| Add Text+ (Edit) | Option+T | Alt+T |
| Add Text+ (Fusion) | Right-click → Add Tool → Text+ | Same |
| Blade (cut text clips) | B | B |
| Keyframe (add) | Option+Click param | Alt+Click param |
| Show Keyframes | Option+K | Alt+K |
| Fusion Viewer 1/2 | 1 / 2 | 1 / 2 |

## Related Skills

- `davinci-resolve-techniques/davinci-masking-compositing` — Power Windows, Magic Mask, tracking
- `davinci-resolve-techniques/davinci-fusion-fairlight-vfx` — Fusion compositing fundamentals
- `davinci-resolve-techniques/davinci-edit-speed-ramp` — Thumbnail creation on Edit page