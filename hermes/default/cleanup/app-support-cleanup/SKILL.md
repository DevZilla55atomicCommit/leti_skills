---
title: App Support Cleanup
description: Safely prune macOS Application Support directories for storage
name: app-support-cleanup
tags: [cleanup, app-support, automation]
owner: user
---

# App Support Cleanup

A class-level skill for safely pruning macOS Application Support directories to reclaim storage space. Designed for Hermes agents managing user storage.

## Overview
- Targets: Claude-3p, Google, Docker installer, VS Code caches, Filmora, ON1, **AI/ML model caches (Ollama, LM Studio, Hermes), system caches, container sandboxes, dotfolder caches**.
- Safety-first: verifies folder sizes, backs up critical data, logs actions.
- Execution: deterministic script with confirmation prompts.

## Key Space-Consumption Patterns (Discovered July 2026)
- **AI/ML Model Caches**: `~/.ollama/models/blobs/` (46 GB in session), `~/.lmstudio/` (7.8 GB orphaned), `~/.hermes/` (4.4 GB)
- **System Caches**: `~/Library/Caches/` (6 GB), `~/.cache/` (3.3 GB)
- **Container Sandboxes**: `~/Library/Containers/` (8.9 GB - Docker, VS Code, etc.)
- **Application Support**: `~/Library/Application Support/` (9.7 GB - Cursor, VS Code, Chrome, Docker, Hermes)
- **Dotfolder Caches**: `~/.vscode` (1.3 GB), `~/.npm` (1.2 GB), `~/.codex` (790 MB), `~/.docker` (179 MB)
- **Orphaned App Data**: App data directories persisting after app uninstall (LM Studio case)

## Identification Commands
```bash
# Top-level user directory scan
du -sh ~/* ~/.* 2>/dev/null | sort -hr | head -30

# Application Support breakdown
du -sh ~/Library/Application\ Support/* 2>/dev/null | sort -hr | head -20

# Ollama model blobs (largest single consumers typically)
du -sh ~/.ollama/models/blobs/* | sort -hr | head -20

# System caches
du -sh ~/Library/Caches/* 2>/dev/null | sort -hr | head -20

# Containers (sandbox data)
du -sh ~/Library/Containers/* 2>/dev/null | sort -hr | head -20
```

## Overview
- Targets: Claude-3p, Google, Docker installer, VS Code caches, Filmora, ON1, **AI/ML model caches (Ollama, LM Studio, Hermes), system caches, container sandboxes, dotfolder caches**.
- Safety-first: verifies folder sizes, backs up critical data, logs actions.
- Execution: deterministic script with confirmation prompts.

## Key Space-Consumption Patterns (Discovered July 2026)
- **AI/ML Model Caches**: `~/.ollama/models/blobs/` (46 GB in session), `~/.lmstudio/` (7.8 GB orphaned), `~/.hermes/` (4.4 GB)
- **System Caches**: `~/Library/Caches/` (6 GB), `~/.cache/` (3.3 GB)
- **Container Sandboxes**: `~/Library/Containers/` (8.9 GB - Docker, VS Code, etc.)
- **Application Support**: `~/Library/Application Support/` (9.7 GB - Cursor, VS Code, Chrome, Docker, Hermes)
- **Dotfolder Caches**: `~/.vscode` (1.3 GB), `~/.npm` (1.2 GB), `~/.codex` (790 MB), `~/.docker` (179 MB)
- **Orphaned App Data**: App data directories persisting after app uninstall (LM Studio case)

## Identification Commands
```bash
# Top-level user directory scan
du -sh ~/* ~/.* 2>/dev/null | sort -hr | head -30

# Application Support breakdown
du -sh ~/Library/Application\ Support/* 2>/dev/null | sort -hr | head -20

# Ollama model blobs (largest single consumers typically)
du -sh ~/.ollama/models/blobs/* | sort -hr | head -20

# System caches
du -sh ~/Library/Caches/* 2>/dev/null | sort -hr | head -20

# Containers (sandbox data)
du -sh ~/Library/Containers/* 2>/dev/null | sort -hr | head -20
```

## Workflow
1. **Identify Targets** - List folders to clean (see references/macOS-app-support-cleanup.md).
2. **Pre-Flight Checks** - Verify backups, sizes, and user intent.
3. **Execute Cleanup** - Run `scripts/run-cleanup.sh`.
4. **Post-Cleanup Report** - Show reclaimed space and verification.

## Common Pitfalls
- Deleting Blackmagic Design or Adobe folders accidentally (see Pitfall #3).
- Removing snapshots that are still in use by background processes.
- **Orphaned App Data**: App bundles may be gone but data persists in `~/Library/Application Support/`, `~/Library/Containers/`, `~/.<appname>`. Always check for these before assuming cleanup is complete.
- **AI Model Blobs**: Ollama/LM Studio models use content-addressable storage (blobs shared across models). Removing one model's manifest may not free space if blobs are shared. Use `ollama rm <model>` to properly dereference.
- **Sparse Files**: Docker VM disk images (`Docker.raw`) report massive *apparent* sizes (228 GB) but consume minimal *actual* disk (8 MB). Always verify with `du -sh` not `ls -lh` before flagging as a space issue.
- **System-Protected Caches**: `~/Library/Caches/` contains macOS-protected directories (CloudKit, Safari, HomeKit, FindMy) that cannot be deleted without SIP disable. Target only user-writable caches.
- **Incomplete Downloads**: `.crdownload` / `.part` files on Desktop/Downloads are safe to delete — they're failed/partial downloads.

## LM Studio Cleanup (Orphaned Install - July 2026)
**Discovered**: LM Studio app bundle removed but `~/.lmstudio/` (7.8 GB) and `~/Library/Application Support/LM Studio/` (1.8 MB) remained.
**Models found**: `lmstudio-community/gemma-4-E4B-it-MLX-4bit/` (6.4 GB)
**Action**: 
```bash
# Safe removal (no app to manage it)
rm -rf ~/.lmstudio
rm -rf "~/Library/Application Support/LM Studio"
```
**Space reclaimed**: ~7.8 GB

## Verification
- Compare `du -sh` before/after.
- Confirm no critical apps break after cleanup.

## Recent Execution (July 29, 2026)
- Freed ~6.3 GB across ON1, FluidAudio, Minecraft, Google Cache, VS Code caches.
- Deleted directories safely; no critical apps impacted.
- Verified free space increased from 128 GB to 135 GB.

## Support Files
- `references/macOS-app-support-cleanup.md` - Detailed directory breakdown and size tables.
- `templates/cleanup-confirmation.yaml` - Config template for customizing target folders.
- `scripts/run-cleanup.sh` - Main execution script.
- `references/macOS-app-support-cleanup-2026-07-30.md` - Log of the July 30 cleanup actions.