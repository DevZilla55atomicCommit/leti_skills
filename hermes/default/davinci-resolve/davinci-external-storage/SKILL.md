---
name: davinci-external-storage
description: Use when hosting DaVinci Resolve cache on external storage.
category: davinci-resolve
version: 1.0.0
---

# DaVinci Resolve External Storage Setup

Keep Resolve's growth paths (render cache, gallery stills, optimized media,
project backups, renders) off the internal SSD by hosting them on an external
volume with symlinks back to the default `~/Movies` locations.

## When to Use
- Internal SSD above ~80% and Resolve projects are planned
- User reports SSD filling fast during editing/grading
- Setting up a new machine or drive for Resolve work

## 1. Qualify the Drive (in order — any fail disqualifies)

```bash
# Filesystem + protocol + writability (note: trailing space in volume names is real)
diskutil info "/Volumes/NAME" | grep -E "File System Personality|Protocol"
touch "/Volumes/NAME/.__writetest" && rm "/Volumes/NAME/.__writetest" && echo WRITABLE
```
- Filesystem: APFS/HFS+/ExFAT acceptable. ExFAT works but has no journaling —
  eject properly before unplugging.
- Must be writable from macOS (NTFS without a driver fails here).

```bash
# Sequential speed: 2 GB write + read (cache is write-heavy — weight WRITE)
dd if=/dev/zero of="/Volumes/NAME/.__speedtest" bs=64m count=32 2>&1 | tail -1
dd if="/Volumes/NAME/.__speedtest" of=/dev/null bs=64m 2>&1 | tail -1
rm -f "/Volumes/NAME/.__speedtest"
```
- Thresholds: write >= ~100 MB/s handles DNxHR LB/SQ cache + proxy media.
  Full-res HQ 4K cache wants 200+ MB/s (usually internal-SSD only).
- Compare candidates head-to-head; SSDs can lose on write (QLC + ExFAT
overhead observed at ~58 MB/s vs HDD at ~134 MB/s).
- Headroom: cache + optimized media exceed 10 GB per project fast. A drive
  with < 20 GB free is disqualified regardless of speed.

## 2. Workspace Layout

Create beside any existing folders (never inside course/training material):

```bash
W="/Volumes/NAME/DaVinci Resolve/Resolve_Workspace"
mkdir -p "$W/Cache" "$W/Gallery" "$W/Optimized" "$W/Projects" "$W/Renders"
```

## 3. Move + Symlink (Resolve keeps working, zero reconfig)

Quit Resolve first. Move each internal dir, symlink back to the old path:

```bash
mv ~/Movies/CacheClip "$W/Cache/CacheClip" && ln -s "$W/Cache/CacheClip" ~/Movies/CacheClip
mv ~/Movies/.gallery "$W/Gallery/stills" && ln -s "$W/Gallery/stills" ~/Movies/.gallery
mv ~/Movies/Fairlight\ Sound\ Library "$W/Fairlight Sound Library" && ln -s "$W/Fairlight Sound Library" ~/Movies/Fairlight\ Sound\ Library
```
- `TV/` and `reolink/` in ~/Movies are NOT Resolve's — leave them.
- `Resolve Project Backups/` relocates via Project Manager settings (in-app),
  not by moving files.

## 4. In-App Prefs (user does this — cannot be set reliably from terminal)

- Preferences → Media Storage → Add → workspace root → make it FIRST entry
  (first = cache + gallery home). Keep `~/Movies` as fallback or remove.
  Reorder trick: Remove then re-Add entries in desired order. Save, Cmd+Q,
  reopen (storage changes need a restart).
- Project Settings → Master Settings → Working Folders → confirm all resolve
  under the workspace.
- Project Manager → project backup location → `$W/Projects`.
- Deliver → default render output → `$W/Renders`.

## 5. Verify

```bash
for l in ~/Movies/CacheClip ~/Movies/.gallery ~/Movies/Fairlight\ Sound\ Library; do
  [ -d "$l" ] && echo "OK: $l ($(du -shL "$l" | cut -f1))" || echo "BROKEN: $l"
done
df -h /System/Volumes/Data
```
- NOTE: `du -sh` on a symlink reports the link (near 0B) — use `du -shL` to
  follow links and confirm real data.
- In-app storage list CANNOT be read from any plist — it lives in Resolve's
  project-library DB. Verify via user-confirmed screenshot (OCR it, see below).

## 6. Screenshot OCR (no vision tool in session)

When the user sends a prefs-dialog screenshot, OCR it with the bundled script:

```bash
swiftc -o /tmp/ocr <skill>/scripts/ocr.swift  # one-time build
/tmp/ocr /path/to/screenshot.png
```
Uses Apple's on-device Vision framework: offline, no downloads, no API cost.

## Standing Rules for the User

- Mount the external drive BEFORE launching Resolve (cache writes fail to
  missing volumes).
- Never edit from ~/Downloads or Desktop — import with "Copy to" the workspace.
- Post-project closeout: Playback → Delete Render Cache → All, delete
  Optimized Media, export .drp + Project Archive to `$W/Projects`.

## Pitfalls

- ExFAT `._AppleDouble` sidecar files inflate small-dir sizes after moves —
  cosmetic, ignore (or `dot_clean`).
- Volume names with trailing spaces ("Alfred Ext ") are real — quote paths.
- Samsung-class QLC SSDs over USB can write slower than HDDs; always measure
  WRITE, not just read.
- Do not `rm` user media (mp4/pdf on Desktop) when "move to external" was
  the intent — confirm delete vs move explicitly.
