# Vision Analysis: Dual-Mode Strategy

**Session:** 2026-07-28 (Phase 2 Vision Analysis Pipeline)
**Context:** Massive Instagram Reels → DaVinci Resolve knowledge extraction pipeline. 659 pending videos after Phase 1 content processing.

---

## Problem

- **Cloud Vision (Hermes `vision_analyze` tool)**: 20 RPM hard limit, ~10-15s/call, high quality
- **Local Ollama (qwen3-vl:8b)**: No rate limit, ~30-60s/call (with thinking), good quality
- Subagents timeout at 600s → must use background script with log monitoring

---

## Cloud Vision (Hermes `vision_analyze`)

| Parameter | Value |
|-----------|-------|
| Rate Limit | 20 RPM (3s minimum between calls) |
| Latency | ~10-15s/call |
| Quality | High (native vision model) |
| Use For | Priority batches, validation, small sets |
| Tool | `vision_analyze(image_url, question)` — ONLY works in Hermes agent context |

**Failure Pattern**: Subprocess wrapping `vision_analyze` fails because tool only works in Hermes agent context, not standalone Python.

---

## Local Ollama (qwen3-vl:8b)

| Parameter | Value |
|-----------|-------|
| Rate Limit | None (local) |
| Latency | ~30-60s/call (with thinking tags) |
| Quality | Good (8B params, vision) |
| Use For | Large backlogs, overnight runs |
| API | `http://localhost:11434/api/generate` with base64 images |

### Working Endpoint
```
POST http://localhost:11434/api/generate
{
  "model": "qwen3-vl:8b",
  "prompt": "...",
  "images": ["base64..."],
  "stream": false,
  "options": {"temperature": 0.1, "num_predict": 1024}
}
```

### Ollama Port Behavior
- `ollama serve` → port 11434 (stable)
- `llama-server` → random ports (52317, 53776, 55618...) when model loaded
- Use `/api/generate` on 11434 for stability

---

## Background Worker Pattern (CRITICAL)

```python
# Start
terminal(background=True, notify_on_complete=True, command="python worker.py")

# Monitor
process(action="poll", session_id="...")

# View logs
process(action="log", session_id="...", limit=50)
```

**Workers Used:**
1. `cloud_vision_worker.py` — wraps `vision_analyze` via subprocess → **FAILS** (tool context)
2. `local_ollama_vision_worker.py` — direct HTTP to Ollama `/api/generate` → **WORKS**

---

## JSON Parsing: qwen3-vl Output

```python
import re

def extract_json(text):
    # Remove thinking tags
    text = re.sub(r'', '', text, flags=re.DOTALL)
    
    # Try markdown code blocks
    for pattern in [r'```json\s*(.*?)\s*```', r'```\s*(.*?)\s*```']:
        matches = re.findall(pattern, text, re.DOTALL)
        for m in matches:
            try:
                return json.loads(m.strip())
            except:
                pass
    
    # Try direct JSON
    try:
        return json.loads(text.strip())
    except:
        pass
    
    # Find first complete JSON object
    try:
        start = text.index('{')
        depth = 0
        for i, ch in enumerate(text[start:], start):
            if ch == '{': depth += 1
            elif ch == '}':
                depth -= 1
                if depth == 0:
                    return json.loads(text[start:i+1])
    except:
        pass
    
    raise ValueError(f"No valid JSON in: {text[:300]}")
```

---

## Vision Progress File (`VISION_PROGRESS.json`)

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

---

## Frame Sampling Strategy

- Target frames: `frame_0001`, `frame_0020`, `frame_0050`, `frame_0080`, `frame_last`
- Max 5 frames/video
- Skip talking-head/title frames (detected via vision)
- ~1,680 vision calls for Color Grading collection (336 videos × 5)

---

## Storage Layout

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

---

## Session Progress (2026-07-28)

| Phase | Status | Details |
|-------|--------|---------|
| Phase 1: Content Processing | ✅ Complete | 1,156/2,818 videos; frames, GIFs, transcripts, analysis |
| Phase 2a: Vision - Color Grading | 🔄 In Progress | 659 pending; local Ollama worker running (proc_95f01d68347d) |
| Phase 2b-2g | ⏳ Pending | DaVinci Tricks (224), Cinematic (156), Drone (114), Gimbal (474), Ideas (796), Other (~30) |

---

## Next Steps

1. Let local Ollama worker complete 659 pending videos
2. Regenerate skills from vision results
3. Build Obsidian vault with GIFs
4. Process remaining Phase 2 collections