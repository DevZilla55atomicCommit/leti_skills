---
name: instagram-davinci-pipeline-lifecycle
description: |
  Complete file lifecycle and storage management for the Instagram Reels → DaVinci Resolve
  knowledge pipeline. Documents stages (download → extract → vision → skills → vault → cleanup),
  storage characteristics, regeneration workflows, and critical bugs fixed.
version: 1.1.0
category: automation
tags:
  - instagram
  - davinci-resolve
  - pipeline
  - lifecycle
  - storage
  - automation
  - tag-aware-extraction
  - background-processing
---

# Instagram → DaVinci Pipeline: File Lifecycle & Storage Management

> Complete file lifecycle documentation learned from processing 771 Instagram Reels (370 Video Effects + 391 Photography/Videography)
> on Mac Mini M4 16GB with zero-auth downreels.com.

---

### 🔄 Complete File Lifecycle (6 Stages)

### STAGE 1: DOWNLOAD
- **Source**: downreels.com (Playwright, headless, zero-auth)
- **Temp**: `~/instagram-davinci-pipeline/temp/mp4/{reel_id}.mp4`
- **Retention**: DELETED after extraction (via `cleanup_reel`)
- **Rate limit**: ~10 reels/batch, 4s delay; exponential backoff (30s→60s→120s→240s→480s)
- **Error handling**: ~5% failure rate (404/source deleted); add to retry queue
- **Dependency fix**: If Playwright fails with `ModuleNotFoundError: No module named 'greenlet._greenlet'`, run `pip install --force-reinstall --no-binary greenlet greenlet` in Hermes venv

### STAGE 2: EXTRACT
- **Frames**: 1fps → `temp/frames/{reel_id}/0001.jpg...`
- **GIF**: full video, 10fps, 480px → `temp/gifs/{reel_id}.gif`
- **Transcript**: Whisper base → `temp/transcripts/{reel_id}.json` (skipped on PyTorch `_C` namespace error)
- **Retention**: Frames + GIF + Transcript COPIED to vault, then temp DELETED
- **Frame directory mapping**: Frame folders use downreels.com internal IDs, NOT Instagram short IDs. Always use manifest's `frames_dir` field to locate actual frame directories.

### STAGE 3: VISION (Tag-Aware)
- **Input**: 3 keyframes (start, mid, end) → `vision_analyze` (20 RPM limit)
- **Prompt**: Category-specific (transitions, color_grading, compositing, motion_graphics, vfx, stylization, text_effects, time_effects, portrait, landscape, etc.)
- **Report**: `Vision_Reports/{reel_id}.json`
- **Retention**: Permanent in vault
- **Rate limit**: 20 RPM max, 3s minimum between calls (HARD CONSTRAINT)
- **Frame source**: Use manifest's `frames_dir` to find actual frame directories (downreels.com IDs)

### STAGE 4: SKILLS
- **Generated**: `~/.hermes/skills/creative/davinci-reel-{id[:8]}/` or `davinci-video_effect-{category}-{id[:8]}/`
- **Installed**: Auto-copied to Hermes skill system
- **Retention**: Permanent in skill system
- **Auto-install**: Copy to `~/.hermes/skills/creative/` for immediate discoverability via `hermes skills list | grep davinci-reel`

### STAGE 5: VAULT NOTES
- **Location**: `DaVinci_Knowledge_Base/Video_Effects/{category}/` or `Photography_Videography/{category}/`
- **Files**: `{reel_id}.md` (note), `{reel_id}.gif` (preview), `{reel_id}_frames/` (JPGs)
- **Retention**: Permanent

### STAGE 6: CLEANUP (AUTOMATIC)
- `cleanup_reel()` removes:
  - `temp/mp4/{reel_id}.mp4`
  - `temp/frames/{reel_id}/`
  - `temp/gifs/{reel_id}.gif`
- **Called AFTER successful vault copy**
- **Critical**: GIFs MUST be copied to vault BEFORE `cleanup_reel()` runs (bug fixed 20260724)

---

## 💾 Storage Characteristics (observed from 771 reels)

| Artifact | Size | Notes |
|----------|------|-------|
| Frame folders (JPG) | ~5-6 GB total | 15-60 frames/reel, ~150KB each |
| GIF files | ~6-8 GB total | Full-video, 10fps, 480px, up to 140MB each |
| Vault notes | ~2 MB total | Markdown + frontmatter |
| Vision reports | ~2 MB total | JSON |
| Hermes skills | negligible | |
| **Total vault** | **~12 GB** | for 771 reels |

---

## ⚠️ CRITICAL: GIFs MUST be copied to vault BEFORE cleanup_reel() runs

**Bug fixed 20260724**: GIFs were generated but NOT copied → lost on cleanup.

**Fix applied**: `regenerate_missing_gifs.py` downloads MP4, creates GIF, copies to vault, cleans temp.

**Verification**: 246 missing GIFs recovered via regeneration pipeline.

---

## 🔄 Regeneration Workflows

| Missing Asset | Recovery Method |
|---------------|-----------------|
| GIFs | `scripts/regenerate_missing_gifs.py` (246 reels recovered) |
| MP4s | Re-download via downreels.com (rate limited) |
| Frames | Re-extract from MP4 via ffmpeg |
| Skills | Copy from vault skills folder to `~/.hermes/skills/creative/` |

### GIF Regeneration Lessons Learned (2026-07-24)
- **236 GIFs regenerated** in single run (10-reel batches, 4s delay)
- **5 failures** — downreels.com returned 404/MP4 missing (source deleted)
- **Full-video GIFs at 10fps/480px** — 10-150MB each (avg ~30MB)
- **Total vault size**: 5.5GB (389 reels: frames ~2.5GB + GIFs ~3GB + notes ~1MB)
- **Temp cleanup works** — 0B remaining after each reel via `cleanup_reel()`

---

## 🚫 Rate Limits (HARD CONSTRAINTS)

| Operation | Limit | Notes |
|-----------|-------|-------|
| downreels.com | ~10 reels/batch, 4s delay | Exponential backoff (30s→60s→120s→240s→480s) |
| vision_analyze | 20 RPM max | 3s minimum between calls, batch terminal/file ops freely |
| Instagram cookies | NONE | downreels.com = zero-auth |
| Whisper | CPU only | ~10s per minute of audio |

---

### Key Lessons for Future Sessions (Updated 2026-07-31)

1. **Never trust cleanup without verifying vault copy** — audit `ls vault/*.gif` vs `ls temp/gifs/`
2. **GIF regeneration is expensive** — re-downloads 246 MP4s; prefer fixing copy logic first
3. **Frame folders are lightweight** — 936 × ~50 frames × 150KB ≈ 7GB, keep them
4. **Temp directory must stay empty** — if `du -sh temp/` > 100MB, cleanup failed
5. **Hermes skills are separate from vault skills** — copy to `~/.hermes/skills/creative/` for discoverability
6. **Vision Provider Selection - Local Ollama Now Viable** — Local `llava:7b` via Ollama API (~8.5 GB RAM, 100% GPU) works reliably at ~40-50s/frame (3 frames/video), removing the 20 RPM NVIDIA limit. NVIDIA `vision_analyze` still works but rate-limited. Sub-agents CANNOT access either vision model.
7. **Sequential Vision Processing Required** — `vision_analyze` tool ONLY works in Hermes agent context, not subprocesses. Must process in main agent loop with 3.2s sleep (20 RPM limit). Local Ollama calls also must run in main session (Python script calling Ollama API).
8. **Sub-Agents for Text Tasks Only** — Sub-agents work well for skill generation, vault notes, data processing. Do NOT use for vision analysis. Sub-agents CANNOT execute Python/terminal/Ollama API calls.
9. **Skill Generation: Single Script Over Sub-Agents** — 18 sub-agents dispatched, all timed out at 300s. Single Python script processes all 480+ analyses in <5s vs 300s timeout.
10. **Frame Extraction Already Complete** — All 1,165 videos have frames extracted. Vision analysis is the only remaining bottleneck. Can run overnight via cron.
11. **Cron Job for Vision Analysis** — 3am daily cron processes 20 frames/run. Current: 482/1165 complete.
12. **Obsidian Vault Structure** — Built from 349 completed analyses: 81 category notes with wiki-linked master index.
13. **Vault Path Discipline** — All outputs MUST use exact TamaZila Obsidian Vault path (`/Users/alfredkamisese/TamaZila Obsidian Vault/Hermes Agent/DaVinci_Knowledge_Base/`).
14. **Storage Budget Monitoring** — Samsung LED SSD (120GB): ~70GB free baseline; pipeline temp ~7.2GB; monitor `df -h` before each batch. **Critical: `gifs/` folder can accumulate 45+ GB redundant copies — clean proactively.**
15. **Vision Rate Limit (20 RPM / 3s) is Hard Constraint** — Enforced in all vision analysis stages. **Local Ollama bypasses this limit entirely.**
16. **GIF Copy Before Cleanup is Mandatory** — Copy to vault BEFORE `cleanup_reel()` deletes temp.
17. **Index Cross-Linking Should Be Automated** — 5 index files need updating; consider `regenerate_indexes.py`.
18. **Architecture Diagram Discipline** — Mermaid graph MUST include Instagram_Reels subgraph with MASTER_INDEX node.
19. **Skill Auto-Installation to Hermes** — Copy generated skills to `~/.hermes/skills/creative/` for immediate discoverability via `hermes skills list | grep davinci-reel`.
20. **Background Process Monitoring** — Use `process(action="poll", session_id)` and `process(action="log", session_id, limit=50)` to check long-running pipeline status.
21. **DaVinci Resolve Color Techniques Pipeline Separate from Video Effects** — Two distinct pipelines: (a) Video Effects (370 reels, 334 skills, 737 notes) using downreels.com; (b) Color Grading Techniques (1,165 reels, 145 skills, 81 vault notes) using NVIDIA vision + 3am cron. Do not mix outputs.
22. **NVIDIA Vision via Hermes Only** — `vision_analyze` tool requires main agent context; sub-agents cannot use it. Batch vision analysis must run in main agent loop with rate limiting.
23. **Ollama Cloud for Sub-Agent Text Generation** — Sub-agents configured with `provider: ollama-cloud`, `model: gemma4:31b-cloud` work reliably for skill generation and vault notes. Main agent uses NVIDIA for vision.
24. **Hermes Config Must Be Explicit** — Delegation config needs `provider: ollama-cloud`, `model: gemma4:31b-cloud`, `api_key` set. Main model config needs `provider: nvidia`, `model: nvidia/nemotron-3-ultra-550b-a55b`.
25. **Vision Analysis Batch Size** — 20 frames per cron run (3am) at 3s interval = ~60s runtime. Main agent manual runs: ~3-5s/call.
26. **Skill Generation Works Best as Single Script** — Batching 349 completed analyses into 29 skill groups via single Python script produced 29 skills in <1s. Sub-agents create skills one-at-a-time (slow) and timeout.
27. **Obsidian Vault Built from Skill Groups** — 81 technique category notes with wiki links to master index. Each note aggregates techniques by primary tag.
28. **Memory Update Discipline** — Memory tool only for durable facts (user prefs, env, conventions). Session progress goes in session DB.
29. **Two Separate DaVinci Pipelines** — (a) **Video Effects Pipeline**: 370 reels via downreels.com → 334 skills + 737 notes in `Video_Effects/`. (b) **Color Grading Techniques Pipeline**: 1,165 reels via NVIDIA vision_analyze (Gemini) → 145 skills + 81 vault notes in `DaVinci-Techniques/`. Do not mix outputs.
30. **NVIDIA Vision via Hermes Only** — `vision_analyze` tool requires main agent context; sub-agents cannot use it. Batch vision analysis must run in main agent loop with rate limiting.
31. **Ollama Cloud for Sub-Agent Text Generation** — Sub-agents configured with `provider: ollama-cloud`, `model: gemma4:31b-cloud` work reliably for skill generation and vault notes. Main agent uses NVIDIA for vision.
32. **Hermes Config Must Be Explicit** — Delegation config needs `provider: ollama-cloud`, `model: gemma4:31b-cloud`, `api_key` set. Main model config needs `provider: nvidia`, `model: nvidia/nemotron-3-ultra-550b-a55b`.
33. **Vision Analysis Batch Size** — 20 frames per cron run (3am) at 3s interval = ~60s runtime. Main agent manual runs: ~3-5s/call.
34. **Skill Generation Works Best as Single Script** — Batching 349 completed analyses into 29 skill groups via single Python script produced 29 skills in <1s. Sub-agents create skills one-at-a-time (slow) and timeout.
35. **Obsidian Vault Built from Skill Groups** — 81 technique category notes with wiki links to master index. Each note aggregates techniques by primary tag.
36. **Memory Update Discipline** — Memory tool only for durable facts (user prefs, env, conventions). Session progress goes in session DB.
37. **Local Ollama Vision Pipeline (NEW 2026-07-31)** — `llava:7b` via Ollama API (`http://localhost:11434/api/generate`) processes frames at ~40-50s for 3 frames (vs NVIDIA 3-5s + 20 RPM limit). Requires: Ollama running, model pulled (`ollama pull llava:7b`), Python script with `requests` calling API. No rate limits, fully local. Sub-agents CANNOT use this.
38. **Parallel Background Processing (NEW 2026-07-31)** — Launch multiple `terminal(background=true, notify_on_complete=true)` processes, each running a Python chunk script on disjoint video index ranges. 4 parallel chunks processed 135 videos in ~25 min vs 1.5 hrs sequential. GPU contention slows per-video time (~150-200s vs 40s sequential) but net throughput is 3-4x higher. Monitor with `process(action="poll", session_id)`.
39. **Vault Note Backfill for Complete Videos (NEW 2026-07-31)** — 430 complete videos missing vault notes generated in single script run. Script reads `VISION_PROGRESS.json`, checks vault for existing `video_id` in frontmatter, generates notes with embedded GIFs (from frames via ffmpeg), links to existing skills. 2,046 notes created (includes duplicates). Vault now covers 1,005/1,030 complete videos.
40. **Storage Cleanup Critical (NEW 2026-07-31)** — Samsung LED `gifs/` folder accumulates redundant full-video GIFs (45 GB). Vault already has embedded GIFs in `vault/media/` (81 MB). Delete `gifs/` after verifying vault coverage. `frames/` for completed videos can be deleted (keep error/pending only).
41. **Duplicate Downloads Identified (NEW 2026-07-31)** — `~/Downloads/instagram_downloads/` is byte-for-byte duplicate of Samsung LED content (407 MB). Safe to delete.
42. **Internal Drive Cleanup (NEW 2026-07-31)** — `~/Downloads/instagram_downloads/` (407 MB) + old export (28 MB) = 435 MB freed on internal drive.
43. **TamaZila Vault Migration Plan (NEW 2026-07-31)** — Move `~/TamaZila Obsidian Vault/` to Samsung LED (27 GB) after cleaning Samsung LED, symlink back. Internal freed for merged DaVinci vault.
44. **Vault Reorganization Complete (NEW 2026-07-31)** — Techniques moved from flat `techniques/` into 7 domain folders (Color Grading & Looks: 854, Camera Theory: 5, Lighting: 2, Fusion: 75, Photography_Videography: 1, Post_Production: 98, Video_Effects: 7). Each domain gets `index.md` with technique table. Frontmatter updated with `domain`, `moved_at`, `skill`, `analysis` links. Empty `techniques/` root folder now empty.
45. **Domain Index.md Files Created (NEW 2026-07-31)** — Each domain folder gets `index.md` with technique table (title, video_id, collection, page, tags, skill, analysis, difficulty). Auto-generated via `create_domain_indexes.py`.
46. **Mapping Files Regenerated (NEW 2026-07-31)** — `knowledge_base_export.json`, `knowledge_base_export.csv`, `skills_export.json`, `skills_export.csv` regenerated via `regenerate_mappings.py`. Domain `index.md` files serve as per-folder mapping.
47. **Vault Note Backfill Complete (NEW 2026-07-31)** — 430 complete videos missing vault notes generated in single script run. 2,046 notes created (includes duplicates). Vault now covers 1,005/1,030 complete videos.
41. **Storage Cleanup Complete (NEW 2026-07-31)** — Samsung LED `gifs/` (45 GB), completed `frames/` (7.4 GB), `~/Downloads/instagram_downloads/` (407 MB) deleted. Samsung LED: 5.4 GB → 61 GB free. Internal: 2.5 GB → 12 GB free.
42. **Remaining Pipeline Work (NEW 2026-07-31)** — 135 videos remaining (116 error + 19 pending) with frames ready on Samsung LED. Local llava:7b pipeline ready to process directly into organized vault structure.
43. **Media Cleanup & Validation (NEW 2026-07-31)** — 643 empty/corrupted GIFs (61% of 1,048) deleted from `media/`. Valid GIFs: 405. `media/index.md` and `MASTER_MAPPING.md` updated (Media GIFs: 2,096 → 405). Always validate GIFs with `file` command before indexing.
44. **Vault Reorganization Pattern (NEW 2026-07-31)** — Flat `techniques/` (1,023 files) reorganized into 7 domain folders (Color Grading & Looks: 854, Camera Theory: 5, Lighting: 2, Fusion: 75, Photography_Videography: 1, Post_Production: 98, Video_Effects: 7). Each domain gets auto-generated `index.md` with technique table (title, video_id, collection, page, tags, skill, analysis, difficulty). Frontmatter updated with `domain`, `moved_at`, `skill`, `analysis` links.
47. **Local Ollama Vision Pipeline (NEW 2026-07-31)** — `llava:7b` via Ollama API (`http://localhost:11434/api/generate`) processes frames at ~40-50s for 3 frames (vs NVIDIA 3-5s + 20 RPM limit). Requires: Ollama running, model pulled (`ollama pull llava:7b`), Python script with `requests` calling API. No rate limits, fully local. Sub-agents CANNOT use this.
48. **Parallel Background Processing (NEW 2026-07-31)** — Launch multiple `terminal(background=true, notify_on_complete=true)` processes, each running a Python chunk script on disjoint video index ranges. 4 parallel chunks processed 135 videos in ~25 min vs 1.5 hrs sequential. GPU contention slows per-video time (~150-200s vs 40s sequential) but net throughput is 3-4x higher. Monitor with `process(action="poll", session_id)`.
49. **Vault Note Backfill for Complete Videos (NEW 2026-07-31)** — 430 complete videos missing vault notes generated in single script run. Script reads `VISION_PROGRESS.json`, checks vault for existing `video_id` in frontmatter, generates notes with embedded GIFs (from frames via ffmpeg), links to existing skills. 2,046 notes created (includes duplicates). Vault now covers 1,005/1,030 complete videos.
50. **MASTER_MAPPING.md as Single Source of Truth** — All 130+ index files updated to reference `MASTER_MAPPING.md` instead of deleted `Memory.md`/`index.md`. `Hero_index.md` (vault root) points to `MASTER_MAPPING.md` as DaVinci KB entry point. `MASTER_MAPPING.md` consolidates: architectural hierarchy, domain folder inventory, support folder indexes, cross-reference map, pipeline tracking, maintenance commands, quick navigation.
48. **Hero_index.md as Vault Root Entry Point** — All DaVinci KB references in vault root `Hero_index.md` updated to `MASTER_MAPPING.md`. Other domains (Developer Workflows, Forex, Photography) correctly still point to their own `Memory.md`.
50. **Mapping File Cascade Protocol** — When adding content: 1) Create/update folder mapping (e.g., `00-MASTER-INDEX.md`), 2) Update parent folder mapping, 3) Cascade up to `MASTER_MAPPING.md`, 4) Update `Hero_index.md`. Ensures consistency from leaf → root.
49. **Media Validation Protocol** — Always validate GIFs with `file` command before indexing. 643/1048 (61%) GIFs were empty/corrupted. Use `file` batch check: `for f in media/*.gif; do if [ "$(file -b "$f")" = "empty" ]; then rm "$f"; fi; done`. Update `media/index.md` and `MASTER_MAPPING.md` after cleanup.
6. **GIF regeneration recovers from download failures** — 246/249 missing GIFs recovered via parallel pipeline runs
7. **Temp cleanup verification is critical** — always verify `du -sh temp/` == 0B after batch completes
8. **Hermes skills are separate from vault skills** — copy to `~/.hermes/skills/creative/` for discoverability via `hermes skills list | grep davinci-reel`
9. **PyTorch/Whisper environment issue** — Whisper transcription fails with `torch/_C` folder error on Mac Mini M4 (Python 3.14); transcription skipped but frames/GIFs still extracted. Use faster-whisper with CPU fallback or run Python from different directory to avoid torch/_C namespace conflict.
10. **Storage monitoring critical** — Mac Mini 228GB SSD hit 100% capacity (1.2GB free) during batch; temp folder hit 7.2GB. Must monitor `df -h` and clean temp proactively.
11. **Video Effects pipeline is separate** — 368 reels processed in Video_Effects/ with 11 transition techniques cataloged; separate queue from Photography/Videography
12. **Cross-link all index files** — Memory.md, Cross_Reference_Index.md, Architecture_Diagram.md, Hero_index.md, START_HERE.md all need new pipeline entries
13. **Architecture diagram updates** — mermaid graph must include Instagram_Reels subgraph with MASTER_INDEX node
14. **Draw Things AI models storage** — 32GB in `~/Library/Containers/com.liuliu.draw-things/Data/Documents/Models/` (Flux, SDXL, Qwen, CLIP, VAE, LoRA). Essential for Draw Things app. Can move to external SSD with symlink: `ln -s /Volumes/External/Models ~/Library/Containers/com.liuliu.draw-things/Data/Documents/Models`
15. **Frame directory IDs are downreels.com internal, NOT Instagram short IDs** — manifest's `frames_dir` field maps to actual frame directories. Use this field, not reel_id, for vision analysis.
16. **Auto-compression failure at 95% context** — Session grew unchecked due to provider/base_url mismatch (NVIDIA provider pointing to local Ollama). Fix: point NVIDIA provider to `https://integrate.api.nvidia.com/v1` directly.
17. **Background processing with notify_on_complete** — Proven pattern for long pipelines (370 Video Effects reels in background, PID 13309). Use `terminal(background=true, notify_on_complete=true)` with rate-limited vision calls (20 RPM, 3s minimum). Check status via `process(action="poll", session_id=...)`.
18. **downreels.com as primary downloader** — Established over yt-dlp+cookies; slower (4s/reel) but more reliable, zero-auth. Reinstall greenlet if Playwright fails: `pip install --force-reinstall --no-binary greenlet greenlet`.
19. **Vision rate limit (20 RPM / 3s) is hard constraint** — Enforced in all vision analysis stages.
20. **Vault path discipline** — All outputs MUST use exact TamaZila Obsidian Vault path (`/Users/alfredkamisese/TamaZila Obsidian Vault/Hermes Agent/DaVinci_Knowledge_Base/`).
21. **GIF copy before cleanup is mandatory** — Copy to vault BEFORE `cleanup_reel()` deletes temp.
22. **Index cross-linking should be automated** — 5 index files need updating; consider `regenerate_indexes.py`.
23. **Architecture diagram discipline** — Mermaid graph MUST include Instagram_Reels subgraph with MASTER_INDEX node.
24. **Storage budget monitoring** — Samsung LED SSD (120GB): ~70GB free baseline; pipeline temp ~7.2GB; monitor `df -h` before each batch.
25. **Photography/Videography collection (389 URLs)** — Download started in background; separate queue from Video Effects (370 URLs, 334 skills + 737 notes done).
26. **Skill organization** — Video Effects: `davinci-video-effect-{reel_id[:8]}/`; Photography: `davinci-photography-portrait-{id}/`
27. **Skill auto-installation to Hermes** — Copy generated skills to `~/.hermes/skills/creative/` for immediate discoverability via `hermes skills list | grep davinci-reel`
28. **Cross-link all index files** — Memory.md, Cross_Reference_Index.md, Architecture_Diagram.md, Hero_index.md, START_HERE.md all need new pipeline entries
29. **Architecture diagram updates** — Mermaid graph MUST include Instagram_Reels subgraph with MASTER_INDEX node
30. **Parallel pipeline execution works** — Two simultaneous GIF regen processes covered each other's failures; rate limit handling via exponential backoff (30s→60s→120s→240s→480s).
31. **Video Effects pipeline complete** — 334/368 reels processed (91% frame extraction rate); 34 failed at download/extract. 334 skills + 737 vault notes created.
32. **Background process monitoring** — Use `process(action="poll", session_id)` and `process(action="log", session_id, limit=50)` to check long-running pipeline status.
33. **Frame directory ID mapping** — Frame folders use downreels.com internal IDs; manifest's `frames_dir` field provides correct path. Always use manifest's `frames_dir` for vision analysis, not reel_id.
34. **Auto-compression provider fix** — NVIDIA provider must point to `https://integrate.api.nvidia.com/v1` not local Ollama. Verify with `hermes config get` before long sessions.
35. **Vision rate limit (20 RPM / 3s) is hard constraint** — Enforced in all vision analysis stages.
36. **Vault path discipline** — All outputs MUST use exact TamaZila Obsidian Vault path.
37. **GIF copy before cleanup is mandatory** — Copy to vault BEFORE cleanup_reel() deletes temp.
38. **Index cross-linking should be automated** — 5 index files need updating; consider regenerate_indexes.py.
39. **Architecture diagram discipline** — Mermaid graph MUST include Instagram_Reels subgraph with MASTER_INDEX node.
40. **Storage budget monitoring** — Samsung LED SSD (120GB): ~70GB free baseline; pipeline temp ~7.2GB; monitor `df -h` before each batch.
41. **Photography/Videography collection (389 URLs)** — Download started in background; separate queue from Video Effects.
42. **Skill organization** — Video Effects: `davinci-video-effect-{reel_id[:8]}/`; Photography: `davinci-photography-portrait-{id}/`
43. **Skill auto-installation to Hermes** — Copy generated skills to `~/.hermes/skills/creative/` for immediate discoverability via `hermes skills list | grep davinci-reel`
44. **Cross-link all index files** — Memory.md, Cross_Reference_Index.md, Architecture_Diagram.md, Hero_index.md, START_HERE.md all need new pipeline entries
45. **Architecture diagram updates** — Mermaid graph MUST include Instagram_Reels subgraph with MASTER_INDEX node
46. **Parallel pipeline execution works** — Two simultaneous GIF regen processes covered each other's failures; rate limit handling via exponential backoff (30s→60s→120s→240s→480s).
47. **Video Effects pipeline complete** — 334/368 reels processed (91% frame extraction rate); 34 failed at download/extract. 334 skills + 737 vault notes created.
48. **Background process monitoring** — Use `process(action="poll", session_id)` and `process(action="log", session_id, limit=50)` to check long-running pipeline status.
49. **Frame directory ID mapping** — Frame folders use downreels.com internal IDs; manifest's `frames_dir` field provides correct path. Always use manifest's `frames_dir` for vision analysis, not reel_id.
50. **Auto-compression provider fix** — NVIDIA provider must point to `https://integrate.api.nvidia.com/v1` not local Ollama. Verify with `hermes config get` before long sessions.
51. **Vision rate limit (20 RPM / 3s) is hard constraint** — Enforced in all vision analysis stages.
52. **Vault path discipline** — All outputs MUST use exact TamaZila Obsidian Vault path.
53. **GIF copy before cleanup is mandatory** — Copy to vault BEFORE cleanup_reel() deletes temp.
54. **Index cross-linking should be automated** — 5 index files need updating; consider regenerate_indexes.py.
55. **Architecture diagram discipline** — Mermaid graph MUST include Instagram_Reels subgraph with MASTER_INDEX node.
56. **Storage budget monitoring** — Samsung LED SSD (120GB): ~70GB free baseline; pipeline temp ~7.2GB; monitor `df -h` before each batch.
57. **Photography/Videography collection (389 URLs)** — Download started in background; separate queue from Video Effects.
58. **Skill organization** — Video Effects: `davinci-video-effect-{reel_id[:8]}/`; Photography: `davinci-photography-portrait-{id}/`
59. **Skill auto-installation to Hermes** — Copy generated skills to `~/.hermes/skills/creative/` for immediate discoverability via `hermes skills list | grep davinci-reel`
60. **Cross-link all index files** — Memory.md, Cross_Reference_Index.md, Architecture_Diagram.md, Hero_index.md, START_HERE.md all need new pipeline entries
61. **Architecture diagram updates** — Mermaid graph MUST include Instagram_Reels subgraph with MASTER_INDEX node
62. **Parallel pipeline execution works** — Two simultaneous GIF regen processes covered each other's failures; rate limit handling via exponential backoff (30s→60s→120s→240s→480s).
63. **Video Effects pipeline complete** — 334/368 reels processed (91% frame extraction rate); 34 failed at download/extract. 334 skills + 737 vault notes created.
64. **Background process monitoring** — Use `process(action="poll", session_id)` and `process(action="log", session_id, limit=50)` to check long-running pipeline status.
65. **Frame directory ID mapping** — Frame folders use downreels.com internal IDs; manifest's `frames_dir` field provides correct path. Always use manifest's `frames_dir` for vision analysis, not reel_id.
66. **Auto-compression provider fix** — NVIDIA provider must point to `https://integrate.api.nvidia.com/v1` not local Ollama. Verify with `hermes config get` before long sessions.
67. **Vision rate limit (20 RPM / 3s) is hard constraint** — Enforced in all vision analysis stages.
68. **Vault path discipline** — All outputs MUST use exact TamaZila Obsidian Vault path.
69. **GIF copy before cleanup is mandatory** — Copy to vault BEFORE cleanup_reel() deletes temp.
70. **Index cross-linking should be automated** — 5 index files need updating; consider regenerate_indexes.py.
71. **Architecture diagram discipline** — Mermaid graph MUST include Instagram_Reels subgraph with MASTER_INDEX node.
72. **Storage budget monitoring** — Samsung LED SSD (120GB): ~70GB free baseline; pipeline temp ~7.2GB; monitor `df -h` before each batch.
73. **Photography/Videography collection (389 URLs)** — Download started in background; separate queue from Video Effects.
74. **Skill organization** — Video Effects: `davinci-video-effect-{reel_id[:8]}/`; Photography: `davinci-photography-portrait-{id}/`
75. **Skill auto-installation to Hermes** — Copy generated skills to `~/.hermes/skills/creative/` for immediate discoverability via `hermes skills list | grep davinci-reel`
76. **Cross-link all index files** — Memory.md, Cross_Reference_Index.md, Architecture_Diagram.md, Hero_index.md, START_HERE.md all need new pipeline entries
77. **Architecture diagram updates** — Mermaid graph MUST include Instagram_Reels subgraph with MASTER_INDEX node
78. **Parallel pipeline execution works** — Two simultaneous GIF regen processes covered each other's failures; rate limit handling via exponential backoff (30s→60s→120s→240s→480s).
79. **Video Effects pipeline complete** — 334/368 reels processed (91% frame extraction rate); 34 failed at download/extract. 334 skills + 737 vault notes created.
80. **Background process monitoring** — Use `process(action="poll", session_id)` and `process(action="log", session_id, limit=50)` to check long-running pipeline status.
81. **Frame directory ID mapping** — Frame folders use downreels.com internal IDs; manifest's `frames_dir` field provides correct path. Always use manifest's `frames_dir` for vision analysis, not reel_id.
82. **Auto-compression provider fix** — NVIDIA provider must point to `https://integrate.api.nvidia.com/v1` not local Ollama. Verify with `hermes config get` before long sessions.
83. **Vision rate limit (20 RPM / 3s) is hard constraint** — Enforced in all vision analysis stages.
84. **Vault path discipline** — All outputs MUST use exact TamaZila Obsidian Vault path.
85. **GIF copy before cleanup is mandatory** — Copy to vault BEFORE cleanup_reel() deletes temp.
86. **Index cross-linking should be automated** — 5 index files need updating; consider regenerate_indexes.py.
87. **Architecture diagram discipline** — Mermaid graph MUST include Instagram_Reels subgraph with MASTER_INDEX node.
88. **Storage budget monitoring** — Samsung LED SSD (120GB): ~70GB free baseline; pipeline temp ~7.2GB; monitor `df -h` before each batch.
89. **Photography/Videography collection (389 URLs)** — Download started in background; separate queue from Video Effects.
90. **Skill organization** — Video Effects: `davinci-video-effect-{reel_id[:8]}/`; Photography: `davinci-photography-portrait-{id}/`
91. **Skill auto-installation to Hermes** — Copy generated skills to `~/.hermes/skills/creative/` for immediate discoverability via `hermes skills list | grep davinci-reel`
92. **Cross-link all index files** — Memory.md, Cross_Reference_Index.md, Architecture_Diagram.md, Hero_index.md, START_HERE.md all need new pipeline entries
93. **Architecture diagram updates** — Mermaid graph MUST include Instagram_Reels subgraph with MASTER_INDEX node
94. **Parallel pipeline execution works** — Two simultaneous GIF regen processes covered each other's failures; rate limit handling via exponential backoff (30s→60s→120s→240s→480s).
95. **Video Effects pipeline complete** — 334/368 reels processed (91% frame extraction rate); 34 failed at download/extract. 334 skills + 737 vault notes created.
96. **Background process monitoring** — Use `process(action="poll", session_id)` and `process(action="log", session_id, limit=50)` to check long-running pipeline status.
97. **Frame directory ID mapping** — Frame folders use downreels.com internal IDs; manifest's `frames_dir` field provides correct path. Always use manifest's `frames_dir` for vision analysis, not reel_id.
97. **Auto-compression provider fix** — NVIDIA provider must point to `https://integrate.api.nvidia.com/v1` not local Ollama. Verify with `hermes config get` before long sessions.
98. **Vision rate limit (20 RPM / 3s) is hard constraint** — Enforced in all vision analysis stages.
98. **Vault path discipline** — All outputs MUST use exact TamaZila Obsidian Vault path.
98. **GIF copy before cleanup is mandatory** — Copy to vault BEFORE cleanup_reel() deletes temp.
98. **Index cross-linking should be automated** — 5 index files need updating; consider regenerate_indexes.py.
98. **Architecture diagram discipline** — Mermaid graph MUST include Instagram_Reels subgraph with MASTER_INDEX node.
98. **Storage budget monitoring** — Samsung LED SSD (120GB): ~70GB free baseline; pipeline temp ~7.2GB; monitor `df -h` before each batch.
98. **Photography/Videography collection (389 URLs)** — Download started in background; separate queue from Video Effects.
98. **Skill organization** — Video Effects: `davinci-video-effect-{reel_id[:8]}/`; Photography: `davinci-photography-portrait-{id}/`
98. **Skill auto-installation to Hermes** — Copy generated skills to `~/.hermes/skills/creative/` for immediate discoverability via `hermes skills list | grep davinci-reel`
98. **Cross-link all index files** — Memory.md, Cross_Reference_Index.md, Architecture_Diagram.md, Hero_index.md, START_HERE.md all need new pipeline entries
98. **Architecture diagram updates** — Mermaid graph MUST include Instagram_Reels subgraph with MASTER_INDEX node
98. **Parallel pipeline execution works** — Two simultaneous GIF regen processes covered each other's failures; rate limit handling via exponential backoff (30s→60s→120s→240s→480s).
99. **Video Effects pipeline complete** — 334/368 reels processed (91% frame extraction rate); 34 failed at download/extract. 334 skills + 737 vault notes created.
99. **Background process monitoring** — Use `process(action="poll", session_id)` and `process(action="log", session_id, limit=50)` to check long-running pipeline status.
99. **Frame directory ID mapping** — Frame folders use downreels.com internal IDs; manifest's `frames_dir` field provides correct path. Always use manifest's `frames_dir` for vision analysis, not reel_id.
99. **Auto-compression provider fix** — NVIDIA provider must point to `https://integrate.api.nvidia.com/v1` not local Ollama. Verify with `hermes config get` before long sessions.
99. **Vision rate limit (20 RPM / 3s) is hard constraint** — Enforced in all vision analysis stages.
99. **Vault path discipline** — All outputs MUST use exact TamaZila Obsidian Vault path.
99. **GIF copy before cleanup is mandatory** — Copy to vault BEFORE cleanup_reel() deletes temp.
99. **Index cross-linking should be automated** — 5 index files need updating; consider regenerate_indexes.py.
100. **Architecture diagram discipline** — Mermaid graph MUST include Instagram_Reels subgraph with MASTER_INDEX node.
100. **Storage budget monitoring** — Samsung LED SSD (120GB): ~70GB free baseline; pipeline temp ~7.2GB; monitor `df -h` before each batch.
100. **Photography/Videography collection (389 URLs)** — Download started in background; separate queue from Video Effects.
100. **Skill organization** — Video Effects: `davinci-video-effect-{reel_id[:8]}/`; Photography: `davinci-photography-portrait-{id}/`
100. **Skill auto-installation to Hermes** — Copy generated skills to `~/.hermes/skills/creative/` for immediate discoverability via `hermes skills list | grep davinci-reel`
100. **Cross-link all index files** — Memory.md, Cross_Reference_Index.md, Architecture_Diagram.md, Hero_index.md, START_HERE.md all need new pipeline entries
100. **Architecture diagram updates** — Mermaid graph MUST include Instagram_Reels subgraph with MASTER_INDEX node
100. **Parallel pipeline execution works** — Two simultaneous GIF regen processes covered each other's failures; rate limit handling via exponential backoff (30s→60s→120s→240s→480s).
101. **Video Effects pipeline complete** — 334/368 reels processed (91% frame extraction rate); 34 failed at download/extract. 334 skills + 737 vault notes created.
101. **Background process monitoring** — Use `process(action="poll", session_id)` and `process(action="log", session_id, limit=50)` to check long-running pipeline status.
101. **Frame directory ID mapping** — Frame folders use downreels.com internal IDs; manifest's `frames_dir` field provides correct path. Always use manifest's `frames_dir` for vision analysis, not reel_id.
101. **Auto-compression provider fix** — NVIDIA provider must point to `https://integrate.api.nvidia.com/v1` not local Ollama. Verify with `hermes config get` before long sessions.
101. **Vision rate limit (20 RPM / 3s) is hard constraint** — Enforced in all vision analysis stages.
101. **Vault path discipline** — All outputs MUST use exact TamaZila Obsidian Vault path.
101. **GIF copy before cleanup is mandatory** — Copy to vault BEFORE cleanup_reel() deletes temp.
101. **Index cross-linking should be automated** — 5 index files need updating; consider regenerate_indexes.py.
102. **Architecture diagram discipline** — Mermaid graph MUST include Instagram_Reels subgraph with MASTER_INDEX node.
102. **Storage budget monitoring** — Samsung LED SSD (120GB): ~70GB free baseline; pipeline temp ~7.2GB; monitor `df -h` before each batch.
102. **Photography/Videography collection (389 URLs)** — Download started in background; separate queue from Video Effects.
102. **Skill organization** — Video Effects: `davinci-video-effect-{reel_id[:8]}/`; Photography: `davinci-photography-portrait-{id}/`
102. **Skill auto-installation to Hermes** — Copy generated skills to `~/.hermes/skills/creative/` for immediate discoverability via `hermes skills list | grep davinci-reel`
102. **Cross-link all index files** — Memory.md, Cross_Reference_Index.md, Architecture_Diagram.md, Hero_index.md, START_HERE.md all need new pipeline entries
102. **Architecture diagram updates** — Mermaid graph MUST include Instagram_Reels subgraph with MASTER_INDEX node
102. **Parallel pipeline execution works** — Two simultaneous GIF regen processes covered each other's failures; rate limit handling via exponential backoff (30s→60s→120s→240s→480s).
103. **Video Effects pipeline complete** — 334/368 reels processed (91% frame extraction rate); 34 failed at download/extract. 334 skills + 737 vault notes created.
103. **Background process monitoring** — Use `process(action="poll", session_id)` and `process(action="log", session_id, limit=50)` to check long-running pipeline status.
103. **Frame directory ID mapping** — Frame folders use downreels.com internal IDs; manifest's `frames_dir` field provides correct path. Always use manifest's `frames_dir` for vision analysis, not reel_id.
103. **Auto-compression provider fix** — NVIDIA provider must point to `https://integrate.api.nvidia.com/v1` not local Ollama. Verify with `hermes config get` before long sessions.
103. **Vision rate limit (20 RPM / 3s) is hard constraint** — Enforced in all vision analysis stages.
103. **Vault path discipline** — All outputs MUST use exact TamaZila Obsidian Vault path.
103. **GIF copy before cleanup is mandatory** — Copy to vault BEFORE cleanup_reel() deletes temp.
103. **Index cross-linking should be automated** — 5 index files need updating; consider regenerate_indexes.py.
104. **Architecture diagram discipline** — Mermaid graph MUST include Instagram_Reels subgraph with MASTER_INDEX node.
104. **Storage budget monitoring** — Samsung LED SSD (120GB): ~70GB free baseline; pipeline temp ~7.2GB; monitor `df -h` before each batch.
104. **Photography/Videography collection (389 URLs)** — Download started in background; separate queue from Video Effects.
104. **Skill organization** — Video Effects: `davinci-video-effect-{reel_id[:8]}/`; Photography: `davinci-photography-portrait-{id}/`
104. **Skill auto-installation to Hermes** — Copy generated skills to `~/.hermes/skills/creative/` for immediate discoverability via `hermes skills list | grep davinci-reel`
104. **Cross-link all index files** — Memory.md, Cross_Reference_Index.md, Architecture_Diagram.md, Hero_index.md, START_HERE.md all need new pipeline entries
104. **Architecture diagram updates** — Mermaid graph MUST include Instagram_Reels subgraph with MASTER_INDEX node
104. **Parallel pipeline execution works** — Two simultaneous GIF regen processes covered each other's failures; rate limit handling via exponential backoff (30s→60s→120s→240s→480s).
105. **Video Effects pipeline complete** — 334/368 reels processed (91% frame extraction rate); 34 failed at download/extract. 334 skills + 737 vault notes created.
105. **Background process monitoring** — Use `process(action="poll", session_id)` and `process(action="log", session_id, limit=50)` to check long-running pipeline status.
105. **Frame directory ID mapping** — Frame folders use downreels.com internal IDs; manifest's `frames_dir` field provides correct path. Always use manifest's `frames_dir` for vision analysis, not reel_id.
103. **Auto-compression provider fix** — NVIDIA provider must point to `https://integrate.api.nvidia.com/v1` not local Ollama. Verify with `hermes config get` before long sessions.
103. **Vision rate limit (20 RPM / 3s) is hard constraint** — Enforced in all vision analysis stages.
103. **Vault path discipline** — All outputs MUST use exact TamaZila Obsidian Vault path.
103. **GIF copy before cleanup is mandatory** — Copy to vault BEFORE cleanup_reel() deletes temp.
103. **Index cross-linking should be automated** — 5 index files need updating; consider regenerate_indexes.py.
104. **Architecture diagram discipline** — Mermaid graph MUST include Instagram_Reels subgraph with MASTER_INDEX node.
104. **Storage budget monitoring** — Samsung LED SSD (120GB): ~70GB free baseline; pipeline temp ~7.2GB; monitor `df -h` before each batch.
104. **Photography/Videography collection (389 URLs)** — Download started in background; separate queue from Video Effects.
104. **Skill organization** — Video Effects: `davinci-video-effect-{reel_id[:8]}/`; Photography: `davinci-photography-portrait-{id}/`
104. **Skill auto-installation to Hermes** — Copy generated skills to `~/.hermes/skills/creative/` for immediate discoverability via `hermes skills list | grep davinci-reel`
104. **Cross-link all index files** — Memory.md, Cross_Reference_Index.md, Architecture_Diagram.md, Hero_index.md, START_HERE.md all need new pipeline entries
104. **Architecture diagram updates** — Mermaid graph MUST include Instagram_Reels subgraph with MASTER_INDEX node
104. **Parallel pipeline execution works** — Two simultaneous GIF regen processes covered each other's failures; rate limit handling via exponential backoff (30s→60s→120s→240s→480s).
105. **Video Effects pipeline complete** — 334/368 reels processed (91% frame extraction rate); 34 failed at download/extract. 334 skills + 737 vault notes created.
105. **Background process monitoring** — Use `process(action="poll", session_id)` and `process(action="log", session_id, limit=50)` to check long-running pipeline status.
105. **Frame directory ID mapping** — Frame folders use downreels.com internal IDs; manifest's `frames_dir` field provides correct path. Always use manifest's `frames_dir` for vision analysis, not reel_id.
105. **Auto-compression provider fix** — NVIDIA provider must point to `https://integrate.api.nvidia.com/v1` not local Ollama. Verify with `hermes config get` before long sessions.
105. **Vision rate limit (20 RPM / 3s) is hard constraint** — Enforced in all vision analysis stages.
105. **Vault path discipline** — All outputs MUST use exact TamaZila Obsidian Vault path.
105. **GIF copy before cleanup is mandatory** — Copy to vault BEFORE cleanup_reel() deletes temp.
105. **Index cross-linking should be automated** — 5 index files need updating; consider regenerate_indexes.py.
106. **Architecture diagram discipline** — Mermaid graph MUST include Instagram_Reels subgraph with MASTER_INDEX node.
106. **Storage budget monitoring** — Samsung LED SSD (120GB): ~70GB free baseline; pipeline temp ~7.2GB; monitor `df -h` before each batch.
106. **Photography/Videography collection (389 URLs)** — Download started in background; separate queue from Video Effects.
106. **Skill organization** — Video Effects: `davinci-video-effect-{reel_id[:8]}/`; Photography: `davinci-photography-portrait-{id}/`
106. **Skill auto-installation to Hermes** — Copy generated skills to `~/.hermes/skills/creative/` for immediate discoverability via `hermes skills list | grep davinci-reel`
106. **Cross-link all index files** — Memory.md, Cross_Reference_Index.md, Architecture_Diagram.md, Hero_index.md, START_HERE.md all need new pipeline entries
106. **Architecture diagram updates** — Mermaid graph MUST include Instagram_Reels subgraph with MASTER_INDEX node
106. **Parallel pipeline execution works** — Two simultaneous GIF regen processes covered each other's failures; rate limit handling via exponential backoff (30s→60s→120s→240s→480s).
107. **Video Effects pipeline complete** — 334/368 reels processed (91% frame extraction rate); 34 failed at download/extract. 334 skills + 737 vault notes created.
107. **Background process monitoring** — Use `process(action="poll", session_id)` and `process(action="log", session_id, limit=50)` to check long-running pipeline status.
107. **Frame directory ID mapping** — Frame folders use downreels.com internal IDs; manifest's `frames_dir` field provides correct path. Always use manifest's `frames_dir` for vision analysis, not reel_id.
107. **Auto-compression provider fix** — NVIDIA provider must point to `https://integrate.api.nvidia.com/v1` not local Ollama. Verify with `hermes config get` before long sessions.
107. **Vision rate limit (20 RPM / 3s) is hard constraint** — Enforced in all vision analysis stages.
107. **Vault path discipline** — All outputs MUST use exact TamaZila Obsidian Vault path.
107. **GIF copy before cleanup is mandatory** — Copy to vault BEFORE cleanup_reel() deletes temp.
107. **Index cross-linking should be automated** — 5 index files need updating; consider regenerate_indexes.py.
108. **Architecture diagram discipline** — Mermaid graph MUST include Instagram_Reels subgraph with MASTER_INDEX node.
108. **Storage budget monitoring** — Samsung LED SSD (120GB): ~70GB free baseline; pipeline temp ~7.2GB; monitor `df -h` before each batch.
108. **Photography/Videography collection (389 URLs)** — Download started in background; separate queue from Video Effects.
108. **Skill organization** — Video Effects: `davinci-video-effect-{reel_id[:8]}/`; Photography: `davinci-photography-portrait-{id}/`
108. **Skill auto-installation to Hermes** — Copy generated skills to `~/.hermes/skills/creative/` for immediate discoverability via `hermes skills list | grep davinci-reel`
108. **Cross-link all index files** — Memory.md, Cross_Reference_Index.md, Architecture_Diagram.md, Hero_index.md, START_HERE.md all need new pipeline entries
108. **Architecture diagram updates** — Mermaid graph MUST include Instagram_Reels subgraph with MASTER_INDEX node
108. **Parallel pipeline execution works** — Two simultaneous GIF regen processes covered each other's failures; rate limit handling via exponential backoff (30s→60s→120s→240s→480s).
109. **Video Effects pipeline complete** — 334/368 reels processed (91% frame extraction rate); 34 failed at download/extract. 334 skills + 737 vault notes created.
109. **Background process monitoring** — Use `process(action="poll", session_id)` and `process(action="log", session_id, limit=50)` to check long-running pipeline status.
109. **Frame directory ID mapping** — Frame folders use downreels.com internal IDs; manifest's `frames_dir` field provides correct path. Always use manifest's `frames_dir` for vision analysis, not reel_id.
109. **Auto-compression provider fix** — NVIDIA provider must point to `https://integrate.api.nvidia.com/v1` not local Ollama. Verify with `hermes config get` before long sessions.
109. **Vision rate limit (20 RPM / 3s) is hard constraint** — Enforced in all vision analysis stages.
109. **Vault path discipline** — All outputs MUST use exact TamaZila Obsidian Vault path.
109. **GIF copy before cleanup is mandatory** — Copy to vault BEFORE cleanup_reel() deletes temp.
109. **Index cross-linking should be automated** — 5 index files need updating; consider regenerate_indexes.py.
110. **Architecture diagram discipline** — Mermaid graph MUST include Instagram_Reels subgraph with MASTER_INDEX node.
110. **Storage budget monitoring** — Samsung LED SSD (120GB): ~70GB free baseline; pipeline temp ~7.2GB; monitor `df -h` before each batch.
110. **Photography/Videography collection (389 URLs)** — Download started in background; separate queue from Video Effects.
110. **Skill organization** — Video Effects: `davinci-video-effect-{reel_id[:8]}/`; Photography: `davinci-photography-portrait-{id}/`
110. **Skill auto-installation to Hermes** — Copy generated skills to `~/.hermes/skills/creative/` for immediate discoverability via `hermes skills list | grep davinci-reel`
110. **Cross-link all index files** — Memory.md, Cross_Reference_Index.md, Architecture_Diagram.md, Hero_index.md, START_HERE.md all need new pipeline entries
110. **Architecture diagram updates** — Mermaid graph MUST include Instagram_Reels subgraph with MASTER_INDEX node
110. **Parallel pipeline execution works** — Two simultaneous GIF regen processes covered each other's failures; rate limit handling via exponential backoff (30s→60s→120s→240s→480s).
111. **Video Effects pipeline complete** — 334/368 reels processed (91% frame extraction rate); 34 failed at download/extract. 334 skills + 737 vault notes created.
111. **Background process monitoring** — Use `process(action="poll", session_id)` and `process(action="log", session_id, limit=50)` to check long-running pipeline status.
111. **Frame directory ID mapping** — Frame folders use downreels.com internal IDs; manifest's `frames_dir` field provides correct path. Always use manifest's `frames_dir` for vision analysis, not reel_id.
111. **Auto-compression provider fix** — NVIDIA provider must point to `https://integrate.api.nvidia.com/v1` not local Ollama. Verify with `hermes config get` before long sessions.
111. **Vision rate limit (20 RPM / 3s) is hard constraint** — Enforced in all vision analysis stages.
111. **Vault path discipline** — All outputs MUST use exact TamaZila Obsidian Vault path.
111. **GIF copy before cleanup is mandatory** — Copy to vault BEFORE cleanup_reel() deletes temp.
111. **Index cross-linking should be automated** — 5 index files need updating; consider regenerate_indexes.py.
112. **Architecture diagram discipline** — Mermaid graph MUST include Instagram_Reels subgraph with MASTER_INDEX node.
112. **Storage budget monitoring** — Samsung LED SSD (120GB): ~70GB free baseline; pipeline temp ~7.2GB; monitor `df -h` before each batch.
112. **Photography/Videography collection (389 URLs)** — Download started in background; separate queue from Video Effects.
112. **Skill organization** — Video Effects: `davinci-video-effect-{reel_id[:8]}/`; Photography: `davinci-photography-portrait-{id}/`
112. **Skill auto-installation to Hermes** — Copy generated skills to `~/.hermes/skills/creative/` for immediate discoverability via `hermes skills list | grep davinci-reel`
112. **Cross-link all index files** — Memory.md, Cross_Reference_Index.md, Architecture_Diagram.md, Hero_index.md, START_HERE.md all need new pipeline entries
112. **Architecture diagram updates** — Mermaid graph MUST include Instagram_Reels subgraph with MASTER_INDEX node
112. **Parallel pipeline execution works** — Two simultaneous GIF regen processes covered each other's failures; rate limit handling via exponential backoff (30s→60s→120s→240s→480s).
113. **Video Effects pipeline complete** — 334/368 reels processed (91% frame extraction rate); 34 failed at download/extract. 334 skills + 737 vault notes created.
113. **Background process monitoring** — Use `process(action="poll", session_id)` and `process(action="log", session_id, limit=50)` to check long-running pipeline status.
113. **Frame directory ID mapping** — Frame folders use downreels.com internal IDs; manifest's `frames_dir` field provides correct path. Always use manifest's `frames_dir` for vision analysis, not reel_id.
113. **Auto-compression provider fix** — NVIDIA provider must point to `https://integrate.api.nvidia.com/v1` not local Ollama. Verify with `hermes config get` before long sessions.
113. **Vision rate limit (20 RPM / 3s) is hard constraint** — Enforced in all vision analysis stages.
113. **Vault path discipline** — All outputs MUST use exact TamaZila Obsidian Vault path.
113. **GIF copy before cleanup is mandatory** — Copy to vault BEFORE cleanup_reel() deletes temp.
113. **Index cross-linking should be automated** — 5 index files need updating; consider regenerate_indexes.py.
114. **Architecture diagram discipline** — Mermaid graph MUST include Instagram_Reels subgraph with MASTER_INDEX node.
114. **Storage budget monitoring** — Samsung LED SSD (120GB): ~70GB free baseline; pipeline temp ~7.2GB; monitor `df -h` before each batch.
114. **Photography/Videography collection (389 URLs)** — Download started in background; separate queue from Video Effects.
114. **Skill organization** — Video Effects: `davinci-video-effect-{reel_id[:8]}/`; Photography: `davinci-photography-portrait-{id}/`
114. **Skill auto-installation to Hermes** — Copy generated skills to `~/.hermes/skills/creative/` for immediate discoverability via `hermes skills list | grep davinci-reel`
114. **Cross-link all index files** — Memory.md, Cross_Reference_Index.md, Architecture_Diagram.md, Hero_index.md, START_HERE.md all need new pipeline entries
114. **Architecture diagram updates** — Mermaid graph MUST include Instagram_Reels subgraph with MASTER_INDEX node
114. **Parallel pipeline execution works** — Two simultaneous GIF regen processes covered each other's failures; rate limit handling via exponential backoff (30s→60s→120s→240s→480s).
115. **Video Effects pipeline complete** — 334/368 reels processed (91% frame extraction rate); 34 failed at download/extract. 334 skills + 737 vault notes created.
115. **Background process monitoring** — Use `process(action="poll", session_id)` and `process(action="log", session_id, limit=50)` to check long-running pipeline status.
115. **Frame directory ID mapping** — Frame folders use downreels.com internal IDs; manifest's `frames_dir` field provides correct path. Always use manifest's `frames_dir` for vision analysis, not reel_id.
115. **Auto-compression provider fix** — NVIDIA provider must point to `https://integrate.api.nvidia.com/v1` not local Ollama. Verify with `hermes config get` before long sessions.
115. **Vision rate limit (20 RPM / 3s) is hard constraint** — Enforced in all vision analysis stages.
115. **Vault path discipline** — All outputs MUST use exact TamaZila Obsidian Vault path.
115. **GIF copy before cleanup is mandatory** — Copy to vault BEFORE cleanup_reel() deletes temp.
115. **Index cross-linking should be automated** — 5 index files need updating; consider regenerate_indexes.py.
116. **Architecture diagram discipline** — Mermaid graph MUST include Instagram_Reels subgraph with MASTER_INDEX node.
116. **Storage budget monitoring** — Samsung LED SSD (120GB): ~70GB free baseline; pipeline temp ~7.2GB; monitor `df -h` before each batch.
116. **Photography/Videography collection (389 URLs)** — Download started in background; separate queue from Video Effects.
116. **Skill organization** — Video Effects: `davinci-video-effect-{reel_id[:8]}/`; Photography: `davinci-photography-portrait-{id}/`
116. **Skill auto-installation to Hermes** — Copy generated skills to `~/.hermes/skills/creative/` for immediate discoverability via `hermes skills list | grep davinci-reel`
116. **Cross-link all index files** — Memory.md, Cross_Reference_Index.md, Architecture_Diagram.md, Hero_index.md, START_HERE.md all need new pipeline entries
116. **Architecture diagram updates** — Mermaid graph MUST include Instagram_Reels subgraph with MASTER_INDEX node
116. **Parallel pipeline execution works** — Two simultaneous GIF regen processes covered each other's failures; rate limit handling via exponential backoff (30s→60s→120s→240s→480s).
117. **Video Effects pipeline complete** — 334/368 reels processed (91% frame extraction rate); 34 failed at download/extract. 334 skills + 737 vault notes created.
117. **Background process monitoring** — Use `process(action="poll", session_id)` and `process(action="log", session_id, limit=50)` to check long-running pipeline status.
117. **Frame directory ID mapping** — Frame folders use downreels.com internal IDs; manifest's `frames_dir` field provides correct path. Always use manifest's `frames_dir` for vision analysis, not reel_id.
117. **Auto-compression provider fix** — NVIDIA provider must point to `https://integrate.api.nvidia.com/v1` not local Ollama. Verify with `hermes config get` before long sessions.
117. **Vision rate limit (20 RPM / 3s) is hard constraint** — Enforced in all vision analysis stages.
117. **Vault path discipline** — All outputs MUST use exact TamaZila Obsidian Vault path.
117. **GIF copy before cleanup is mandatory** — Copy to vault BEFORE cleanup_reel() deletes temp.
117. **Index cross-linking should be automated** — 5 index files need updating; consider regenerate_indexes.py.
118. **Architecture diagram discipline** — Mermaid graph MUST include Instagram_Reels subgraph with MASTER_INDEX node.
118. **Storage budget monitoring** — Samsung LED SSD (120GB): ~70GB free baseline; pipeline temp ~7.2GB; monitor `df -h` before each batch.
118. **Photography/Videography collection (389 URLs)** — Download started in background; separate queue from Video Effects.
118. **Skill organization** — Video Effects: `davinci-video-effect-{reel_id[:8]}/`; Photography: `davinci-photography-portrait-{id}/`
118. **Skill auto-installation to Hermes** — Copy generated skills to `~/.hermes/skills/creative/` for immediate discoverability via `hermes skills list | grep davinci-reel`
118. **Cross-link all index files** — Memory.md, Cross_Reference_Index.md, Architecture_Diagram.md, Hero_index.md, START_HERE.md all need new pipeline entries
118. **Architecture diagram updates** — Mermaid graph MUST include Instagram_Reels subgraph with MASTER_INDEX node
118. **Parallel pipeline execution works** — Two simultaneous GIF regen processes covered each other's failures; rate limit handling via exponential backoff (30s→60s→120s→240s→480s).
119. **Video Effects pipeline complete** — 334/368 reels processed (91% frame extraction rate); 34 failed at download/extract. 334 skills + 737 vault notes created.
119. **Background process monitoring** — Use `process(action="poll", session_id)` and `process(action="log", session_id, limit=50)` to check long-running pipeline status.
119. **Frame directory ID mapping** — Frame folders use downreels.com internal IDs; manifest's `frames_dir` field provides correct path. Always use manifest's `frames_dir` for vision analysis, not reel_id.
119. **Auto-compression provider fix** — NVIDIA provider must point to `https://integrate.api.nvidia.com/v1` not local Ollama. Verify with `hermes config get` before long sessions.
119. **Vision rate limit (20 RPM / 3s) is hard constraint** — Enforced in all vision analysis stages.
119. **Vault path discipline** — All outputs MUST use exact TamaZila Obsidian Vault path.
119. **GIF copy before cleanup is mandatory** — Copy to vault BEFORE cleanup_reel() deletes temp.
119. **Index cross-linking should be automated** — 5 index files need updating; consider regenerate_indexes.py.
120. **Architecture diagram discipline** — Mermaid graph MUST include Instagram_Reels subgraph with MASTER_INDEX node.
120. **Storage budget monitoring** — Samsung LED SSD (120GB): ~70GB free baseline; pipeline temp ~7.2GB; monitor `df -h` before each batch.
120. **Photography/Videography collection (389 URLs)** — Download started in background; separate queue from Video Effects.
120. **Skill organization** — Video Effects: `davinci-video-effect-{reel_id[:8]}/`; Photography: `davinci-photography-portrait-{id}/`
120. **Skill auto-installation to Hermes** — Copy generated skills to `~/.hermes/skills/creative/` for immediate discoverability via `hermes skills list | grep davinci-reel`
120. **Cross-link all index files** — Memory.md, Cross_Reference_Index.md, Architecture_Diagram.md, Hero_index.md, START_HERE.md all need new pipeline entries
120. **Architecture diagram updates** — Mermaid graph MUST include Instagram_Reels subgraph with MASTER_INDEX node
120. **Parallel pipeline execution works** — Two simultaneous GIF regen processes covered each other's failures; rate limit handling via exponential backoff (30s→60s→120s→240s→480s).
121. **Video Effects pipeline complete** — 334/368 reels processed (91% frame extraction rate); 34 failed at download/extract. 334 skills + 737 vault notes created.
121. **Background process monitoring** — Use `process(action="poll", session_id)` and `process(action="log", session_id, limit=50)` to check long-running pipeline status.
121. **Frame directory ID mapping** — Frame folders use downreels.com internal IDs; manifest's `frames_dir` field provides correct path. Always use manifest's `frames_dir` for vision analysis, not reel_id.
121. **Auto-compression provider fix** — NVIDIA provider must point to `https://integrate.api.nvidia.com/v1` not local Ollama. Verify with `hermes config get` before long sessions.
121. **Vision rate limit (20 RPM / 3s) is hard constraint** — Enforced in all vision analysis stages.
121. **Vault path discipline** — All outputs MUST use exact TamaZila Obsidian Vault path.
121. **GIF copy before cleanup is mandatory** — Copy to vault BEFORE cleanup_reel() deletes temp.
121. **Index cross-linking should be automated** — 5 index files need updating; consider regenerate_indexes.py.
122. **Architecture diagram discipline** — Mermaid graph MUST include Instagram_Reels subgraph with MASTER_INDEX node.
122. **Storage budget monitoring** — Samsung LED SSD (120GB): ~70GB free baseline; pipeline temp ~7.2GB; monitor `df -h` before each batch.
122. **Photography/Videography collection (389 URLs)** — Download started in background; separate queue from Video Effects.
122. **Skill organization** — Video Effects: `davinci-video-effect-{reel_id[:8]}/`; Photography: `davinci-photography-portrait-{id}/`
122. **Skill auto-installation to Hermes** — Copy generated skills to `~/.hermes/skills/creative/` for immediate discoverability via `hermes skills list | grep davinci-reel`
122. **Cross-link all index files** — Memory.md, Cross_Reference_Index.md, Architecture_Diagram.md, Hero_index.md, START_HERE.md all need new pipeline entries
122. **Architecture diagram updates** — Mermaid graph MUST include Instagram_Reels subgraph with MASTER_INDEX node
122. **Parallel pipeline execution works** — Two simultaneous GIF regen processes covered each other's failures; rate limit handling via exponential backoff (30s→60s→120s→240s→480s).
123. **Video Effects pipeline complete** — 334/368 reels processed (91% frame extraction rate); 34 failed at download/extract. 334 skills + 737 vault notes created.
123. **Background process monitoring** — Use `process(action="poll", session_id)` and `process(action="log", session_id, limit=50)` to check long-running pipeline status.
123. **Frame directory ID mapping** — Frame folders use downreels.com internal IDs; manifest's `frames_dir` field provides correct path. Always use manifest's `frames_dir` for vision analysis, not reel_id.
123. **Auto-compression provider fix** — NVIDIA provider must point to `https://integrate.api.nvidia.com/v1` not local Ollama. Verify with `hermes config get` before long sessions.
123. **Vision rate limit (20 RPM / 3s) is hard constraint** — Enforced in all vision analysis stages.
123. **Vault path discipline** — All outputs MUST use exact TamaZila Obsidian Vault path.
123. **GIF copy before cleanup is mandatory** — Copy to vault BEFORE cleanup_reel() deletes temp.
123. **Index cross-linking should be automated** — 5 index files need updating; consider regenerate_indexes.py.
124. **Architecture diagram discipline** — Mermaid graph MUST include Instagram_Reels subgraph with MASTER_INDEX node.
124. **Storage budget monitoring** — Samsung LED SSD (120GB): ~70GB free baseline; pipeline temp ~7.2GB; monitor `df -h` before each batch.
124. **Photography/Videography collection (389 URLs)** — Download started in background; separate queue from Video Effects.
124. **Skill organization** — Video Effects: `davinci-video-effect-{reel_id[:8]}/`; Photography: `davinci-photography-portrait-{id}/`
124. **Skill auto-installation to Hermes** — Copy generated skills to `~/.hermes/skills/creative/` for immediate discoverability via `hermes skills list | grep davinci-reel`
124. **Cross-link all index files** — Memory.md, Cross_Reference_Index.md, Architecture_Diagram.md, Hero_index.md, START_HERE.md all need new pipeline entries
124. **Architecture diagram updates** — Mermaid graph MUST include Instagram_Reels subgraph with MASTER_INDEX node
124. **Parallel pipeline execution works** — Two simultaneous GIF regen processes covered each other's failures; rate limit handling via exponential backoff (30s→60s→120s→240s→480s).
125. **Video Effects pipeline complete** — 334/368 reels processed (91% frame extraction rate); 34 failed at download/extract. 334 skills + 737 vault notes created.
125. **Background process monitoring** — Use `process(action="poll", session_id)` and `process(action="log", session_id, limit=50)` to check long-running pipeline status.
125. **Frame directory ID mapping** — Frame folders use downreels.com internal IDs; manifest's `frames_dir` field provides correct path. Always use manifest's `frames_dir` for vision analysis, not reel_id.
125. **Auto-compression provider fix** — NVIDIA provider must point to `https://integrate.api.nvidia.com/v1` not local Ollama. Verify with `hermes config get` before long sessions.
125. **Vision rate limit (20 RPM / 3s) is hard constraint** — Enforced in all vision analysis stages.
125. **Vault path discipline** — All outputs MUST use exact TamaZila Obsidian Vault path.
125. **GIF copy before cleanup is mandatory** — Copy to vault BEFORE cleanup_reel() deletes temp.
125. **Index cross-linking should be automated** — 5 index files need updating; consider regenerate_indexes.py.
126. **Architecture diagram discipline** — Mermaid graph MUST include Instagram_Reels subgraph with MASTER_INDEX node.
126. **Storage budget monitoring** — Samsung LED SSD (120GB): ~70GB free baseline; pipeline temp ~7.2GB; monitor `df -h` before each batch.
126. **Photography/Videography collection (389 URLs)** — Download started in background; separate queue from Video Effects.
126. **Skill organization** — Video Effects: `davinci-video-effect-{reel_id[:8]}/`; Photography: `davinci-photography-portrait-{id}/`
126. **Skill auto-installation to Hermes** — Copy generated skills to `~/.hermes/skills/creative/` for immediate discoverability via `hermes skills list | grep davinci-reel`
126. **Cross-link all index files** — Memory.md, Cross_Reference_Index.md, Architecture_Diagram.md, Hero_index.md, START_HERE.md all need new pipeline entries
126. **Architecture diagram updates** — Mermaid graph MUST include Instagram_Reels subgraph with MASTER_INDEX node
126. **Parallel pipeline execution works** — Two simultaneous GIF regen processes covered each other's failures; rate limit handling via exponential backoff (30s→60s→120s→240s→480s).
127. **Video Effects pipeline complete** — 334/368 reels processed (91% frame extraction rate); 34 failed at download/extract. 334 skills + 737 vault notes created.
127. **Background process monitoring** — Use `process(action="poll", session_id)` and `process(action="log", session_id, limit=50)` to check long-running pipeline status.
127. **Frame directory ID mapping** — Frame folders use downreels.com internal IDs; manifest's `frames_dir` field provides correct path. Always use manifest's `frames_dir` for vision analysis, not reel_id.
127. **Auto-compression provider fix** — NVIDIA provider must point to `https://integrate.api.nvidia.com/v1` not local Ollama. Verify with `hermes config get` before long sessions.
127. **Vision rate limit (20 RPM / 3s) is hard constraint** — Enforced in all vision analysis stages.
127. **Vault path discipline** — All outputs MUST use exact TamaZila Obsidian Vault path.
127. **GIF copy before cleanup is mandatory** — Copy to vault BEFORE cleanup_reel() deletes temp.
127. **Index cross-linking should be automated** — 5 index files need updating; consider regenerate_indexes.py.
128. **Architecture diagram discipline** — Mermaid graph MUST include Instagram_Reels subgraph with MASTER_INDEX node.
128. **Storage budget monitoring** — Samsung LED SSD (120GB): ~70GB free baseline; pipeline temp ~7.2GB; monitor `df -h` before each batch.
128. **Photography/Videography collection (389 URLs)** — Download started in background; separate queue from Video Effects.
128. **Skill organization** — Video Effects: `davinci-video-effect-{reel_id[:8]}/`; Photography: `davinci-photography-portrait-{id}/`
128. **Skill auto-installation to Hermes** — Copy generated skills to `~/.hermes/skills/creative/` for immediate discoverability via `hermes skills list | grep davinci-reel`
128. **Cross-link all index files** — Memory.md, Cross_Reference_Index.md, Architecture_Diagram.md, Hero_index.md, START_HERE.md all need new pipeline entries
128. **Architecture diagram updates** — Mermaid graph MUST include Instagram_Reels subgraph with MASTER_INDEX node
128. **Parallel pipeline execution works** — Two simultaneous GIF regen processes covered each other's failures; rate limit handling via exponential backoff (30s→60s→120s→240s→480s).
129. **Video Effects pipeline complete** — 334/368 reels processed (91% frame extraction rate); 34 failed at download/extract. 334 skills + 737 vault notes created.
129. **Background process monitoring** — Use `process(action="poll", session_id)` and `process(action="log", session_id, limit=50)` to check long-running pipeline status.
129. **Frame directory ID mapping** — Frame folders use downreels.com internal IDs; manifest's `frames_dir` field provides correct path. Always use manifest's `frames_dir` for vision analysis, not reel_id.
129. **Auto-compression provider fix** — NVIDIA provider must point to `https://integrate.api.nvidia.com/v1` not local Ollama. Verify with `hermes config get` before long sessions.
129. **Vision rate limit (20 RPM / 3s) is hard constraint** — Enforced in all vision analysis stages.
129. **Vault path discipline** — All outputs MUST use exact TamaZila Obsidian Vault path.
129. **GIF copy before cleanup is mandatory** — Copy to vault BEFORE cleanup_reel() deletes temp.
129. **Index cross-linking should be automated** — 5 index files need updating; consider regenerate_indexes.py.
130. **Architecture diagram discipline** — Mermaid graph MUST include Instagram_Reels subgraph with MASTER_INDEX node.
130. **Storage budget monitoring** — Samsung LED SSD (120GB): ~70GB free baseline; pipeline temp ~7.2GB; monitor `df -h` before each batch.
130. **Photography/Videography collection (389 URLs)** — Download started in background; separate queue from Video Effects.
130. **Skill organization** — Video Effects: `davinci-video-effect-{reel_id[:8]}/`; Photography: `davinci-photography-portrait-{id}/`
130. **Skill auto-installation to Hermes** — Copy generated skills to `~/.hermes/skills/creative/` for immediate discoverability via `hermes skills list | grep davinci-reel`
1