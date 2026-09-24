# Session 20260728 — Vision Pipeline Execution & Skills Generation

**Context:** Active vision analysis session using NVIDIA `vision_analyze` (DiffusionGemma) for DaVinci Resolve technique extraction from Instagram Reels.

## Current Metrics (Live)

| Metric | Value |
|--------|-------|
| Vision Complete | 482/1,165 (41%) |
| Skills Created | 145 in `~/.hermes/skills/davinci-resolve-techniques/` |
| Obsidian Vault | 81 technique notes in `/Users/alfredkamisese/Obsidian/DaVinci-Techniques/` |
| 3am Cron Job | Running (20 frames/night) |

## Key Learnings This Session

### 1. Vision Provider - Cloud Only (NVIDIA DiffusionGemma)
- **Local Ollama qwen3-vl:8b**: Times out at 180s+ on 16GB Mac Mini M4, llama-server crashes on random ports
- **NVIDIA `vision_analyze`**: 3-5s/call, reliable, 20 RPM limit
- **Decision**: Use cloud `vision_analyze` exclusively

### 2. Sequential Processing Required
- `vision_analyze` tool ONLY works in Hermes agent context, NOT in subprocesses/sub-agents
- **Pattern**: Main agent loop with 3.2s sleep (20 RPM):
```python
for item in pending_items:
    result = vision_analyze(image_url=item['frame_path'], question=PROMPT)
    parse_and_store_result(result)
    time.sleep(3.2)
```

### 3. Sub-Agents for Text Tasks Only
- Use `delegate_task` for: skill generation, vault notes, data processing, Ollama Cloud text (gemma4:31b-cloud)
- **Do NOT** use sub-agents for vision analysis

### 4. Skill Generation: Single Script Over Sub-Agents
- **Problem**: 18 sub-agents dispatched, all timed out at 300s during file I/O + API calls
- **Solution**: Single Python script processes all 480+ completed analyses:
```python
# Load VISION_PROGRESS.json → group by (page, tag) → write skill files
# Completed in <5s vs 300s timeout
```
Created 145 skills in `~/.hermes/skills/davinci-resolve-techniques/`.

### 5. Obsidian Vault Structure
Built from 349 completed analyses:
```text
/Users/alfredkamisese/Obsidian/DaVinci-Techniques/
├── techniques/     # 81 category notes
├── index/MASTER_INDEX.md  # Wiki-linked master table
```

### 6. Cron Job for Vision Analysis
```bash
0 3 * * * /path/to/venv/bin/python /Users/alfredkamisese/vision_cron_job.py
```
Processes 20 frames/run overnight.

### 7. Model Config Fix (Hermes config.yaml)
**Problem**: Sub-agents failing with "model 'nvidia/nemotron-3-ultra-550b-a55b' not found" — they inherited main model config instead of delegation config.
**Fix**: Explicit delegation config with ollama-cloud:
```yaml
delegation:
  provider: ollama-cloud
  model: gemma4:31b-cloud
  base_url: https://ollama.com/api
  api_mode: ollama
  child_timeout_seconds: 300
  max_concurrent_children: 6
```
After this fix, sub-agents successfully created 145 skills.