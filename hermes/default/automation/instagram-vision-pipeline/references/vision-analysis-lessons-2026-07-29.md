# Vision Analysis Lessons Learned (2026-07-29)

## Context
Processing 1,165 Instagram Reels for DaVinci Resolve technique extraction via vision analysis.

## Approaches Tested

### 1. Local Ollama qwen3-vl:8b (FAILED - Too Slow)
- **Speed**: ~60-90 seconds per frame
- **Reliability**: Frequent read timeouts (300s)
- **Parallel workers**: 4 workers hitting same Ollama endpoint caused cascading timeouts
- **Result**: 100 frames processed in ~4 hours, mostly errors
- **Conclusion**: Local 8B vision model on M4 16GB is not viable for batch processing

### 2. NVIDIA API (google/diffusiongemma-26b-a4b-it) - WORKS
- **Speed**: ~3-5 seconds per frame
- **Rate limit**: 20 RPM (enforced by provider)
- **Reliability**: Good when rate limits respected
- **Auth**: Requires NVIDIA_API_KEY
- **Cost**: Cloud credits

### 3. Manual vision_analyze Tool (NVIDIA) - WORKS
- **Speed**: ~3-5 seconds per call
- **Rate limit**: Hits 429 at ~20 RPM
- **Throughput**: ~100-150 frames/day manually

### 4. Hermes Browser Tools + vision_analyze - WORKS (for frame capture)
- **Use case**: When yt-dlp fails, use browser automation to navigate reel, inject cookies, capture frames via canvas.toDataURL()
- **Validated**: 92/93 failed reels recovered (2026-07-20)
- **Not for**: Full vision analysis (no batch capability)

## Key Findings

| Factor | Local Ollama | NVIDIA Cloud | Manual NVIDIA |
|--------|--------------|--------------|---------------|
| Speed/frame | 60-90s | 3-5s | 3-5s |
| Reliability | Poor (timeouts) | Good | Good |
| Batch capacity | ~20/day | Rate limited | ~150/day |
| Cost | Free (local) | Cloud credits | Cloud credits |
| Concurrency | **Fails** | Sequential OK | Sequential OK |

## Parallel Processing Lesson

**Local Ollama cannot handle concurrent requests** - 4 workers hitting the same endpoint caused all to timeout. The Ollama server queues requests but the 300s timeout kills them all.

**Solution**: If using local model, process sequentially with single worker. If parallel needed, use cloud provider with higher concurrency limits.

## Current Status (2026-07-29)

- **Complete**: 506/1,165 (43%)
- **Pending**: 535
- **Errors**: 105 (non-Resolve content)
- **Skills generated**: 499
- **Vault notes**: 441

## Recommended Path Forward

1. **Manual NVIDIA batches**: Process 50-100 frames/day via `vision_analyze` tool
2. **Cron job**: Run overnight with NVIDIA (single-threaded, respect rate limits)
3. **Don't use local Ollama for vision** - it's a bottleneck
4. **Sub-agent skill generation works** - just needs fixed delegation config

## Files/Commands for Reference

```bash
# Check vision progress
python3 -c "
import json
from pathlib import Path
p = Path('/Volumes/Samsung LED/Instagram Downloads/New Untouched Reels Download/CONTENT_PROCESSING/VISION_PROGRESS.json')
data = json.load(open(p))
complete = sum(1 for v in data if v.get('status') == 'complete')
pending = sum(1 for v in data if v.get('status') == 'pending')
error = sum(1 for v in data if v.get('status') == 'error')
print(f'Complete: {complete}, Pending: {pending}, Error: {error}')
"

# Manual vision analysis (NVIDIA)
# Uses vision_analyze tool with image_url=frame_path + prompt
```