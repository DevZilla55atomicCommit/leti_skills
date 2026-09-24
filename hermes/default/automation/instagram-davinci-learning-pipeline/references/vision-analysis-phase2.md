# Phase 2: Vision Analysis Pipeline — Reference Document

> **Session:** 2026-07-21 (current)
> **Context:** Processing 1,156 pre-extracted videos through vision analysis to build DaVinci Resolve technique knowledge base
> **Rate Limit:** 20 RPM (vision_analyze tool) — **HARD LIMIT**

---

## Phase 2 Collections & Video Counts

| Sub-phase | Collection | Videos | Est. Vision Calls (5/vid) | Status |
|-----------|------------|--------|---------------------------|--------|
| **2a** | Color Grading | 336 | 1,680 | 🔄 In Progress (8 done) |
| **2b** | DaVinci Tricks | 224 | 1,120 | ⏳ Pending |
| **2c** | Cinematic | 156 | 780 | ⏳ Pending |
| **2d** | Drone | 114 | 570 | ⏳ Pending |
| **2e** | Gimbal Moves | 474 | 2,370 | ⏳ Pending |
| **2f** | Ideas for Shooting | 796 | 3,980 | ⏳ Pending |
| **2g** | Other DaVinci | ~30 | ~150 | ⏳ Pending |
| **TOTAL** | | **2,130** | **~10,650** | |

---

## Rate Limiting Protocol (CRITICAL)

### Vision API: 20 RPM Maximum
- **Hard limit** enforced by provider
- Minimum **3 seconds between vision_analyze calls**
- If 429 received: exponential backoff
  - 30s → 60s → 120s → 240s → 480s
- **Do NOT batch vision calls** — each counts individually against RPM
- Terminal/file operations can be batched freely; only vision_analyze is rate-limited

### Implementation Pattern
```python
# Pseudocode for rate-limited vision calls
import time

MIN_INTERVAL = 3.0  # seconds between calls (20 RPM)
last_call = 0

def rate_limited_vision_analyze(image_url, question):
    global last_call
    elapsed = time.time() - last_call
    if elapsed < MIN_INTERVAL:
        time.sleep(MIN_INTERVAL - elapsed)
    result = vision_analyze(image_url, question)
    last_call = time.time()
    return result
```

---

## Frame Sampling Strategy

### Key Frames Per Video (Max 5)
| Frame | Purpose |
|-------|---------|
| `frame_0001.jpg` | Opening/title — identifies technique, page, context |
| `frame_0020.jpg` | Early demo — tools/nodes being introduced |
| `frame_0050.jpg` | Core technique — main workflow being shown |
| `frame_0080.jpg` | Parameters/settings — specific values visible |
| `frame_last.jpg` | Result/comparison — before/after or final look |

### Skip Heuristics (detected via vision)
- **Talking head frames** — person on camera, no UI
- **Title/transition frames** — large text overlay, no Resolve UI
- **Duplicate frames** — visually identical to previous sample
- **Outro/CTA frames** — "follow me", "save this", social handles

---

## Vision Analysis Prompt Template

```python
VISION_PROMPT = """
Analyze this frame from a DaVinci Resolve tutorial. Identify:
1. What Resolve page is shown? (Edit, Color, Fusion, Fairlight, Deliver, Cut)
2. What specific tools/nodes/effects are visible? (Node graph, Color Wheels, Curves, Power Windows, Magic Mask, OFX plugins, etc.)
3. What technique is being demonstrated? (Be specific: "Serial Node LUT Application", "Power Window Sky Replacement", "RGB Mixer White Balance", etc.)
4. Any visible settings/parameters? (Numbers, slider positions, dropdown selections)
5. Segment type: DEMO (live action), EXPLANATION (teaching), RESULT (before/after), TITLE/INTRO, OUTRO

Return structured JSON with these 5 fields.
"""
```

---

## Output Structure

### Analysis JSON per Video
```json
{
  "video_id": "DanLIz8OPqK",
  "collection": "Color_grading",
  "frames_analyzed": 5,
  "frame_analyses": [
    {
      "frame": "frame_0001.jpg",
      "page": "Color",
      "tools": ["Color Wheels (Offset)", "Waveform Scope"],
      "technique": "Global Color Balance via Offset Wheel",
      "parameters": {"Offset": "0.435", "RGB": "25.00 each"},
      "segment": "EXPLANATION"
    }
  ],
  "synthesized_technique": {
    "name": "Global Offset Color Balance",
    "page": "Color",
    "node_structure": "Single Serial Node → Offset Wheel",
    "key_parameters": {"Offset": "0.435"},
    "use_case": "Overall image tint/warmth adjustment"
  }
}
```

### Aggregated Output Location
```
/Volumes/Samsung LED/Instagram Downloads/New Untouched Reels Download/
├── CONTENT_PROCESSING/
│   └── vision_analysis/          # NEW
│       ├── Color_grading/
│       ├── DaVinci_Tricks/
│       ├── Cinematic/
│       ├── Drone/
│       ├── Gimbal_Moves/
│       ├── Ideas_for_Shooting/
│       └── Other_DaVinci/
```

---

## Technique Classification Keywords (for auto-clustering)

### Color Page
| Keywords | Technique Cluster |
|----------|-------------------|
| "LUT", "Film Look", "Kodak 2383", "Film Emulation" | LUT Application & Film Emulation |
| "Power Window", "Mask", "Qualifier", "HSL", "Tracker" | Masking & Isolation |
| "Curves", "RGB Mixer", "Hue vs Sat", "Hue vs Hue", "Hue vs Lum" | Curve-Based Grading |
| "Noise Reduction", "Temporal NR", "Spatial NR" | Noise Reduction |
| "Magic Mask", "Person Mask", "Face Refinement" | AI Magic Mask |
| "Split Tone", "Shadow Tint", "Highlight Tint" | Split Toning |
| "Gamut Mapping", "CST", "Color Space Transform" | Color Management |

### Edit Page
| Keywords | Technique Cluster |
|----------|-------------------|
| "Render in Place", "Optimized Media", "Proxy" | Performance Optimization |
| "Speed Ramp", "Retime", "Optical Flow" | Retime & Speed Effects |
| "Transition", "Edge Wipe", "Push", "Cross Dissolve" | Transitions |
| "Multicam", "Sync" | Multicam Editing |

### Fusion Page
| Keywords | Technique Cluster |
|----------|-------------------|
| "Tracker", "Planar Tracker", "Camera Tracker" | Tracking |
| "Merge", "Transform", "Blur", "Glow" | Compositing |
| "Text+", "Title", "Fusion Title" | Motion Graphics |

---

## Progress Tracking

### Checkpoint File
```json
{
  "phase": "2a",
  "collection": "Color_grading",
  "completed_videos": ["DanLIz8OPqK", "DZBC2GIMCpC", ...],
  "failed_videos": [],
  "total_vision_calls": 40,
  "last_call_timestamp": "2026-07-21T...",
  "next_video_index": 8
}
```

### Resume Protocol
1. Load checkpoint
2. Skip completed_videos
3. Continue from next_video_index
4. Append results atomically

---

## Integration with Phase 3 (Skill Authoring)

After Phase 2 complete per collection:
1. Cluster `synthesized_technique` entries by name/page/parameters
2. For each cluster with ≥2 videos:
   - Generate Hermes SKILL.md using `templates/skill_template.md`
   - Include: technique name, Resolve page, node graph description, key parameters, GIF references, transcript excerpts
   - Install to `~/.hermes/skills/creative/davinci-resolve/`
3. Create vault index note linking skills, GIFs, source reels

---

## Storage Notes

- **Samsung LED SSD**: Primary (70GB free) — vision analysis JSONs, skills
- **PNY128GB**: Emergency overflow — raw frames if needed
- **Frame directories**: Already exist from Phase 1 (1,156 videos × 1fps frames)
- **GIFs**: Already exist from Phase 1 (2,312 full-duration GIFs, 45.9 GB)

---

## Troubleshooting

| Issue | Resolution |
|-------|------------|
| 429 Too Many Requests | Wait full backoff; reduce to 15 RPM if persistent |
| Vision returns "talking head" | Mark frame as skip; try next key frame |
| Frame file missing | Video had < N frames; use available frames only |
| Analysis JSON write fails | Check disk space; fallback to PNY128GB |
| Session interrupted | Load checkpoint; resume from next_video_index |