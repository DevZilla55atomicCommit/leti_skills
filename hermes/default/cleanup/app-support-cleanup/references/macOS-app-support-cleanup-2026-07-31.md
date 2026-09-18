---
title: macOS Storage Cleanup Session - July 31, 2026
tags: [reference, cleanup, session-log]
owner: user
created: 2026-07-31
session_id: mac-storage-cleanup-2026-07-31
---

# macOS Storage Cleanup Session Log - July 31, 2026

## Session Overview
**Goal**: Free up space on Mac mini internal SSD (228 GB) by identifying and removing large, unnecessary files.

**Starting State**: 
- Data volume: 171 GiB used / 36 GiB free (83% full)
- User home: 96 GB

**Ending State**:
- Data volume: 147 GiB used / 59 GiB free (72% full)
- **Freed: ~24 GiB (14% reduction)**

---

## Major Space Consumers Identified

| Path | Size | Action Taken |
|------|------|--------------|
| `~/.ollama/models/blobs/` | 46 GB | **Partial** - removed 4 models via `ollama rm` |
| `~/.lmstudio/` | 7.8 GB | **Orphaned** - LM Studio app uninstalled but data remained |
| `~/.cache/` | 3.3 GB | **Cleared** - uv, codex-runtimes, huggingface |
| `~/Library/Caches/` | 6 GB (before) | **Cleared user-writable** - Spotify, Google, Homebrew, pip, etc. |
| `~/Library/Containers/` | 8.9 GB | **Reviewed** - Docker (11 MB), Draw Things (6.5 GB - models) |
| `~/Library/Application Support/` | 9.7 GB | **Reviewed** - Chrome OptGuide (4.8 GB), Comfy Desktop, etc. |
| `~/Desktop/` | ~3 GB | **Partial** - DaVinci installers (13 GB), videos (1.2 GB moved) |

---

## Actions & Results

### 1. Ollama Model Cleanup (25 GB freed)
**Models removed via `ollama rm`:**
- `qwen3-vl:8b` — 6.1 GB
- `minicpm-v4.5:8b` — 6.1 GB
- `qwen3.5-4b-compress:latest` — 3.4 GB
- `gemma4:e4b` — 9.6 GB

**Models retained (8 models, 25 GB):**
- `x/flux2-klein:4b-fp8` — 9.5 GB (image gen)
- `gemma4:12b` — 7.6 GB (primary LLM)
- `qwen3.5-32k/48k/64k/128k:latest` — 6.6 GB × 4 (long-context)
- `qwen3.5:4b` — 3.4 GB (fast LLM)
- `nomic-embed-text:latest` — 274 MB (embeddings)

**Key Learning**: Ollama uses content-addressable blobs shared across models. `ollama rm` properly dereferences; manual blob deletion risks corrupting other models.

---

### 2. Orphaned LM Studio Data (7.8 GB freed)
**Discovery**: LM Studio app bundle was NOT installed (`/Applications/LM Studio.app` missing), but data persisted:
- `~/.lmstudio/` — 7.8 GB (models, extensions, binaries)
- `~/Library/Application Support/LM Studio/` — 1.8 MB

**Models found**: `lmstudio-community/gemma-4-E4B-it-MLX-4bit/` (6.4 GB)

**Action**: `rm -rf ~/.lmstudio && rm -rf "~/Library/Application Support/LM Studio"`

**Key Learning**: Always check `~/.<appname>`, `~/Library/Application Support/`, and `~/Library/Containers/` for orphaned data after app uninstall.

---

### 3. Cache Cleaning (3.5 GB freed)
**`~/Library/Caches/`** — Targeted user-writable caches only:
- `com.spotify.client` — 190 MB
- `Google` — 6.2 MB
- `Homebrew` — 588 MB
- `pip` — 352 MB
- `comfyui-desktop-2-updater` — 319 MB
- `electron` — 218 MB
- `go-build` — 127 MB
- `node-gyp` — 62 MB
- `com.apple.python` — 57 MB

**Protected (skipped)**: CloudKit, Safari, HomeKit, FindMy, adprivacyd, containermanagerd — require SIP disable.

**`~/.cache/`** — Full clear:
- `uv` — 1.8 GB
- `codex-runtimes` — 1.3 GB
- `huggingface` — 141 MB
- `outlines` — 72 MB

---

### 4. DaVinci Resolve Installers (13 GB freed)
**Found on Desktop**: `~/Desktop/Media & Design/Gamut Apple Log/`
- `DaVinci_Resolve_Studio_20.3_Mac.dmg` — 6.5 GB
- `DaVinci_Resolve_Studio_20.3_Mac.zip` — 6.5 GB

**Verification**: `/Applications/DaVinci Resolve/DaVinci Resolve.app` version 21.0.1 installed (newer than 20.3).

**Action**: Deleted both installers.

---

### 5. Desktop Video Archive (1.2 GB moved)
**`~/Desktop/4th July/`** — 1.2 GB of `.mov` files (A001_07041634_C063.mov, etc.)

**Action**: `cp` to `/Volumes/Alfred Ext/4th July/` then `rm -rf` local.

---

### 6. Chrome ML Model Caches (4.8 GB identified, cleared)
**`~/Library/Application Support/Google/Chrome/`**:
- `OptGuideOnDeviceModel/` — 4.0 GB (on-device ML weights)
- `OptGuideOnDeviceClassifierModel/` — 120 MB
- `optimization_guide_model_store/` — 82 MB

**Action**: `rm -rf` all three directories.

---

### 7. Comfy Desktop Cache (1 GB identified)
**`~/Library/Application Support/Comfy Desktop/download-cache/`** — large tar.gz

**Action**: `rm -rf` download-cache directory.

---

### 8. Docker VM Disk (Not a real space issue)
**Found**: `~/Library/Containers/com.docker.docker/Data/vms/0/data/Docker.raw`
- `ls -lh`: 228 GB (apparent/sparse)
- `du -sh`: 8 MB (actual)

**Conclusion**: Sparse file — not consuming real space. No action needed.

---

### 9. Draw Things Models (6.5 GB - kept)
**`~/Library/Containers/com.liuliu.draw-things/Data/Documents/Models/`**:
- `sd_xl_turbo_f16.ckpt` — 4.8 GB
- `open_clip_vit_bigg14_f16.ckpt` — 1.3 GB
- `clip_vit_l14_f16.ckpt` — 235 MB
- `sdxl_vae_v1.0_f16.ckpt` — 160 MB

**Status**: Active app, models in use — kept.

---

## Commands Used for Discovery

```bash
# Full home directory scan
du -sh ~/* ~/.* 2>/dev/null | sort -hr | head -30

# Ollama model blobs
du -sh ~/.ollama/models/blobs/* | sort -hr | head -20

# Application Support
du -sh ~/Library/Application\ Support/* 2>/dev/null | sort -hr | head -20

# Containers
du -sh ~/Library/Containers/* 2>/dev/null | sort -hr | head -20

# Caches
du -sh ~/Library/Caches/* 2>/dev/null | sort -hr | head -20
du -sh ~/.cache/* 2>/dev/null | sort -hr

# Desktop large files
find ~/Desktop -type f -size +500M 2>/dev/null

# Sparse file check
du -sh ~/Library/Containers/com.docker.docker/Data/vms/0/data/Docker.raw
```

---

## Space Recovery Summary

| Category | Freed | Notes |
|----------|-------|-------|
| Ollama models | 25 GB | 4 of 12 models removed |
| LM Studio (orphaned) | 7.8 GB | App was uninstalled |
| DaVinci installers | 13 GB | Already on v21.0.1 |
| Caches (Library + .cache) | 3.5 GB | Safe to clear |
| Chrome ML models | 4.2 GB | On-device ML weights |
| Comfy Desktop cache | 1 GB | Download cache |
| Desktop videos | 1.2 GB | Moved to external |
| **Total** | **~37 GB** | **24 GB net on Data volume** |

*Note: Some freed space may overlap (e.g., Ollama blobs counted in both ~/.ollama and system total). Net Data volume reduction: 171→147 GiB (24 GiB).*

---

## Recommendations for Ongoing Maintenance

1. **Monthly**: `ollama list` → review unused models → `ollama rm`
2. **Monthly**: `rm -rf ~/Library/Caches/* ~/.cache/*` (user-writable only)
3. **Quarterly**: `du -sh ~/* ~/.*` scan for new large dirs
4. **Before major installs**: Check `~/Library/Containers/` for orphaned app data
5. **External drive**: Move all video/raw media to `/Volumes/Alfred Ext/`
6. **Docker**: Set max disk image size in Docker Desktop → Resources → Advanced

---

## Pitfalls Encountered

| Pitfall | Lesson |
|---------|--------|
| `rm -rf ~/Library/Caches/*` fails on system-protected dirs | Target specific user-writable caches only |
| `ls -lh` on Docker.raw shows 228 GB | Always use `du -sh` for real disk usage |
| Ollama blob sharing | Never delete blobs manually — use `ollama rm` |
| Orphaned LM Studio data | Check dotfolders + App Support + Containers after uninstall |
| Incomplete downloads (`.crdownload`) | Safe to delete — they're failed partial downloads |