# Session 2026-07-28 — Vision Pipeline Configuration & Sub-Agent Fixes

**Context:** Massive Instagram Reels → DaVinci Resolve knowledge extraction pipeline. Dual Mac (Mac Mini M4 16GB + MBP), Samsung LED SSD (120GB, 70GB free) primary, PNY128GB overflow.

## Pipeline Status (2026-07-28)

| Phase | Progress | Status |
|-------|----------|--------|
| **Vision (Cinematic/Shooting)** | 496/1,165 (43%) | 🔄 Running via 3am cron + manual |
| **Skills** | 145 created | ✅ In `~/.hermes/skills/davinci-resolve-techniques/` |
| **Obsidian Vault** | 81 technique notes | ✅ Built at `/Users/alfredkamisese/Obsidian/DaVinci-Techniques/` |

## Vision Analysis Configuration

### Working Vision Providers

| Provider | Model | Vision? | Speed | Status |
|----------|-------|---------|-------|--------|
| **NVIDIA** | `google/diffusiongemma-26b-a4b-it` | ✅ Yes | ~3-5s/call | **Primary** |
| **Ollama Cloud** | All models | ❌ No | N/A | Unusable |
| **Local Ollama** | `qwen3-vl:8b` | ✅ Yes | ~30s/call | **Backup only** |

### Vision Config in `~/.hermes/config.yaml`

```yaml
vision:
  provider: nvidia
  model: google/diffusiongemma-26b-a4b-it
```

## Sub-Agent Delegation Config (Fixed)

```yaml
delegation:
  provider: ollama-cloud
  model: gemma4:31b-cloud
  base_url: https://ollama.com  # NOT https://ollama.com/api
  api_key: <your-api-key>
  max_concurrent_children: 6
  child_timeout_seconds: 300
  max_spawn_depth: 1
  orchestrator_enabled: true
```

**Critical Fix:** `base_url` must be `https://ollama.com` (without `/api`). The SDK appends `/api/...` automatically. Using `https://ollama.com/api` causes double `/api/api/...` paths and 404 errors.

## Local Model Performance

- `qwen3-vl:8b` on M4 16GB: ~30s per call, works but too slow for batch processing
- NVIDIA provider: ~3-5s per call, rate limited (~20 RPM)
- **Recommendation**: Use NVIDIA for production, local only for offline/fallback

## Cron Job Automation

```bash
0 3 * * * /Users/alfredkamisese/.hermes/hermes-agent/venv/bin/python /Users/alfredkamisese/vision_cron_job.py >> /Users/alfredkamisese/vision_cron.log 2>&1
```

**Script**: `/Users/alfredkamisese/vision_cron_job.py` — processes 20 frames per run via NVIDIA vision

## Sub-Agent Skills Generation

- Sub-agents process `skill_batch_*.json` files (each ~5-64 techniques)
- Each sub-agent handles one batch file, writes skills via `write_file` tool
- **Known Issue**: Sub-agents timeout at 300s for large batches
- **Workaround**: Use smaller batch sizes (5-10 techniques) or run skills generation as single Python script

## Session Findings (2026-07-28)

- Vision analysis: 496/1,165 complete (43%)
- NVIDIA vision provider: reliable 3-5s/call
- Local qwen3-vl:8b: works but ~30s/call (too slow for batch)
- Sub-agents: partially working, need delegation config fix
- Cron job: active at 3am, processes ~20 frames/night
- Skills: 145 in davinci-resolve-techniques
- Vault: 81 technique notes with master index