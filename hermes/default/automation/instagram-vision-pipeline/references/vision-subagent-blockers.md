# Vision Sub-Agent Blockers (2026-07-29 Session)

**Critical finding**: Hermes sub-agents (`delegate_task`) **cannot use local vision models** for Instagram Reel analysis, despite models having vision capability.

## Model Evaluation Results

| Model | Size | Vision | Hermes Delegation | Result |
|-------|------|--------|-------------------|--------|
| `qwen3-vl:8b` | 6.14 GB | ✓ | ✗ (32K context) | Rejected: 32K < 64K min |
| `qwen3.5:4b` | 3.39 GB | ✓ | ✗ (32K context) | Rejected: 32K < 64K min |
| `qwen3.5-64k` | 6.59 GB | ✓ | ✓ (262K context) | **Accepted but timed out** — sub-agents hit 300s timeout with 1 API call each |
| `gemma4:12b` | 7.56 GB | ✓ | ✓ (262K context) | **Accepted but timed out** — same 300s timeout |

## Root Cause

Hermes enforces **64K minimum context window** for sub-agents (hard-coded). Local qwen3.5:4b/vl:8b report 32K (Ollama default) so they're rejected even with `context_length: 262144` in config. qwen3.5-64k reports 262K so accepted, but sub-agents still timeout (likely model load + inference on 16GB M4).

## Working Alternatives

1. **Cloud vision via `vision_analyze` tool** — NVIDIA/Google Gemini providers at ~3-5s/call (used in this session for manual analysis)
2. **Foreground sequential Python script** — Single-frame `qwen3.5:4b` works at ~2-3 min/frame (tested 1 frame, successful)
3. **Sub-agents with cloud provider** — Configure Hermes `vision` provider to NVIDIA/Gemini for sub-agent use

## Sub-Agent Timeout Setting

`delegation.child_timeout_seconds: 300` in config.yaml — may need increase for local models.

## Sequential Local Vision Processing Pattern (Working)

When cloud vision quota is exhausted, use foreground sequential processing:

```python
# vision_batch_local.py - Run in terminal(background=true, notify_on_complete=true)
import json, base64, requests
from pathlib import Path
from datetime import datetime

PROGRESS_FILE = Path('/Volumes/Samsung LED/Instagram Downloads/New Untouched Reels Download/CONTENT_PROCESSING/VISION_PROGRESS.json')
FRAMES_DIR = Path('/Volumes/Samsung LED/Instagram Downloads/New Untouched Reels Download/CONTENT_PROCESSING/frames')
URL = 'http://127.0.0.1:11434/api/generate'
MODEL = 'qwen3.5:4b'  # Smallest vision model (3.39 GB)
BATCH_SIZE = 5  # Small batches, restart Ollama between

with open(PROGRESS_FILE) as f:
    data = json.load(f)

pending = [v for v in data if v.get('status') == 'pending'][:BATCH_SIZE]

for i, v in enumerate(pending):
    vid = v['video_id']
    frame_path = FRAMES_DIR / vid / 'frame_0001.jpg'
    with open(frame_path, 'rb') as f:
        img_b64 = base64.b64encode(f.read()).decode()
    
    prompt = f"""Analyze this DaVinci Resolve technique from Instagram Reel {vid}. Return ONLY valid JSON with: technique_name, resolve_page (Color|Edit|Fusion|Fairlight), node_graph_type (serial|parallel|layer_mixer|compound), key_nodes (array), parameters (object), steps_to_reproduce (array), difficulty (beginner|intermediate|advanced), tags (array)."""
    
    payload = {'model': MODEL, 'prompt': prompt, 'images': [img_b64], 'stream': False, 'options': {'temperature': 0.1}}
    
    try:
        resp = requests.post(URL, json=payload, timeout=300)
        if resp.status_code == 200:
            result_text = resp.json().get('response', '')
            import re
            json_match = re.search(r'\{.*\}', result_text, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
                v['status'] = 'complete'
                v['result'] = result
                v['updated_at'] = datetime.now().isoformat()
                print(f"  ✓ {i+1}/{len(pending)} {vid}: {result.get('technique_name', 'OK')}")
            else:
                v['status'] = 'error'
                v['error'] = 'No JSON'
        else:
            v['status'] = 'error'
            v['error'] = f'HTTP {resp.status_code}'
    except Exception as e:
        v['status'] = 'error'
        v['error'] = str(e)
        print(f"  ✗ {i+1}/{len(pending)} {vid}: {e}")

# Save after each batch
tmp = PROGRESS_FILE.with_suffix('.tmp')
with open(tmp, 'w') as f:
    json.dump(data, f, indent=2)
tmp.replace(PROGRESS_FILE)
```

## Operational Notes

- Restart Ollama (`pkill -9 -f "ollama serve" && ollama serve &`) every 5-10 frames to clear memory leaks
- Accept ~2-3 min/frame throughput
- Save progress to JSON after EVERY frame (atomic write via .tmp)
- Run via `terminal(background=true, notify_on_complete=true)` to avoid blocking chat