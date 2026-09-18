---
name: macos-mp4-gather
description: Locate all .mp4 files across macOS for audits.
title: macOS MP4 File Gathering
---

# macOS MP4 Gather Skill

## Purpose
Discover every `.mp4` file across the user's home directory, handling large project directories, CapCut caches, or scattered media assets.

## Trigger
Use when the user asks to "gather all raw mp4 files" or similar.

## Core Procedure

1. **Primary Search – `search_files`**
   ```yaml
   search_files:
     pattern: "*.mp4"
     target: "files"
     limit: 200
     path: <starting‑point>
   ```
   - Start at the user’s home (`/Users/<username>`) or a specific root.
   - High `limit` (200) and monitor for `truncated` flag.

2. **Chunked Expansion – `offset`**
   If `truncated: true`, repeat with `offset=200` until `truncated` is `false`.

3. **Fallback – `terminal find`**
   When `search_files` times out, run:
   ```bash
   find <root> -name "*.mp4" -maxdepth 4 2>/dev/null | head -50
   ```
   - `-maxdepth 4` limits recursion depth.
   - Pipe to `head -50` for manageable output.

4. **Organize Results**
   - Store list in `/tmp/mp4‑gather‑<timestamp>.txt`.
   - Optionally compute sizes (`du -sh`) to highlight space hogs.
   - Return concise summary (count, notable directories, space hogs).

## Pitfalls & Gotchas
- **Timeouts**: `search_files` may hit 60 s on huge trees; treat `truncated` as a cue to use `find` fallback.
- **Hidden Cache Folders**: CapCut caches under `Movies/CapCut/...` are often ignorable unless user wants cleanup.
- **Duplicate Paths**: Multiple sync locations can duplicate files; flag if needed.
- **Permission Errors**: Suppress “Permission denied” with `2>/dev/null`; only surface real results.

## Verification
- Optionally run `ls -lh <files>` to show sizes.
- Use `du -sh` on top‑level directories to identify space hogs.
- For cleanup, delegate to a cleanup skill (e.g., `mp4‑cleanup‑cache`).

## Example Output
```
Found 33 MP4 files.
- 7 on Desktop (project assets)
- 24 in Movies/CapCut cache (temporary renders)
- 2 in Downloads (duplicates)
Consider cleaning CapCut cache if free space is low.
```

## Extensions
- **Automatic Cleanup**: Move files older than X days to `~/Archive/mp4`.
- **Size Filtering**: Add `--size +100M` to `find` to ignore tiny clips.
- **Metadata Extraction**: Run `ffprobe` on each file to log duration/resolution.

---

*Register with `skill_manage(action='create', name='macos-mp4-gather', category='file', content='<markdown>')` for future reuse.*