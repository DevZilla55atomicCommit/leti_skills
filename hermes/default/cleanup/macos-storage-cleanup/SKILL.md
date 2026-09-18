---
name: macos-storage-cleanup
description: Analyze macOS disk usage, identify space hogs, and safely reclaim storage on Apple Silicon Macs
category: cleanup
version: 1.0.0
---

# macOS Storage Cleanup & Disk Space Analysis

A class-level skill for analyzing macOS disk usage, identifying space hogs, and safely reclaiming storage on Apple Silicon Macs.

## When to Use
- User reports low disk space on macOS
- Need to audit storage before major installs/updates
- Regular maintenance to reclaim GBs of space
- Preparing external drives for media workflows

## Core Workflow

### 1. Quick Disk Overview
```bash
df -h
```
Shows all mounted volumes, capacity, used, available. Focus on `/System/Volumes/Data` (user data volume on APFS).

### 2. Top-Level Directory Scan
```bash
du -sh ~/* ~/.* 2>/dev/null | sort -hr | head -20
```
Identifies largest directories in home folder. Run as user (no sudo needed for ~/).

### 3. Deep Dive on Suspects
```bash
# Library caches (safe to clear)
du -sh ~/Library/Caches/* | sort -hr

# Application Support (app-specific data)
du -sh ~/Library/Application\ Support/* | sort -hr

# Containers (sandboxed app data)
du -sh ~/Library/Containers/* | sort -hr

# Common AI/ML tool caches
du -sh ~/.ollama ~/.lmstudio ~/.cache ~/.huggingface 2>/dev/null | sort -hr
```

### 4. Find Large Files
```bash
find ~ -type f -size +500M 2>/dev/null | head -30
```
Lists files >500MB in home directory.

### 5. Check Specific Known Hogs

**Ollama Models:**
```bash
ollama list
# Remove unused: ollama rm <model>
# Data at: ~/.ollama/models/blobs/
```

**Claude Cowork VM (Ollama-provisioned Claude Desktop):**
```bash
du -sh ~/Library/Application\ Support/Claude-3p/vm_bundles ~/Library/Application\ Support/Claude-3p/local-agent-mode-sessions 2>/dev/null
ps aux | grep -E "claude-code|local-agent-mode|cowork" | grep -v grep
```
- Chat/Code with an Ollama local model is just API calls to `http://localhost:11434` using weights already in `~/.ollama/models` — no VM, nothing extra to clean.
- Cowork with a local model spins up the sandboxed VM (`vm_bundles/claudevm.bundle`, 8-15 GB); it regenerates on the next Cowork+local run, so deleting it only sticks if the user stays on Chat/Code or Cowork+cloud. Confirm the cowork `claude-code` process is gone (only `Claude Helper` processes remain) before deleting, or it recreates immediately.

**LM Studio:**
```bash
du -sh ~/.lmstudio/models/*
# App may not be installed but data remains
```

**Docker:**
```bash
docker system df
docker system prune -a --volumes  # ⚠️ destructive
```

**Node/npm:**
```bash
npm cache clean --force
du -sh ~/.npm  # cache clean frees only the cache portion; global-package metadata remains, so re-run du before quoting gains
```

**Python/uv/pip:**
```bash
pip cache purge
uv cache clean
du -sh ~/.cache/uv ~/.cache/pip
# ~/.local/share/uv holds uv-managed Python INTERPRETERS, not cache — `uv cache clean`
# does not touch them. Never delete them to chase space; projects pin those versions.
```

**pnpm:**
```bash
pnpm store prune  # drops only packages no project references; re-fetches on next install
# If the store stays large after prune, it is live project dependencies — leave it.
```

### 6. Safe Cache Clearing
```bash
# User caches (safe - apps rebuild)
rm -rf ~/Library/Caches/com.spotify.client  # Spotify offline
rm -rf ~/Library/Caches/com.google.Chrome   # Chrome cache
rm -rf ~/.cache/uv ~/.cache/pip ~/.cache/huggingface
rm -rf ~/.npm/_npx  # one-off npx package cache; re-downloads on next npx run

# NEVER delete these (macOS protected):
# ~/Library/Caches/CloudKit
# ~/Library/Caches/com.apple.Safari
# ~/Library/Caches/com.apple.findmy.*
```

### 7. External Drive Management
```bash
# Check external usage
df -h /Volumes/*

# Move large media folders
mkdir -p /Volumes/ExternalDrive/Video_Archive
mv ~/Desktop/VideoProject /Volumes/ExternalDrive/Video_Archive/

# For app-owned cache paths (e.g. DaVinci `~/Movies/CacheClip`), move then symlink back
# so the app keeps working without reconfiguration:
mkdir -p /Volumes/ExternalDrive/DaVinci_Cache
mv ~/Movies/CacheClip /Volumes/ExternalDrive/DaVinci_Cache/CacheClip
ln -s /Volumes/ExternalDrive/DaVinci_Cache/CacheClip ~/Movies/CacheClip
# Caveat: the external volume MUST be mounted whenever the app runs, or cache writes fail.
# Prefer the roomiest volume — check `df -h /Volumes/*` first and avoid moving onto a drive already >85% full.
# Before assigning any external as app scratch/cache, qualify it first:
# see `references/external-scratch-disk.md` (sequential-WRITE benchmark + filesystem checks).
```

### Common Space Hogs on Creative Macs

| Location | Typical Size | Safe to Clean? |
|----------|-------------|----------------|
| `~/.ollama/models/blobs/` | 10-100 GB | ✅ Via `ollama rm` |
| `~/.hermes/backups/pre-update-*.zip` | 7-50 GB each | ✅ Keep latest 1-2 |
| `~/.hermes/state.db.pre-update-emergency-*.bak` | 1 GB each | ✅ Keep latest 1 |
| `~/.hermes/state-snapshots/` | 0.5-1 GB each | ✅ Keep latest 1 |
| `~/.hermes/profiles/*/skills/` (duplicated) | 6-7 GB per profile | ✅ Dedup to shared (see hermes-profile-skills-dedup) |
|| `~/.lmstudio/models/` | 5-50 GB | ✅ Delete folder if app gone |
|| `~/.lmstudio/extensions/backends/` | 1-3 GB | ✅ Keep latest version only |
|| `~/Library/Caches/` | 1-10 GB | ✅ Most entries |
|| `~/.cache/` | 1-20 GB | ✅ All (uv, pip, huggingface, codex) |
|| `~/Library/Containers/com.docker.docker/` | 10-100 GB | ✅ `docker system prune` |
|| `~/Library/Parallels/Downloads/*.iso` | 5-10 GB | ✅ After VM verified |
|| `~/Downloads/` | 1-20 GB | ✅ Review manually |
|| `~/Desktop/*.mov/*.mp4` | 1-50 GB | ✅ Move to external |
|| DaVinci Resolve installers (.dmg/.zip) | 5-15 GB each | ✅ After install verified |
|| `~/Movies/CacheClip/` | 1-10 GB | ✅ Regenerable render cache (`.dvcc` frames in per-project GUID folders + Fairlight `.pfl` audio) — move to external + symlink, or Playback → Delete Render Cache in Resolve |
|| `~/Library/Application Support/Google/Chrome/OptGuideOnDeviceModel/` | 1-5 GB | ⚠️ Ask first — if the user uses Chrome AI features (Help Me Write, tab organizer) it is working space and Chrome re-downloads it |
|| `~/Library/Application Support/Claude-3p/vm_bundles/` | 8-15 GB | ⚠️ Only if VM stale — verify first (see pitfall 8); deleting an active Cowork VM breaks local-agent-mode until it re-downloads |
|| Telegram `.../Group Containers/*.ru.keepcoder.Telegram/appstore/<account>/postbox/media/` | 1-10 GB | ✅ Cached media, re-fetches from cloud — keep sibling `postbox/db/` (login + chats); quit Telegram first |
|| `~/Library/Application Support/Google/GoogleUpdater/crx_cache/` | 0.5-1 GB | ✅ Stale update payloads, re-download on next update |
|| `~/Movies/Fairlight Sound Library/` | 1-2 GB | ✅ Static content — move to external + symlink like CacheClip |

## Hermes-Specific Deep Cleanup

Hermes Agent accumulates several categories of large, safe-to-delete artifacts. Audit these **before** generic cache cleaning — they're often the biggest wins.

### 1. Pre-Update Backup Zips (`~/.hermes/backups/pre-update-*.zip`)
- **Size**: 7-50 GB each (full Hermes state: skills, profiles, state.db, sessions)
- **Behavior**: Auto-created before Hermes updates
- **Action**: Keep latest 1-2; delete older:
```bash
ls -la ~/.hermes/backups/pre-update-*.zip
rm ~/.hermes/backups/pre-update-*.zip  # delete all old ones
```

### 2. Emergency State DB Backups (`~/.hermes/state.db.pre-update-emergency-*.bak`)
- **Size**: ~1 GB each (exact copy of state.db at update time)
- **Behavior**: Created during Hermes updates as safety copies
- **Action**: Keep latest 1; delete older:
```bash
ls -la ~/.hermes/state.db.pre-update-emergency-*.bak
rm ~/.hermes/state.db.pre-update-emergency-*.bak  # delete all if current works
```

### 3. State Snapshots (`~/.hermes/state-snapshots/`)
- **Size**: 0.5-1 GB each (full profile directory snapshot)
- **Behavior**: Created before major updates
- **Action**: Keep latest 1; delete older:
```bash
ls -la ~/.hermes/state-snapshots/
rm -rf ~/.hermes/state-snapshots/<old-folder>
```

### 4. Profile Skills Deduplication (`~/.hermes/profiles/*/skills/`)
- **Size**: ~6.9 GB per profile (mirrors shared skills)
- **Behavior**: Each profile gets a full copy of `~/.hermes/skills/`
- **Action**: Remove duplicated profile skills folders (fallback to shared):
```bash
for p in ~/.hermes/profiles/*/; do
  profile=$(basename "$p")
  if [ "$profile" != "default" ] && [ -d "$p/skills" ]; then
    rm -rf "$p/skills"
  fi
done
```
- **Expected savings**: 5 specialized profiles × 6.9 GB = **~34.5 GB**
- **See also**: `hermes-profile-skills-dedup` skill for full workflow

### 5. Corrupt Config Backups (`~/.hermes/config.yaml.corrupt.*.bak`)
- **Size**: ~15 KB each (negligible but messy)
- **Action**: `rm ~/.hermes/config.yaml.corrupt.*.bak`

---

**Real session result (Aug 2026):**
| Item | Freed |
|------|-------|
| Profile skills dedup (5 profiles) | 34.5 GB |
| Emergency state.db backups (3) | 2.9 GB |
| State snapshot (1) | 741 MB |
| Pre-update backup zip (1, Aug 20) | 42 GB |
| Corrupt configs (~30) | ~400 KB |
| **Total** | **~45.6 GB** |

SSD went from 85% full (66 GiB free) → 75% full (111 GiB free).

## Pitfalls & Gotchas

1. **System vs Data volumes** — On APFS, `/` (system) and `/System/Volumes/Data` (user) share space. `df -h /` shows system volume; check Data volume for user files.

2. **Protected caches** — macOS blocks deletion of CloudKit, Safari, Find My caches. Ignore "Operation not permitted" errors; skip those.

3. **Ollama blobs are deduplicated** — Multiple models share blob layers. `ollama list` shows logical size; `du` on blobs shows physical. Removing one model may free less than listed. Same-family variants (e.g. `qwen3.5-32k/-48k/-96k`) share one weight blob, so removing a single stale variant frees ~0 — only removing the whole family frees the blob. Verify by re-running `du -sh ~/.ollama/models` after `ollama rm`; if physical size barely moved, the blobs were shared. After removing a variant, repoint any consumer pinned to its tag (Claude Code `model` in settings.json, model-switcher scripts, default-context pointers) — a removed default tag breaks the next launch; confirm the replacement tag exists in `ollama list` first.

4. **Docker.raw disk image** — `~/Library/Containers/com.docker.docker/Data/vms/0/data/Docker.raw` grows but doesn't shrink. Must use `docker system prune` + restart Docker Desktop.

5. **Time Machine local snapshots** — Can consume 50+ GB. Check: `tmutil listlocalsnapshots /` and thin: `tmutil thinlocalsnapshots / 10000000000 4`

6. **Don't use `sudo du` on ~/Library** — Permission errors slow it down. Run as user; `du` skips unreadable dirs gracefully.

7. **Verify apparent size with `du` before promising gains** — Interrupted model downloads (Draw Things `.ckpt.partial`, LM Studio partials) preallocate full size as sparse files: `ls -lh` shows tens of GB apparent while `du -sh` shows only written blocks. Deleting frees only the `du` figure — compare both before quoting savings. Healthy sparse VM disk images behave the same way: `du` can report the provisioned/logical size (e.g. an 11 G bundle that is mostly empty holes) while only a fraction is physical — the `df` before/after delta is ground truth, not `du`.

8. **Verify a VM bundle is stale before deleting it** — `Claude-3p/vm_bundles/claudevm.bundle` holds Cowork's Linux VM (`rootfs.img` + kernel + `sessiondata.img`); deleting an active one breaks local-agent-mode until it re-downloads and re-extracts. Check `sessiondata.img`/`vmIP` mtimes, presence of `.cowork-adopted`, and running app processes first — recent timestamps mean it is working space, not junk. Post-deletion effect is bounded: chat history, sessions, and the native CLI survive — only the next sandboxed run pays a re-download plus environment re-setup, so confirm the user accepts that cold start before deleting an active VM.

9. **Quit the app before clearing its cache** — Deleting cache files out from under a running app (Telegram, Spotify, Chrome) risks glitches or immediate re-creation that hides the gain. Quit via osascript, delete, verify with `du`, then relaunch.

10. **Attribute sudden jumps by mtime before treating them as creep** — A multi-GB jump in a week is usually discrete downloads, not leaks. Run `stat -f "%Sm %z %N" -t "%Y-%m-%d %H:%M"` on the top suspects (ollama blobs, VM bundles, Desktop) and match timestamps to known pulls/installs — a VM download plus two model pulls explains tens of GB and needs no remediation, only awareness at pull time.

11. **Full-home `du` stalls on symlinks to external volumes** — `du -sh ~/*` follows symlinks, so a vault or media folder symlinked to a USB drive can hang the scan past any timeout. Exclude the link (`du -sh ~/* --exclude=<link>` is unreliable on BSD du — instead enumerate targets explicitly) or fall back to targeted scans (`~/Library`, top dotfiles) when a full pass times out.

12. **Debug dumps regrow while the underlying failure continues** — `sessions/request_dump_*.json` with same-day mtimes means requests are failing *now*; deleting the files frees space once but they accumulate again within hours. Check freshness first — current timestamps mean fix the failing model call, not the dumps.

13. **Spot dead profiles by cross-profile mtime, not by name** — A profile folder untouched for days while every sibling was modified today is a leftover duplicate, not an in-use profile. Compare `stat -f "%Sm %N"` across `~/.hermes/profiles/*/` before deleting; confirm with the user when the name is ambiguous (e.g. `default-2`).

14. **`df` lags large deletes on APFS — re-check before concluding** — Deleting a multi-GB bundle (VM image, model blob) may show only partial gain in `df` immediately; macOS reclaims the rest asynchronously over minutes. Re-run `df -h /System/Volumes/Data` after a few minutes before reporting savings or chasing further deletes.

15. **Exclude AppleDouble sidecars when verifying archive copies to ExFAT externals** — macOS writes a `._*` sidecar per file on ExFAT/FAT32 volumes, roughly doubling file counts. Compare real files only (`find <dir> -type f ! -name '._*'` on both sides) before concluding a backup is incomplete or corrupt — and before deleting the original.

16. **Confirm disuse by mtime and archive before removing app containers** — For opaque app data (Wine prefixes, abandoned tool installs), run `find <dir> -type f -newermt "<N-months-ago>"` first: zero recent hits means disused. Copy to external, verify (see 15), then `rm -rf` — never delete-first on data the user may want back.

17. **macOS volume paths are literal — list `/Volumes` before scripting them** — Names can carry trailing spaces or unexpected characters that break hand-typed quoting. Copy the exact name from `ls /Volumes/` output. Related: BSD `find` on macOS has no `-printf`; use `stat -f "%Sm %N" -t "%Y-%m-%d %H:%M"` for mtime-sorted listings.

18. **Check for iCloud-dataless files before promising gains from organizing folders** — With Optimize Mac Storage, evicted files show real logical sizes in `ls -lh` but `du -sh` reports ~0B and `ls -laO` flags them `compressed,dataless`. Reorganizing such folders frees ~0 local SSD (iCloud already did) — say so up front so the user calibrates expectations. Related: moving dataless files to an external volume triggers a download-then-move (network + temp SSD); moves within iCloud-synced locations cost nothing. Quote external moves accordingly.

## Verification Checklist
After cleanup, verify:
- [ ] `df -h /System/Volumes/Data` shows increased free space
- [ ] Critical apps still launch (Docker, Ollama, Chrome, DaVinci)
- [ ] No "Operation not permitted" errors on user-writable paths
- [ ] External drive has expected media files after move

## References
- `references/common-hogs.md` — Detailed breakdown of typical space consumers on creative Macs
- `references/safe-cache-list.md` — Whitelist of caches safe to delete vs protected
- `scripts/scan-storage.sh` — Reusable scan script for quick audits
- `references/safe-capcut-cache.md` — CapCut cache cleanup specifics
- `references/trash-management.md` — Emptying and verifying Trash across volumes, TCC pitfalls
- `references/external-scratch-disk.md` — Qualifying an external drive as app scratch/cache: write-benchmark, filesystem, mount caveats