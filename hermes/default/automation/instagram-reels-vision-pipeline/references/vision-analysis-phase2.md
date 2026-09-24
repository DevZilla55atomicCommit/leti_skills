# Phase 2 Vision Analysis Pipeline — Reference Document

**Created:** 2026-07-30
**Session:** 20260730 (796/1,146 complete, 69.5%)

---

## Phase 2 Status Summary

| Phase | Collection | Total | Complete | Pending | Errors | Progress |
|-------|------------|-------|----------|---------|--------|----------|
| **2c** | Cinematic/Shooting | 1,146 | 796 | 209 | 141 | **69.5%** |
| **2d** | Remaining Collections | ~688 | 0 | ~688 | 0 | 0% |

---

## Vision Analysis Protocol

### Frame Path Pattern
```
/Volumes/Samsung LED/Instagram Downloads/New Untouched Reels Download/CONTENT_PROCESSING/frames/{VIDEO_ID}/frame_0001.jpg
```

### Vision Prompt Template
```
Analyze this cinematic shot from Instagram Reel {VIDEO_ID}. Describe the visual technique (composition, lighting, color grading style) and return ONLY valid JSON for a DaVinci Resolve technique that would recreate this look:
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

### Vision Analyze Call
```python
result = vision_analyze(
    image_url=frame_path,
    question=VISION_PROMPT.format(video_id=video_id)
)
```

### Progress Update
```python
# Update VISION_PROGRESS.json
for v in data:
    if v['video_id'] == video_id:
        v['status'] = 'complete'
        v['result'] = parsed_json
        v['updated_at'] = datetime.now().isoformat()
        break
```

---

## Rate Limiting (CRITICAL)

- **Vision API: 20 RPM maximum** — hard limit enforced by provider
- Minimum 3 seconds between `vision_analyze` calls
- If 429: exponential backoff (30s → 60s → 120s → 240s → 480s)
- **Do NOT batch vision calls** — they count individually against RPM
- Terminal/file operations can be batched freely

---

## Sub-Agent Configuration (CRITICAL — USER CORRECTED 2026-07-30)

### ❌ FAILED: Local Ollama Sub-Agents

**6 parallel sub-agents dispatched (37 videos each)**
- All 6 timed out at 600s with **only 1 API call completed**
- Local Ollama cannot proxy NVIDIA `vision_analyze` calls in sub-contexts
- Mac Mini M4 16GB: 6 × 3-4GB = 18-24GB needed → OOM guaranteed

**User Correction:** "Never run a delegate tasks like that using a local ollama model as it hit OOM and crash my Mac mini"

### ✅ WORKING: Manual Sequential Processing

- **74 videos processed this session** (722 → 796)
- **100% success rate** (~1 min/video)
- No timeouts, no OOM, reliable

### 🔧 Correct Config for Cloud Sub-Agents (if needed later)

```yaml
delegation:
  provider: ollama-cloud
  model: qwen3.5-64k
  base_url: https://api.ollama.com/v1
  api_key: ${OLLAMA_CLOUD_API_KEY}
  child_timeout_seconds: 300
  max_concurrent_children: 3
```

**Batch Size Recommendations:**
| Approach | Batch Size | Concurrent | Timeout | Notes |
|----------|------------|------------|---------|-------|
| Cloud sub-agents | 10-15 videos | 3-4 | 300s | Recommended for Phase 2c/2d |
| Manual sequential | 1 video | 1 | N/A | ~1 min/video, reliable |
| **Local sub-agents** | **NEVER** | **NEVER** | **NEVER** | **Hard blocked — OOM guaranteed** |

---

## Manual Vision Analysis Workflow (PROVEN)

```bash
# For each pending video:
1. vision_analyze(frame_path, prompt)  # Returns JSON technique
2. Update VISION_PROGRESS.json with result
3. Repeat (~1 min/video, reliable, no timeouts)
```

**Session Progress:** 74 videos processed manually (722 → 796) with 100% success rate.

---

## Current State (2026-07-30 End of Session)

| Metric | Value |
|--------|-------|
| Total Cinematic/Shooting | 1,146 |
| Complete | 796 (69.5%) |
| Pending | 209 |
| Errors | 141 |
| Session Processed | 74 videos |
| Remaining Phase 2c | 209 videos |
| Remaining Phase 2d | ~688 videos |

---

## Next Session Resume Plan

1. Load VISION_PROGRESS.json
2. Get pending list: `[v['video_id'] for v in data if v.get('status') == 'pending']`
3. Process next 10-15 videos manually using `vision_analyze`
4. Update JSON after each
5. Re-run `generate_skills.py` and `build_vault.py` periodically

---

## Files Modified This Session

- `scripts/generate_skills.py` — Generate Hermes skills from 651 completed analyses
- `scripts/build_vault.py` — Build Obsidian vault (651 techniques, 19 collections, 519 tags, 643 GIFs)
- `scripts/generate_skills.py` — Updated and re-ran for new completions
- `scripts/build_vault.py` — Re-ran to include new techniques