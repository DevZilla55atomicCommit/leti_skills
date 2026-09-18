# Instagram Reels Pipeline v2 — Unified Architecture Plan

**Status**: PLANNED (not yet implemented)  
**Created**: 2026-07-20  
**Target**: Merge `process_reels.py` (URL-based) + `process_block_a_v2.py` (local files) into single script with `--source` flag.

---

## Unified Entry Point

```bash
# URL-based (downloads fresh via Hermes browser tools)
python3 process_reels.py --source urls --urls-file /tmp/reel_urls.json \
    --cookies ~/Downloads/cookies_www.instagram.com_YYYY-MM-DD.txt \
    --vault-base "/path/to/DaVinci_Knowledge_Base" \
    --skills-base ~/.hermes/skills/videographer

# Local files (skips download, uses existing MP4s)
python3 process_reels.py --source local --input-dir "/Volumes/Samsung LED/Instagram Downloads" \
    --vault-base "/path/to/DaVinci_Knowledge_Base" \
    --skills-base ~/.hermes/skills/videographer

# Hybrid: URLs but check archive first
python3 process_reels.py --source urls --urls-file /tmp/reel_urls.json \
    --archive-dir "/Volumes/Samsung LED/Instagram Downloads" \
    --vault-base "/path/to/DaVinci_Knowledge_Base"
```

---

## v2 Key Improvements (All Validated 2026-07-20)

| # | Improvement | Status | Validation |
|---|-------------|--------|------------|
| 1 | **Pre-flight cookie check** embedded in script (exits non-zero if sessionid < 1hr) | ✅ Planned | Cookie expired mid-batch Jul 19 |
| 2 | **Archive-first logic** | ✅ Planned | Check `/Volumes/Samsung LED/.../{CODE}.mp4` before download |
| 3 | **99.9% frame seek** instead of 100% | ✅ Validated | Avoids seek-past-end on short clips |
| 4 | **≥7 frame tolerance** | ✅ Validated | Short clips may fail at one percentage |
| 5 | **Single GIF output**: `frames/{CODE}.gif` only | ✅ Validated | No vault root duplicate |
| 6 | **Note references**: `frames/frame_XX.png` and `frames/{CODE}.gif` | ✅ Validated | No root copies |
| 7 | **Hermes browser tools as primary** (yt-dlp fallback removed) | ✅ Validated 92/93 | Browser tools bypass IG API blocks |

---

## Archive-First Logic

```python
def get_or_download_video(reel_code, url, cookies_file, archive_base):
    """Return local video path — download only if not archived."""
    archive_path = os.path.join(archive_base, f"{reel_code}.mp4")
    
    if os.path.exists(archive_path):
        print(f"  ♻️  Using archived: {archive_path}")
        return archive_path
    
    # Download to temp, then copy to archive
    temp_path = download_reel(reel_code, url, cookies_file)
    if temp_path:
        shutil.copy2(temp_path, archive_path)
        os.remove(temp_path)
        return archive_path
    return None
```

---

## Frame Extraction Fixes (from `process_block_a_v2.py`)

```python
# Use 99.9% instead of 100% to avoid seeking past last frame
FRAME_PERCENTAGES_V2 = [0, 14, 28, 42, 57, 71, 86, 99.9]

# Accept ≥7 frames (short reels may fail at 100%)
MIN_FRAMES_REQUIRED = 7
```

---

## Single GIF + Vault Note Structure

```
Videographer/{Discipline}/
├── frames/                    # Canonical frame store
│   ├── {CODE}/
│   │   ├── frame_00.png ... frame_07.png
│   │   └── {CODE}.gif         # ONLY GIF here
├── {CODE}.md                  # Note references frames/{CODE}/...
```

Note content:
```markdown
## Frames (0%, 14%, 28%, 42%, 57%, 71%, 86%, 100%)
![[frames/{CODE}/frame_00.png]]
...
![[frames/{CODE}/frame_07.png]]

## Preview
![[frames/{CODE}/{CODE}.gif]]
```

---

## DaVinci MCP Color Analysis (Phase 2)

After vault note creation:

```python
async def analyze_with_davinci_mcp(reel_code, mp4_path):
    # 1. Import to Media Pool
    clip_id = media_storage.import_to_pool([mp4_path])
    
    # 2. Vision analysis
    vision = media_analysis.analyze_clip(
        clip_id=clip_id,
        vision=True,
        transcription=False
    )
    
    # 3. Grade evidence base
    evidence = timeline_item_color.grade_evidence_base(
        track_type="video", track_index=1, item_index=0
    )
    
    # 4. Parse for color science metadata
    color_data = extract_color_science(vision, evidence)
    
    # 5. Append to vault note
    append_davinci_section(note_path, color_data)
```

**Extracted fields**:
- Log format (S-Log3, Apple Log 2, etc.)
- Color space (S-Gamut3.Cine, etc.)
- Exposure level (IRE, stops over/under)
- Suggested CST input/output
- LUT recommendations (Kodak 2383, Fujifilm, etc.)

---

## Implementation Order

1. **Phase 1** (this session): Refactor `process_reels.py` with:
   - Mandatory pre-flight cookie check ✅ (patched)
   - `--source` flag (urls|local)
   - Archive-first download logic
   - 99.9% frame seek + ≥7 tolerance
   - Single GIF in frames/
   - Note refs

2. **Phase 2** (next session): DaVinci MCP integration
   - Requires DaVinci Resolve running + MCP server connected
   - Append `## DaVinci Color Analysis` to vault notes

3. **Phase 3**: Batch retry of 93 failed reels from `failed_reels_93.md`

---

## References

- `scripts/process_reels.py` — main pipeline (patched with pre-flight)
- `scripts/process_block_a_v2.py` — local-file processor (reference for v2 features)
- `scripts/process_local_files.py` — shared local processing logic
- `references/frame-extraction-fix.md` — 99.9% seek + ≥7 frames rationale
- `references/cookie-setup.md` — cookie workflow
- `references/failed_reels_93.md` — retry queue