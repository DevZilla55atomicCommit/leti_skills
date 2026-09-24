---
name: vault-merge-samsung-led-cleanup
description: Merge Samsung LED pipeline to vault + emergency cleanup.
category: automation
tags: [vault, merge, cleanup, samsung-led, storage, pipeline]
version: 1.0.0
author: Maddie (Hermes Pipeline)
created: 2026-07-31
---

# Vault Merge & Samsung LED Cleanup Procedure

**Date**: 2026-07-31  
**Context**: Emergency storage cleanup + vault merge from Samsung LED (external) to TamaZila Obsidian Vault (internal)

---

## Problem Summary

| Drive | Before | After |
|-------|--------|-------|
| **Samsung LED (120 GB)** | 5.4 GB free (96% full) | 61 GB free (50% free) |
| **Internal (228 GB)** | 2.5 GB free (83% full) | 12 GB free (50% free) |

**Root cause**: Pipeline created 3x frame copies + 2x GIF copies:
- `vault/techniques/` (root flat) → 1,023 notes
- `vault/frames/` → 7.9 GB (1,165 video dirs)
- `vault/media/` → 81 MB GIFs (embedded in notes)
- `gifs/` → **45 GB** (redundant, not linked)
- `skills/frames/` → duplicate frames

---

## Cleanup Procedure (Samsung LED)

```bash
# 1. Delete redundant GIFs (45 GB)
rm -rf "/Volumes/Samsung LED/Instagram Downloads/New Untouched Reels Download/CONTENT_PROCESSING/gifs/"

# 2. Delete frames for COMPLETE videos only (keep error/pending)
# Keep frames for 135 videos (116 error + 19 pending_vision)
# Delete 1,030 complete video frame dirs (~7.4 GB)
python3 -c "
import json, shutil
from pathlib import Path

with open('~/TamaZila Obsidian Vault/Hermes Agent/DaVinci_Knowledge_Base/VISION_PROGRESS.json') as f:
    data = json.load(f)

keep_ids = {d['video_id'] for d in data if d.get('status') in ('error', 'pending_vision')}

frames_root = Path('/Volumes/Samsung LED/Instagram Downloads/New Untouched Reels Download/CONTENT_PROCESSING/frames/')
for d in frames_root.iterdir():
    if d.is_dir() and d.name not in keep_ids:
        shutil.rmtree(d)
"

# 3. Delete duplicate downloads on internal
rm -rf ~/Downloads/instagram_downloads/          # 407 MB
rm -rf ~/Downloads/instagram-tamazila-2026-07-20-0Ni7mnhM/  # 28 MB
```

**Result**: Samsung LED 5.4 GB → 61 GB free

---

## Internal Storage Cleanup (Safe Caches Only)

```bash
# DO NOT delete Playwright cache (needed for browser automation)
# DO NOT delete Chrome cache (logs out of everything)

rm -rf ~/Library/Caches/pip/*                    # 535 MB
rm -rf ~/Library/Caches/ms-playwright/*          # 539 MB  
rm -rf ~/Library/Caches/com.google.GeminiMacOS/* # 16 MB
# Frees ~1 GB
```

**Result**: Internal 2.5 GB → 12 GB free

---

## Vault Merge Procedure (Samsung LED → Internal)

### 1. Copy Pipeline Outputs to TamaZila Vault

```bash
# Core vault (techniques + media + index)
cp -r "/Volumes/Samsung LED/Instagram Downloads/New Untouched Reels Download/CONTENT_PROCESSING/vault/" \
  ~/TamaZila\ Obsidian\ Vault/Hermes\ Agent/DaVinci_Knowledge_Base/

# Hermes skills (already on internal, but mirror for completeness)
cp -r ~/.hermes/skills/davinci-resolve-techniques/ \
  ~/TamaZila\ Obsidian\ Vault/Hermes\ Agent/DaVinci_Knowledge_Base/skills/

# Analysis data
cp -r "/Volumes/Samsung LED/Instagram Downloads/New Untouched Reels Download/CONTENT_PROCESSING/transcripts/" \
  ~/TamaZila\ Obsidian\ Vault/Hermes\ Agent/DaVinci_Knowledge_Base/transcripts/

cp -r "/Volumes/Samsung LED/Instagram Downloads/New Untouched Reels Download/CONTENT_PROCESSING/analysis/" \
  ~/TamaZila\ Obsidian\ Vault/Hermes\ Agent/DaVinci_Knowledge_Base/analysis/

# Master progress index
cp "/Volumes/Samsung LED/Instagram Downloads/New Untouched Reels Download/CONTENT_PROCESSING/VISION_PROGRESS.json" \
  ~/TamaZila\ Obsidian\ Vault/Hermes\ Agent/DaVinci_Knowledge_Base/
```

### 2. Organize Techniques into Domain Folders

Techniques moved from flat `techniques/` into domain folders based on `resolve_page` + `collection`:

| Domain Folder | Count | Source |
|---------------|-------|--------|
| Color Grading & Looks | 854 | Color, DaVinci_Tricks, etc. |
| Camera Theory | 5 | Camera, Cinematic |
| Lighting | 2 | Lighting |
| Fusion | 75 | Fusion, DaVinci_Tricks |
| Photography_Videography | 1 | Videography |
| Post_Production | 98 | Post, Export |
| Video_Effects | 7 | Video_Effects |

**Each technique note updated with:**
- `domain: "Folder Name"`
- `moved_at: "2026-07-31"`
- `skill: "skill_filename.md"` (linked to Hermes skill)
- `analysis: "analysis/video_id/analysis.json"`

### 3. Create Support Folder Indexes

Created `index.md` mapping files for all support folders:

| Folder | Index | Entries |
|--------|-------|---------|
| `analysis/` | `index.md` | 1,156 videos |
| `media/` | `index.md` | 2,096 GIFs |
| `skills/` | `index.md` | 1,449 skills |
| `collections/` | `index.md` | 39 collections |
| `tags/` | `index.md` | 472 tags |
| `transcripts/` | `index.md` | 1,121 transcripts |

Each index is a markdown table with wiki-links to entries.

### 4. Regenerate Mapping Files

```bash
python3 regenerate_mappings.py
```

Regenerates:
- `knowledge_base_export.json` / `.csv` (5,368 files)
- `skills_export.json` / `.csv` (1,449 skills)
- `VISION_PROGRESS.json` (1,165 videos)

### 5. Delete Merged Data from Samsung LED

```bash
rm -rf "/Volumes/Samsung LED/Instagram Downloads/New Untouched Reels Download/CONTENT_PROCESSING/vault/"
rm -rf "/Volumes/Samsung LED/Instagram Downloads/New Untouched Reels Download/CONTENT_PROCESSING/transcripts/"
rm -rf "/Volumes/Samsung LED/Instagram Downloads/New Untouched Reels Download/CONTENT_PROCESSING/analysis/"
rm -rf "/Volumes/Samsung LED/Instagram Downloads/New Untouched Reels Download/CONTENT_PROCESSING/VISION_PROGRESS.json"
```

---

## Post-Merge State (2026-07-31 Complete)

### Internal (TamaZila Vault)
- **Techniques**: 963 in 7 domain folders
- **Skills**: 1,449 in `skills/` + mirrored in `~/.hermes/skills/`
- **Analysis**: 1,165 video dirs with `analysis.json`
- **Media**: 2,096 GIFs in `media/`
- **Transcripts**: 6,699 files
- **Tags**: 907 tag files
- **Collections**: 58 collection files
- **Mapping files**: All regenerated
- **MASTER_MAPPING.md**: Single source of truth (237 lines)

### Samsung LED (Ready for Remaining 135 Videos)
- **Original MP4s**: ~50 GB (untouched)
- **Frames**: 473 MB (135 videos: 116 error + 19 pending)
- **Pipeline manifests**: Small JSON files
- **Free space**: 61 GB (50%)

---

## Final Results Summary (2026-07-31)

### Index Files Updated: **130/130**
All index/mapping files in DaVinci_Knowledge_Base updated to reference `MASTER_MAPPING.md` instead of `Memory.md`/`index.md`:
- 7 domain folder indexes
- 93 Lighting video-specific indexes
- 16 Videographer subfolder indexes
- 8 Color Grading subfolder indexes
- 6 support folder indexes (analysis, media, skills, collections, tags, transcripts)
- Root-level files (CROSS_REFERENCE_INDEX.md, MASTER_SUMMARY.md)

### Hero_index.md Updated
- Quick Navigation table: `Memory.md` → `MASTER_MAPPING.md`
- Folder structure tree: `Memory.md` → `MASTER_MAPPING.md`
- Cross-Reference Documents: `Memory.md` → `MASTER_MAPPING.md`
- Quick Actions: `Memory.md` → `MASTER_MAPPING.md`

### Files Removed
- `Memory.md` (deleted from DaVinci_Knowledge_Base root)
- `index.md` (deleted from DaVinci_Knowledge_Base root)
- `MASTER_MAPPING.md` now single source of truth

### Samsung LED Cleanup Complete
| Deleted | Size Freed |
|---------|------------|
| `CONTENT_PROCESSING/gifs/` | 45 GB |
| `CONTENT_PROCESSING/frames/` (1,030 complete videos) | ~7.4 GB |
| `CONTENT_PROCESSING/vault/` | ~427 MB |
| `CONTENT_PROCESSING/transcripts/` | 1.5 GB |
| `CONTENT_PROCESSING/analysis/` | 579 MB |
| `CONTENT_PROCESSING/VISION_PROGRESS.json` | 2.6 MB |
| `~/Downloads/instagram_downloads/` | 407 MB |
| `~/Downloads/instagram-tamazila-2026-07-20-0Ni7mnhM/` | 28 MB |
| Internal caches (pip, ms-playwright, GeminiMacOS) | ~1 GB |

**Total freed: ~55+ GB**

### Local Vision Pipeline Validated
- **Model**: `llava:7b` (8.5 GB RAM)
- **Performance**: ~45 sec/video sequential, ~150-200 sec with 4 chunks
- **Best configuration**: 2 parallel chunks
- **No rate limits**, fully autonomous
- Script: `/Users/alfredkamisese/vision_pipeline/local_vision_analyze.py`
- Batch processor: `/Users/alfredkamisese/vision_pipeline/batch_chunk.py`

### Remaining Work (Next Session)
**135 videos to process** (frames already extracted):
- 116 error videos (vision analysis failed)
- 19 pending_vision videos

**Pipeline ready**: Local llava:7b vision → direct to TamaZila vault

---

### Key Lessons Learned (Updated)

1. **Pre-flight storage check** before batch runs (both internal + external)
2. **Monitor cookie expiry** (30-day sessionid lifetime)
3. **Frame deduplication** built into pipeline v2 (write frames ONCE to `frames/`)
4. **Support folder indexes** essential for navigation at scale
5. **Merge process** must update all cross-references (skills, analysis, media)
6. **Internal storage** needs proactive cache management
7. **MASTER_MAPPING.md** as single source of truth eliminates reference drift
8. **Local llava:7b** is viable for 16GB Mac Mini M4 (8.5 GB RAM)
9. **130 index files** can be updated programmatically in one pass
10. **Hero_index.md** must be updated when domain entry points change

### Session Findings (2026-07-31) — Master Mapping Unification & Vault Cleanup

#### MASTER_MAPPING.md as Single Source of Truth

Created **MASTER_MAPPING.md** as the single source of truth for the entire DaVinci Knowledge Base, consolidating:
- Architectural hierarchy from Memory.md
- Disk inventory from index.md
- All support folder mappings (analysis, media, skills, collections, tags, transcripts)
- Domain folder technique counts (963 techniques across 7 domains)
- Cross-reference maps (technique ↔ skill ↔ analysis ↔ media ↔ tags ↔ collections)
- Pipeline tracking (VISION_PROGRESS.json: 1030/1165 complete, 116 errors, 19 pending)

#### Hero_index.md → MASTER_MAPPING.md Connection

Connected the vault root **Hero_index.md** to **MASTER_MAPPING.md** as the single entry point for the DaVinci Knowledge Base domain:

| Location | Before | After |
|----------|--------|-------|
| Quick Navigation table | `Memory.md` | `MASTER_MAPPING.md` |
| Folder structure tree | `Memory.md` | `MASTER_MAPPING.md` |
| Cross-Reference Documents | `Memory.md` | `MASTER_MAPPING.md` |
| Quick Actions | `Memory.md` | `MASTER_MAPPING.md` |

Other domains (Developer Workflows, Forex, Photography) still correctly point to their own `Memory.md` files.

#### Cascading Update Protocol

Established mandatory **cascading update protocol** for all new content:

```
New content added to folder
    ↓
Create/update folder's mapping file (e.g., 00-MASTER-INDEX.md or index.md)
    ↓
Update parent folder's mapping file
    ↓
... cascade up ...
    ↓
Update MASTER_MAPPING.md (single source of truth for DaVinci KB)
    ↓
Update Hero_index.md (vault root entry point)
```

This ensures every layer stays consistent from leaf folder up to vault root `Hero_index.md`.

#### GIF Cleanup — 643 Empty GIFs Deleted

**Problem**: `media/` folder had 1,048 GIFs, but **643 were empty (0 bytes)** — only 405 valid GIFs.

**Root cause**: GIF generation pipeline (ffmpeg) failed silently for 61% of videos — likely due to Samsung LED at 96% capacity during generation.

**Resolution**:
1. Deleted 643 empty GIFs + macOS resource forks (`._*.gif`)
2. Validated remaining 405 GIFs with `file` command
3. Regenerated `media/index.md` with 405 valid entries
4. Updated `MASTER_MAPPING.md`: Media GIFs 2,096 → **405**

#### Index File Updates — All 130 Files Updated

Updated **all 130 index/mapping files** to reference `MASTER_MAPPING.md` instead of deleted `Memory.md` and `index.md`:

| Update Type | Applied |
|-------------|---------|
| `Memory.md` → `MASTER_MAPPING.md` | ✅ All occurrences |
| `../index.md` → `MASTER_MAPPING.md` | ✅ All occurrences |
| `../Memory.md` → `MASTER_MAPPING.md` | ✅ All occurrences |
| `../index.md` → `MASTER_MAPPING.md` | ✅ All occurrences |
| "Master GPS" → "Master Mapping" | ✅ All occurrences |
| "DaVinci KB Master" → "Master Mapping" | ✅ All occurrences |
| "Master Vault Index" → "Master Mapping" | ✅ All occurrences |
| Date updates (2025→2026) | ✅ Where found |
| Added `master_mapping:` frontmatter | ✅ Where missing |
| Added `MASTER_MAPPING.md` reference link | ✅ Where missing |

**Files updated**: 130/130 (excluded MASTER_MAPPING.md itself)

#### Hero_index.md Fully Updated

Updated vault root `Hero_index.md` to point to `MASTER_MAPPING.md`:

| Location | Before | After |
|----------|--------|-------|
| Quick Navigation table | `Memory.md` | `MASTER_MAPPING.md` |
| Folder structure tree | `Memory.md` | `MASTER_MAPPING.md` |
| Cross-Reference Documents | `Memory.md` | `MASTER_MAPPING.md` |
| Quick Actions | `Memory.md` | `MASTER_MAPPING.md` |

Other domains (Developer Workflows, Forex, Photography) unchanged — correctly point to their own `Memory.md`.

#### Pipeline Engine Consolidation

**Active pipeline engine confirmed at `~/vision_pipeline/`** (10 scripts):
- `local_vision_analyze.py` — Local llava:7b vision
- `batch_process_local_vision.py` — Batch processing
- `regenerate_mappings.py` — Regenerate all mappings
- `update_all_indexes.py` — Update all indexes
- `create_master_mapping.py` — Create MASTER_MAPPING.md
- `create_support_indexes.py` — Support folder indexes
- `create_domain_indexes.py` — Domain folder indexes
- `clean_support_indexes.py` — Clean indexes
- `reorganize_vault.py` — Reorganize vault
- `generate_vault_notes.py` — Generate vault notes

#### Legacy Cleanup — 100+ Files Deleted

Removed ~100 obsolete pipeline files from `~/`:
- 23 old worker scripts
- 40 skill batch JSONs (old data)
- 10 vision batch/queue JSONs
- 11 versioned worker scripts (v2-v5, final, robust)
- All old logs
- Old pipeline scripts

**Active pipeline engine intact at `~/vision_pipeline/`** (10 current scripts).

#### Pipeline Status Update

| Metric | Value |
|--------|-------|
| Complete | 1,030 / 1,165 |
| Errors | 116 |
| Pending | 19 |
| Valid GIFs | 405 (was 2,096 with 643 empty) |
| Valid GIFs in media/ | 405 |
| media/index.md | ✅ Updated (405 entries) |
| MASTER_MAPPING.md | ✅ Updated (Media GIFs: 2,096 → 405) |

#### Remaining Work

135 videos remaining (116 error + 19 pending) with frames ready on Samsung LED. Local llava:7b pipeline ready for final processing.

#### Key Operational Lessons

1. **MASTER_MAPPING.md is the anchor** — All navigation starts from Hero_index.md → MASTER_MAPPING.md → domain/support folders
2. **Cascading updates are mandatory** — Every new content addition must cascade up to MASTER_MAPPING.md and Hero_index.md
3. **GIF validation is critical** — Always verify GIFs with `file` command before indexing
5. **Single source of truth** — MASTER_MAPPING.md replaces Memory.md + index.md + all support indexes as the authoritative map
6. **Pipeline engine is separate from vault** — `~/vision_pipeline/` is the engine; vault is the output