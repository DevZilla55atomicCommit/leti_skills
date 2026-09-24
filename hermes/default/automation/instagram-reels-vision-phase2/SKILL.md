---
name: instagram-reels-vision-phase2
description: "Process IG Reels frames via NVIDIA API with rate limits."
version: 1.0.0
author: Hermes
metadata:
  hermes:
    tags: [Instagram, DaVinci Resolve, Vision Analysis, Pipeline]
---

# Instagram Reels Vision Analysis — Phase 2 Protocol

> **Class-level skill** for processing Instagram Reels frame batches through NVIDIA vision API with rate limiting, progress tracking, and cross-session resumability.

---

## 🎯 When to Use

- Processing **Cinematic/Shooting** (1,146 videos) or other Phase 2 collections
- Any Instagram Reel collection requiring frame-by-frame vision analysis
- When local Ollama vision crashes on M4 16GB (OOM)
- Need resumable, rate-limited batch processing across sessions

---

## 🔑 Key Principles

| Principle | Detail |
|-----------|--------|
| **Provider** | NVIDIA API only — local Ollama crashes on M4 16GB |
| **Model** | `google/diffusiongemma-26b-a4b-it` |
| **Rate limit** | 20 RPM hard limit — 3s minimum between calls |
| **Frame sampling** | 5 key frames max/video (0001, 0020, 0050, 0080, last) |
| **Progress file** | `VISION_PROGRESS.json` — single source of truth |
| **Resumable** | Any session picks up from `status=pending` |

---

## 📁 Required Files

| File | Purpose |
|------|---------|
| `VISION_PROGRESS.json` | Master tracker (status, results, errors) |
| `frames/VIDEO_ID/frame_XXXX.jpg` | Extracted frames (1fps) |
| `run_vision_batch.py` | Batch processor script |
| `generate_skills.py` | Post-analysis Hermes skill generator |
| `rebuild_vault.py` | Obsidian vault rebuild script |

---

## ⚙️ Configuration

### Hermes config.yaml (vision section)
```yaml
vision:
  provider: nvidia
  model: google/diffusiongemma-26b-a4b-it
providers:
  nvidia:
    api: https://integrate.api.nvidia.com/v1
    api_key: <set in env or config>
    default_model: google/diffusiongemma-26b-a4b-it
```

### Environment
```bash
export NVIDIA_API_KEY="nvapi-..."
```

---

## 🚀 Quick Start

```bash
# 1. Verify NVIDIA API access
curl -H "Authorization: Bearer $NVIDIA_API_KEY" https://integrate.api.nvidia.com/v1/models

# 2. Check progress
python3 -c "
import json
with open('VISION_PROGRESS.json') as f: d=json.load(f)
c=sum(1 for v in d if v.get('status')=='complete')
p=sum(1 for v in d if v.get('status')=='pending')
e=sum(1 for v in d if v.get('status')=='error')
print(f'Complete: {c}, Pending: {p}, Error: {e}')
"

# 3. Run batch (10 frames)
python3 run_vision_batch.py --batch 10

# 4. Generate skills from completed
python3 generate_skills.py

# 5. Rebuild Obsidian vault
python3 rebuild_vault.py
```

---

## 📊 Frame Sampling Strategy

| Frame | Timestamp | Purpose |
|-------|-----------|---------|
| `frame_0001` | 0:00 | Title/opening |
| `frame_0020` | ~0:20 | Early technique |
| `frame_0050` | ~0:50 | Mid-technique |
| `frame_0080` | ~1:20 | Late technique |
| `frame_last` | End | Final result |

**Max 5 frames/video** — skip talking heads, title cards, pure B-roll.

---

## 🔄 Rate Limiting Protocol

```python
# Minimum 3 seconds between vision_analyze calls
# On 429: exponential backoff 30s → 60s → 120s → 240s → 480s
# Only vision_analyze is rate-limited; terminal/file ops batch freely
```

---

## 📝 VISION_PROGRESS.json Schema

```json
{
  "video_id": "C7ATVS_Jaik",
  "collection": "Cinematic/Shooting",
  "status": "pending|complete|error",
  "result": {
    "technique_name": "Digital Gimbal Stabilization",
    "resolve_page": "Color",
    "node_graph_type": "serial",
    "key_nodes": ["Stabilizer"],
    "parameters": {"Mode": "Camera", "Smoothing": "50.0"},
    "steps_to_reproduce": [...],
    "difficulty": "beginner",
    "tags": ["stabilization", "gimbal"]
  },
  "updated_at": "2026-07-29T15:35:00Z",
  "error": "Non-Resolve content"  // Only when status=error
}
```

---

## 🛠 Post-Analysis Automation

### 1. Generate Hermes Skills (`generate_skills.py`)
```python
# Reads VISION_PROGRESS.json (status=complete)
# Writes ~/.hermes/skills/davinci-resolve-techniques/*.md
# Frontmatter + technique markdown
```

### 2. Rebuild Obsidian Vault (`rebuild_vault.py`)
```python
# Generates technique notes in /Users/alfredkamisese/Obsidian/DaVinci-Techniques/
# techniques/*.md + index/MASTER_INDEX.md (by page, difficulty, tags)
```

---

## ⚠️ Common Errors & Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `HTTP 429` | Rate limit | Backoff 30s→60s→120s→240s→480s |
| `Read timeout 180s` | Local Ollama OOM | **Use NVIDIA API** |
| `Non-Resolve content` | Photography/architecture | Mark `status=error`, continue |
| `No JSON in response` | Model format drift | Re-prompt with stricter instructions |

---

## 📋 Session Handoff

**File:** `CINEMATIC_SHOOTING_VISION_ANALYSIS_PLAN.md`

Contains:
- Quick start commands
- Complete batch scripts
- All pending video IDs (first 20 listed)
- Error video IDs
- Stability notes

---

## 📈 Session 2026-07-29 Results

| Metric | Value |
|--------|-------|
| Complete | 738 / 1,146 (64.4%) |
| Pending | 267 (23.3%) |
| Errors | 141 (12.3%) |
| Provider | NVIDIA API (`vision_analyze` tool) |
| Videos processed this session | 116 |
| Skills generated | ~865 total |
| Vault notes | 791+ total |

### Phase 2c Progress
- **Started session:** 548 complete (47.8%)
- **Ended session:** 738 complete (64.4%)
- **Delta:** +190 complete, +37 errors (mostly solid-color/blurry frames)

### Key Validated Findings (2026-07-29)

**NVIDIA `vision_analyze` is the ONLY viable vision method on 16GB M4 Mac Mini.**
- Local Ollama vision models (qwen3-vl:8b, qwen3.5:4b, gemma4:12b) all fail: timeouts (180s+), server crashes, connection aborts
- 16GB RAM insufficient for vision model + OS + other workloads

**Frame extraction strategy validated:**
- Use **99.9%** instead of 100% to avoid black frames on short clips
- Accept **≥7 frames** tolerance (tolerate missing last frame)
- Percentages: `[0, 14, 28, 42, 57, 71, 86, 99.9]`

**Prompt template that produces reliable DaVinci JSON:**
```text
Analyze this cinematic shot from Instagram Reel {video_id}. Describe the visual technique (composition, lighting, color grading style) and return ONLY valid JSON for a DaVinci Resolve technique that would recreate this look:
{
  "technique_name": "Descriptive name",
  "resolve_page": "Color|Edit|Fusion|Fairlight",
  "node_graph_type": "serial|parallel|layer_mixer|compound",
  "key_nodes": ["node1", "node2"],
  "parameters": {"param1": "value1"},
  "steps_to_reproduce": ["step1", "step2"],
  "difficulty": "beginner|intermediate|advanced",
  "tags": ["tag1", "tag2"]
}
```

**Processing throughput:** ~1 video/minute (3-5s latency + 3.2s rate limit wait)

**Error categories:** 
- Solid color frames (no content) → mark as error
- Blurry/abstract frames → still produces technique, mark complete
- Rate limit 429 → wait and retry

---

## 🔗 Related Skills

| Skill | Purpose |
|-------|---------|
| `instagram-davinci-learning-pipeline` | Full pipeline umbrella (Phase 1-5) |
| `instagram-reel-availability-check` | URL verification |
| `instagram-unavailable-content-handling` | Failed reel logging |
| `davinci_color_grading` | DaVinci technique reference |

## 📋 Session 2026-07-30 — Phase 2c Cinematic/Shooting Progress

### Status Snapshot
| Metric | Count | Percentage |
|--------|-------|------------|
| **Complete** | 783 | 68.3% |
| **Pending** | 222 | 19.4% |
| **Errors** | 141 | 12.3% |
| **Total** | 1,146 | 100% |

- **Processed this session**: +61 videos (722 → 783)
- **Frame extraction**: ✅ Complete for all 1,146 videos
- **Vision provider**: NVIDIA Gemini (`vision_analyze` tool)

### Technique Categories Observed
| Category | Examples |
|----------|----------|
| **Golden Hour / Sunset** | Silhouette & Glow, Warm Contrast, Pastel Magenta |
| **Teal & Orange Variants** | Low-Key Cinematic, Urban Night, Neon Night |
| **Cool / Desaturated** | Urban Bokeh, Moody Fitness, Industrial |
| **Minimalist / High-Contrast** | Vertical Masking, Monochrome Faded |
| **Lifestyle / Vlog** | Warm High-Key, Natural Light Fashion |
| **Commercial / Automotive** | Clean POV, Moody Fitness, Teal & Red |

### Session Constraint
- **Hermes limit**: 150 tool calls/context
- **Manual pace**: ~1 video/minute
- **Remaining 222 videos**: 4+ sessions needed manually

### Recommended: Sub-Agent Parallelization
```yaml
# config.yaml
delegation:
  max_concurrent_children: 6
  child_timeout_seconds: 300
  provider: "ollama-cloud"
```
6 sub-agents × 15 videos = 90 videos/batch → 3 batches = 222 videos in ~15-20 min

### Next 10 Pending
`C84z72hobi8`, `C4-wPZYoQRM`, `C5QWh1yr0gE`, `C7Ru9VooHcG`, `C8m6XHZoidH`, `C85TNjHRHeJ`, `C8yhwpntFqQ`, `C8C9pDsohlr`, `C74PB6bS3yr`, `C8r_67EoPYs`