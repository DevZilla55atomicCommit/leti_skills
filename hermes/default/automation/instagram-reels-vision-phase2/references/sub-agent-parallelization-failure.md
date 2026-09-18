# Sub-Agent Parallelization Failure (2026-07-30)

## What Was Attempted
Launched 6 parallel sub-agents via `delegate_task` to process the 222 remaining Cinematic/Shooting videos:
- Each sub-agent: ~37 videos, `ollama-launch` provider, `qwen3.5:4b` model, 300s timeout
- Expected: 6 × 37 = 222 videos in ~5 minutes

## What Happened
**All 6 sub-agents timed out at 600s with only 1 API call completed each.**

## Root Cause
**`vision_analyze` uses the assistant's built-in NVIDIA vision model (Gemini), NOT local Ollama models.**

Sub-agents spawned with `ollama-launch` provider have NO access to the parent session's `vision_analyze` tool. They were trying to use local Ollama for vision, which fails on M4 16GB (OOM, timeouts, crashes).

## Correct Architecture

```
Main Session (has vision_analyze tool) → Sequential manual calls
    │
    ├── Frame extraction: ffmpeg (local, batch, fast)
    ├── Vision analysis: vision_analyze (rate-limited 20 RPM, sequential)
    ├── Skill generation: Python scripts (batch, fast)
    └── Vault build: Python scripts (batch, fast)
```

## What Works (Sequential)
- Process 10-20 videos per main session manually
- Each video: 3-5 `vision_analyze` calls (key frames)
- ~1 min/video including JSON updates
- 20 RPM = 3 sec minimum between calls
- Session tool limit (150) ≈ 75 videos max per session

## Future Parallelization Options
1. **Multiple main sessions** (separate Hermes windows) — each gets own `vision_analyze` quota
2. **Cron jobs** with `vision_analyze` in background scripts  
3. **Wait for native batch API** from NVIDIA if added

## Lesson
**Never delegate `vision_analyze` to sub-agents.** They cannot access the tool. Only the main session has the NVIDIA vision model access.