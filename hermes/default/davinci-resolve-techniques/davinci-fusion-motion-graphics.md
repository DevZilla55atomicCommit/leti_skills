---
name: davinci-fusion-motion-graphics
description: Motion graphics and title design in DaVinci Resolve Fusion page. Covers Text+, modifiers, expressions, templates, lower thirds, kinetic typography, and macro creation for reusable motion graphics.
trigger: motion graphics, fusion titles, text+, lower thirds, kinetic typography, fusion templates, macros, expressions, davinci resolve fusion
steps:
  - "Fusion Page: Create new composition or use timeline Fusion clip"
  - "Add Text+ tool for advanced text formatting"
  - "Use Modifiers (Publish, Expressions, Animations) for dynamic behavior"
  - "Build reusable templates with Published parameters"
  - "Create Macros (.setting) for drag-and-drop reuse"
  - "Animate with Keyframes, Splines, or Expressions"
  - "Add effects: Glow, Blur, Shatter, Displace, Particles"
  - "Save as Fusion Title Template for Edit page use"
parameters:
  - name: template_type
    type: string
    description: Type of motion graphic template
    enum: ["Lower Third", "Full Screen Title", "Kinetic Typography", "Logo Reveal", "Transition", "Social Media Pack", "Broadcast Package"]
    default: "Lower Third"
  - name: text_tool
    type: string
    description: Text tool to use
    enum: ["Text+ (Advanced)", "Text (Legacy)", "Text 3D"]
    default: "Text+ (Advanced)"
  - name: animation_method
    type: string
    description: Primary animation approach
    enum: ["Keyframes", "Expressions", "Modifiers (Follower/Trigger)", "Scripted (Lua/Python)", "Hybrid"]
    default: "Keyframes + Expressions"
  - name: publish_parameters
    type: array
    description: Parameters to publish for template users
    items:
      type: string
      enum: ["Text Content", "Font", "Font Size", "Text Color", "Background Color", "Animation Speed", "Position", "Scale", "Opacity", "In/Out Duration", "Style Preset"]
    default: ["Text Content", "Font", "Font Size", "Text Color", "Animation Speed", "In/Out Duration"]
tags:
  - motion-graphics
  - fusion
  - text-plus
  - titles
  - lower-thirds
  - kinetic-typography
  - templates
  - macros
  - expressions
  - davinci-resolve
  - motion-design
category: davinci-resolve-fusion-mograph
---

# DaVinci Resolve Fusion Motion Graphics & Titles

Complete guide to creating professional motion graphics, animated titles, lower thirds, and reusable templates in DaVinci Resolve Fusion page.

## Fusion Motion Graphics Architecture

### Core Tools for Motion Graphics
```
Text Tools:
- Text+ (Primary): Advanced formatting, per-character animation, OpenType features
- Text 3D: Extruded 3D text with materials, lighting
- Text (Legacy): Simple, deprecated

Animation Tools:
- Keyframes: Standard timeline animation
- Spline Editor: Graph editor for easing, overshoot
- Expressions: Mathematical/conditional animation (Lua-based)
- Modifiers: Follower, Trigger, Wiggle, Step, Ease
- TimeStretcher: Speed control, loops, ping-pong

Effects Tools:
- Background: Solid, Gradient, Image
- Merge: Composite layers (Over, Add, Multiply, Screen)
- Transform: Position, Scale, Rotation, Skew, Anchor
- Blur: Gaussian, Directional, Box, Lens
- Glow: Standard, Lens, Custom
- Shatter: Break text into pieces
- Displace: Warp with texture/map
- Particles: pEmitter, pRender (particle systems)
- Shape3D: 3D primitives for backgrounds
```

### Text+ Deep Dive (The Power Tool)
```
Text+ Tabs:
1. Text: Content, Font, Size, Alignment, Tracking, Leading
2. Shading: Fill (Solid/Gradient/Image), Stroke, Shadow, Outline
3. Layout: Frame, Anchor, Tab Stops, Columns
4. Transform: Per-character Position, Rotation, Scale, Skew
5. Style: Presets, Character/Paragraph styles
6. Animation: Write-on, Range selectors, Per-character timing

Key Text+ Features:
- Unicode support (emoji, CJK, RTL)
- Variable fonts (weight/width/optical size axes)
- OpenType features (ligatures, alternates, fractions)
- Per-character animation via Range Selector
- Expression-driven text content
- RTL/LTR mixed support
```

---

## Building Lower Thirds (Step-by-Step)

### Basic Lower Third Structure
```
Fusion Composition:
Background (Shape/Gradient) → Merge → Text+ (Name) → Merge → Text+ (Title) → MediaOut
                         ↑                                            ↑
                    Transform (Position)                        Transform (Position)

Published Parameters (Right-click → Publish):
- Name Text (Text+1.Text)
- Title Text (Text+2.Text)
- Name Font (Text+1.Font)
- Title Font (Text+2.Font)
- Primary Color (Background.Gradient.Color1)
- Secondary Color (Background.Gradient.Color2)
- Animation Speed (TimeStretcher.Speed)
- Position X/Y (Transform1.Center / Transform2.Center)
```

### Step-by-Step: Professional Lower Third
```
1. New Fusion Comp (Fusion page → New Comp)
2. Add Background tool:
   - Type: Gradient
   - Color1: Brand Primary (e.g., #0066CC)
   - Color2: Darker variant (e.g., #003366)
   - Angle: 90° (vertical) or 0° (horizontal)
   - Publish Color1, Color2 as "Primary Color", "Secondary Color"

3. Add Rectangle Mask on Background (for shape):
   - Rectangle tool → Connect to Background.EffectMask
   - Width: 0.8, Height: 0.15 (relative)
   - Center: X=0.5, Y=0.9
   - Corner Radius: 0.05
   - Publish Width/Height/Position as "Width", "Height", "Position"

4. Add Text+ (Name):
   - Font: Bold weight (Montserrat Bold, Inter Bold)
   - Size: 0.08 (relative to comp)
   - Color: White
   - Alignment: Left
   - Position: X=0.1, Y=0.88
   - Publish Text as "Name", Font as "Name Font", Size as "Name Size"

5. Add Text+ (Title):
   - Font: Regular weight
   - Size: 0.045
   - Color: Light gray (#CCCCCC)
   - Position: X=0.1, Y=0.93
   - Publish Text as "Title", Font as "Title Font"

6. Animation (In/Out):
   - Add TimeStretcher before MediaOut
   - Speed: 1.0 (Publish as "Animation Speed")
   - Keyframe Text+ Position Y: Start off-screen (1.2) → End (0.88)
   - Keyframe Background Mask Width: 0 → 0.8
   - Use Spline Editor: Ease Out (Back) for entrance, Ease In for exit
   - Publish In Duration, Out Duration

7. Save as Template:
   - File → Export → Macro (.setting)
   - Name: "Lower Third - Brand"
   - Category: "Templates/Motion Graphics"
   - Or: Right-click comp → "Create Template" → Appears in Edit page Titles
```

---

## Kinetic Typography (Text Animation)

### Range Selector Animation (Per-Character)
```
Text+ → Animation Tab:
1. Add Range Selector (click +)
2. Range Selector 1:
   - Start: 0, End: 1 (animate these)
   - Offset: 0 (animate for write-on)
3. Transform (under Range Selector):
   - Position Y: 0.5 (start below) → 0 (final)
   - Rotation Z: 15° → 0°
   - Scale: 0.5 → 1.0
   - Opacity: 0 → 1
4. Keyframe Start/End/Offset for cascading animation

Advanced: Multiple Range Selectors
- Selector 1: Position (entrance)
- Selector 2: Scale (overshoot)
- Selector 3: Opacity (fade)
- Selector 4: Color (highlight)
Each with different timing offsets
```

### Expression-Driven Typography
```
Text+ → Right-click parameter → "Expression"
Useful Expressions (Lua):

-- Random wiggle (per character)
math.sin(time * 5 + char_index * 0.5) * 10

-- Beat-reactive (requires audio analysis keyframes)
-- Assuming "AudioAmplitude" published from Fairlight
AudioAmplitude * 20

-- Time-based cycle
math.sin(time * frequency) * amplitude

-- Counter/Number animation
string.format("%.0f", time * 100) -- Counts up

-- Conditional (if/else)
if time < 1 then 0 else 1 end

-- Per-character delay (in Range Selector Transform)
-- Use "Index" variable (0-1 per character)
Position Y = Index * 50 * (1 - Progress)
```

### Write-On Effects
```
Method 1: Text+ Write-On (Built-in)
- Text+ → Animation → Write On: 0 to 1 (keyframe)
- Cursive/connected fonts work best

Method 2: Mask Reveal (Any font)
- Text+ → Rectangle Mask (animated Width)
- Mask: Left=0, Right=Progress (0→1)
- Soft Edge: 2-5px for smooth reveal

Method 3: Stroke Reveal (Path-based)
- Convert text to path (Right-click Text+ → "Convert to Path")
- Stroke tool → Animate "End" 0→1
- Only works on single-line paths
```

---

## Reusable Templates & Macros

### Creating a Fusion Title Template (Edit Page Integration)
```
1. Build composition with Published parameters
2. Right-click composition background → "Create Template"
3. Template Settings:
   - Name: "Modern Lower Third"
   - Category: "Custom / Motion Graphics"
   - Icon: Auto-generated or custom 100x100 PNG
   - Description: "Brand lower third with dual text lines"
4. Appears in Edit Page → Effects Library → Titles → Custom
5. Drag to timeline → Inspector shows published parameters
```

### Creating Macros (.setting files) for Fusion Page
```
1. Select all tools in comp (Ctrl+A)
2. Right-click → "Create Macro"
3. Macro Editor:
   - Name: "Lower Third - Corporate"
   - Inputs: Published parameters become macro inputs
   - Outputs: MediaOut (usually)
   - Icon: Generate or custom
4. Save: .setting file to:
   - User: ~/Library/Application Support/Blackmagic Design/DaVinci Resolve/Fusion/Macros/
   - Studio: /Library/Application Support/.../Macros/
5. Use: Right-click Flow view → "Add Macro" → Select .setting
```

### Template Parameter Best Practices
```
Naming Convention:
- Use spaces: "Animation Speed" not "animSpeed"
- Group with prefix: "Name - Font", "Name - Size", "Title - Font"
- Units in name: "Position X (%)", "Duration (frames)"

Parameter Types:
- Text: String (Text Content)
- Font: Font (dropdown)
- Color: Color (picker)
- Number: Slider (min/max/step)
- Boolean: Checkbox (On/Off)
- Choice: Dropdown (Preset 1, Preset 2, Custom)

Default Values:
- Always set sensible defaults
- Test with empty/long text
- Provide "Reset to Default" button (Script)
```

---

## Advanced Techniques

### Particle Text Effects
```
Text+ → pText (Particle Text) → pRender
1. Text+ with desired text
2. pText tool:
   - Input: Text+ (connect to pText.Style)
   - Particles Per Character: 10-50
   - Velocity: Random 3D
   - Life: 60-120 frames
3. pRender:
   - Render Mode: Points / Sprites / Mesh
   - Size: 0.01-0.05
   - Color: From Text+ shading
4. Forces: pTurbulence, pGravity, pVortex

Text Disintegration:
- Animate pText "Velocity" from 0 → high
- Add pAge → Color by Age (fade out)
- Trigger with Expression on "Active" checkbox
```

### 3D Text with Lighting
```
Text 3D Tool:
- Text: "TITLE"
- Extrusion Depth: 0.5
- Bevel: Round, Size 0.05
- Material: Phong / PBR
  - Diffuse: Brand color
  - Specular: White, Roughness 0.3
  - Metallic: 0.0 (or 1.0 for metal)

Lighting Setup:
- EnvironmentMap (HDRI) → Renderer3D.GlobalIllumination
- OR: 3-Point Lighting:
  - Key: DirectionalLight, Intensity 2.0, Angle -45°
  - Fill: AreaLight, Intensity 0.5, Opposite side
  - Rim: DirectionalLight, Intensity 1.5, Behind camera

Renderer3D:
- Quality: 2-4 (motion blur)
- Motion Blur: ON (Shutter Angle 180°)
- Anti-Aliasing: 4x
```

### Data-Driven Graphics (Spreadsheet/CSV)
```
Method 1: Text+ Expression + Lua Table
1. Create Lua script tool (Script tool)
2. Load CSV in script:
   local data = {}
   for line in io.lines("data.csv") do table.insert(data, line) end
3. Publish "Row Index" slider (1 to #data)
4. Text+ Expression: data[RowIndex]

Method 2: Fusion Template + CSV Import Script
1. Build template with published params
2. Python script (Resolve API):
   - Read CSV rows
   - Duplicate template comp
   - Set published params per row
   - Add to timeline

Method 3: Google Sheets / Airtable (via API)
- Requires external script + Resolve API
- Real-time updates possible
```

### Social Media Pack (Multi-Format)
```
Single Template → Multiple Aspect Ratios:
1. Build "Master" comp at 4K (3840x2160)
2. Add Transform tools for each output:
   - Transform_16x9: Scale 1.0, Center
   - Transform_9x16: Scale 0.56, Center Y (crop sides)
   - Transform_1x1: Scale 0.56, Center (crop top/bottom)
   - Transform_4x5: Scale 0.7, Center
3. Each Transform → MediaOut (named)
4. Publish "Format" dropdown:
   Expression on each Transform.Blend:
   if Format == "16x9" then 1 else 0 end
   (Repeat for each format)
5. User selects format → Only that output active
```

---

## Expressions Cookbook (Lua in Fusion)

### Common Expressions
```lua
-- Looping animation (0-1 cycle)
math.fmod(time, duration) / duration

-- Ping-pong (0-1-0)
local t = math.fmod(time, duration * 2)
if t > duration then return 2 - t/duration else return t/duration end

-- Wiggle (frequency, amplitude)
math.sin(time * frequency) * amplitude

-- Elastic ease out
local t = time / duration
if t >= 1 then return 1 end
return 1 - math.pow(2, -10 * t) * math.sin((t - 0.1) * 5 * math.pi)

-- Follow another tool's position (with offset)
ToolName.Center.X + 0.1

-- Clamp value
math.max(min, math.min(max, value))

-- Random seed per frame (for noise)
math.randomseed(frame); math.random()

-- Audio reactive (if AudioAmplitude published)
AudioAmplitude * multiplier

-- Text character counter
string.format("%03d", frame) -- 001, 002, 003...
```

### Expression on Published Parameter
```
Right-click published parameter → "Expression"
- Can reference other published params
- Can use time, frame, comp variables
- Cannot directly reference non-published tool params
- Workaround: Publish the source param too
```

---

## Performance Optimization

### Render Optimization
```
- Use Proxy Mode (Playback → Proxy → Half/Quarter)
- Cache tools: Right-click → "Cache Tool" (stores result)
- Merge tools: Flatten static layers (Background + Logo → Merge → Cache)
- Reduce Text+ complexity: Limit per-char animation to visible chars
- Particle count: Keep < 1000 for real-time
- 3D: Lower Renderer3D Quality (1 for draft, 4 for final)
- Motion Blur: Disable during design, enable for render
```

### Template Performance
```
- Minimize tool count (merge static elements)
- Avoid expressions on every frame (use keyframes + modifiers)
- Pre-render complex backgrounds as image sequences
- Use "Proxy" versions of assets in template
- Test on minimum spec machine
```

---

## Export & Delivery

### Fusion Title in Edit Page
```
1. Template appears in Effects Library → Titles
2. Drag to timeline
3. Inspector → Edit published parameters
4. Right-click → "Open in Fusion Page" for deep editing
5. Changes to template affect ALL instances (unless "Make Local Copy")
```

### Rendering Motion Graphics
```
Deliver Page:
- Individual clips: In/Out points on each graphic
- Alpha channel: Format → QuickTime → Apple ProRes 4444 (with Alpha)
- Or: EXR (multi-part, with Alpha)
- For web: WebM VP9 (with Alpha) or MOV HEVC Alpha

Batch Render:
- Select all graphic clips
- Add to Render Queue
- Use "Individual Clips" naming: %ClipName%_%TimelineName%
```

---

## Related Skills

- `davinci-fusion-compositing` - Core Fusion workflows
- `davinci-fusion-expressions` - Advanced Lua expressions
- `davinci-fusion-particles` - Particle systems deep dive
- `davinci-fusion-3d` - 3D compositing in Fusion
- `davinci-template-creation` - Template/macro authoring best practices