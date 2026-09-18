# Local Ollama Worker Pattern — Extractable Pattern

> **Context:** Batch vision analysis using local `qwen3-vl:8b` via Ollama API
> **Discovered:** Session 2026-07-28 after multiple failed approaches

---

## The Winning Pattern: `local_ollama_vision_worker.py`

```python
# Key architectural decisions:
# 1. ThreadPoolExecutor with shared rate limiter
# 2. Ollama /api/generate (NOT /api/chat - avoids llama-server)
# 3. Robust JSON extraction (markdown, thinking tags)
# 4. File-locked atomic progress writes
# 5. Checkpoint resume capability
```

### Why Previous Approaches Failed

| Approach | Failure | Root Cause |
|----------|---------|------------|
| `vision_analyze` (Hermes tool) | 429 at 20 RPM | Cloud provider hard limit |
| `qwen_vision_worker.py` (llama-server) | Timeouts, port churn | `llama-server` spawned per `/api/chat`, dies, restarts on new port |
| `cloud_vision_worker_v2.py` (subprocess) | Tool context error | `vision_analyze` only works IN Hermes agent context |
| **`local_ollama_vision_worker.py`** | ✅ Works | Direct HTTP to stable `ollama serve` on 11434 |

---

## Ollama Process Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│  ollama serve (PID 70327) — STABLE                              │
│  ├── Listens on :11434 (native API)                             │
│  ├── Listens on :11434/v1 (OpenAI-compatible)                   │
│  └── Single process, runs for days                              │
├─────────────────────────────────────────────────────────────────┤
│  llama-server (ephemeral) — UNSTABLE                            │
│  ├── Spawned per /api/chat call                                 │
│  ├── Ports: 52317 → 53776 → 55618 → ...                         │
│  ├── Dies under load, restarts on random port                   │
│  └── Causes "Max retries exceeded" / timeouts                   │
└─────────────────────────────────────────────────────────────────┘
```

**Critical Rule:** Use `/api/generate` (completion) for vision. Never `/api/chat`.

---

## Worker Implementation Essentials

### 1. Shared Rate Limiter (Thread-Safe)
```python
last_call_time = 0
rate_lock = threading.Lock()

def rate_limited_call():
    global last_call_time
    with rate_lock:
        elapsed = time.time() - last_call_time
        if elapsed < RATE_LIMIT_SECONDS:
            time.sleep(RATE_LIMIT_SECONDS - elapsed)
        last_call_time = time.time()
```

### 2. Robust JSON Extraction (Handles qwen3-vl Output)
```python
def extract_json(text):
    # Remove thinking tags
    text = re.sub(r'<thinking>.*?</thinking>', '', text, flags=re.DOTALL)
    
    # Try markdown code blocks
    for pattern in [r'```json\s*(.*?)\s*```', r'```\s*(.*?)\s*```']:
        for m in re.findall(pattern, text, re.DOTALL):
            try:
                return json.loads(m.strip())
            except:
                pass
    
    # Fallback: find first complete JSON object
    start = text.index('{')
    # ... depth-tracking parser ...
```

### 3. Atomic Progress Writes (File-Locked)
```python
# Always write to .tmp then rename
temp = VISION_PROGRESS_PATH.with_suffix('.tmp')
with open(temp, 'w') as f:
    json.dump(progress, f, indent=2)
temp.replace(VISION_PROGRESS_PATH)  # Atomic on POSIX
```

### 4. Checkpoint Resume
```python
pending = [v for v in progress if v.get('status') == 'pending']
# Skips completed, continues from next index
```

---

## Usage Template

```bash
# Start in background with notification
hermes terminal --background --notify -- python local_ollama_vision_worker.py

# Or direct
python local_ollama_vision_worker.py
```

### Configuration Constants
```python
MODEL = "qwen3-vl:8b"
OLLAMA_URL = "http://localhost:11434/api/generate"
MAX_WORKERS = 2
RATE_LIMIT_SECONDS = 3.0  # ~20 RPM
BATCH_SIZE = 10
```

---

## Troubleshooting Quick Reference

| Error | Fix |
|-------|-----|
| `HTTPConnectionPool... Max retries` | `ollama serve` not running |
| `No valid JSON in: ...` | Model emitted `<thinking>` or markdown; check extraction |
| `Frame not found` | Phase 1 extraction incomplete for that video |
| Worker dies silently | OOM (16GB limit) or 180s timeout hit |
| 429 errors | Using cloud `vision_analyze` instead of local |

---

## Integration Points

- **Upstream:** `instagram-davinci-learning-pipeline` (provides VISION_PROGRESS.json)
- **Downstream:** Skill generation from vision results (Phase 3)
- **Parallel:** `batch-vision-analysis` (legacy cloud approach)
- **Config:** `instagram-vision-pipeline` skill references this pattern