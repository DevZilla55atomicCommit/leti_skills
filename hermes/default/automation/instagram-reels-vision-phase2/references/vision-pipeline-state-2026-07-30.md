# Vision Pipeline State — 2026-07-30 Session Summary

## Overall Pipeline Status

| Phase | Collection | Total | Complete | Pending | Errors | Progress |
|-------|------------|-------|----------|---------|--------|----------|
| 2a | Color Grading | 336 | 336 | 0 | 0 | 100% ✅ |
| 2b | DaVinci Tricks | 224 | 224 | 0 | 0 | 100% ✅ |
| 2c | Cinematic/Shooting | 1,146 | 798 | 207 | 141 | 69.6% 🔄 |
| 2d | Drone | 114 | 0 | 114 | 0 | 0% ⏳ |
| 2e | Gimbal Moves | 474 | 0 | 474 | 0 | 0% ⏳ |
| 2f | Ideas for Shooting | 796 | 0 | 796 | 0 | 0% ⏳ |
| 2g | Other DaVinci | ~30 | 0 | ~30 | 0 | 0% ⏳ |

## This Session (2026-07-30) Achievements

### Vision Analysis (Phase 2c - Cinematic/Shooting)
- **Processed**: +76 videos (722 → 798 complete)
- **Current progress**: 69.6% (798/1,146)
- **Remaining**: 207 pending + 141 errors
- **Frame extraction**: 100% complete (0 missing frames)

### Downstream Pipeline (Fully Automated - Working)
- **Skills generated**: 798 skills in `~/.hermes/skills/davinci-resolve-techniques/`
- **Vault notes**: 798 technique notes in `/Volumes/Samsung LED/.../vault/techniques/`
- **Media copied**: 643 GIFs to vault/media/
- **Collections indexed**: 19 collection indexes, 519 tag indexes
- **Master index**: vault/index.md with full cross-references

### Scripts Created & Validated
1. `generate_skills.py` — Converts VISION_PROGRESS.json → Hermes skills
2. `build_vault.py` — Builds Obsidian vault with cross-links, media, indexes
3. Both scripts are idempotent, resume-safe, handle missing GIFs gracefully

## Critical Technical Lessons

### 1. Vision Model Constraint (VALIDATED)
**NVIDIA `vision_analyze` is the ONLY viable vision method on 16GB M4 Mac Mini.**
- Local Ollama vision models (qwen3-vl:8b, qwen3.5:4b, gemma4:12b) ALL fail: OOM kills, timeouts >180s, connection crashes
- 16GB RAM insufficient for vision model + OS + workloads
- `vision_analyze` tool uses NVIDIA's hosted Gemini model — zero local RAM cost

### 2. Sub-Agent Parallelization FAILED
**Root cause**: `vision_analyze` tool is NOT available to sub-agents.
- Launched 6 parallel sub-agents with `ollama-launch` provider
- Sub-agents tried to use local Ollama for vision → OOM/timeouts
- All 6 timed out at 600s with 1 API call each
- **Only the MAIN session has access to NVIDIA `vision_analyze`**

### 3. Rate Limiting Protocol (VALIDATED)
- NVIDIA `vision_analyze`: 20 RPM hard limit → 3 sec minimum between calls
- Exponential backoff on 429: 30s → 60s → 120s → 240s → 480s
- Terminal/file operations: batch freely (no rate limit)
- Manual pace: ~1 video/minute (3-5 vision calls + JSON update)

### 4. Session Limit Constraint
- Hermes session tool limit: 150 calls
- Manual pace: ~75 videos max per session (150/2 calls per video)
- 207 remaining Cinematic videos = 3+ full sessions manually

## Frame Extraction Strategy (VALIDATED)
- **Percentages**: `[0, 14, 28, 42, 57, 71, 86, 99.9]` — avoids black frames on short clips
- **Tolerance**: ≥7 frames accepted (missing last frame tolerated)
- **Already complete**: All 1,146 Cinematic videos have frames extracted

## Next Steps

### Immediate (This Session)
- [ ] Process 10-15 more Cinematic videos manually (hit 150 tool limit)
- [ ] Document any new technique categories observed

### Near Term (Next Sessions)
- [ ] Complete remaining 207 Cinematic videos (3 more sessions)
- [ ] Run `generate_skills.py` and `rebuild_vault.py` incrementally
- [ ] Phase 2d: Drone collection (114 videos)
- [ ] Phase 2e: Gimbal Moves (474 videos)

### Parallelization Options (Future)
1. **Multiple main sessions** — Open separate Hermes windows, each gets own vision quota
2. **Cron jobs** — Background scripts calling `vision_analyze` in separate processes
3. **Wait for NVIDIA batch API** — If/when provider adds native batch endpoint

## Files Created This Session

| File | Purpose |
|------|---------|
| `generate_skills.py` | VISION_PROGRESS → Hermes skills |
| `build_vault.py` | VISION_PROGRESS → Obsidian vault |
| `references/sub-agent-parallelization-failure.md` | Root cause analysis |
| `references/vision-pipeline-state-2026-07-30.md` | This document |

## Environment
- **Hardware**: Mac Mini M4 16GB + MacBook Pro (dual)
- **Primary storage**: Samsung LED SSD 120GB (70GB free)
- **Overflow**: PNY 128GB
- **Vision provider**: NVIDIA API (integrate.api.nvidia.com/v1)
- **Models available**: `google/diffusiongemma-26b-a4b-it` (vision)