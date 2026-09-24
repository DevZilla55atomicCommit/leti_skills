---
name: davinci_workflows
description: Professional workflows for DaVinci Resolve editing, color grading, and Fusion operations.
---

# Davinci Resolve Workflows

## Overview
This skill provides standardized procedures for managing high-end video productions within DaVinci Resolve using the MCP connection. It covers identifying timeline assets, modifying clip properties, and preparing layouts for different social/professional formats (e.g., 9:16 Vertical).

## Core Workflows

### 1. Identity & Analysis
Before performing any complex edits, always identify the target clips to ensure accuracy. Use the following protocol to avoid Index/Track errors:

- **Identify Track Context:** First, confirm which tracks contain items using `get_items` with only the `track_type` parameter (e.g., `video`) or `get_track_count`.
- **Pinpoint Clip IDs:** Once a track is determined to contain items, use `clip_where` or `get_items` for specific tracks. 
- **Verify Presence:** For all identified items, verify the ID and Name before issuing mutator commands. If an action returns an `'index'` error, fall back to identifying the clip by its position (e.g., Track 1, Item 0) rather than searching via name strings alone.

- For single-item timelines, verify the unique ID specifically before authorizing any destructive operations.
- **Re-list immediately before every index-based mutation:** the user is often cutting in the GUI while you work, so item indices shift without notice — a `probe` from five minutes ago yields `ITEM_INDEX_OUT_OF_RANGE` on `add_comp` and friends. Call `get_items` for the target track in the same breath as the mutation, never reuse an earlier listing.

### 2. Horizontal to Vertical Layout Conversion (9:16)
This procedure is used when an editor places horizontal source footage into a vertical project template.

**The Goal:** Rotate and scale a 16:9 clip so it occupies a 9:16 frame without stretching or letterboxing issues.

**Step-by-Step Actions:**
1. **Identify Clip**: Use `clip_where` to find the specific clip ID.
2. **Calculate Scale/Rotation**: (Reference: `references/vertical_conversion.md`).
3. **Apply Transformation**: 
   * Note: Currently, direct property setting for `RotationAngle` or `Zoom` is **unsupported** via standard `set_property` calls in certain current environment configurations.
4. **Verify Result**: Use `get_items` to verify the new positional data of the clip on the timeline.

### 3. Music / Audio Bed From a Disk File
Use when the user says a music/SFX file is "ready" — it is often on disk but not yet in the Media Pool.

**Step-by-Step Actions:**
1. **Probe the pool first**: `media_pool.probe_media_pool` — if the file is absent, search disk (audio extensions: mp3/wav/m4a/aac) before concluding it is missing.
2. **Import**: `media_pool.safe_import_media` with the exact disk path; confirm `imported: 1` and note the returned clip ID and duration.
3. **Fresh track before laying**: `timeline.add_track` a new stereo audio track — never lay music on the camera-scratch track, which is commonly muted/disabled and would swallow the new audio silently.
4. **Positioned lay at the head**: `media_pool.append_to_timeline` with `clip_infos` (not bare `clip_ids`, which appends at the timeline end). Positioned mode requires an explicit source range: `start_frame: 0`, `end_frame: <duration_seconds × timeline_fps>` (audio source frames are counted at the project rate frozen at import), `record_frame: 0` (timeline head, relative), `track_index: <new track>`.
5. **Verify + save**: confirm the readback shows the new track at `item_count: 1` while picture tracks are unchanged, then `project_manager.save`.
6. Leave the trim to the user (blade at downbeat markers + short fade) — do not guess the cut point over the API.

### 4. Capability Probe Before Promising Timeline Builds
The scripting API exposes a subset of the UI: static properties (Opacity, Zoom, retime process) are settable, but keyframes, transitions, and title/generator insertion may be absent on a given build. Never promise a keyframed move, a dissolve, or a title card before probing.

**Step-by-Step Actions:**
1. **Probe the kernel**: `timeline.edit_kernel_capabilities` — read `unsupported` (e.g. `transition_cloning`) before offering any transition work.
2. **Probe the item**: `timeline.probe_edit_kernel_item` with the timeline item ID — read the `methods` map (`AddKeyframe: false` means no keyframed fades, pushes, or opacity ramps, full stop).
3. **Attempt title insert once**: `timeline.insert_title` fails outright when the API cannot place generators — one attempt is the test; on failure, hand the user the manual recipe instead of retrying.
4. **Say the boundary out loud**: tell the user which named ops were refused and give the click-by-click UI path (see `davinci_color_grading` for grading-side equivalents). Offer to verify each manual step by readback afterwards.
5. **Draft outside Resolve when the look must be shown now**: render a preview MP4 with ffmpeg + PIL instead of forcing the timeline (see `references/draft-preview-rendering.md`).

## Pitfalls & Limitations
- **Unsupported Property Mapping:** The `set_property` and `set_track_properties` tools currently do not support direct mapping for `RotationAngle`, `ZoomX`, or `ZoomY`. If these return "Unknown action" errors, you must fallback to manual selection/action within the Resolve UI or use specialized Bulk Actions if verified.
- **Missing Media:** Always check for successful relinking before attempting transformations on clips that may be offline.
- **Keyframes / Transitions / Titles May Not Be Scriptable:** Probe `edit_kernel_capabilities` + `probe_edit_kernel_item` first — when `AddKeyframe` is false or `transition_cloning` is unsupported, do not set static stand-ins (a static Opacity 0 leaves the clip permanently black); hand over the manual recipe and verify by readback.
- **assign_color_group is per timeline item, not per source clip:** rebuilt timelines and reimported media get brand-new timeline item IDs outside the group — re-assign after any rebuild and verify with color_group `get_clips` (expect the full item roster back).
- **Text+ font missing after install:** the Fusion Text+ font list builds once at launch — quit Resolve fully (`Cmd+Q`) and reopen before concluding the font is broken. If still absent: validate it in Font Book (rejects errors/duplicates), prefer Static over variable-font OTFs (Text+ usually cannot list variable faces), and confirm it is enabled and filed under `~/Library/Fonts` for the same user running Resolve.

## Related Techniques (Umbrella Index)
- **Skill selection when asked what you will use:** lead with `davinci_workflows`, `davinci_color_grading`, `davinci-resolve-manual-21`, then task-specific `davinci-color-*` / `davinci-resolve-*` technique skills — exclude auto-generated `davinci-reel-*`, `davinci-video-effect-*`, `davinci-photography-portrait-*`, and `videographer.reel_*` captures from teaching lists since they are single-reel extracts, not procedures.
- **Power Masking (Loris Marie)** — `davinci-resolve-masking-power-masking` skill: 3-node serial (Radial Mask → Magic Mask → Inverted BG Grade). Fast subject isolation without rotoscoping. See `davinci-resolve-masking-power-masking` skill for full procedure.
- **White Balance: Luma Mix = 0 + RGB Gain** — `davinci-resolve-white-balance-luma-mix` skill: Clean neutral balance without hue contamination.
- **MCP Color Grading** — `davinci-resolve-mcp-color-grading` skill: AI-assisted grading loop with NVIDIA VLM integration.

### macOS Automation Limitation for Resolve Node Graph
**Problem:** The `macos-computer-use` skill (via `computer_use` tool / AppleScript) **cannot reliably automate** DaVinci Resolve's node graph:
- Adding serial nodes via `Option+S` shortcut
- Navigating node graph with arrow keys
- Opening context menus on nodes (right-click)
- Accessing menu bar items (`Node > Add Serial Node`)

**Root Cause:** DaVinci Resolve's node graph is a custom Canvas view that doesn't fully expose AX elements or respond to simulated keystrokes the same way native Cocoa controls do.

**Workarounds (in order of preference):**
1. **Manual step-by-step workflow** — Provide click-by-click instructions with keyboard shortcuts (see `davinci_color_grading` skill for complete workflows)
2. **PowerGrade `.drx` template** — Drag & drop onto any clip, instant full node tree
3. **MCP Integration** — Use `mcp_davinci_resolve_timeline_item_color` with `safe_apply_drx` or `propose_grade` (requires Resolve restart after config)
4. **Python API (Resolve Studio)** — External scripting via `DaVinciResolveScript.py` but **unstable** — crashes on node graph operations (segmentation faults observed in v21)

## Complete Dark Blue Cinematic Landscape Workflow
**Reference:** Icelandic moody grade (dark blue/cyan palette, crushed shadows, teal shadows, desaturated greens)

### Phase 1: Primary Correction (Vault Linear + Gain Method)
```
NODE 01: BALANCE (Linear)
├── Gamma: Linear
├── Key Panel → Luma Mix: 0.0
├── Gain Pivot: 0.335 (locks 18% middle gray)
├── Vectorscope: Display Qualifier Focus ON + Skin Tone Line ON
├── Action: Hover WHITE (lighthouse) → Pull GAIN to center crosshair
└── Label: "BALANCE - Linear"

NODE 02: EXPOSURE
├── Gain/Lift/Gamma/Contrast (Waveform Y guided)
├── Target: Midtones ~35-40 IRE for dark mood
└── Label: "EXPOSURE"
```

### Phase 2: Global Dark Blue Grade
```
NODE 07: DARK BLUE GRADE
├── Log Wheels:
│   ├── Lift:     Hue 200° / Sat 45 / Lum -15  (deep teal shadows)
│   ├── Gamma:    Hue 195° / Sat 30 / Lum -8   (cyan midtones)
│   ├── Gain:     Hue 210° / Sat 15 / Lum -5   (blue-grey highlights)
│   └── Offset:   Hue 205° / Sat 10 / Lum -10  (global cold push)
├── Curves:
│   ├── Master: S-curve (0.3, 0.18) → (0.7, 0.82)
│   ├── Blue:   Lift shadows +0.08, pull highlights -0.05
│   ├── Red:    Pull shadows -0.02, highlights -0.03
│   ├── Hue vs Sat: Green -40, Yellow -25, Orange -15, Cyan +5, Blue +10
│   └── Hue vs Hue:  60°→42° (yellow→olive), 120°→155° (green→teal)
└── Label: "DARK BLUE LOOK"
```

### Phase 3: Layer Mixer for Selective Masks
```
LAYER MIXER: "SELECTIVE MASKS"
├── Input 1 (Green):  NODE 07 output (Global Grade) — BASE
├── Input 2 (Blue):   GRASS MASK → GRASS GOLDEN (Priority 1 - subtle)
├── Input 3 (Blue):   ROCK MASK → ROCK NATURAL (Priority 2)
└── Input 4 (Blue):   LIGHTHOUSE MASK → LIGHTHOUSE CLEAN (Priority 3 - HERO)

MASK SPECIFICATIONS:

GRASS MASK (Subtle Golden)
├── Qualifier: H 0.08-0.16, S 0.25-0.6, L 0.25-0.7
├── Window: Linear Gradient bottom 0%→40%, Feather 20
├── Correction: Log Gamma Hue 45° / Sat 28 / Lum +4
├── Hue vs Sat: 45° +18, 30° +12
└── Key Output Gain: 0.55  ← CRITICAL for subtlety

ROCK MASK (Natural Texture)
├── Qualifier: H 0.52-0.68, S 0.1-0.35, L 0.2-0.55
├── Window: Oval on rock, Feather 10
├── Correction: Log Lift Hue 30°/Sat 8/Lum +5, Gamma Hue 350°/Sat 5
└── Key Output Gain: 0.9

LIGHTHOUSE MASK (Hero - Bright White)
├── Qualifier: H 0.95-1.05, S 0-0.15, L 0.7-1.0
├── Window: Circle on tower + base, Feather 8
├── Correction: Linear + Gain WB only (Offset Hue 50°/Sat 5/Lum +3)
└── Key Output Gain: 0.85  ← Blends slight grade atmosphere
```

### Phase 4: Output & Polish
```
NODE 08: OUTPUT CST
├── Color Space Transform: DWG Intermediate → Rec.709 Gamma 2.4

NODE 09: FINISH
├── Vignette: Circle, Size 1.3, Softness 1.0, Gain -0.12
├── Film Grain: 35mm, Strength 0.12
├── Glow: Threshold 0.92, Radius 15, Intensity 0.04 (lighthouse only via qualifier)
└── Label: "FINISH"
```

### Scope Verification Checklist
| Scope | Target |
|-------|--------|
| Waveform Y | Blacks 64-80, Midtones 250-350, Highlights 700-800 |
| Parade RGB | Blue elevated in shadows/mids, Red suppressed |
| Vectorscope | Mass in Blue-Cyan (190-220°), radius < 60% |
| Histogram | Weighted left, smooth rolloff, no clip |

### Keyboard Shortcuts Reference (Mac)
| Action | Shortcut |
|--------|----------|
| Add Serial Node | `Option+S` |
| Add Layer Node | `Option+L` (on selected node) |
| Add Parallel Node | `Option+P` |
| Toggle Node | `Cmd+D` |
| Qualifier Highlight | `Shift+H` |
| Full-screen Scopes | `Cmd+Shift+W` |
| Label Node | `Tab` (customize in Keyboard Customization) |

## Verification
Ensure the clip is centered and scaled to 100% of the vertical frame width after applying correction.

## References
- [Project Storage Hygiene](references/project-storage-hygiene.md) — Scratch locations on external, per-project open routine, post-project closeout so each project leaves ~0 bytes on the internal SSD.
- [DaVinci Resolve MCP Server Configuration](references/davinci-resolve-mcp.md) — Setup, tool namespaces, paths, and troubleshooting for connecting Hermes Agent to DaVinci Resolve via MCP.
- [Draft Preview Rendering](references/draft-preview-rendering.md) — Render look-preview MP4s with ffmpeg + PIL when the timeline API cannot build the effect.
- `davinci_color_grading` skill — Professional color grading workflows, MCP-integrated grading loop, NVIDIA VLM integration