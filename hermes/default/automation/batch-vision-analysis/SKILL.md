---
name: batch-vision-analysis
description: "Batch-process frames with vision_analyze under rate limits."
---

# Batch Vision Analysis

## When to Use
- Processing 10+ images/frames with `vision_analyze`
- Need to respect API rate limits (e.g., 20 RPM = 3.2s between calls)
- Need persistent progress tracking across sessions
- Want automatic retry on 429/transient errors
- Need to deduplicate partial results

## Prerequisites
- Queue file (JSON array) with `video_id`, `frame_path`, `caption`, `techniques`, `transcript`
- Progress file (JSON array) to track completed/pending items
- Vision model access via `vision_analyze` tool

## Workflow

### 1. Load Queue & Progress
```python
with open(queue_path) as f:
    queue = json.load(f)
with open(progress_path) as f:
    progress = json.load(f)

processed_ids = {p['video_id'] for p in progress if p.get('status') == 'complete'}
unprocessed = [item for item in queue if item['video_id'] not in processed_ids]
```

### 2. Process with Rate Limiting
```python
for i, item in enumerate(unprocessed):
    result = vision_analyze(image_url=item['frame_path'], question=prompt)
    # Parse JSON from response
    # Append to progress
    # Write progress file
    if i < len(unprocessed) - 1:
        time.sleep(3.2)  # 20 RPM
```

### 3. Handle Errors
- **429 Too Many Requests**: Increase sleep to 5-10s, retry
- **Connection error**: Retry once after 5s
- **Parse failure**: Store raw response, mark status="error"

### 4. Deduplicate Progress File
After each session, remove stale `pending` entries for videos that now have `complete` entries:
```python
complete_ids = {p['video_id'] for p in progress if p.get('status') == 'complete'}
progress = [p for p in progress if not (p.get('status') == 'pending' and p['video_id'] in complete_ids)]
```

## Prompt Template
```text
Analyze this DaVinci Resolve technique reel frame.

Context:
- Video ID: {video_id}
- Collection: {collection}
- Caption: {caption}
- Known techniques: {techniques}
- Transcript: {transcript}

Return ONLY valid JSON with:
{
  "technique_name": "...",
  "resolve_page": "Color|Fusion|Edit|Fairlight",
  "node_graph_type": "Serial|Parallel|Layer Mixer|Compound",
  "key_nodes": ["..."],
  "parameters": {...},
  "steps_to_reproduce": ["..."]
}
```

## Progress Entry Schema
```json
{
  "video_id": "string",
  "collection": "string",
  "url": "https://www.instagram.com/reel/{video_id}",
  "caption": "string",
  "duration_sec": 0,
  "techniques": ["string"],
  "frames_analyzed": ["frame_xxx.jpg"],
  "frame_count": 0,
  "gif_path": "",
  "transcript_excerpt": "string",
  ## Vision Analysis: NVIDIA `vision_analyze` Only Strategy (UPDATED 2026-07-29)

### NVIDIA `vision_analyze` Tool — PRIMARY VIABLE METHOD (2026-07-29)

The Hermes `vision_analyze` tool using NVIDIA's `google/diffusiongemma` (or `gemini-2.5-flash`) is the **only reliable vision method** on 16GB Mac Mini M4.

| Parameter | Value |
|-----------|-------|
| Rate Limit | 20 RPM (3s minimum between calls) |
| Latency | ~3-5s/call (NVIDIA DiffusionGemma / Gemini) |
| Quality | High (native vision model) |
| Use For | ALL vision analysis |
| Tool | `vision_analyze(image_url, question)` — ONLY works in Hermes agent context |

**Failure Pattern**: Subprocess wrapping `vision_analyze` fails because tool only works in Hermes agent context, not standalone Python.

### Local Ollama Vision Models — NOW VIABLE (2026-07-31 Update)

| Model | Size | RAM | Vision? | Status |
|-------|------|-----|---------|--------|
| `llava:7b` | 8.5 GB | ~9 GB | ✅ | ✅ **WORKS** — ~35-50 sec/video, no rate limits |
| `qwen3-vl:8b` | 15 GB | ~16 GB | ✅ | ❌ Too large for 16GB |
| `qwen3.5:4b` | 3.4 GB | ~4 GB | ✅ | ❌ Connection issues |
| `gemma3:4b` | ~4 GB | ~5 GB | ✅ | ⚠️ Untested |
| `moondream:1.8b` | 1.8 GB | ~2 GB | ✅ | ❌ Broken (returns "urn") |

**Critical Update (2026-07-31):** `llava:7b` works reliably on 16GB Mac Mini M4 for batch vision analysis. It fits alongside a text model (gemma4:12b = 7.6 GB) with ~8.5 GB RAM for llava:7b.

### Local Ollama Vision Pipeline (Validated 2026-07-31)

**Architecture:**
```
Main Session (only component that can run local vision)
├── Terminal tool → Python → Ollama API (llava:7b) ✅
├── vision_analyze tool → NVIDIA vision (20 RPM) ❌ for local
└── delegate_task → Sub-Agent (text-only, no vision) ❌
```

**Script:** `/Users/alfredkamisese/vision_pipeline/local_vision_analyze.py`
**Batch processor:** `/Users/alfredkamisese/vision_pipeline/batch_chunk.py`

**Performance:**
- ~45 sec/video sequential (3 frames)
- ~150-200 sec/video with 4 parallel chunks (GPU contention)
- No rate limits, fully autonomous
- Best: **2 parallel chunks** for optimal throughput

### MASTER_MAPPING.md as Central Hub (2026-07-31)

**Created:** `MASTER_MAPPING.md` as single source of truth for entire DaVinci Knowledge Base vault.

**Updated Files (2026-07-31):**
- **130 index files** updated to reference `MASTER_MAPPING.md` instead of `Memory.md`/`index.md`
- **Hero_index.md** (vault root) updated to point to `MASTER_MAPPING.md` as DaVinci KB entry point
- **Memory.md** and `index.md` removed from DaVinci_Knowledge_Base root
- All support folder indexes (`analysis/`, `media/`, `skills/`, `collections/`, `tags/`, `transcripts/`) cleaned and validated

**Key Updates Across 130 Files:**
| Update Type | Applied |
|-------------|---------|
| `Memory.md` → `MASTER_MAPPING.md` | ✅ All occurrences |
| `../index.md` → `MASTER_MAPPING.md` | ✅ All occurrences |
| `../Memory.md` → `MASTER_MAPPING.md` | ✅ All occurrences |
| "Master GPS" → "Master Mapping" | ✅ All occurrences |
| "DaVinci KB Master" → "Master Mapping" | ✅ All occurrences |
| "Master Vault Index" → "Master Mapping" | ✅ All occurrences |
| Added `master_mapping:` frontmatter | ✅ Where missing |
| Added `MASTER_MAPPING.md` reference link | ✅ Where missing |

**Hero_index.md (vault root) Updates:**
- Quick Navigation table: `Memory.md` → `MASTER_MAPPING.md`
- Folder structure tree: `Memory.md` → `MASTER_MAPPING.md`
- Cross-Reference Documents: `Memory.md` → `MASTER_MAPPING.md`
- Quick Actions: `Memory.md` → `MASTER_MAPPING.md`

### Storage Cleanup (2026-07-31)

**Samsung LED (120GB) freed from 96% to 50%:**
| Deleted | Size Freed |
|---------|------------|
| `CONTENT_PROCESSING/gifs/` | 45 GB |
| `CONTENT_PROCESSING/frames/` (1,030 complete videos) | ~7.4 GB |
| `~/Downloads/instagram_downloads/` (duplicate) | 435 MB |

**Remaining on Samsung LED:**
- `Instagram Downloads/{collection}/` — ~50 GB original MP4s
- `CONTENT_PROCESSING/frames/` — 473 MB (135 error/pending videos only)
- `CONTENT_PROCESSING/*.json` — Processing manifests

**JSON Schema Output:**
```json
{
  "grading_style": "teal/orange|film look|log|S-Log3|Rec709|custom",
  "camera_movement": "static|dolly|gimbal|handheld|tripod|slider|drone|crane",
  "lighting": "key/fill ratio, soft/hard, natural, artificial, practical, mixed",
  "effects": ["transitions", "overlays", "text", "LUTs", "filters", "composites"],
  "color_temperature": "warm|cool|neutral|mixed",
  "contrast_level": "high|low|medium|flat/log",
  "saturation": "high|low|medium|desaturated",
  "notes": "DaVinci-relevant observations"
}
```

### Vision Analysis Prompt Structure (Validated 2026-07-29)

The following prompt template produces reliable DaVinci Resolve technique JSON from NVIDIA `vision_analyze`:

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

### Frame Extraction Fixes (Validated 2026-07-29)

| Issue | Fix |
|-------|-----|
| Frame at 100% = black on short clips | Extract at **99.9%** instead of 100% |
| Require all 8 frames | Accept **≥7 frames** (tolerate missing last frame) |
| Frame percentages hardcoded | Use: `[0, 14, 28, 42, 57, 71, 86, 99.9]` |

### Progress Tracking Schema

```json
{
  "video_id": "string",
  "status": "complete|pending|error",
  "collection": "string",
  "result": { /* technique JSON */ },
  "error": "string (if error)",
  "updated_at": "ISO timestamp"
}
```

**Deduplication:** After each session, remove stale `pending` entries for videos that now have `complete` entries.

### Sequential Processing Pattern (CRITICAL)

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

### Performance Metrics (2026-07-29 Session)

| Metric | Value |
|--------|-------|
| Latency per frame | 3-5s |
| Rate limit | 20 RPM (3.2s minimum) |
| Success rate | ~100% |
| JSON parsing | Reliable (native vision model) |
| Session throughput | ~15-20 frames |

### Why This Works When Local Ollama Fails

| Aspect | Local Ollama (qwen3-vl:8b) | NVIDIA vision_analyze |
|--------|---------------------------|----------------------|
| Latency | 180s+ (often timeout) | 3-5s |
| Server stability | Crashes llama-server | N/A (cloud) |
| Memory | 6GB+ VRAM + system | 0 local |
| Rate limit | None (but unusable) | 20 RPM |
| JSON output | Needs `<thinking>` strip | Clean native JSON |
| Sub-agent compatible | No | No (both need main agent) |