---
name: instagram-reels-pipeline
description: Automated Instagram Reels processing pipeline using yt-dlp nightly + cookies for fast downloads, ffmpeg for frame extraction, Obsidian vault notes, and Hermes skills
category: automation
tags: [instagram, reels, yt-dlp, ffmpeg, vault, automation, video-processing]
version: 1.0.0
author: Maddie (Hermes Pipeline)
created: 2026-07-19
---

# Instagram Reels Processing Pipeline

End-to-end automation for downloading Instagram Reels, extracting key frames, and creating structured knowledge assets.

## Overview

| Component | Tool | Purpose |
|-----------|------|---------|
| **Download** | yt-dlp (nightly) | Fast 1080p MP4 + metadata with browser cookies |
| **Frames** | ffmpeg | 8 frames at 0/14/28/42/57/71/86/100% |
| **Vault Notes** | Python → Markdown | Organized by discipline in Obsidian |
| **Hermes Skills** | Python → SKILL.md | Searchable technique references |
| **Archive** | shutil | External SSD backup |

## Quick Start

```bash
# 1. Fresh cookies (monthly)
# Export via "Get cookies.txt LOCALLY" extension → ~/Downloads/cookies_www.instagram.com_YYYY-MM-DD.txt

# 2. Prepare URL list
# JSON format at /tmp/reel_urls.json:
# [{"url": "https://www.instagram.com/reel/CODE/", "creator": "...", "notes": "", "priority": "Normal"}]

# 3. Pre-flight cookie check (MANDATORY - prevents batch failure)
python3 -c "
import re, time
with open('~/Downloads/cookies_www.instagram.com_2026-07-19.txt') as f:
    for line in f:
        if 'sessionid' in line:
            expiry = int(line.split()[4])
            print(f'sessionid expires: {time.ctime(expiry)}')
            print(f'Time remaining: {(expiry - time.time())/3600:.1f} hours')
            if expiry < time.time() + 3600:
                print('⚠️  EXPIRES SOON — REFRESH COOKIES')
                exit(1)
            break
"

# 4. Run pipeline
python3 ~/.hermes/skills/automation/instagram-reels-pipeline/scripts/process_reels.py
```

## Pre-Flight Cookie Validation (Critical)

**The #1 cause of pipeline failure is expired `sessionid` cookie (30-day lifetime).** On 2026-07-19, the cookie expired mid-batch after 3 reels, causing 93 subsequent failures with HTTP 404.

**Always run pre-flight check before batch runs:**
```bash
python3 -c "
import re, time
with open('~/Downloads/cookies_www.instagram.com_YYYY-MM-DD.txt') as f:
    for line in f:
        if 'sessionid' in line:
            expiry = int(line.split()[4])
            remaining_hours = (expiry - time.time()) / 3600
            print(f'sessionid expires: {time.ctime(expiry)} ({remaining_hours:.1f}h remaining)')
            if remaining_hours < 1:
                print('❌ EXPIRES WITHIN 1 HOUR — REFRESH COOKIES FIRST')
                exit(1)
            break
"
```
The pipeline script should embed this check and exit non-zero if cookie expiry < 1 hour.

## Configuration

Edit constants at top of `scripts/process_reels.py`:

```python
REEL_URLS_FILE = "/tmp/reel_urls.json"
COOKIES_FILE = "~/Downloads/cookies_www.instagram.com_2026-07-19.txt"
VAULT_BASE = "~/TamaZila Obsidian Vault/Hermes Agent/DaVinci_Knowledge_Base/Videographer"
SKILLS_BASE = "~/.hermes/skills/videographer"
OUTPUT_BASE = "/Volumes/Samsung LED/Instagram Downloads"
MAX_WORKERS = 3
RATE_LIMIT_DELAY = 2
```

## Output Structure

```
~/.hermes/skills/videographer/reel_{CODE}/
├── SKILL.md              # Technique reference with frame table
├── frame_00.png          # 0%   - Opening hook
├── frame_01.png          # 14%  - Early development
├── frame_02.png          # 28%  - First technique reveal
├── frame_03.png          # 42%  - Mid-point / core concept
├── frame_04.png          # 57%  - Secondary technique
├── frame_05.png          # 71%  - Advanced application
├── frame_06.png          # 86%  - Refinement / detail
└── frame_07.png          # 100% - Closing / result

TamaZila Obsidian Vault/.../Videographer/{Discipline}/
├── {CODE}.md             # Full note with embedded frames
├── {CODE}.gif            # Animated preview (2fps)
└── frame_00.png ... frame_07.png

/Volumes/Samsung LED/Instagram Downloads/
└── {CODE}.mp4            # Full 1080p source
```

## Discipline Classification

Auto-classified by caption keywords:

| Discipline | Keywords |
|------------|----------|
| Camera_Movement | movement, dolly, slider, gimbal, tracking, pan, tilt, push, pull |
| Cinematography | cinematography, lighting, exposure, lens, focal, depth of field, bokeh, anamorphic |
| Color_Grading_&_Looks | color, grade, lut, look, film emulation, log, slog, rec709, hdr |
| Post_Production | edit, cut, transition, timeline, premiere, davinci, resolve, after effects, fusion |
| VFX_&_Compositing | effect, vfx, composite, mask, key, track, rotoscope, particle |
| Composition | composition, framing, rule of thirds, leading lines, symmetry, negative space |
| Lighting | light, key light, fill, rim, softbox, led, natural light, golden hour |
| Lenses_&_Optics | lens, mm, focal, aperture, t-stop, anamorphic, spherical, vintage |
| Business_&_Career | business, client, pricing, contract, portfolio, freelance, career |
| Camera_Theory | (default fallback) |

## Pipeline Evolution & Multi-Source Handling

### Two Pipeline Runs Coexist

| Pipeline | When | Reels | Code Format | Note Format | Frames in Vault |
|----------|------|-------|-------------|-------------|-----------------|
| **Learning Pipeline** (instagram-videographer-learning-pipeline) | Jul 19 AM | ~130 | D* (DEbQiEDPoLq) | `{CODE}_reel_technique.md` (detailed) | **No** — only in skills |
| **Production Pipeline** (instagram-reels-pipeline) | Jul 19 PM | 91 | C* (C-76iegvchD) | `{CODE}.md` + frames/ (minimal) | **Yes** — `frames/` subdir |

### Folder Structure

```
Videographer/                          # Production pipeline (current)
├── Camera_Theory/                     # 29 reels, frames/ subdirs
├── Cinematography/                    # 7 reels
├── Camera_Movement/                   # 4 reels
└── ... (underscore discipline folders)

Videographer/Videographer/             # Learning pipeline (earlier)
├── Camera_Movement/                   # ~35 D* reels, no frames/
├── Cinematography/
└── ... (same disciplines, different content)
```

### Merge Strategy (if needed)

**Do NOT auto-merge** — note formats differ:
- Learning: 150-line detailed technique analysis with DaVinci node tree
- Production: 50-line metadata + frame table

**If merging later:**
1. Keep both note formats side-by-side (different filenames: `CODE.md` vs `CODE_reel_technique.md`)
2. Copy frames from skills to vault for D* reels: `~/.hermes/skills/videographer/reel_{D*}/frames/` → `Videographer/{Discipline}/{D*}/frames/`
3. Regenerate master index covering both

### Duplicate Discipline Folders

Root has both spaced and underscored variants from different pipeline eras:
- `Camera_Theory/` (production) ↔ `Camera Theory/` (learning notes only)
- `Camera_Movement/` (production) ↔ `Camera Movement/` (learning)
- `Color_Grading_&_Looks/` ↔ `Color Grading/`
- etc.

**Production pipeline writes to underscored folders only.**

## Expected Results

| Metric | Typical |
|--------|---------|
| **Fresh reels success** | ~95% |
| **Older reels (6mo+)** | ~15% (most 404/private) |
| **Throughput** | ~15-20 reels/min |
| **Frame extraction** | 8 frames in ~2s |
| **Vault note creation** | <1s |

## Common Issues

| Symptom | Fix |
|---------|-----|
| "Empty media response" | Refresh cookies (expired sessionid) |
| 404 on working URLs | Cookie domain mismatch — use `.instagram.com` |
| Frame extraction fails | Check ffmpeg installed; duration detection edge case |
| GIF creation fails | Palette generation issue — non-blocking |
| Rate limited (429) | Reduce MAX_WORKERS to 1-2, increase RATE_LIMIT_DELAY |
| **All reels fail after ~1 month** | **Instagram sessionid cookie expires monthly (timestamp in cookies.txt). Refresh: login to IG → Get cookies.txt LOCALLY extension → save as ~/Downloads/cookies_www.instagram.com_YYYY-MM-DD.txt → update COOKIES_FILE in script** |
| **yt-dlp returns 404 on ALL reels (even with valid cookies)** | **Instagram API blocks yt-dlp requests regardless of cookies. Use browser automation fallback (Playwright + injected cookies)** |
| **Playwright "No module named greenlet._greenlet"** | **pip uninstall greenlet playwright -y && pip install --no-binary greenlet greenlet playwright && playwright install chromium** |
| **All reels fail with 404 after cookie refresh (playwright + yt-dlp both fail)** | **Instagram has IP/device fingerprint blocks. Workaround: Use different network (mobile hotspot) + fresh browser profile + manual login + export cookies immediately. OR: Accept some reels are unreachable and rely on saved local MP4s from prior runs.** |

## Session Findings (2026-07-19)

- **Cookie lifetime**: ~30 days. Sessionid expiry at timestamp 1815977441 (~23:30 UTC). First 3 reels downloaded before expiry; remaining 93 failed with HTTP 404.
- **Verified working**: yt-dlp nightly + fresh cookies downloads 1080p MP4s with full metadata for ALL reels tested (DDzMI60sBvM, DDo8k0hRiWE, DDF9Ahzpqtp, DCUb-vFvooS, DC1iY8LvN3Y, C-FNBHuIECz, C9urS8rIia_).
- **Browser automation (Method B)** fails because it doesn't send cookies — shows login wall even for public reels.
- **Pipeline is production-ready** when cookies are fresh. Expected success rate: ~95% (only truly deleted/private reels fail).
- **Critical operational lesson**: The pipeline must check cookie freshness BEFORE starting a batch. A simple timestamp check on `sessionid` in cookies.txt would have caught the expiry before wasting 3 minutes. Future version should add pre-flight validation: `sessionid` expiry > now + 1 hour.

## Session Findings (2026-07-20) — Overnight Bulk Download & Full Pipeline Execution

- **Saved Collections Export processed**: 128 collections, 3,959 total URLs extracted from `saved_collections.json`
- **Deduplication against DaVinci Knowledge Base**: 425 URLs already processed → 3,504 NEW URLs across 116 collections
- **Per-collection NEW_ONLY files generated**: `instagram_new_urls_by_collection/*_NEW.txt` (116 files)
- **Bulletproof download script**: `download_instagram_collections.py` with:
  - 2 concurrent downloads (Instagram-safe rate limiting)
  - Exponential backoff: 30s → 60s → 120s → 240s → 480s
  - Resume support (`--continue --no-overwrites`)
  - Metadata sidecars (`.meta.json` with caption, hashtags, owner, collection, timestamp)
  - Heartbeat logging every 60s per collection
  - Graceful shutdown on SIGTERM (writes `DOWNLOAD_REPORT.json` + `failed_urls.txt`)
  - Bug fixed: `idx` vs `index` variable name consistency in retry loop
- **Target**: External Samsung LED SSD (120 GB, 70 GB free → 62 GB free after run)
- **Results**: 41/116 collections started, 2,818 MP4s downloaded, ~5 GB used in ~5 hours
- **Collections completed**: AI, Animal_potrait, Aperture, Apple_LOG, Apple_Shortcuts, Audio_Effects, Billards, Blackmagic_App, Blending_Modes, Bracketing, Business_Tricks, Camera, Canva_Hack, Capcut, Car_Shooting_tips, Cheat_Card, Cinematic, Claude, Collage, Color_Grading_Assets, Color_grading, Content_creators_idea, Cooking_Recipes, Cooking_shooting, Creating_Jarvis, Cybersecurity, DRS_20, DR_Making_CG, DR_Masking, DR_Noise_Reduction, DR_Photo_Editing, DaVinci, DaVinci_Tricks, Dance, Directing_Board, Dji_Gimbals_Tips, Dressing, Drone, Exercise, Export_Photos, Export_Videos, Filters, Fitness (in progress)
- **Failed URLs**: 2 (both from AI collection - deleted/private reels)
- **Disk usage**: 57 GB / 120 GB (49%) on Samsung LED — ample headroom for remaining ~700 URLs
- **Estimated completion**: ~3-4 more hours for remaining ~700 URLs

### Session Findings (2026-07-20) — Cookie Expiry Mid-Run

- **Cookies expired during run**: `sessionid` cookie expired July 19, 2025 16:06 UTC (mid-run on July 20)
- **Impact**: Life collection (141 URLs) and subsequent collections failing with HTTP 400 "Bad Request" on all videos
- **Progress at failure**: 41/116 collections started, 2,818/3,504 MP4s downloaded (80%)
- **Action required**: Refresh cookies, restart with same script (resumes via `--continue --no-overwrites`)
- **Remaining**: ~700 URLs in 75 collections

### Session Findings (2026-07-20) — Full Pipeline Execution & DaVinci/Other Separation

#### Instagram Saved Collections Export Processing
- **Export processed**: `saved_collections.json` (14.9 MB, ~4,000 items, 128 collections)
- **Deduplication against DaVinci Knowledge Base**: 425 URLs already processed → 3,504 NEW URLs across 116 collections
- **Per-collection NEW_ONLY files**: 116 files in `instagram_new_urls_by_collection/`
- **Collection-to-Discipline mapping**: Multiple collections map to same DaVinci discipline (e.g., "Color grading" + "DaVinci Tricks" → `Color_Grading_&_Looks/`)

#### Bulletproof Download Script: `download_instagram_collections.py`
```python
# Key features:
# - 2 concurrent downloads (Instagram-safe rate limiting)
# - Exponential backoff: 30s → 60s → 120s → 240s → 480s
# - Resume via `--continue --no-overwrites`
# - Metadata sidecars (`.meta.json`: caption, hashtags, owner, collection, timestamp)
# - Heartbeat logging every 60s per collection
# - Graceful shutdown on SIGTERM (writes `DOWNLOAD_REPORT.json` + `failed_urls.txt`)
# - Fixed: `idx` vs `index` variable name consistency in retry loop
```

#### Execution Results (5.5 hours)
| Metric | Value |
|--------|-------|
| Collections started | 41 / 116 |
| MP4s downloaded | 2,818 / 3,504 |
| Disk used | ~5 GB (57 GB / 120 GB on Samsung LED) |
| Failed URLs | 2 (AI collection - deleted/private) |
| Cookie expiry | sessionid expired July 19, 2025 16:06 UTC |
| Remaining | ~700 URLs in 75 collections |

#### DaVinci vs Other Content Separation
- **DaVinci-related collections**: 55 (Color_grading, DaVinci_Tricks, Cinematic, Video_Effect, Ideas_for_Shooting_Videos, Videographer, Gimbal_Moves, Drone, etc.)
- **Other collections**: 61 (Fitness, Life, Lens, Lightroom, Photography_Videography, Food_for_thoughts, etc.)
- **Separation logic**: Collection name matching against `DAVINCI_COLLECTIONS` set

#### Complete Pipeline Outputs Generated
```
PIPELINE_OUTPUT/
├── DaVinci_Knowledge_Base/
│   ├── csv/           # all_videos.csv, collections_summary.csv, by_technique.csv, by_creator.csv
│   ├── db/            # videos.db (composite PK: video_id + collection)
│   ├── obsidian/      # Index + 55 collection notes + technique notes
│   └── resolve/       # DaVinci Resolve bin structure (planned)
└── Other_Content/
    ├── csv/
    ├── db/
    ├── obsidian/
    └── resolve/
```

#### SQLite Schema (Composite Key Fix)
```sql
CREATE TABLE videos (
    video_id TEXT,
    collection TEXT,
    -- all metadata columns...
    PRIMARY KEY (video_id, collection)  -- Composite key allows same video in multiple collections
);
```

#### Obsidian Notes Structure (Both Outputs)
```
DaVinci_Knowledge_Base/obsidian/
├── 📚 Instagram Reels Index.md          # Master index with collections table
├── Color_Grading_&_Looks.md             # Collection note with frame table + techniques
├── Technique: color-grading.md          # Technique-specific index
└── ... (55 collections)

Other_Content/obsidian/
├── 📚 Instagram Reels Index.md
├── Fitness.md
├── Life.md
└── ... (61 collections)
```

#### Technique Tagging System (Auto-applied)
18 technique categories with keyword matching: color-grading, speed-ramp, masking, gimbal, drone, lighting, composition, camera-settings, skin-tones, luts, noise-reduction, transitions, editing, sound-design, motion-graphics, vfx, camera-theory

#### Scripts Created This Session
| Script | Purpose |
|--------|---------|
| `scripts/extract_saved_collections.py` | Parses saved_collections.json → per-collection JSON + flat CSV + URL .txt |
| `scripts/dedupe_against_kb.py` | Deduplicates collection URLs against existing vault KB |
| `scripts/gen_collection_new_only.py` | Generates per-collection NEW_ONLY.txt files |
| `scripts/download_instagram_collections.py` | **Overnight bulk downloader with concurrency control, retry logic, resume, metadata sidecars, heartbeat logging, graceful shutdown** |

## Session Findings (2026-07-20) — Full Pipeline Execution & DaVinci/Other Separation

### Instagram Saved Collections Export Processing
- **Export processed**: `saved_collections.json` (14.9 MB, ~4,000 items, 128 collections)
- **Deduplication against DaVinci Knowledge Base**: 425 URLs already processed → 3,504 NEW URLs across 116 collections
- **Per-collection NEW_ONLY files**: 116 files in `instagram_new_urls_by_collection/`
- **Collection-to-Discipline mapping**: Multiple collections map to same DaVinci discipline (e.g., "Color grading" + "DaVinci Tricks" → `Color_Grading_&_Looks/`)

### Bulletproof Download Script: `download_instagram_collections.py`
```python
# Key features:
# - 2 concurrent downloads (Instagram-safe)
# - Exponential backoff: 30s → 60s → 120s → 240s → 480s
# - Resume via `--continue --no-overwrites`
# - Metadata sidecars (`.meta.json`: caption, hashtags, owner, collection, timestamp)
# - Heartbeat logging every 60s per collection
# - Graceful shutdown on SIGTERM (writes DOWNLOAD_REPORT.json + failed_urls.txt)
# - Fixed: idx vs index variable name consistency in retry loop
```

### Execution Results (5.5 hours)
| Metric | Value |
|--------|-------|
| Collections started | 41 / 116 |
| MP4s downloaded | 2,818 / 3,504 |
| Disk used | ~5 GB (57 GB / 120 GB on Samsung LED) |
| Failed URLs | 2 (AI collection - deleted/private) |
| Cookie expiry | sessionid expired July 19, 2025 16:06 UTC |
| Remaining | ~700 URLs in 75 collections |

### DaVinci vs Other Content Separation
- **DaVinci-related collections**: 55 (Color_grading, DaVinci_Tricks, Cinematic, Video_Effect, Ideas_for_Shooting_Videos, Videographer, Gimbal_Moves, Drone, etc.)
- **Other collections**: 61 (Fitness, Life, Lens, Lightroom, Photography_Videography, Food_for_thoughts, etc.)
- **Separation logic**: Collection name matching against `DAVINCI_COLLECTIONS` set

### Complete Pipeline Outputs Generated
```
PIPELINE_OUTPUT/
├── DaVinci_Knowledge_Base/
│   ├── csv/           # all_videos.csv, collections_summary.csv, by_technique.csv, by_creator.csv
│   ├── db/            # videos.db (composite PK: video_id + collection)
│   ├── obsidian/      # Index + 55 collection notes + technique notes
│   └── resolve/       # DaVinci Resolve bin structure (planned)
└── Other_Content/
    ├── csv/
    ├── db/
    ├── obsidian/
    └── resolve/
```

### SQLite Schema (Composite Key Fix)
```sql
CREATE TABLE videos (
    video_id TEXT,
    collection TEXT,
    -- all metadata columns...
    PRIMARY KEY (video_id, collection)  -- Composite key allows same video in multiple collections
);
```

### Obsidian Notes Structure (Both Outputs)
```
DaVinci_Knowledge_Base/obsidian/
├── 📚 Instagram Reels Index.md          # Master index with collections table
├── Color_Grading_&_Looks.md             # Collection note with frame table + techniques
├── Technique: color-grading.md          # Technique-specific index
└── ... (55 collections)

Other_Content/obsidian/
├── 📚 Instagram Reels Index.md
├── Fitness.md
├── Life.md
└── ... (61 collections)
```

### Technique Tagging System (Auto-applied)
18 technique categories with keyword matching: color-grading, speed-ramp, masking, gimbal, drone, lighting, composition, camera-settings, skin-tones, luts, noise-reduction, transitions, editing, sound-design, motion-graphics, vfx, camera-theory

---

## Session Findings (2026-07-20) — Cookie Expiry Mid-Run

## Block Processing Results (2026-07-19)

| Block | Reels | Success | Failed | Notes |
|-------|-------|---------|--------|-------|
| Block A | 29 | 29 | 0 | Processed via `process_block_a_v2.py` |
| Block B | 30 | 30 | 0 | Processed via `process_block_b.py` |
| Block C | 32 | 32 | 0 | Processed via `process_block_c.py` |
| **Total** | **91** | **91** | **0** | 100% success rate |

## Duplicate Restoration (2026-07-19)

User requested restoration of removed duplicates for backward compatibility with old pipeline scripts. Verified byte-for-byte identical via `cmp` and vision model analysis:
- 240 frame PNGs restored to vault root directories
- 30 preview.gif files restored to `frames/` subdirectories
- All restored files are exact duplicates of canonical copies in `frames/` and skills directories

## Maintenance

- **Monthly**: Refresh cookies.txt
- **Weekly**: `pip install -U --pre yt-dlp` (nightly has active IG fixes)
- **As needed**: Add discipline keywords in `classify_discipline()`

## Vault Storage Optimization (Added 2026-07-19)

See [frame-extraction-fix.md](references/frame-extraction-fix.md#vault-storage-optimization-deduplicate-frame-storage) for full deduplication procedure and results.

**Summary**: Pipeline was creating 3 copies of each frame set (vault root, vault frames/, skills frames/) + 2 GIF copies. Applied Option A cleanup:
- Removed 107.6 MB duplicate frames from vault root
- Updated 93 notes to reference `frames/frame_XX.png`
- Removed 160 MB legacy `/assets/` folder
- **Total vault savings: 108 MB (19%)**

**Future pipeline fix (v2 — NOT YET IMPLEMENTED)**: Write frames ONLY to `frames/`, reference `frames/frame_XX.png` in notes, write GIF only to reel root. See Phase 1 of the v2 plan.

## Unified Pipeline Architecture (v2 Plan — 2026-07-20)

The current codebase has two entry points:
- `process_reels.py` — URL-based, downloads via yt-dlp
- `process_block_a_v2.py` / `process_local_files.py` — Local MP4 files, skips download

**v2 Unification (planned)**: Single script with `--source` flag:
```bash
# URL-based (downloads fresh)
python3 process_reels.py --source urls --urls-file /tmp/reel_urls.json

# Local files (skips download, uses existing MP4s)
python3 process_reels.py --source local --input-dir "/Volumes/Samsung LED/Instagram Downloads"
```

**v2 Key Improvements**:
1. **Pre-flight cookie check** embedded in script (exits non-zero if sessionid < 1hr)
2. **Archive-first logic**: Check `/Volumes/Samsung LED/.../{CODE}.mp4` before download
3. **99.9% frame seek** instead of 100% (avoids seek-past-end on short clips)
4. **≥7 frame tolerance** (accepts 7/8 frames for short reels)
5. **Single GIF output**: `frames/{CODE}.gif` only (no vault root duplicate)
6. **Note references**: `frames/frame_XX.png` and `frames/{CODE}.gif` (no root copies)
7. **DaVinci MCP integration** (Phase 2): Import MP4 → `media_analysis.analyze_clip` → `timeline_item_color.grade_evidence_base` → append color science metadata to vault note

## DaVinci MCP Color Analysis Integration (v2 Phase 2 — Planned)

After frame extraction and vault note creation, pipeline will:
1. Import MP4 to DaVinci Media Pool via `media_storage.import_to_pool`
2. Run `media_analysis.analyze_clip(clip_id=..., vision=true, transcription=false)` 
3. Run `timeline_item_color.grade_evidence_base()` on imported clip
4. Parse vision output for: log format, color space, exposure level, suggested CST/LUT
5. Append `## DaVinci Color Analysis` section to vault note with structured findings

This provides color science context for each reel technique — critical for DaVinci Resolve replication work.

## Instagram Saved Collections Export Processing (Added 2026-07-20)

**New workflow for bulk processing Instagram's "Your Activity → Saved → Collections" data export.**

### Export Acquisition
1. Instagram → Settings → Your Activity → Download Your Information
2. Select "Saved" → JSON format → Download
3. Extract `saved_collections.json` (14.9 MB typical, ~4,000 items, 128 collections)

### Export Structure Parsing
```python
# JSON structure: List[Collection]
# Each Collection has:
#   - timestamp (creation)
#   - label_values: [Name, Type, Privacy, Update time, Media]
#   - Media items nested in label_values[4].dict[] with:
#       - URL, Caption, Hashtags, Owner, Brand partner
```

### Extraction Script (Reusable)
```python
# Key extraction logic (from session):
# 1. Find collection name from label_values[label="Name"]
# 2. Find Media container from label_values[title="Media"]
# 3. For each media item: extract URL, caption, hashtags, owner, brand
# 4. Output: per-collection JSON + flat CSV + per-collection URL .txt files
```

### Deduplication Against Existing Vault/Knowledge Base
```bash
# 1. Extract all instagram.com/reel URLs from vault markdown
grep -r "instagram.com/reel" "TamaZila Obsidian Vault/Hermes Agent/DaVinci_Knowledge_Base" \
  -o -E "https://www.instagram.com/reel/[A-Za-z0-9_-]+" | sort -u > kb_urls.txt

# 2. Compare with saved collections flat URL list
comm -12 <(sort kb_urls.txt) <(sort instagram_all_urls_flat.txt) > overlap.txt
comm -13 <(sort kb_urls.txt) <(sort instagram_all_urls_flat.txt) > new_only.txt

# Results (2026-07-20):
# - Vault URLs: 425 unique
# - Saved Collection URLs: 3,820 unique  
# - Overlap: 408 (already processed)
# - New to process: 3,412
```

### Per-Collection NEW_ONLY URL Files
```bash
# For each collection, generate NEW_ONLY.txt (excludes overlap)
# Structure:
instagram_new_urls_by_collection/
├── Color_grading_NEW.txt           # 186 URLs (362 total - 176 done)
├── Video_Effect_NEW.txt            # 366 URLs (394 total - 28 done)
├── Videographer_NEW.txt            # 62 URLs  (275 total - 213 done)
├── Ideas_for_Shooting_Videos_NEW.txt  # 398 URLs
├── Photography_Videography_NEW.txt # 395 URLs (0 done)
├── Gimbal_Moves_NEW.txt            # 237 URLs
├── DaVinci_Tricks_NEW.txt          # 113 URLs
└── ... (117 collections total)
```

### Pipeline Integration
```bash
# Process each collection's NEW_ONLY file through existing pipeline
for f in instagram_new_urls_by_collection/*_NEW.txt; do
  python3 process_reels.py --urls-file "$f" --collection "$(basename "$f" _NEW.txt)"
done
```

### Collection Processing Status (2026-07-20 Snapshot)

| Collection | Total | Already Done | New | Priority |
|------------|-------|--------------|-----|----------|
| Videographer | 275 | 213 | 62 | High |
| Color grading | 362 | 176 | 186 | High |
| Video Effect | 394 | 28 | 366 | High |
| Ideas for Shooting Videos | 410 | 12 | 398 | Medium |
| Photography/Videography | 395 | 0 | 395 | Medium |
| Gimbal Moves | 238 | 1 | 237 | Medium |
| DaVinci Tricks | 115 | 2 | 113 | High |
| Lightroom | 192 | 1 | 191 | Low |
| Fitness | 201 | 0 | 201 | Low |

### Key Insight: Collections ≠ Disciplines
- **Collections** = User-curated folders (128 in export)
- **Disciplines** = Auto-classified by caption keywords (Camera Theory, Color Grading, etc.)
- Pipeline writes to **Discipline folders** in vault
- Multiple collections map to same discipline (e.g., "Color grading" + "DaVinci Tricks" → `Color_Grading_&_Looks/`)

---

## Hermes Browser Tools Fallback (Validated 2026-07-20)

### Working Method (Validated on DZ95PwrBsCQ and 92/93 failed reels)

```python
# 1. Navigate to reel (browser loads page with login wall)
browser_navigate(url="https://www.instagram.com/reel/CODE/")

# 2. Inject cookies via browser_console (Netscape format → document.cookie)
# Parse cookies.txt, set each as document.cookie = "name=value; domain=.instagram.com; path=/; secure; expires=..."
browser_console(expression="""
const cookieData = `...netscape format...`;
cookieData.trim().split('\n').forEach(line => {
  if (line.startsWith('#') || !line.trim()) return;
  const [domain, flag, path, secure, expiry, name, value] = line.split('\t');
  const cookieStr = `${name}=${value}; domain=${domain.replace(/^\./, '')}; path=${path}; ${secure==='TRUE' ? 'secure;' : ''} expires=${new Date(expiry*1000).toUTCString()};`;
  document.cookie = cookieStr;
});
console.log('Cookies set:', document.cookie);
""")

# 3. Navigate again (now authenticated)
browser_navigate(url="https://www.instagram.com/reel/CODE/")

# 4. Capture frames at percentages via canvas.toDataURL()
browser_console(expression="""
const v = document.querySelector('video');
const percentages = [0, 14, 28, 42, 57, 71, 86, 99.9];
const frames = [];
for (const pct of percentages) {
  v.currentTime = (pct/100) * v.duration;
  await new Promise(r => { v.onseeked = () => { setTimeout(r, 200); }; setTimeout(r, 3000); });
  const c = document.createElement('canvas');
  c.width = v.videoWidth; c.height = v.videoHeight;
  c.getContext('2d').drawImage(v, 0, 0);
  frames.push({percent: pct, dataUrl: c.toDataURL('image/png')});
}
frames;
""")

# 5. Save base64 → PNG → ffmpeg GIF → write vault note + skill
```

### Why This Works When yt-dlp Fails

| Aspect | yt-dlp | Hermes Browser Tools |
|--------|--------|---------------------|
| **Request type** | Direct API calls (IG blocks) | Real browser navigation (IG allows) |
| **Cookies** | Sent in HTTP headers | Injected into `document.cookie` |
| **JS execution** | None | Full browser JS engine |
| **Login wall** | Returns 404 | Bypassed by cookies |
| **Video access** | Blob URL extraction fails | `video.currentSrc` works |
| **Frame capture** | Requires download first | `canvas.toDataURL()` direct from playing video |
| **Dependencies** | yt-dlp nightly + cookies | Built-in Hermes tools (no extra install) |

**Result**: 92/93 previously failed reels processed successfully using this method (2026-07-20 batch run).

### Frame Capture Details

- **Percentages**: `[0, 14, 28, 42, 57, 71, 86, 99.9]` (99.9% avoids seek-past-end on short clips)
- **Seek wait**: `onseeked` + 200ms settle + 3s timeout fallback
- **Canvas size**: `videoWidth` × `videoHeight` (native resolution)
- **Output**: `data:image/png;base64,...` → Python base64 decode → PNG files

### GIF Generation (ffmpeg)

```bash
ffmpeg -y -framerate 2 -i frame_%02d.png \
  -vf "scale=720:-1:flags=lanczos,palettegen=stats_mode=diff" /tmp/palette.png
ffmpeg -y -framerate 2 -i frame_%02d.png -i /tmp/palette.png \
  -lavfi "scale=720:-1:flags=lanczos,paletteuse=dither=bayer:bayer_scale=5:diff_mode=rectangle" \
  output.gif
```

### Vault Note Structure

```
{Discipline}/{CODE}/
├── {CODE}.md              # Frontmatter + frame table + technique breakdown
├── INDEX.md               # Mapping reference for this reel
└── frames/
    ├── frame_00.png ... frame_07.png
    └── {CODE}.gif
```

### Hermes Skill Structure

```
~/.hermes/skills/videographer/reel_{CODE}/
├── SKILL.md
├── frame_00.png ... frame_07.png
└── {CODE}.gif
```

### Key Implementation Notes

1. **Cookie injection must happen BEFORE second navigate** — first navigate loads login wall, cookies set, second navigate loads authenticated page
2. **Video element may not be first** — `document.querySelectorAll('video')` returns multiple; the reel video is typically index 0 after auth
3. **Blob URLs** — `video.currentSrc` returns `blob:https://www.instagram.com/...` which plays in browser but isn't directly downloadable
4. **Frame 07 at 99.9%** — 100% seeks past end on some clips, returns black frame
5. **Accept ≥7 frames** — short clips may fail at one percentage; tolerate missing last frame
6. **No Playwright needed** — Hermes browser tools (navigate/console/vision) do everything; avoids greenlet/ARM64 issues entirely
7. **Metadata extraction** — Creator from profile link, likes/comments from caption regex, date from ISO timestamp, hashtags from caption
8. **Discipline classification** — Auto-classified by caption keywords (Lighting, Fusion, Post_Production, etc.)

### Batch Processing Results (2026-07-20)

| Metric | Value |
|--------|-------|
| Reels in failed batch | 93 |
| Successfully processed | 92 |
| Failed | 1 (likely deleted/private: C4GdCUfsJyP) |
| Success rate | 98.9% |
| Throughput | ~2-3 min/reel (browser navigation + frame capture) |
| Disciplines created | Lighting (all 92 reels in this batch) |
| Total Hermes skills | 215 |

## Local File Processing (Added 2026-07-19)

The pipeline now supports processing already-downloaded MP4 files without re-downloading:

```bash
# Point to a folder of MP4s (filenames contain reel codes)
python3 process_block_a_v2.py
```

**Key differences from URL-based pipeline:**
- Skips yt-dlp download step entirely — uses local files
- Still fetches metadata from Instagram (lightweight `--skip-download --print-json`)
- Extracts reel code from filename pattern: `reel:CODE:` or `DC1iY8LvN3Y.mp4`
- **Frame extraction fix**: Use 99.9% instead of 100% to avoid seeking past last frame
- **Frame count tolerance**: Accept ≥7 frames (100% frame sometimes fails on short clips)
- **Throughput**: ~20 reels/min (limited by yt-dlp metadata fetch + ffmpeg frame extraction)

**Filename patterns handled:**
- `https-::www.instagram.com:reel:C_lD_RTtUU6:?utm_source=...mp4` → `C_lD_RTtUU6`
- `2. https-::www.instagram.com:reel:DDo8k0hRiWE:...mp4` → `DDo8k0hRiWE`
- `DC1iY8LvN3Y.mp4` → `DC1iY8LvN3Y`

## References

- [cookie-setup.md](references/cookie-setup.md) — Detailed cookie workflow
- [process_reels.py](scripts/process_reels.py) — Main pipeline script
- [playwright-greenlet-issue.md](references/playwright-greenlet-issue.md) — Playwright/Greenlet issue on macOS ARM64
- [failed_reels_93.md](references/failed_reels_93.md) — Complete list of 93 failed reels with URLs
- [browser-fallback.md](references/browser-fallback.md) — Browser automation fallback (Playwright + cookies) for when yt-dlp fails
- [v2-pipeline-plan.md](references/v2-pipeline-plan.md) — Unified architecture plan for v2 pipeline
- [hermes-browser-tools-fallback.md](references/hermes-browser-tools-fallback.md) — **Hermes browser tools (navigate/console/vision) for zero-auth Reel processing** — 2026-07-20 validated
- [frame-analysis-validation.md](references/frame-analysis-validation.md) — Vision model analysis of captured frames confirming technique coverage
- [frame-extraction-fix.md](references/frame-extraction-fix.md) — Frame extraction fixes and vault deduplication
- [ig-saved-collections-export-processing.md](references/ig-saved-collections-export-processing.md) — **Instagram Saved Collections JSON export parsing, deduplication, and per-collection NEW_ONLY generation** — 2026-07-20
- [download_instagram_collections.py](scripts/download_instagram_collections.py) — **Bulletproof overnight downloader with per-collection isolation, exponential backoff, resume, metadata sidecars, heartbeat logging, graceful shutdown** — 2026-07-20

## Scripts

- [scripts/process_reels.py](scripts/process_reels.py) — Main URL-based pipeline
- [scripts/process_block_a_v2.py](scripts/process_block_a_v2.py) — Local file processor (Block A)
- [scripts/process_local_files.py](scripts/process_local_files.py) — Local MP4 processor
- [scripts/dedupe_against_kb.py](scripts/dedupe_against_kb.py) — Deduplicates collection URLs against existing vault KB
- [scripts/gen_collection_new_only.py](scripts/gen_collection_new_only.py) — Generates per-collection NEW_ONLY.txt files
- [scripts/extract_saved_collections.py](scripts/extract_saved_collections.py) — Parses saved_collections.json export
- [scripts/capture_reel_frames.py](scripts/capture_reel_frames.py) — Frame capture via browser tools
- [scripts/download_instagram_collections.py](scripts/download_instagram_collections.py) — **Overnight bulk downloader with concurrency control, retry logic, resume support**

## License

MIT — Use freely, modify, share.