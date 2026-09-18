# Video Effects Pipeline — Extension Reference

> **Added:** 2025-07-15 | **Session:** First video effects URL processing (@art3.studi0 Pro Cut Out Transition)

---

## 🎯 Overview

This document extends the main `instagram-davinci-learning-pipeline` skill to support **Video Effects** (transitions, compositing, motion graphics, VFX, text effects, stylization, time effects) as a new domain alongside Color Grading.

The pipeline architecture is identical — only the classification categories, vault paths, and skill prefixes differ.

---

## 📁 Vault Structure (Video Effects)

```
/Users/alfredkamisese/TamaZila Obsidian Vault/Hermes Agent/DaVinci_Knowledge_Base/Video_Effects/
├── 00-MASTER-INDEX.md                    # Category TOC + navigation
├── TEMPLATE-Video-Effect.md              # Template for new effects
├── VIDEO_EFFECTS_QUEUE.md                # Processing queue tracking
├── VIDEO_EFFECTS_PIPELINE_PLAN.md        # Full pipeline architecture
├── IMPLEMENTATION_HANDOFFS.md            # Step-by-step task breakdown
├── VIDEO_EFFECTS_Exports/                # JSON/CSV/HTML exports
│   ├── video_effects_export.json
│   ├── video_effects_export.csv
│   ├── ARCHITECTURE_DIAGRAM.md           # Mermaid diagram
│   └── ARCHITECTURE_DIAGRAM_INTERACTIVE.html
├── assets/                               # Visual assets (GIFs, screenshots)
│   ├── transitions/
│   ├── compositing/
│   ├── motion-graphics/
│   ├── vfx/
│   ├── text-effects/
│   ├── stylization/
│   └── time-effects/
├── transitions/
│   ├── 00-MASTER-INDEX.md
│   └── NN-Effect_Name_Source_Tools.md
├── compositing/
├── motion-graphics/
├── vfx/
├── text-effects/
├── stylization/
└── time-effects/
```

---

## 🎬 Effect Classification System

| Category | Keywords | Folder |
|----------|----------|--------|
| **Transitions** | cut out, whip pan, match cut, morph, dissolve, wipe, slide, push, iris | `transitions/` |
| **Compositing** | green screen, rotoscope, matte, keying, alpha, chroma key, luma key | `compositing/` |
| **Motion Graphics** | lower third, kinetic type, title, lowerthird | `motion-graphics/` |
| **VFX** | particles, explosion, fire, smoke, sci-fi | `vfx/` |
| **Text Effects** | kinetic type, 3D text, callout, subtitle style | `text-effects/` |
| **Stylization** | glitch, VHS, film damage, halation, film burn | `stylization/` |
| **Time Effects** | speed ramp, time remap, freeze frame, slo-mo | `time-effects/` |

---

## 🖼️ Visual Asset Capture Strategy (Key Differentiator)

For **each effect**, capture:

| Asset | Description | Tool |
|-------|-------------|------|
| **Effect Demo GIF** | 2-3 sec looping GIF of effect in action | `ffmpeg` from video frames |
| **Node Graph Screenshot** | DaVinci node graph / Fusion flow | Manual or screen capture |
| **Parameter Panels** | Key settings visible | Browser vision / DaVinci |
| **Key Frames (3-5)** | Before, during, after | Browser vision / frame extraction |
| **Before/After Comparison** | Side-by-side frame | Compose from key frames |

**Storage:** `Video_Effects/assets/{category}/{effect-slug}/`

---

## 🔧 Pipeline Steps Detail

### Step 1: Parse & Deduplicate
```bash
# Input formats: RTF, CSV, JSON, TXT
# Extract: URL, Creator, Context, Priority
# Dedupe by: Reel short code (e.g., DaxUaKYuhb0)
```

### Step 2: Availability Check (reuse existing skill)
- Use `instagram-reel-availability-check` skill
- Navigate to URL → snapshot → check for:
  - ✅ Video element present
  - ❌ Login wall / "Sign up" modal
  - ❌ Age restriction
  - ❌ "Content unavailable" / "Page not found"

### Step 3: Content Extraction
| Tool | Purpose |
|------|---------|
| `browser_navigate` | Load reel page |
| `browser_vision` | Analyze video effect visually |
| `browser_snapshot` | Extract caption, hashtags, comments |
| `browser_get_images` | Get thumbnail/video frame URLs |
| `browser_console` | Execute JS to capture video frames |

**Critical:** Handle Instagram login wall — use authenticated session (cookies) or embed API.

### Step 4: Effect Classification
Auto-classify based on:
- **Caption keywords** (transition, composite, VFX, etc.)
- **Visual analysis** (what the effect actually does)
- **Hashtags** (#transition, #vfx, #motiongraphics, etc.)

### Step 5: Visual Asset Capture (KEY DIFFERENTIATOR)
For each effect, capture:
1. **Effect Demo GIF** — 2-3 sec loop from reel
2. **Key Frames** — Before / During / After screenshots
3. **Node Graph Screenshot** — DaVinci node graph/Fusion flow
4. **Parameter Panels** — Key settings visible
5. **Before/After Comparison** — Side-by-side frame

### Step 6: Skill Generation
Create Hermes skill at:
```
~/.hermes/skills/video-effects/davinci-resolve-{effect-slug}/
├── SKILL.md              # Full skill with frontmatter
├── assets/               # GIFs, screenshots bundled
│   ├── demo.gif
│   ├── node-graph.png
│   ├── params-01.png
│   └── before-after.png
└── references/           # Source URL, creator info
```

### Step 7: Vault Note Creation
Create detailed markdown at:
```
Video_Effects/{category}/NN-Effect_Name_Source_Tools.md
```
Using `templates/vault_note_template_video_effect.md`

### Step 8: Queue Management
Update `VIDEO_EFFECTS_QUEUE.md` with status:
| # | URL | Creator | Effect | Category | Status | Vault File |

### Step 9: Export Regeneration
- `video_effects_export.json`
- `video_effects_export.csv`
- `ARCHITECTURE_DIAGRAM.md` (Mermaid)
- `ARCHITECTURE_DIAGRAM_INTERACTIVE.html`

---

## 🎬 Test Case: First URL Processing

**URL:** `https://www.instagram.com/reel/DaxUaKYuhb0/`
**Creator:** @art3.studi0
**Caption:** "Pro Cut Out Transition⚡"
**Hashtags:** #videoediting #transition #davinciresolve #tutorial #effects

**Classification:**
- **Category:** Transitions
- **Effect Type:** Cut Out / Mask Transition
- **Tools:** Power Window + Tracking + Keyframes + Alpha Composite
- **DaVinci Page:** Color (Power Window) + Fusion (Composite)

**Assets Captured:**
1. **GIF** — Cut out transition loop (2-3 sec)
2. **Key Frames** — Before cut, during wipe, after reveal
3. **Node Graph** — Power Window → Tracker → Keyframes → Alpha Output
4. **Parameter Panels** — Tracker settings, Keyframe curves, Alpha Output

**Vault Path:** `Video_Effects/transitions/01-Pro-Cut-Out-Transition_Art3Studi0_Cut-Out-Mask.md`

---

## 🔧 Technical Requirements

### Browser Automation
- Handle Instagram login wall (may need cookies/session)
- Video frame extraction via `browser_console` + canvas
- GIF generation via `ffmpeg` (terminal)

### DaVinci Resolve Integration (for node graphs)
- Use `mcp__davinci_resolve__fusion_comp` to recreate node graphs
- Use `mcp__davinci_resolve__graph` for color page nodes
- Screenshot via Fusion/Color page

### Visual Asset Pipeline
```bash
# Extract frames from video
ffmpeg -i input.mp4 -vf "fps=10,scale=720:-1" frame_%03d.png

# Create GIF
ffmpeg -i input.mp4 -vf "fps=10,scale=720:-1:flags=lanczos" -loop 0 output.gif

# Optimize
gifsicle -O3 --lossy=80 output.gif -o output_opt.gif
```

---

## 🎯 Success Criteria

| Metric | Target |
|--------|--------|
| URL → Vault Note time | < 10 min per effect |
| Visual assets per effect | ≥ 1 GIF + 3 screenshots |
| Classification accuracy | > 90% |
| Skill generation | 100% valid SKILL.md |
| Vault note completeness | All template sections filled |

---

## 🔗 Integration Points

| Component | Integration |
|-----------|-------------|
| `instagram-reel-availability-check` | Step 2 — reuse |
| `instagram-unavailable-content-handling` | Log failed reels |
| `regenerate_exports_and_diagram` | Step 9 — adapt for effects |
| `davinci-resolve` MCP | Recreate node graphs, capture screenshots |
| Existing Color Grading pipeline | Shared queue format, shared vault conventions |

---

## 📝 Notes & Considerations

1. **Login Wall:** Instagram increasingly requires auth. Options:
   - Use authenticated browser session (cookies)
   - Alternative: Instagram embed API / oEmbed
   - Fallback: Manual capture + automated processing

2. **Visual Analysis:** Vision model can identify effect type from video frames but cannot see DaVinci UI inside reel (reel shows RESULT, not process). Need to infer technique from result + caption.

3. **GIF Creation:** Requires `ffmpeg` + `gifsicle` installed. Add to setup.

4. **Skill Naming:** `davinci-resolve-{effect-slug}` convention (e.g., `davinci-resolve-cut-out-transition`)

5. **Cross-Reference:** Link to existing color grading skills where techniques overlap (Power Windows, Tracking, Keyframes)

---

*Part of the **DaVinci Knowledge Base automation suite** — Video Effects extension*