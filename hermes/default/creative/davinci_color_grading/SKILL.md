---
name: davinci_color_grading
description: Professional color grading workflows for DaVinci Resolve using MCP integration
---
## Overview
This skill provides specialized procedures for professional color grading in DaVinci Resolve, including:
- Primary color correction workflows
- Creative grading techniques
- LUT creation and application
- Skin tone preservation methods
- HDR and SDR workflows
- Node-based grading structures

## Core Workflows

### 1. Primary Color Correction
**Goal:** Establish proper exposure, white balance, and color balance before creative grading

**Steps:**
1. **Identify Timeline:** Confirm project settings (color space, gamma, color depth)
2. **Select Primary Clip:** Use `clip_where` to identify target clip
3. **Set Timeline Color Space:** Verify project color space matches footage (Rec.709, Log, etc.)
4. **Balance Exposure:** Use waveform and vectorscope to set proper exposure
5. **White Balance:** Use color picker on neutral gray area or apply temperature/tint adjustments
6. **Color Balance:** Adjust shadows, midtones, and highlights separately using color wheels
7. **Verify Scopes:** Check vectorscope for skin tone compliance and waveform for proper exposure

**Pitfalls:**
- Never adjust color before establishing proper exposure
- Avoid over-saturation in midtones which creates unnatural skin tones
- Be cautious with temperature adjustments on mixed lighting scenes

### 2. Creative Grading
**Goal:** Apply stylized color grades while maintaining natural skin tones

**Steps:**
1. **Create Grade Node:** Add a serial node after primary correction
2. **Select Grade Type:** Choose between:
   - Film emulation (Kodak, Fuji)
   - Cinematic looks (Teal-Orange, Orange-Blue)
   - Specific mood (warm/cool tones)
3. **Adjust Saturation:** Use saturation curves to control color intensity
4. **Modify Hue/Saturation:** Use hue vs. saturation curves for targeted adjustments
5. **Add Film Grain:** Apply subtle grain for organic texture (0.5-2% intensity)
6. **Vignette Control:** Add subtle vignette for focus (5-15% feather)
7. **Verify with Scopes:** Check vectorscope for skin tone compliance

**Pitfalls:**
- Avoid extreme saturation that clips skin tones
- Don't overdo vignette which creates unnatural edges
- Maintain consistent skin tones across shots in a scene

### 3. LUT Management
**Goal:** Create, apply, and manage custom LUTs

**Steps:**
1. **Create Reference Footage:** Shoot a color checker chart under controlled lighting
2. **Use Color Match Tool:** Match reference to desired grade
3. **Export LUT:** Save as .cube file with proper naming convention
4. **Apply LUT:** Use `apply_lut` command or node-based approach
5. **Fine-tune:** Adjust LUT intensity using opacity controls

**Pitfalls:**
- LUTs can create color banding if overused
- Custom LUTs may not match footage color space
- Always verify LUT application with vectorscope

**Resolve Built-in Film Looks (Kodak 2383, Fuji, etc.):**
- **Critical:** Built-in Film Looks expect **Cineon Log** input, not Rec.709
- **Correct Pipeline:** Grade in Rec.709/DWG Intermediate → CST (Rec.709→Cineon) → Apply Film Look LUT
- **Wrong Way:** Direct LUT on Rec.709 = crushed blacks, blown highlights, oversaturation
- **Intensity Control:** Wrap CST + LUT in **Compound Node** → use Key Output Gain for clean blending

### 4. Skin Tone Preservation
**Goal:** Maintain natural skin tones while grading

**Steps:**
1. **Use Qualifier Tool:** Select skin tones using hue/saturation/lightness ranges
2. **Create Power Window:** Isolate skin tones with circular/rectangular mask
3. **Adjust Specific Parameters:** Modify only skin tone parameters (temperature, saturation)
4. **Track Across Shots:** Use tracking tools to maintain isolation through movement
5. **Verify with Vectorscope:** Check for skin tone compliance (typically in midrange hues)

**Pitfalls:**
- Avoid over-isolating which creates unnatural edges
- Don't over-saturate skin tones which creates "waxy" appearance
- Be cautious with hue shifts that move skin tones out of natural range

**Advanced Workflows:**

**A. Layer Node Skin Protection (Teal/Orange Grades):**
```
1. Qualifier Key on skin (Node 3) → Outputs Alpha
2. Creative Grade (Node 5)
3. Option/Alt+L on Node 5 → Layer Mixer
4. Connect BLUE (Alpha) from Node 3 → BLUE input of Layer Mixer
5. If inverted: Key Panel → Invert Qualifier icon
6. Key Output Gain on Node 3 → Blend corrected skin WITH grade (~0.7-0.85)
```

**B. Qualifier + Vectorscope Workflow (Darren Mostyn):**
```
1. Get skin "in good place" in PRIMARIES first (Nodes 1-2)
2. CST/LUT → Rec.709
3. Qualifier Node: Select skin (eyedropper) → Shift+H = Highlight mode
4. Refine HSL manually: Hue Width → Sat Low (remove hair) → Lum
5. Matte Finesse: Clean Black (remove hair/bg) > Clean White > Blur Radius 1-3
6. Vectorscope ON + Skin Tone Indicator
7. Gamma → Nudge to skin tone line (most natural)
8. Saturation → Final pop
```

**C. Parallel Mixer Skin Isolation (Gabe Lomotey):**
```
Parallel Mixer
├── Main Grade (Serial)
└── Skin Branch
    ├── HSL Qualifier (Shift+H to view)
    ├── Matte Finesse (Clean Black/White, Blur)
    ├── Vectorscope → Warm to skin tone line
    └── HDR Wheels (¼ stop shadow/highlight) → "in-camera presence"
```

### 5. Color Space Transform Workflows (S-Log3 / Apple Log 2 / Universal Linear)

**Universal Linear + Gain Primary Correction (Waqas Qazi / Joris Hermans) — ⭐ RECOMMENDED PRIMARY METHOD**
```\nNODE 01: PRIMARY BALANCE (Linear)\n├── Right-click node → Gamma → Linear\n├── Key Panel → Luma Mix = 0 (CRITICAL - disables lift/gamma contamination)\n├── Gain Pivot: 0.335 (locks 18% middle gray)\n├── Vectorscope: Display Qualifier Focus ON + Skin Tone Line ON\n├── Action: Hover WHITE object → Pull GAIN to center trace on crosshair\n├── Result: Pure RGB offset = white balance + exposure in ONE wheel\n├── Time per shot: 5-15 seconds\n└── Label: \"BALANCE - Linear\"\n\nNODE 02: EXPOSURE/CONTRAST (Optional - same node or new)\n├── Gain up/down = Clean exposure (pivot locked)\n├── Waveform (Y) monitoring\n└── Label: \"EXPOSURE\"\n\nNODE 03: CREATIVE GRADE (Convert to Log/DWG first)\n├── CST: Linear → DaVinci Wide Gamut Log\n├── Log Wheels / Curves / Color Warper / LUTs\n├── Label: \"LOOK\"\n\nNODE 04: SKIN TONE PROTECTION (Layer Node)\n├── Qualifier on skin → Vectorscope 2x zoom + Skin Tone Line\n├── Hue vs Hue / Hue vs Sat fine-tune\n├── Key Output Gain blend (~0.7-0.85)\n└── Label: \"SKIN\"\n\nNODE 05: OUTPUT TRANSFORM\n├── CST: DWG → Display (Rec.709/P3/Rec.2020)\n└── Label: \"OUTPUT\"\n```

**Why Linear + Gain wins:**
- **Clean math**: Gain = pure RGB multiplier (photometric), no lift/gamma cross-contamination
- **Speed**: 10x faster than Lift/Gamma/Gain wheel-wrestling
- **Shot matching**: Copy Node 01 across scene → only minor Gain tweaks per clip
- **VFX pipeline compatible**: Linear is universal intermediate
- **PowerGrade template**: Save once, apply to ANY camera log via upstream CST

**S-Log3 (Sony FX3, A7S III, A7 IV, Venice):**
```\nOption A: Minimal 3-Node (Danny Gan)\nNode 1: PRIMARIES (upstream CST) → Tiny corrections\nNode 2: LOOK (upstream CST) → Creative\nNode 3: CST (end) → S-Gamut3.Cine/S-Log3 → Rec.709/Gamma 2.4\nTone Mapping: DaVinci | Gamut: None\n\nOption B: 7-Node Cinematic (Kyle White)\nNode 1: EXP (Lift/Gain)\nNode 2: WB (Eyedropper)\nNode 3: PW (Power Window + Outside Node for subject pop)\nNode 4: SKIN (Qualifier + Midtone Detail ~10)\nNode 5: CST (end) → S-Gamut3/S-Log3 → Rec.709/Gamma 2.4\nNode 6: LUT (Creative) → Key Output Gain for intensity\n\nOption C: Pro Techniques (Cullen Kelly)\n- ETTR (Expose to Right) philosophy\n- Lum vs Sat: Duck highlight point for filmic roll-off\n- Conservative NR: Spatial Better/Medium/Threshold 20\n- Toe-down curves for noisy shadows\n- Template node tree + Timeline Voyager LUTs\n```

**Apple Log 2 (iPhone 15/17 Pro Max):**
```\nOption A: Group Pre/Post-Clip Dual CST (Russell Wofford) ⭐ BATCH WORKFLOW\n1. Select all iPhone clips → Right-click → Add into New Group: \"iPhone Apple Log 2\"\n2. Group Pre-Clip Node: CST → Input: Apple Log 2 / Apple Log → Output: DaVinci Wide Gamut / DaVinci Intermediate\n3. Group Post-Clip Node: CST → Input: DWG Intermediate → Output: Rec.709 / Rec.709 (Gamma 2.4)\n4. All clip-level nodes BETWEEN Pre/Post grade in MASSIVE DWG space\n5. Benefit: Batch conversion, max latitude for highlight recovery/saturation\n\nOption B: Manual 2-Node CST (CineMirage)\nNode 1: CST Apple Log 2 → Rec.709\nNode 2: Primaries Grade (Sat~70, Gain/Lift/Gamma)\n\nOption C: Free Path (FujiCinema)\nCST: Rec.2020/Apple Log → Rec.709/Gamma 2.4\nHDR Exposure Fix → Contrast 1.3 + Sat (Commercial)\nOR CST→ST2084 + Kodak 2383 LUT (Film)\n```

**DaVinci Wide Gamut Intermediate (DWG):**
- Wider gamut/DR than Rec.709 → better highlight retention
- Grade in DWG → CST to Cineon for Film Looks → CST to Rec.709 for delivery
- Works with S-Log3, Apple Log 2, RED, Blackmagic, etc.
- **Universal Linear workflow**: CST (Camera Log → Linear) → Grade → CST (Linear → DWG/Log) → Creative → Output

**DaVinci Wide Gamut Intermediate (DWG):**
- Wider gamut/DR than Rec.709 → better highlight retention
- Grade in DWG → CST to Cineon for Film Looks → CST to Rec.709 for delivery
- Works with S-Log3, Apple Log 2, RED, Blackmagic, etc.

### 6. Kodak 2383 Film Emulation
**Correct Application (Darren Mostyn):**
```
1. Grade fully in Rec.709/DWG Intermediate
2. Disable all creative nodes
3. Add CST: Input Rec.709/Gamma 2.4 → Output Cineon Film Log
4. Apply Kodak 2383 LUT (D55 or D65)
5. Select CST + LUT → Right-click → Create Compound Node
6. Key Output Gain on Compound = Film intensity slider
```

**Advanced Free Path (Gabe Lomotey):**
```
DWG Intermediate Grade → Disable Grade → CST DWG→Cineon → Kodak 2383 D55
→ Fine-tune (e.g., -½ stop face) → Film Grain → Compound for blend
```

**Paid Path (Dehancer OFX):**
```
Source: DWG Intermediate → Film Stock: Kodak Gold 200 → Print: Kodak 2383
→ Tonal Contrast → Color Density → Grain → Bloom → Gate (Horizontal)
```

### 7. Node Tree Best Practices

| Principle | Application |
|-----------|-------------|
| **Grade in wide space** | DWG Intermediate > Rec.709 for latitude |
| **CST at end (upstream grading)** | Corrections in camera-native space preserve data |
| **Compound Node for LUT blending** | Only way to use Key Output Gain cleanly |
| **Layer Node for skin protection** | Composites corrected skin OVER creative grade |
| **Parallel Mixer for skin** | Blends (not stacks) skin corrections with grade |
| **Vectorscope = Truth** | Don't guess skin tones — verify on line |
| **Gamma = Skin shifter** | Most natural for midtone skin correction |
| **Saturation Low = Hair removal** | Hair often same hue, lower saturation |

---

## 8. MCP-Integrated Grading Workflow (DaVinci Resolve MCP + NVIDIA VLM)

**Overview:** Use the `davinci-resolve-mcp` NPM package (34 compound tools) to control Resolve from Hermes, combined with NVIDIA vision models (`neva-22b`, `vila`) for frame analysis and grade recommendations.

### 8.1 Setup

```yaml
# ~/.hermes/config.yaml
mcp_servers:
  davinci-resolve:
    command: "npx"
    args: ["-y", "davinci-resolve-mcp"]
    timeout: 120
    connect_timeout: 60
```

**Prerequisites:**
- DaVinci Resolve Studio running (or free version with limited API)
- External Scripting enabled: Preferences → System → General → "External scripting using" → "Local"
- Project open with timeline on Color page

Restart Hermes after adding config. Tools appear as `mcp_davinci_resolve_*`.

### 8.2 Core MCP Tools for Grading

| Tool | Key Actions |
|------|-------------|
| `mcp_davinci_resolve_timeline_item_color` | `grade_evidence_base`, `probe_node_graph`, `safe_set_cdl`, `safe_copy_grade`, `safe_apply_drx`, `bulk_match_to_hero`, `propose_grade`, `grade_boundary_report`, `grade_version_snapshot` |
| `mcp_davinci_resolve_media_analysis` | `analyze_clip`, `analyze_bin`, `analyze_sequence`, `capabilities`, `install_guidance`, `commit_vision` |
| `mcp_davinci_resolve_timeline_markers` | `get_thumbnail_image` (returns MCP Image for chat) |
| `mcp_davinci_resolve_project_settings` | `export_frame_as_still` |

### 8.3 Frame-First Grading Loop (VLM → CDL)

```
1. Resolve: Playhead on target clip → timeline_markers.get_thumbnail_image
2. VLM: Send frame to nvidia/neva-22b or nvidia/vila with grading prompt
3. VLM returns: Directional guidance ("Push Gamma toward warm orange...")
4. Resolve: timeline_item_color.safe_set_cdl with derived CDL values
5. Resolve: timeline_item_color.grade_version_snapshot (auto-version)
6. Resolve: timeline_markers.get_thumbnail_image → Compare before/after
```

**Grading Prompt for VLM:**
```text
You are a colorist assistant. Compare REFERENCE (look to match) vs MY FRAME (current).
For each tonal range, give directional wheel moves:
- Lift (shadows): push crosshair toward [hue], saturation [+/-]
- Gamma (midtones): push crosshair toward [hue], saturation [+/-]
- Gain (highlights): push crosshair toward [hue], saturation [+/-]
- Offset (global): push crosshair toward [hue], saturation [+/-]
Global: Saturation [+/-], Contrast [+/-], Color Boost [+/-]
No exact numbers — I tune by eye. Just directions.
```

### 8.4 Hero Clip Matching (Bin-Wide)

```text
# 1. Select hero clip in Resolve (playhead on it)
mcp_davinci_resolve_media_analysis(action="analyze_clip", params={"selected": true})

# 2. Get evidence base (one-line summary + structured data)
mcp_davinci_resolve_timeline_item_color(action="grade_evidence_base", params={"min_source_trust": "high"})

# 3. Analyze target bin
mcp_davinci_resolve_media_analysis(action="analyze_bin", params={"recursive": true})

# 4. Dry-run match
mcp_davinci_resolve_timeline_item_color(
  action="bulk_match_to_hero",
  params={
    "hero_id": "<hero-clip-id>",
    "target_ids": ["clip-1", "clip-2", "..."],
    "method": "copy_grade",
    "dry_run": true
  }
)

# 5. Review proposals, then execute with confirm_token
mcp_davinci_resolve_timeline_item_color(
  action="bulk_match_to_hero",
  params={... "dry_run": false, "confirm_token": "..." }
)
```

### 8.5 Visual Analysis Pipeline (host_chat_paths)

The MCP uses **deferred vision**:
1. `media_analysis(analyze_clip, vision={enabled: true, provider: "host_chat_paths"})`
2. Returns `frame_paths` (local files) + `vision_token` + JSON schema
3. **You must read each frame as image**, produce JSON per schema
4. Call `media_analysis(commit_vision, params={clip_id, visual: <your JSON>, vision_token})`
5. Metadata + Media Pool markers written automatically

**Do not skip `commit_vision`** — analysis stays in `pending_host_vision_analysis` limbo.

### 8.6 Propose Grade (Structured, Validated)

```text
mcp_davinci_resolve_timeline_item_color(
  action="propose_grade",
  params={
    "target_id": "<timeline-item-id>",
    "evidence_base": "<line from grade_evidence_base>",
    "frame_paths": ["/path/to/frame.png"],
    "operation_class": "direct",
    "cdl_delta_or_artifact": {"cdl": {"slope": [...], "offset": [...], "power": [...], "saturation": 1.0}},
    "execute": false
  }
)
```
Returns `plan_id` + `preview_path`. Review, then re-call with `execute: true`.

### 8.7 Key Actions Quick Reference

| Action | Use For |
|--------|---------|
| `grade_evidence_base` | **Always first** — snapshot versions, node graph, color groups, coverage |
| `grade_boundary_report` | Full capabilities + item snapshot + groups + gallery |
| `probe_node_graph` | Inspect node count, LUTs, cache mode, labels |
| `safe_set_cdl` | Primary correction (validates, dry-run, normalizes) |
| `safe_copy_grade` | Copy grade to N items (dry-run first) |
| `safe_apply_drx` | Apply `.drx` grade file (replaces graph, snapshots first) |
| `safe_export_lut` | Export LUT to temp path (sandboxed) |
| `bulk_match_to_hero` | Match bin clips to hero (copy_grade / match_to_reference / skin_match) |
| `propose_grade` | Formal recommendation with validation + preview |
| `grade_version_snapshot` / `restore` | Version control for grades |

### 8.9 MCP Connection Verification (Added 2025-07-06)

After adding the MCP server config, **restart Hermes** (no hot-reload for native MCP client). Verify:

```text
# In Hermes chat after restart:
"List available MCP tools"
```

Expected tools (prefixed `mcp_davinci_resolve_`):
- `timeline_item_color` — grading actions
- `gallery_stills` — grab/export Gallery stills + `.drx`
- `media_analysis` — visual analysis, transcription
- `timeline_markers` — thumbnails, markers, frame images
- `resolve_control` — version, page switching
- `project_manager` — project operations

**Config gotcha fixed this session:** `args` must be a YAML array, not a string:
```yaml
# WRONG (what hermes config set wrote)
args: '["-y", "davinci-resolve-mcp"]'

# CORRECT (manual YAML edit)
args:
  - "-y"
  - "davinci-resolve-mcp"
```

### 8.10 macOS Automation Limitation for Resolve Node Graph (Added 2025-07-06)

**Problem:** The `macos-computer-use` skill (via `computer_use` tool / AppleScript) **cannot reliably automate** DaVinci Resolve's node graph:
- Adding serial nodes via `Option+S` shortcut
- Navigating node graph with arrow keys
- Opening context menus on nodes (right-click)
- Accessing menu bar items (`Node > Add Serial Node`)

**Root Cause:** DaVinci Resolve's node graph is a custom Canvas view that doesn't fully expose AX elements or respond to simulated keystrokes the same way native Cocoa controls do.

**Workarounds (in order of preference):**
1. **Manual step-by-step workflow** — Provide click-by-click instructions with keyboard shortcuts (see workflows above)
2. **PowerGrade `.drx` template** — Drag & drop onto any clip, instant full node tree
3. **MCP Integration** — Use `mcp_davinci_resolve_timeline_item_color` with `safe_apply_drx` or `propose_grade` (requires Resolve restart after config)
4. **Python API (Resolve Studio)** — External scripting via `DaVinciResolveScript.py` but **unstable** — crashes on node graph operations (segmentation faults observed in v21)

### 8.11 Complete Dark Blue Cinematic Landscape Workflow (Added 2025-07-06)

**Reference:** Icelandic moody grade (dark blue/cyan palette, crushed shadows, teal shadows, desaturated greens)

#### Phase 1: Primary Correction (Vault Linear + Gain Method)
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

#### Phase 2: Global Dark Blue Grade
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

#### Phase 3: Layer Mixer for Selective Masks
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

#### Phase 4: Output & Polish
```
NODE 08: OUTPUT CST
├── Color Space Transform: DWG Intermediate → Rec.709 Gamma 2.4

NODE 09: FINISH
├── Vignette: Circle, Size 1.3, Softness 1.0, Gain -0.12
├── Film Grain: 35mm, Strength 0.12
├── Glow: Threshold 0.92, Radius 15, Intensity 0.04 (lighthouse only via qualifier)
└── Label: "FINISH"
```

#### Scope Verification Checklist
| Scope | Target |
|-------|--------|
| Waveform Y | Blacks 64-80, Midtones 250-350, Highlights 700-800 |
| Parade RGB | Blue elevated in shadows/mids, Red suppressed |
| Vectorscope | Mass in Blue-Cyan (190-220°), radius < 60% |
| Histogram | Weighted left, smooth rolloff, no clip |

#### Keyboard Shortcuts Reference (Mac)
| Action | Shortcut |
|--------|----------|
| Add Serial Node | `Option+S` |
| Add Layer Node | `Option+L` (on selected node) |
| Add Parallel Node | `Option+P` |
| Toggle Node | `Cmd+D` |
| Qualifier Highlight | `Shift+H` |
| Full-screen Scopes | `Cmd+Shift+W` |
| Label Node | `Tab` (customize in Keyboard Customization) |

### 8.8 NVIDIA VLM Models Available

| Model | Best For |
|-------|----------|
| `nvidia/neva-22b` | Strongest general VLM, good color reasoning |
| `nvidia/vila` | Multi-frame/video conversation, temporal reasoning |
| `nvidia/nemotron-nano-12b-v2-vl` | Fast/cheap, decent quality |
| `nvidia/llama-3.1-nemotron-nano-vl-8b-v1` | Lightweight, 8B |

Access via `https://integrate.api.nvidia.com/v1` with `NVIDIA_API_KEY`.

---

## 9. Magic Mask / Neural Engine Masking Workflows (Resolve Studio)

**New Section Added 2025-07-07** — Neural Engine-powered subject isolation replacing manual rotoscoping.

### 9.1 Power Masking — Loris Marie Technique (Radial → Magic Mask → Inverted BG)

**Source:** Instagram @loris_marie "Power of Masking 🥶" (July 7, 2026)
**Requires:** DaVinci Resolve Studio 18.5+ (Neural Engine), GPU 8GB+ VRAM

```
INPUT → [PRIMARY GRADE] → NODE 01 → NODE 02 → NODE 03 → OUTPUT
                        Radial    Magic     BG Grade
                        Mask      Mask      (Inverted)
```

#### Node 01: Radial Power Window (Search Constraint)
| Parameter | Setting | Why |
|-----------|---------|-----|
| **Tool** | Ellipse (Power Window) | Fast, featherable |
| **Target** | Subject (head-to-toe) | ~10-15% padding |
| **Softness** | **0.20 – 0.40** | Natural falloff |
| **Key Output** | **ON** | Verify isolation |

> **Loris's Insight:** *"Start with radial mask... keeps the next mask from grabbing random stuff in the background."* — Limits Magic Mask search region.

#### Node 02: Magic Mask (Precision Silhouette)
| Parameter | Setting | Why |
|-----------|---------|-----|
| **Mode** | **Object → Person** | Human silhouette detection |
| **Stroke** | Single rough across torso | Let AI read edges |
| **Track** | Forward + Backward | Full clip coverage |
| **Edge Softness** | 2-5 px | Match lens falloff |
| **Feather** | 1-3 px | Blend edge |
| **Clean Black** | 5-15% | Remove shadow noise |
| **Clean White** | 5-15% | Remove highlight noise |
| **Temporal Stabilization** | **ON (High)** | Prevent flicker |
| **Key Output** | **ON** | Verify clean matte |

> **Loris's Tip:** *"Magic mask reads edges and contrast to cut out silhouette precisely. Way faster than manual brushing."*

#### Node 03: Inverted Background Grade (The "Power" Look)
| Parameter | Setting |
|-----------|---------|
| **Key Input** | ← Node 02 Alpha Output |
| **Invert** | **ON** (critical — selects background) |
| **Gain** | +0.5 to +1.5 stops |
| **Temperature** | +10 to +30 (warm) |
| **Tint** | +5 to +15 (magenta) |
| **OpenFX Glow/Bloom** | Threshold 0.7-0.85, Radius 20-50, Intensity 0.3-0.6 |
| **Key Output** | **ON** (verify BG white, subject black) |

> **The Look:** *"Light hitting behind the subject, strong backlight effect, silhouette popping clean off the background."*

#### Save as Reusable Asset
1. Select Nodes 01-03 → Right-click → **Create Compound Node**
2. Right-click Compound → **Generate PowerGrade**
3. Name: `01_POWER_MASKING_Radial_MagicMask_BGGrade`

---

### 9.2 Magic Mask Pitfalls & Fixes

| Symptom | Root Cause | Solution |
|---------|------------|----------|
| Grabs background objects | Radial mask too loose/missing | Tighten Node 01 ellipse |
| Matte flickers/jitters | Temporal Stabilization OFF | Enable High; add keyframes |
| Hard edge/halo on subject | Softness low / Clean B/W off | Node 01 Softness 0.4+; Node 02 Feather + Clean B/W |
| BG grade affects subject | Invert OFF / Key Input wrong | Node 03: Invert=ON, Key=Node 02 Alpha |
| Panel missing | Not Studio / Neural Engine OFF | Requires Studio + Prefs→Memory&GPU→Enable |
| Slow tracking / crash | Insufficient VRAM | Lower Quality; Proxy mode (Timeline→Proxy) |
| Loses subject in motion | Low contrast / occlusion | Manual keyframes; Qualifier backup |

---

### 9.3 Advanced Variations

**A. Layer Node Skin Protection (prevent BG bleed on subject edges):**
```
Layer Node above Node 03
├── Key Input: Node 02 Alpha (Normal, not Inverted)
├── Grade: Skin protection / cleanup
└── Key Output Gain: ~0.7-0.85 blend
```

**B. Multiple Subjects (separate isolation chains):**
```
NODE 01a: Radial → Subject A → NODE 02a: Magic Mask → Subject A
NODE 01b: Radial → Subject B (Layer from 01a) → NODE 02b: Magic Mask → Subject B
NODE 03:  BG Grade (Key Input = combined 02a+02b Alpha, Invert=ON)
```

**C. Sky Replacement / BG Swap:**
```
NODE 03: Key Input ← Node 02 Alpha (Invert OFF = Subject)
       → Alpha Output → Layer Node with new BG
```

---

### 9.4 Performance Benchmarks

| Resolution | GPU (VRAM) | Track Speed | Notes |
|------------|------------|-------------|-------|
| 4K | 24GB (RTX4090) | ~15-25 fps | High Quality |
| 4K | 16GB (M3 Max) | ~10-18 fps | High Quality |
| 2K | 8GB (M1 Pro) | ~20-30 fps | Medium Quality |
| 1080p | 8GB | ~30-60 fps | Fast |

**Optimization:** Proxy Mode (Timeline→Proxy→Half/Quarter) for tracking; track at lower res, refine at full.

---

## 10. Related Skills & References

| Skill / Reference | Purpose |
|-------------------|---------|
| `davinci_workflows` | General Resolve editing, Fusion, delivery workflows |
| `references/davinci-resolve-mcp.md` (in `davinci_workflows`) | **Complete MCP setup, tool namespaces, troubleshooting** |
| `references/mcp-vlm-grading-session-2025-07-06.md` | This session's workflow discovery |
| `references/session-2025-07-05-color-grading-extraction.md` | 7 extracted tutorials (S-Log3, Apple Log 2) |
| `references/session-2025-07-06-color-correction-fundamentals.md` | Complete Linear + Gain workflow from vault fundamentals |
| `references/session-2025-07-06-dark-blue-cinematic-workflow.md` | Dark blue cinematic landscape with selective masks (Layer Mixer) |
| `references/session-2025-07-07-power-masking-loris-marie.md` | Power Masking technique capture (this session) |

---

## Verification Protocol
Always verify grading results using:
- Vectorscope for skin tone compliance
- Waveform for exposure consistency
- Parade for color channel balance
- Program monitor for natural skin appearance

**Final Check:** Play back graded footage and verify it looks natural while achieving desired creative intent.