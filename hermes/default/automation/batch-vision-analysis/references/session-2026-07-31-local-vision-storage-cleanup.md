# Session 2026-07-31: Local Ollama Vision Pipeline + Parallel Processing

## Summary
- Switched from NVIDIA `vision_analyze` (20 RPM limit) to local Ollama `llava:7b`
- Processed 45 error videos via local vision
- Launched 4 parallel background chunks (killed due to storage crisis)
- Samsung LED at 96% full → cleaned up 45 GB gifs/

## Key Learnings

### Local Vision Works (but with constraints)
- **Only main session can run it** — sub-agents are text-only, no terminal/Python/HTTP
- **llava:7b is the sweet spot** for 16GB Mac (8.5 GB RAM, fits alongside text model)
- **GPU contention** with 4 parallel chunks: ~150-200 sec/video vs ~45 sec sequential
- **Optimal: 2 parallel chunks** for best throughput

### Parallel Background Processing Pattern (Validated)

```bash
# Launch 2-4 parallel chunks using terminal(background=true, notify_on_complete=true)
cd /Users/alfredkamisese/vision_pipeline

# Each chunk processes a comma-separated list of VISION_PROGRESS.json indices
/opt/homebrew/bin/python3.12 batch_chunk.py "indices..." 1 &
/opt/homebrew/bin/python3.12 batch_chunk.py "indices..." 2 &
```

**Script:** `batch_chunk.py` reads VISION_PROGRESS.json, processes assigned indices via local llava:7b, writes back every video.

### Storage Crisis Root Cause
Pipeline artifacts accumulated 56 GB on Samsung LED:
| Path | Size | Cleanup |
|------|------|---------|
| `gifs/` | **45 GB** | Delete — regenerated from frames |
| `frames/` | 7.9 GB | Keep only error/pending (1,030 complete = 6+ GB reclaimable) |
| `transcripts/` | 1.5 GB | Regenerate if needed |
| `analysis/` | 579 MB | Keep |
| `vault/` | 346 MB | Keep (final output) |

### Safe Cleanup Procedure
```bash
# 1. Kill background jobs (they write data)
# 2. Delete gifs (45 GB)
rm -rf "/Volumes/Samsung LED/Instagram Downloads/New Untouched Reels Download/CONTENT_PROCESSING/gifs"

# 3. Delete frames for completed videos
# Keep only videos with status "error" or "pending_vision" in VISION_PROGRESS.json
# 1,030 complete videos → ~6+ GB frames reclaimable
```

## VISION_PROGRESS.json Status (2026-07-31)
| Metric | Count |
|--------|-------|
| Total | 1,165 |
| Complete | 1,030 (88.4%) |
| Error | 116 |
| Pending | 19 |
| Local vision processed | 45 |

## Next Session
1. Clean frames for completed videos (reclaim 6+ GB)
2. Resume local vision on remaining 116 errors + 19 pending
3. Process Phase 2d (~688 videos)