# Local llava:7b Vision Pipeline — Operational Reference

## Overview
Local alternative to NVIDIA vision_analyze API using llava:7b via Ollama. No rate limits, runs on local GPU.

## Setup
```bash
# Pull model (one-time)
ollama pull llava:7b

# Verify
curl -X POST http://localhost:11434/api/generate \
  -d '{"model": "llava:7b", "prompt": "test", "images": ["<base64>"]}'
```

## Script: local_vision_analyze.py
Location: `/Users/alfredkamisese/vision_pipeline/local_vision_analyze.py`

### Usage
```python
from local_vision_analyze import analyze_video_frames

# Analyze 3 frames from a video's frame directory
result = analyze_video_frames("/Volumes/.../frames/VIDEO_ID/", 3)
```

### API Call Format
```python
payload = {
    "model": "llava:7b",
    "prompt": VISION_PROMPT,
    "images": [base64_encoded_frame],
    "stream": False,
    "options": {
        "temperature": 0.1,
        "top_p": 0.9,
        "num_predict": 512
    }
}
response = requests.post("http://localhost:11434/api/generate", json=payload, timeout=180)
```

## Performance Profile (Validated 2026-07-31)

| Metric | Value |
|--------|-------|
| Model | llava:7b |
| RAM | 8.5 GB |
| GPU | 100% |
| Speed | 35-50 sec/video (3 frames sequential) |
| Rate limit | **None** |
| Cost | Free |
| Max parallel | 2 (GPU contention at 4x) |

### Parallel Processing (batch_chunk.py)
| Parallel Chunks | Time/Video | Wall Time (35-40 videos) |
|----------------|------------|--------------------------|
| 1 (sequential) | ~45 sec | ~25-30 min |
| 2 (recommended) | ~60-80 sec | ~20-25 min |
| 4 (tested) | 150-200 sec | ~25-30 min (GPU contention) |

**Recommendation**: Max **2 parallel** background processes.

## Pipeline Integration
```bash
# Process specific VISION_PROGRESS.json indices
cd /Users/alfredkamisese/vision_pipeline
/opt/homebrew/bin/python3.12 batch_chunk.py "108,109,110,111,112" 1

# Background with notification
terminal(background=true, notify_on_complete=true)
```

## Output Format
Returns JSON matching NVIDIA vision_analyze schema:
```json
{
  "grading_style": "custom",
  "camera_movement": "static",
  "lighting": "mixed",
  "effects": ["text"],
  "color_temperature": "neutral",
  "contrast_level": "medium",
  "saturation": "medium",
  "notes": "..."
}
```

## Limitations
- **Sub-agents CANNOT run this** — they are text-only, no terminal/Python/Ollama access
- **GPU contention** at >2 parallel processes
- **llava:7b hallucinates** some details (e.g., invents lighting setups)
- Use for: high-volume batches where NVIDIA rate limit (20 RPM) is bottleneck
- **Not for**: Quality-critical reels where NVIDIA Gemini is more accurate