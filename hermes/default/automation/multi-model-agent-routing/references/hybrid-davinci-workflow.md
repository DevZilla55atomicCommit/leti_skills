# Hybrid DaVinci Resolve Workflow — API vs computer_use Boundary

*Authoritative reference for what can/cannot be driven via computer_use on macOS. Based on empirical testing and user correction (2026-08-19).*

---

## The Hard Boundary

**On macOS, DaVinci Resolve's color wheels, curves, and qualifier HSL controls are custom Metal-rendered UI elements with NO accessibility (AX) exposure.**

This means:
- ❌ `computer_use` CANNOT click/drag color wheels (lift/gamma/gain/offset)
- ❌ `computer_use` CANNOT manipulate curve points (custom curve, hue vs sat, hue vs hue, etc.)
- ❌ `computer_use` CANNOT adjust qualifier HSL ranges (hue/sat/lum sliders, color picker)
- ❌ `computer_use` CANNOT drag nodes in the node graph (custom canvas)
- ❌ `computer_use` CANNOT adjust OFX plugin parameters in the inspector (custom controls)

**Any claim otherwise is false and will waste user time.**

---

## What computer_use CAN Drive (AX-Exposed)

| Category | Elements | Method |
|----------|----------|--------|
| **Tabs/Pages** | Color, Edit, Cut, Fairlight, Fusion, Deliver | Click tab buttons (AXButton) |
| **Panels** | Gallery, Nodes, Scopes, Effects, Media Pool | Click panel toggles, expand/collapse |
| **Buttons** | Add Node, Delete Node, Reset Grade, Copy/Paste Grade, Version controls | Click AXButton elements |
| **Dropdowns/Selects** | Color space, LUT selection, render preset, codec | Click AXPopUpButton, select option |
| **Text Fields** | Node labels, version names, render path, clip names | Type into AXTextField |
| **Checkboxes** | Node enable, layer mixer modes, keyframe toggles | Click AXCheckBox |
| **Viewer** | Play/pause, scrub timeline, zoom/pan viewer | Click transport controls, drag in viewer (AXImage) |
| **Qualifier Pick** | **Click in viewer to sample color** | Click at coordinates in viewer AXImage |
| **Power Window** | **Click/drag to create shapes** | Drag in viewer AXImage |
| **Magic Mask** | Click to add strokes, refine | Click in viewer AXImage |
| **Timeline** | Cut/trim clips, add tracks, navigate | Click timeline elements (AXButton, AXSlider) |
| **Media Pool** | Import, create bins, drag to timeline | Click/drag AX elements |
| **Render Queue** | Add job, start/stop render, settings | Click AX buttons, dropdowns |

---

## What Must Use API / Scripting / DCTL

| Operation | Method | Notes |
|-----------|--------|-------|
| **Primary Grade (CDL)** | DCTL / Python script / API | slope/offset/power/sat per node |
| **Color Wheels** | DCTL / API | Lift/Gamma/Gain/Offset — no AX access |
| **Curves** | DCTL / API | Custom, Hue vs Sat, Hue vs Hue, Lum vs Sat — no AX access |
| **Qualifier HSL** | DCTL / API | Hue/Sat/Lum ranges, softness — no AX access |
| **Keyframes** | API / Python | Color keyframes on nodes — limited AX |
| **Node Graph Structure** | API / Python | Connections, parallel/serial/layer — no AX |
| **OFX Parameters** | API / Python | Plugin-specific controls — no AX |
| **Gallery Stills** | API | Save/recall grades — scriptable |
| **Render Settings** | API / Python | Codec, format, burn-ins — scriptable |
| **Project Settings** | API | Color management, timeline res — scriptable |

---

## Hybrid Workflow Pattern (Recommended)

### Phase 1: Setup via computer_use
```python
# 1. Open project, navigate to Color page
computer_use(action="click", element=color_tab_button)

# 2. Create node structure
computer_use(action="click", element=add_serial_node)  # Node 1: Balance
computer_use(action="click", element=add_serial_node)  # Node 2: Creative
computer_use(action="click", element=add_parallel_node)  # Node 3: Skin
computer_use(action="click", element=add_layer_mixer)  # Node 4: Output

# 3. Label nodes
computer_use(action="type", text="Balance", element=node1_label)
computer_use(action="type", text="Creative", element=node2_label)
```

### Phase 2: Primary Grade via API/DCTL
```python
# Apply CDL values precisely
apply_cdl(node="Balance", slope=[1.02, 0.98, 1.0], offset=[0.01, -0.02, 0.0], power=[0.95, 1.0, 1.05], sat=1.1)
```

### Phase 3: Creative/Qualifier via computer_use
```python
# 4. Select Creative node
computer_use(action="click", element=node2_thumbnail)

# 5. Qualifier pick — click in viewer
computer_use(action="click", coordinate=[viewer_x, viewer_y])  # Sample skin tone

# 6. Power window — drag in viewer
computer_use(action="drag", from_coordinate=[x1, y1], to_coordinate=[x2, y2])  # Create circle

# 7. Magic Mask — add strokes
computer_use(action="click", coordinate=[stroke_points...])
```

### Phase 4: Fine-tune via API
```python
# 8. Adjust qualifier ranges precisely
set_qualifier_hsl(node="Creative", hue_range=[20, 40], sat_range=[0.3, 0.8], lum_range=[0.2, 0.7])

# 9. Curve adjustments
set_curve(node="Creative", curve_type="hue_vs_sat", points=[[0,0], [0.3, 1.2], [0.7, 0.8], [1,1]])
```

### Phase 5: Render via API
```python
# 10. Queue render
render_timeline(preset="ProRes_4444", output_path="/Volumes/.../graded/")
```

---

## Implementation in Agent Prompts

### Video-Grader Agent Prompt Must Include:

> **Hybrid Workflow Rule**: You work in a hybrid DaVinci Resolve workflow:
> - **computer_use** for: tab switching, node creation/labeling, viewer clicks (qualifier pick, power window, magic mask), panel toggles, button clicks, dropdowns, text fields, timeline navigation, render queue buttons
> - **API/DCTL/Python** for: CDL values (slope/offset/power/sat), color wheels, ALL curves (custom, hue vs sat, hue vs hue, lum vs sat), qualifier HSL ranges, keyframes, node graph connections, OFX parameters, gallery stills, render settings
> - **NEVER** claim computer_use can drive color wheels, curves, or qualifier HSL on macOS — they are custom Metal controls with no AX exposure. This is a hard boundary.

---

## Verification Checklist

When designing a grading task for Video-Grader agent, verify:

- [ ] CDL/primary grade → API/DCTL
- [ ] Node structure → computer_use (create) + API (connect)
- [ ] Qualifier pick → computer_use (viewer click)
- [ ] Qualifier HSL ranges → API
- [ ] Power window → computer_use (viewer drag)
- [ ] Magic Mask → computer_use (viewer strokes)
- [ ] Curves → API/DCTL
- [ ] Color wheels → API/DCTL
- [ ] Version management → computer_use (version buttons)
- [ ] Gallery stills → API
- [ ] Render → API

---

## Future: When This Changes

If Blackmagic adds AX exposure to color controls (unlikely — Metal rendering is intentional for performance), update this doc and the agent prompts. Until then, **the boundary is absolute**.