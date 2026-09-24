# Sub-Agent Parallelization Failure Analysis (2026-07-30)

## What Was Attempted

Launched 6 parallel sub-agents via `delegate_task` to process the remaining 221 videos in Phase 2c Cinematic/Shooting collection.

- Each sub-agent assigned ~37 videos
- Configured to use local Ollama model `ollama-launch/qwen3.5:4b`
- Expected parallel throughput: 6x speedup

## What Happened

| Sub-Agent | Videos Assigned | Timeout (600s) | API Calls Completed |
|-----------|----------------|----------------|---------------------|
| 1-6       | 37 each        | All timed out  | 1 each              |

All 6 sub-agents timed out at 600 seconds (10 minutes) having completed only **1 vision_analyze call each**.

## Root Cause

**vision_analyze tool uses the parent session's NVIDIA vision model (gemini-2.0-flash), NOT the sub-agent's configured local Ollama model.**

### Architecture Detail

1. **Main session** has NVIDIA provider configured for vision_analyze (gemini-2.0-flash)
2. **Sub-agents** inherit the parent's tool configuration BUT their model config is overridden to local Ollama
3. **vision_analyze tool** bypasses the sub-agent's model config and calls the NVIDIA API directly
4. **Local Ollama** in sub-agent cannot proxy NVIDIA API calls — the sub-agent's context doesn't have access to the parent's NVIDIA credentials/endpoints
5. **Result**: Each sub-agent makes 1 API call (using parent's credentials?), then hangs/fails on subsequent calls

### Evidence

- Manual vision_analyze in main session: ~1 min/video, 100% success rate
- Sub-agents with local Ollama: 1 call then 600s timeout
- Sub-agents with ollama-cloud: UNTESTED (may work if it proxies properly)

## Lesson

**Do NOT use sub-agents for vision_analyze batch processing.**

The tool architecture doesn't support delegated vision calls to local models. The only reliable path is manual sequential processing in the main session.

## Correct Approach

Manual sequential processing in main session:
- Rate: ~1 video/minute
- 100% success rate for videos with frames
- Progress tracking via VISION_PROGRESS.json
- Session limit: ~50-60 videos per session (150 tool call limit)

## Future Consideration

If parallelization is needed, options:
1. Multiple Hermes desktop sessions running in parallel (each with own NVIDIA config)
2. Future batch API endpoint for vision_analyze (not yet available)
3. ollama-cloud provider in sub-agents — untested, may or may not work

For now: accept manual processing as the reliable path.