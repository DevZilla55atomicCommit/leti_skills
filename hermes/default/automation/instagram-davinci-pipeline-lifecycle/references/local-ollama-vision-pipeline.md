# Local Ollama Vision Pipeline

## Overview
Use local Ollama models (llava:7b) for frame analysis without rate limits. Only works in main Hermes session - sub-agents cannot access vision models.

## Setup
```bash
# Pull model
ollama pull llava:7b

# Start Ollama (if not running)
ollama serve
```

## API Usage
```python
import requests
import base64

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llava:7b"

def analyze_frame(image_path):
    with open(image_path, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode("utf-8")
    
    payload = {
        "model": "llava:7b",
        "prompt": "Analyze this frame for DaVinci Resolve techniques...",
        "images": [img_b64],
        "stream": False,
        "options": {"temperature": 0.1, "num_predict": 512}
    }
    
    resp = requests.post(OLLAMA_URL, json=payload, timeout=180)
    return resp.json()["response"]
```

## Performance
- **Speed**: ~40-50s for 3 frames (vs NVIDIA 3-5s + 20 RPM limit)
- **Resources**: ~8.5 GB RAM, 100% GPU, 32K context
- **Rate limits**: NONE (fully local)

## Critical Constraints
1. **Only works in main Hermes session** - sub-agents CANNOT call Ollama API
2. **Must run in main session** - Python script calling Ollama API directly
3. **GPU contention with parallel processes** - 4 parallel chunks slow per-video to ~150-200s but 3-4x net throughput

## Parallel Processing Pattern
```python
# Launch N background processes
for i, chunk in enumerate(chunks):
    terminal(background=True, notify_on_complete=True,
             command=f"python process_chunk.py '{chunk}' {i+1}")

# Monitor
process(action="list")
process(action="log", session_id, limit=50)
```

## Resource Requirements
- Ollama running (`ollama serve`)
- Model pulled (`ollama pull llava:7b`)
- ~8.5 GB RAM, 100% GPU
- Python with `requests` library