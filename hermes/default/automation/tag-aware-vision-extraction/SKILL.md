---
name: tag-aware-vision-extraction
description: |
  Class-level skill for extracting structured technique knowledge from video frames using category-specific vision prompts. Each video category (transitions, color grading, lighting, etc.) requires a different extraction schema - this skill codifies the prompts, frame sampling, rate limiting, and output structure for reliable extraction.
version: 1.0.0
category: automation
tags:
  - vision-analysis
  - instagram-reels
  - davinci-resolve
  - tag-aware-extraction
  - structured-extraction
metadata:
  hermes:
    tags: [vision-analysis, instagram-reels, davinci-resolve, tag-aware-extraction, structured-extraction]
---

# Tag-Aware Vision Extraction

> **Class-level skill** for extracting structured technique knowledge from video frames using category-specific vision prompts. Each video category (transitions, color grading, lighting, etc.) requires a different extraction schema — this skill codifies the prompts, frame sampling, rate limiting, and output structure for reliable extraction.

---

## 🎯 What This Does

```text
Video Frames + Category Tag
        │
        ▼
┌─────────────────────────────────────────────────────────────────┐
│  TAG-AWARE VISION EXTRACTION PIPELINE                           │
├─────────────────────────────────────────────────────────────────┤
│  1. Parse category tag → Select extraction schema               │
│  2. Sample 5 key frames (start, 20%, 50%, 80%, end)             │
│  3. Rate-limited vision analysis (20 RPM → 3s min interval)     │
│  4. Category-specific prompt → Structured JSON extraction       │
│  5. Merge frame results → Synthesized technique record          │
│  6. Output: Vault note + Hermes skill + Asset copying           │
└─────────────────────────────────────────────────────────────────┘
        │
        ▼
Structured Knowledge Base + Interactive Skills
```

---

## 📥 Supported Categories & Extraction Schemas

### Video Effects (DaVinci Resolve)

| Category | Keywords | Extraction Focus |
|----------|----------|------------------|
| **transitions** | transition, cut, wipe, dissolve, morph, match cut, whip pan, speed ramp, zoom transition, pan zoom, smooth cut | Transition type, duration, easing curve, Fusion setup, keyframe structure, color handling, audio crossfade |
| **color_grading** | color grade, lut, cst, color space, power grade, node tree, power window, qualifier, hue vs hue, lift gamma gain, primaries, log wheels, film emulation, teal orange, split tone, halation, film grain | Node tree, CST/LUT chain, Power Windows, curves (Hue vs Hue, Hue vs Sat, Lum vs Sat), wheel settings, film effects, output transform |
| **fusion_compositing** | fusion, composite, keying, rotoscope, mask, tracker, planar tracker, camera tracker, 3d, particle, paint, clone, wire removal, sky replacement, green screen, blue screen, delta keyer, ultra keyer | Node graph, keying workflow (Delta/Ultra/Primatte), tracking setup (Planar/Camera/Point), masking/roto (Bezier/B-Spline), 3D setup, particle systems, paint/clone tools |
| **motion_graphics** | motion graphics, mograph, text animation, kinetic type, lower third, title, template, expression, macro, data-driven, csv, json | Text+ template structure, keyframe animation, expressions/scripts (Lua/Python), modifier chains, publish controls, data-driven setup |
| **vfx** | vfx, visual effect, explosion, fire, smoke, magic, energy, portal, particle, simulation, fluid, cloth, destruction, bullet hit, muzzle flash, blood, wound | Effect type, particle setup (pEmitter, forces, collision), simulation settings, shader/material setup, compositing over plate, render settings |
| **camera_techniques** | camera move, dolly, slider, gimbal, drone, handheld, steadicam, crane, jib, orbital, push in, pull out, tracking shot, reveal, transition move | Movement type, rig/equipment, speed/acceleration, stabilization method, lens info, DaVinci post-stabilization |
| **lighting** | lighting, light setup, key light, fill light, rim light, backlight, softbox, fresnel, led panel, hmi, golden hour, blue hour, natural light, three point, rembrandt, butterfly, split, loop, ratio, contrast | Setup type, light positions/modifiers, ratios, color temps, modifiers (flags/nets/diffusion/bounce), golden/blue hour specifics, DaVinci relighting |
| **composition** | composition, framing, rule of thirds, leading lines, foreground, depth, layers, negative space, symmetry, golden ratio, centered, wide angle, telephoto compression, anamorphic, aspect ratio | Composition rule/technique, lens choice (focal length, aperture), subject placement, depth creation (fg/mg/bg), aspect ratio, camera angle, DaVinci reframe |
| **audio_sound** | audio, sound, music, sound design, foley, voiceover, dialogue, sync, noise reduction, eq, compression, reverb, mastering, soundtrack, sfx, ambience | Technique (noise reduction, EQ, compression, reverb, sync, mixing), Fairlight tools, plugin settings, music layering, dialogue processing, sound design, delivery specs |
| **editing_workflow** | edit, cut, pace, rhythm, j cut, l cut, match cut, smash cut, jump cut, montage, b-roll, coverage, multicam, sync, marker, timeline, ripple, roll, slip, slide | Edit technique (J/L cut, match cut, jump cut, montage), pacing/rhythm, timeline org, multicam setup, trim tools, speed changes, automation |

### Photography / Videography

| Category | Keywords | Extraction Focus |
|----------|----------|------------------|
| **portrait** | portrait, headshot, beauty, fashion, model, posing, expression, eye contact, catchlight, skin retouching, frequency separation, dodge burn | Lighting setup, lens choice, posing direction, camera settings, retouching workflow, color grading for skin |
| **landscape** | landscape, nature, mountains, ocean, sunrise, sunset, golden hour, blue hour, long exposure, nd filter, polarizer, graduated nd, focus stacking, panorama, hyperfocal | Composition, light conditions, lens/focal length, exposure technique, focus technique, post-processing, gear |
| **commercial_product** | product, commercial, advertising, still life, jewelry, watch, cosmetics, food, beverage, splash, high speed, macro, focus stacking, light tent, gradient background | Product staging, lighting setup, camera/lens, background/surface, special techniques, post-processing, deliverables |
| **street_documentary** | street, documentary, candid, storytelling, decisive moment, zone focusing, prime lens, 35mm, 50mm, 28mm, black white, high contrast, grain, zone system | Focus approach, lens choice, composition in chaos, ethics/legal, B&W vs color, post-processing, storytelling |
| **lighting_technique** | lighting, strobe, flash, speedlight, continuous, led, softbox, octabox, beauty dish, grid, snoot, gel, cto, ctb, high speed sync, rear curtain, dragging shutter | Light source type, modifier, position, power settings, ratios, color gels, sync method, DaVinci relighting |

---

## 🔧 Extraction Protocol

### Frame Sampling (Max 5 per Video)
| Frame | Purpose | Heuristic |
|-------|---------|-----------|
| `frame_0001.jpg` | Opening/title — identifies technique, page, context | First frame |
| `frame_0020.jpg` | Early demo — tools/nodes being introduced | ~20% |
| `frame_0050.jpg` | Core technique — main workflow being shown | ~50% |
| `frame_0080.jpg` | Parameters/settings — specific values visible | ~80% |
| `frame_last.jpg` | Result/comparison — before/after or final look | Last frame |

### Skip Heuristics (Detected via Vision)
- **Talking head frames** — person on camera, no UI
- **Title/transition frames** — large text overlay, no Resolve UI
- **Duplicate frames** — visually identical to previous sample
- **Outro/CTA frames** — "follow me", "save this", social handles

---

### Rate Limiting Protocol (CRITICAL)

### Vision API: 20 RPM Maximum (Cloud)
- **Hard limit** enforced by provider
- **Minimum 3 seconds between vision_analyze calls**
- If 429 received: exponential backoff
  - 30s → 60s → 120s → 240s → 480s
- **Do NOT batch vision calls** — each counts individually against RPM
- Terminal/file operations can batch freely; only vision_analyze is rate-limited

### Local Vision Model (Ollama) — No Rate Limits
- **Use when cloud rate limits block progress** (as of 2026-07-27 session)
- Model: `llava:7b` (4.7GB, fits M4 16GB with headroom)
- Pull: `ollama pull llava:7b`
- Call via subprocess (not `vision_analyze` tool):

### NVIDIA vision_analyze Tool — PRIMARY VIABLE METHOD (2026-07-30)

The Hermes `vision_analyze` tool using NVIDIA's `google/diffusiongemma` (or `gemini-2.5-flash`) is the **only reliable vision method** on 16GB Mac Mini M4.

#### Configuration

```yaml
# ~/.hermes/config.yaml
vision:
  provider: nvidia
  model: google/diffusiongemma-26b-a4b-it  # or gemini-2.5-flash
```

#### Usage Pattern (Sequential in Main Agent)

```python
# Main agent loop - works because vision_analyze is native Hermes tool
for item in pending_items:
    result = vision_analyze(
        image_url=item['frame_path'],
        question=VISION_PROMPT.format(**item)
    )
    parse_and_store_result(result)
    time.sleep(3.2)  # 20 RPM limit
```

**DO NOT** use sub-agents for vision analysis — `vision_analyze` tool ONLY works in Hermes agent context.

#### Performance Metrics (2026-07-29 Extended - 564 frames complete)

| Metric | Value |
|--------|-------|
| Total analyzed this session | 54 frames |
| Latency per frame | 3-5s (avg ~4s) |
| Rate limit | 20 RPM enforced via 3.2s sleep |
| Success rate | ~95% (5% non-Resolve marked error) |
| Non-Resolve content rate | ~11% (133/1146) |
| JSON parsing | Clean native output, no markdown stripping needed |
| Session throughput | ~15 frames/hour (manual sequential) |

#### Non-DaVinci Content Handling (Confirmed Pattern)

When vision analysis returns content without DaVinci Resolve techniques:
1. **Mark status = "error"** in VISION_PROGRESS.json with reason: "Non-Resolve content (gimbal tutorial / lens comparison / pure cinematography)"
2. **Skip skill generation** — no Hermes skill created
3. **Skip vault update** — no Obsidian note created
4. **Error count**: 133 videos (11.6% of 1146) as of 2026-07-29

Examples from this session:
- `CxbBIniIbV_` — "2 easy gimbal moves" tutorial (pure camera technique)
- `C4aFM7DNW01` — Shopping cart / POV diagram (not Resolve)
- `C4Hm6kYvoMr` (first analysis) — Behind-the-scenes gimbal shot (no Resolve technique shown)

#### Non-Resolve Skills Created (2026-07-30)

Rather than skipping non-Resolve content entirely, created dedicated skill categories:

**Cinematography Techniques** (`~/.hermes/skills/cinematography-techniques/`):
- `gimbal-movement-basics.md` — 7 core movements, stabilization best practices
- `camera-movement-transitions.md` — Whip pan, match cut, invisible cut, drone transitions

**Photography Techniques** (`~/.hermes/skills/photography-techniques/`):
- `architectural-photography-lighting.md` — Natural/artificial light, HDR, composition
- `lens-selection-cinematic-look.md` — Focal length effects, sensor crop, aperture choices
- `gimbal-camera-movements.md` — 7 core movements, composite moves, Resolve post-stabilization
- `split-screen-comparison-technique.md` — Edit/Fusion methods, layouts, sync/alignment
- `color-grading-theory-fundamentals.md` — Scopes, primary/secondary, creative looks, LUTs, HDR
- `motion-graphics-fundamentals-fusion.md` — Text animation, keyframing, tracking, particles, 3D, macros

**Camera Hardware** (`~/.hermes/skills/camera-hardware/`):
- `camera-gear-workflow.md` — Sensor formats, codecs, log profiles, lens mounts, accessories, media management

---

### Local Vision Worker (Background Process) — Production Protocol
**Deployed 2026-07-27** — Replaces cloud `vision_analyze` calls entirely for bulk processing.
```python
import subprocess, json, time

def analyze_frame_local(frame_path: str, video_id: str) -> dict:
    prompt = f"""Analyze this DaVinci Resolve technique from Instagram Reel {video_id}.

Return ONLY this exact JSON structure (no extra text, no markdown):
{{
  "technique_name": "Descriptive name",
  "resolve_page": "Color|Edit|Fusion|Fairlight",
  "node_graph_type": "serial|parallel|layer_mixer|compound",
  "key_nodes": ["node1", "node2"],
  "parameters": {{"param1": "value1"}},
  "steps_to_reproduce": ["step1", "step2"],
  "difficulty": "beginner|intermediate|advanced",
  "tags": ["tag1", "tag2"]
}}"""
   
    result = subprocess.run([
        'ollama', 'run', 'llava:7b', prompt, frame_path
    ], capture_output=True, text=True, timeout=180)
   
    if result.returncode != 0:
        raise Exception(f"Ollama error: {result.stderr[:200]}")
   
    return extract_json_from_llava(result.stdout)

def extract_json_from_llava(text: str) -> dict:
    """Extract JSON from llava response - handles markdown code blocks, nested braces."""
    import re
   
    # 1. Try markdown code blocks first
    for pattern in [r'```json\s*(\{.*?\})\s*```', r'```\s*(\{.*?\})\s*```']:
        matches = re.findall(pattern, text, re.DOTALL)
        for match in matches:
            try:
                return json.loads(match.strip())
            except json.JSONDecodeError:
                continue
   
    # 2. Try balanced brace extraction
    try:
        start = text.index('{')
        depth = 0
        for i, ch in enumerate(text[start:], start):
            if ch == '{':
                depth += 1
            elif ch == '}':
                depth -= 1
                if depth == 0:
                    return json.loads(text[start:i+1])
    except (ValueError, json.JSONDecodeError):
        pass
   
    # 3. Fallback: regex for complete JSON object
    matches = re.findall(r'(\{.*?\})', text, re.DOTALL)
    for match in matches:
        try:
            return json.loads(match.strip())
        except json.JSONDecodeError:
            continue
   
    raise ValueError(f"No valid JSON found in: {text[:300]}")
```

### Local Vision Worker (Background Process) — Production Protocol
**Deployed 2026-07-27** — Replaces cloud `vision_analyze` calls entirely for bulk processing.

#### Architecture
```
VISION_PROGRESS.json (shared state file)
         │
         ▼
┌─────────────────────────────────────────────┐
│  Local Vision Worker (Python script)        │
│  - Polls VISION_PROGRESS.json for "pending" │
│  - File-locked read/write (fcntl)           │
│  - Processes 5 frames/batch with 2 workers  │
│  - Calls ollama run llava:7b per frame      │
│  - Atomic JSON writes with .tmp rename      │
└─────────────────────────────────────────────┘
         │
         ▼
Progress file updated with "complete" + extracted technique JSON
```

#### VISION_PROGRESS.json Schema
```json
[
  {
    "video_id": "C-FvSX-piqT",
    "collection": "DaVinci_Core",
    "frame_to_analyze": "/Volumes/Samsung LED/Instagram Downloads/New Untouched Reels Download/CONTENT_PROCESSING/frames/C-FvSX-piqT/frame_0001.jpg",
    "status": "pending|complete|error",
    "result": {
      "technique_name": "Dynamic Speed Ramping with Curve Smoothing",
      "resolve_page": "Edit",
      "node_graph_type": "serial",
      "key_nodes": ["Retime Curve", "Transform"],
      "parameters": {"curve_type": "bezier", "easing": "ease_in_out"},
      "steps_to_reproduce": [
        "Add Retime Curve to clip",
        "Set keyframes at speed change points",
        "Adjust Bezier handles for smooth easing"
      ],
      "difficulty": "intermediate",
      "tags": ["speed-ramp", "retime", "curve", "edit-page"]
    },
    "error": null,
    "updated_at": "2026-07-27T16:45:00Z"
  }
]
```

#### Worker Script: `scripts/local_vision_worker.py`
```python
#!/usr/bin/env python3
"""
Local Vision Worker - Background process for llava:7b frame analysis.
Monitors VISION_PROGRESS.json, processes pending frames, updates atomically.
"""

import json, fcntl, time, subprocess, os
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

VISION_PROGRESS = Path("/Volumes/Samsung LED/Instagram Downloads/New Untouched Reels Download/CONTENT_PROCESSING/VISION_PROGRESS.json")
BATCH_SIZE = 5
MAX_WORKERS = 2
MODEL = "llava:7b"
TIMEOUT = 180

def extract_json(text):
    # (same extract_json_from_llava as above)

def analyze_frame(frame_path, video_id):
    prompt = f"""Analyze this DaVinci Resolve technique from Instagram Reel {video_id}.
Return ONLY valid JSON: {{"technique_name":"...","resolve_page":"Color|Edit|Fusion|Fairlight","node_graph_type":"serial|parallel|layer_mixer|compound","key_nodes":["..."],"parameters":{{}},"steps_to_reproduce":["..."],"difficulty":"beginner|intermediate|advanced","tags":["..."]}}
"""
    result = subprocess.run(['ollama', 'run', MODEL, prompt, frame_path], 
                           capture_output=True, text=True, timeout=TIMEOUT)
    if result.returncode != 0:
        raise Exception(f"Ollama {result.returncode}: {result.stderr[:200]}")
    return extract_json(result.stdout)

def process_batch(entries):
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
        futures = {ex.submit(analyze_frame, e['frame_to_analyze'], e['video_id']): e for e in entries}
        for fut in as_completed(futures):
            entry = futures[fut]
            try:
                entry['result'] = fut.result()
                entry['status'] = 'complete'
            except Exception as e:
                entry['status'] = 'error'
                entry['error'] = str(e)[:500]
            entry['updated_at'] = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    return entries

def main():
    print(f"[{time.strftime('%H:%M:%S')}] Local Vision Worker started ({MAX_WORKERS} workers, {MODEL})")
    while True:
        # File-locked read
        with open(VISION_PROGRESS, 'r') as f:
            fcntl.flock(f.fileno(), fcntl.LOCK_SH)
            progress = json.load(f)
            fcntl.flock(f.fileno(), fcntl.LOCK_UN)
       
        pending = [e for e in progress if e.get('status') == 'pending' and e.get('frame_to_analyze') and Path(e['frame_to_analyze']).exists()]
        if not pending:
            print("All pending frames processed.")
            break
       
        batch = pending[:BATCH_SIZE]
        print(f"Processing batch of {len(batch)}...")
        updated = process_batch(batch)
       
        # File-locked atomic write
        with open(VISION_PROGRESS, 'r+') as f:
            fcntl.flock(f.fileno(), fcntl.LOCK_EX)
            current = json.load(f)
            # Merge updates by video_id
            updates = {e['video_id']: e for e in updated}
            for e in current:
                if e['video_id'] in updates:
                    e.update(updates[e['video_id']])
            f.seek(0)
            f.truncate()
            json.dump(current, f, indent=2)
            fcntl.flock(f.fileno(), fcntl.LOCK_UN)
       
        complete = sum(1 for e in progress if e.get('status') == 'complete')
        pending_count = sum(1 for e in progress if e.get('status') == 'pending')
        print(f"Progress: {complete} complete, {pending_count} pending")
        time.sleep(1)

if __name__ == "__main__":
    main()
```

#### Launch & Monitor
```bash
# Start worker (runs in background, no rate limits)
nohup python scripts/local_vision_worker.py > vision_worker.log 2>&1 &

# Monitor progress
watch -n 10 'python -c "
import json
with open(\"VISION_PROGRESS.json\") as f: d=json.load(f)
c=sum(1 for x in d if x.get(\"status\")==\"complete\")
p=sum(1 for x in d if x.get(\"status\")==\"pending\")
e=sum(1 for x in d if x.get(\"status\")==\"error\")
print(f\"Complete: {c}, Pending: {p}, Errors: {e}\")
"'

# Check worker log
tail -f vision_worker.log
```

#### Performance (2026-07-27 Session)
| Metric | Value |
|--------|-------|
| Model | llava:7b (4.7GB) |
| Frame time | ~15-20s per frame |
| Batch (5 frames, 2 workers) | ~45-60s |
| Throughput | ~80-100 frames/hour |
| 1165 frames | ~12-15 hours |
| RAM usage | ~6GB (model + 2 workers) |
| Rate limits | **None** (local) |

#### Results (2026-07-27)
- **VISION_PROGRESS.json**: 1165 entries created from frame extraction
- **Worker started**: Background process processing ~5 frames/batch
- **Progress as of session end**: 181/1165 complete (~15%)
- **Quality**: Structured JSON extraction working; llava:7b returns proper technique names, node graphs, parameters, steps
- **Next**: Let worker run overnight; resume with `python scripts/local_vision_worker.py` (resumes from pending)

#### Critical Fixes Applied
1. **JSON extraction from markdown**: llava:7b wraps JSON in ```json ``` blocks — must parse before json.loads
2. **Frame mapping**: VISION_PROGRESS.json uses `frame_to_analyze` field (not `frames_analyzed[0]`)
3. **File locking**: fcntl prevents corruption from concurrent reads/writes
4. **Atomic writes**: Write to `.tmp` then rename, or seek/truncate in-place with lock
5. **Resume capability**: Worker reads current state, only processes `status: pending`
6. **Error handling**: Failed frames marked `error` with message; don't block batch

#### Integration with Pipeline
- **Upstream**: `scripts/process_all_videos.py` creates VISION_PROGRESS.json with `frame_to_analyze` paths
- **Downstream**: `scripts/generate_skills_from_vision.py` reads complete entries, generates Hermes SKILL.md files
- **Vault**: `scripts/build_vault_from_vision.py` creates Obsidian notes with embedded GIFs and technique tables

### Dual-Mode Vision Strategy (NEW — 2026-07-28)

#### Cloud Vision (Hermes `vision_analyze` tool) — PRIMARY
| Parameter | Value |
|-----------|-------|
| Rate Limit | 20 RPM (3s minimum between calls) |
| Latency | ~3-5s/call (NVIDIA DiffusionGemma) |
| Quality | High (native vision model) |
| Use For | ALL vision analysis |
| Tool | `vision_analyze(image_url, question)` — ONLY works in Hermes agent context |

**Failure Pattern**: Subprocess wrapping `vision_analyze` fails because tool only works in Hermes agent context, not standalone Python.

#### Local Ollama (qwen3-vl:8b) — NOT VIABLE on 16GB Mac Mini M4
| Parameter | Value |
|-----------|-------|
| Rate Limit | None (local) |
| Latency | ~30-60s/call (with thinking tags) |
| Quality | Good (8B params, vision) |
| Use For | N/A — NOT VIABLE |

**TESTED & FAILED on 16GB Mac Mini M4**: qwen3-vl:8b times out at 180s+ per call; llama-server process crashes/restarts on random ports. 16GB RAM insufficient for vision model + OS + other workloads. **USE CLOUD `vision_analyze` TOOL EXCLUSIVELY**.

#### Sequential Processing Pattern (CRITICAL)
Since `vision_analyze` only works in Hermes agent context (not subprocesses), process sequentially in main agent:

```python
# Main agent loop - works because vision_analyze is native tool
for item in pending_items:
    result = vision_analyze(
        image_url=item['frame_path'],
        question=VISION_PROMPT.format(**item)
    )
    parse_and_store_result(result)
    time.sleep(3.2)  # 20 RPM limit
```

**Do NOT** use sub-agents for vision analysis — they cannot call `vision_analyze` tool.

#### Background Script Pattern (for long runs)
```bash
# Main agent runs loop, logs progress
# Background terminal shows progress
terminal(background=true, command="python3 vision_loop.py")
# Monitor via process(action="poll")
```

#### Sub-Agent Use: Text-Only Tasks Only
Sub-agents via `delegate_task` work well for:
- Skill generation from completed analyses
- Vault note generation
- Data processing without vision
- Ollama Cloud text (gemma4:31b-cloud)

#### Vision Progress File (`VISION_PROGRESS.json`)
```json
[
  {
    "video_id": "C04NeUHMGE7",
    "status": "pending|complete|error",
    "frame_to_analyze": "/Volumes/.../frames/C04NeUHMGE7/frame_0001.jpg",
    "gif_path": "/Volumes/.../gifs/C04NeUHMGE7.gif",
    "transcript": "...",
    "result": {...},
    "error": null,
    "updated_at": "2026-07-28T10:00:00"
  }
]
```

#### Frame Sampling Strategy
- Target frames: `frame_0001`, `frame_0020`, `frame_0050`, `frame_0080`, `frame_last`
- Max 5 frames/video
- Skip talking-head/title frames (detected via vision)
- ~1,680 vision calls for Color Grading collection (336 videos × 5)

#### Storage Layout
```
/Volumes/Samsung LED/Instagram Downloads/New Untouched Reels Download/
├── CONTENT_PROCESSING/
│   ├── frames/           # 1,156 video frame dirs
│   ├── gifs/             # 2,312 full-duration GIFs
│   ├── transcripts/      # 2,312 Whisper transcripts
│   └── analysis/         # 1,156 analysis JSONs
├── MASTER_INDEX_FIXED.json
└── COLLECTIONS_AND_URLS_CLEAN.md
```

#### Session Progress (2026-07-28)
| Phase | Status | Details |
|-------|--------|---------|
| Phase 1: Content Processing | ✅ Complete | 1,156/2,818 videos; frames, GIFs, transcripts, analysis |
| Phase 2a: Vision - Color Grading | 🔄 In Progress | 659 pending; local Ollama worker running (proc_95f01d68347d) |
| Phase 2b-2g | ⏳ Pending | DaVinci Tricks (224), Cinematic (156), Drone (114), Gimbal (474), Ideas (796), Other (~30) |

#### Next Steps
1. Let local Ollama worker complete 659 pending videos
2. Regenerate skills from vision results
3. Build Obsidian vault with GIFs
4. Process remaining Phase 2 collections

### Implementation Pattern (Cloud Vision)
```python
import time

MIN_INTERVAL = 3.0  # seconds (20 RPM)
last_call = 0

async def rate_limited_vision_analyze(image_url: str, prompt: str) -> dict:
    global last_call
    elapsed = time.time() - last_call
    if elapsed < MIN_INTERVAL:
        await asyncio.sleep(MIN_INTERVAL - elapsed)
    result = await vision_analyze(image_url, prompt)
    last_call = time.time()
    return result
```

### Local Vision Worker (Background Process)
```bash
# Run as background worker on Mac Mini
cd /Users/alfredkamisese && python local_vision_worker_v3.py &
# Monitors VISION_PROGRESS.json, processes pending frames
# Updates progress file atomically after each batch
```

---

## 📝 Category-Specific Prompts

### Transitions
```
Analyze this frame from a DaVinci Resolve TRANSITION tutorial. Extract:
1. Transition type (morph cut, whip pan, speed ramp, zoom, glitch, light leak, etc.)
2. Exact duration in frames/seconds
3. Easing curve (ease in/out, linear, custom Bezier)
4. Fusion setup if applicable (merge nodes, transforms, masks)
5. Keyframe structure for animation
6. Color handling during transition (color space, LUTs)
7. Audio crossfade handling
8. Whether it uses built-in transition or custom Fusion comp
Return as structured JSON.
```

### Color Grading
```
Analyze this frame from a DaVinci Resolve COLOR GRADING tutorial. Extract:
1. Complete node tree structure (serial/parallel/layer mixer)
2. Each node's purpose and key settings
3. CST/LUT chain (input/output color spaces, gamma)
4. Power Windows / Qualifier usage (shapes, tracking, feather)
5. Key curves: Hue vs Hue, Hue vs Sat, Hue vs Lum, Lum vs Sat, Custom curves
6. Primaries/Log/HDR wheel settings (lift/gamma/gain/offset/contrast/pivot)
5. Effects used: Film grain, Halation, Glow, Lens flare, Vignette
6. Output transform settings
Return as structured JSON with node-by-node breakdown.
```

### Fusion Compositing
```
Analyze this frame from a DaVinci Resolve FUSION COMPOSITING tutorial. Extract:
1. Node graph structure (Loader, Merge, Transform, Keyer, Tracker, etc.)
2. Keying workflow (Delta/Ultra/Primatte, spill suppression, edge feather)
3. Tracking setup (Planar/Camera/Point, stabilize vs match move)
4. Masking/rotoscoping (Bezier, B-Spline, feather, animation)
5. 3D setup (Camera3D, Renderer3D, Light, Geometry, materials)
5. Particle systems (pEmitter, forces, collision, life, velocity)
6. Paint/Clone tools usage
6. Output/render settings
Return as structured JSON.
```

### Motion Graphics
```
Analyze this frame from a MOTION GRAPHICS / TEXT ANIMATION tutorial. Extract:
1. Text+ or Fusion Title template structure
2. Animation keyframes (position, scale, rotation, opacity, tracking)
3. Expressions/scripts used (Lua/Python, publish controls)
4. Modifier chains (Transform, Shake, Wiggle, Follower)
5. Template publish controls (text, color, font, size, animation speed)
5. Data-driven setup (CSV/JSON import, text from spreadsheet)
6. Macro/template creation for reuse
Return as structured JSON.
```

### VFX
```
Analyze this frame from a VFX tutorial. Extract:
1. Effect type (explosion, fire, magic, portal, lightning, particle, simulation, fluid, cloth, destruction)
2. Fusion/Resolve node setup (particles, forces, shaders)
3. Simulation settings (pEmitter, forces, collision, life, velocity)
3. Shader/material setup (glow, incandescence, opacity maps)
4. Compositing over plate (merge modes, color correction, edge treatment)
4. Practical elements integration (stock footage, 3D renders)
5. Render settings (EXR, multi-pass, deep compositing)
Return as structured JSON.
```

### Camera Techniques
```
Analyze this frame from a CAMERA MOVEMENT / VIDEOGRAPHY tutorial. Extract:
1. Camera movement type (dolly, slider, gimbal, drone, handheld, steadicam, crane, jib, orbital)
2. Rig/equipment used (specific gear if visible)
3. Movement parameters (speed, acceleration, distance, arc radius)
4. Stabilization method (IBIS, gimbal, post-stabilize, warp stabilizer)
4. Lens info (focal length, aperture, sensor size if mentioned)
5. Movement purpose (reveal, transition, emotional beat, tracking)
5. DaVinci Resolve post: stabilization, speed warp, optical flow, reframe
Return as structured JSON.
```

### Lighting
```
Analyze this frame from a LIGHTING tutorial. Extract:
1. Lighting setup type (3-point, Rembrandt, butterfly, split, loop, clamshell)
2. Each light: type (LED, HMI, tungsten, natural), position, distance, modifier
3. Light ratios (key:fill, key:rim, background:subject)
4. Color temperature (key, fill, rim, background) in Kelvin
5. Flags, nets, diffusion, bounce, negative fill usage
5. Golden/blue hour specifics (sun angle, time, location)
6. DaVinci Resolve: relighting, color temp correction, power windows for lighting
Return as structured JSON.
```

### Composition
```
Analyze this frame from a COMPOSITION / FRAMING tutorial. Extract:
1. Composition rule/technique (rule of thirds, leading lines, framing, symmetry, layers)
2. Lens choice (focal length, aperture, sensor format)
3. Subject placement (rule of thirds intersection, center, golden ratio)
4. Depth creation (foreground/midground/background, atmospheric perspective)
5. Aspect ratio and framing intent (16:9, 2.39:1, 4:5, 9:16)
5. Camera height/angle (eye level, low, high, dutch)
6. DaVinci Resolve: reframe, crop, transform, aspect ratio conversion
Return as structured JSON.
```

### Audio/Sound
```
Analyze this frame from an AUDIO/SOUND DESIGN tutorial. Extract:
1. Audio technique (noise reduction, EQ, compression, reverb, sync, mixing)
2. Fairlight/Resolve tools used (Noise Reduction, EQ, Dynamics, Reverb, De-Esser)
2. Settings per plugin (threshold, ratio, attack/release, frequency, Q, wet/dry)
3. Music/soundtrack layering (stems, volume automation, ducking)
4. Dialogue processing (de-noise, de-reverb, EQ matching, loudness)
5. Sound design (Foley, ambience, impacts, whooshes, risers)
5. Delivery specs (loudness LUFS, true peak, format)
Return as structured JSON.
```

### Editing Workflow
```
Analyze this frame from an EDITING WORKFLOW tutorial. Extract:
1. Edit technique (J-cut, L-cut, match cut, jump cut, smash cut, montage)
2. Pacing/rhythm (cuts per minute, beat sync, breath timing)
3. Timeline organization (tracks, bins, markers, colors)
4. Multicam setup (sync method, angle switching)
5. Trim tools (ripple, roll, slip, slide, extend, trim)
5. Speed changes (retime, optical flow, speed ramp, freeze frame)
5. Marker/workflow automation (scripts, macros, shortcuts)
Return as structured JSON.
```

### Photography Categories
Similar pattern — each photography category has its own extraction schema (lighting setup, lens choice, composition, retouching, etc.)

---

## 📤 Output Structure

### Vault Note (per reel)
```markdown
---
reel_id: DZt9pF7S1AI
collection: video_effect
subcategory: transitions
source_url: https://www.instagram.com/reel/DZt9pF7S1AI/
analyzed_at: 2026-07-25T17:10:54.573399
tags: [instagram-reel, davinci-resolve, video_effect, transitions]
---

# Transitions: DZt9pF7S1AI

**Source:** [DZt9pF7S1AI](https://www.instagram.com/reel/DZt9pF7S1AI/)  
**Analyzed:** 2026-07-25 17:10:54  
**Category:** video_effect → transitions

## Extracted Knowledge

{
  "transition_type": "Speed Ramp Whip Pan",
  "duration_frames": 12,
  "duration_seconds": 0.5,
  "easing_curve": "Ease In-Out (Bezier: 0.4, 0.0, 0.2, 1.0)",
  "fusion_setup": {
    "merge_nodes": 2,
    "transform_nodes": 2,
    "directional_blur": true
  },
  "keyframe_structure": {
    "position": ["0%", "50%", "100%"],
    "speed": ["100%", "300%", "100%"]
  },
  "color_handling": "Log space maintained, CST to Rec.709 at output",
  "audio_crossfade": "5-frame linear crossfade",
  "is_builtin_or_custom": "Custom Fusion comp"
}

## DaVinci Resolve Application

See extracted techniques above for node structures, settings, and workflows.

## Assets

- **Frames:** `assets/DZt9pF7S1AI_frames/`
- **GIF:** `assets/DZt9pF7S1AI.gif`
- **Hermes Skill:** `davinci-video_effect-transitions-DZt9pF7S`

---
*Generated by Tag-Aware Extraction Pipeline*
```

### Hermes Skill (per reel)
```yaml
---
name: davinci-video_effect-transitions-DZt9pF7S
description: |
  DaVinci Resolve Speed Ramp Whip Pan transition from Instagram Reel DZt9pF7S1AI
  Category: Video Effects → Transitions
  Source: https://www.instagram.com/reel/DZt9pF7S1AI/
  Educational focus: Speed ramp with directional blur via Fusion
version: 1.0.0
category: creative
tags:
  - davinci-resolve
  - video-effects
  - transitions
  - speed-ramp
  - whip-pan
  - fusion-compositing
  - directional-blur
references:
  - "instagram_reel_id": "DZt9pF7S1AI"
  - "source_url": "https://www.instagram.com/reel/DZt9pF7S1AI/"
  - "category": "video_effect"
  - "subcategory": "transitions"
  - "analyzed_at": "2026-07-25T17:10:54.573399"
---

# davinci-video_effect-transitions-DZt9pF7S

## Overview
Speed Ramp Whip Pan transition using Fusion directional blur and speed retime.

## Key Techniques

### Transition Structure
- **Type:** Speed Ramp + Whip Pan
- **Duration:** 12 frames (0.5s at 24fps)
- **Easing:** Ease In-Out Bezier (0.4, 0.0, 0.2, 1.0)

### Fusion Setup
```fusion
Merge (Directional Blur) → Transform (Motion Blur) → Merge
    │                           │
    ▼                           ▼
Speed Ramp (Retime)         Keyframed Position
```

### Key Settings
- Directional Blur: Angle = 90°, Strength = 15
- Retime: Speed curve 100% → 300% → 100%
- Keyframes: Position (0%, 50%, 100%), Speed (0%, 50%, 100%)

## Practice Exercises
1. Build the 3-node Fusion comp above
2. Match the Bezier easing curve exactly
3. Test on different clip lengths

## Related Skills
- `davinci-fusion-directional-blur`
- `davinci-retime-speed-ramp`
- `davinci-transition-whip-pan`

## Metadata
- **Reel ID:** DZt9pF7S1AI
- **Category:** Video Effects → Transitions
- **Source:** https://www.instagram.com/reel/DZt9pF7S1AI/
- **Analyzed:** 2026-07-25T17:10:54.573399
```

---

## 📁 Vault Structure

```
/DaVinci_Knowledge_Base/
├── Video_Effects/
│   ├── transitions/
│   ├── compositing/
│   ├── motion-graphics/
│   ├── vfx/
│   ├── stylization/
│   ├── text-effects/
│   ├── time-effects/
│   ├── assets/
│   │   ├── {reel_id}_frames/
│   │   └── {reel_id}.gif
│   └── {subcategory}/{reel_id}.md
├── Photography_Videography/
│   ├── portrait/
│   ├── landscape/
│   ├── commercial_product/
│   ├── street_documentary/
│   ├── lighting_technique/
│   └── assets/
└── Camera_Theory/
```

---

## 🔗 Integration Points

### With `instagram-davinci-learning-pipeline`
- Provides the extraction engine for the learning pipeline
- Called by `scripts/full_tag_aware_pipeline.py`

### With `instagram-reel-availability-check`
- Pre-filters reels before extraction

### With `regenerate_exports_and_diagram`
- Post-processes generated skills/notes into indexes and diagrams

---

## 🛠️ Scripts & Templates

| File | Purpose |
|------|---------|
| `scripts/full_tag_aware_pipeline.py` | Main orchestrator |
| `scripts/process_batch.py` | Batch processor (resumable) |
| `scripts/extract.py` | Frame/GIF/transcript extraction |
| `scripts/vision_analyze.py` | Vision analysis wrapper |
| `templates/vault_note_template.md` | Generic vault note |
| `templates/vault_note_template_video_effect.md` | Video Effects vault note |
| `templates/vault_note_template_lightroom.md` | Photography vault note |
| `templates/skill_template.md` | Generic skill |
| `templates/skill_template_video_effect.md` | Video Effects skill |
| `templates/skill_template_lightroom.md` | Photography skill |

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Frame directory not found | Check `extraction_manifest.json` mapping; fallback to download-order mapping from `completed.json` |
| Vision 429 (rate limit) | Increase backoff; ensure 3s minimum between calls |
| Generic extraction output | Use category-specific prompt, not generic |
| Missing skills in Hermes | Run `hermes skill load <skill-name>` or restart Hermes |
| Vault assets not embedding | Verify `assets/{reel_id}_frames/` and `assets/{reel_id}.gif` exist |

---

## 📚 References

- `references/session-20260725-tag-aware-pipeline.md` — Full session learnings
- `references/vision-analysis-phase2.md` — Phase 2 vision protocol
- `references/auto-compression-troubleshooting.md` — Compression config fix
- `references/phase2-vision-pipeline-20260726.md` — Phase 2 vision batch processing protocol (20 RPM, frame sampling, prompts, output structure, clustering keywords, checkpoint/resume, progress file updates)
- `references/session-20260726-vision-batch.md` — Session 2026-07-26: vision_batch_queue.json (20 videos) processed at 20 RPM, VISION_PROGRESS.json updated, full protocol documented
- `scripts/process_vision_queue.py` — Batch vision queue processor script
- `references/local-vision-worker-20260727.md` — Local Ollama llava:7b worker protocol (no rate limits, 4.7GB, subprocess call pattern, JSON extraction from markdown, background worker on Mac Mini)

---

## 📈 Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-07-25 | Initial release — tag-aware extraction with 19 category schemas, frame sampling, rate limiting, vault/skill output |

---

## 🤝 Related Skills

| Skill | Purpose |
|-------|---------|
| `instagram-davinci-learning-pipeline` | Main learning pipeline orchestrator |
| `instagram-reel-availability-check` | Pre-filter reel accessibility |
| `regenerate_exports_and_diagram` | Generate exports + architecture diagrams |
| `video-tutorial-extraction` | YouTube equivalent (transcript-based) |

---

## ⚠️ Critical Pitfalls to Avoid

1. **Generic prompts** → Use category-specific prompts (5-10x more useful data)
2. **Wrong frame directory** → Always verify manifest mapping; fallback to download-order map
3. **Skipping reels** → Process all; flag missing frames but continue
4. **Batching vision calls** → 20 RPM is strict; 3s minimum interval
5. **Premature completion claims** → Verify output files exist
6. **Generic skill templates** → Use category-specific templates with relevant metadata
7. **Missing frame mapping** → downreels.com IDs ≠ Instagram short IDs