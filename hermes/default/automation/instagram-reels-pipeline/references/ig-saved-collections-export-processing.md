# Instagram Saved Collections Export Processing

**Date:** 2026-07-20
**Session:** Full pipeline from IG data export → deduplication → per-collection NEW_ONLY files → overnight download

## Overview

This reference documents the complete workflow for processing Instagram's "Your Activity → Saved → Collections" JSON export into actionable download batches, deduplicated against existing DaVinci Knowledge Base vault content.

## Export Acquisition

1. Instagram → Settings → Your Activity → Download Your Information
2. Select "Saved" → JSON format → Download
3. Extract `saved_collections.json` (typical: ~15 MB, ~4,000 items, 128 collections)

## JSON Structure Parsing

```python
# JSON structure: List[Collection]
# Each Collection has:
#   - timestamp (creation)
#   - label_values: [Name, Type, Privacy, Update time, Media]
#   - Media items nested in label_values[4].dict[] with:
#       - URL, Caption, Hashtags, Owner, Brand partner
```

### Key Extraction Logic

```python
# 1. Find collection name from label_values[label="Name"]
# 2. Find Media container from label_values[title="Media"] 
# 3. For each media item: extract URL, caption, hashtags, owner, brand
# 4. Output: per-collection JSON + flat CSV + per-collection URL .txt files
```

### Hashtag Parsing (Critical Fix)

```python
# Structure: hashtags_info['dict'] -> list of {dict: [...], title: ""}
# Each inner dict -> list of {label: "Name", value: "hashtag_name"}
for h_group in hashtags_info.get('dict', []):
    for h_item in h_group.get('dict', []):
        tag = h_item.get('value')  # <-- NOT h_item.get('label')
        if tag:
            hashtags.append(tag)
```

**Bug caught:** Earlier attempt used `label` field which returned "Name" for every hashtag. The actual tag value is in `value` field.

## Deduplication Against Existing Vault/Knowledge Base

### Extract Existing URLs from Vault

```bash
# 1. Extract all instagram.com/reel URLs from vault markdown
grep -r "instagram.com/reel" "TamaZila Obsidian Vault/Hermes Agent/DaVinci_Knowledge_Base" \
  -o -E "https://www.instagram.com/reel/[A-Za-z0-9_-]+" | sort -u > kb_urls.txt

# Result: 425 unique URLs already in vault
```

### Compare with Saved Collections

```bash
# 2. Flat list of all saved collection URLs
comm -12 <(sort kb_urls.txt) <(sort instagram_all_urls_flat.txt) > overlap.txt
comm -13 <(sort kb_urls.txt) <(sort instagram_all_urls_flat.txt) > new_only.txt

# Results (2026-07-20):
# - Vault URLs: 425 unique
# - Saved Collection URLs: 3,820 unique  
# - Overlap: 408 (already processed)
# - New to process: 3,412
```

## Per-Collection NEW_ONLY Generation

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
- **Disciplines** = Auto-classified by caption keywords
- Pipeline writes to **Discipline folders** in vault
- Multiple collections map to same discipline (e.g., "Color grading" + "DaVinci Tricks" → `Color_Grading_&_Looks/`)

## Pipeline Integration

```bash
# Process each collection's NEW_ONLY file through existing pipeline
for f in instagram_new_urls_by_collection/*_NEW.txt; do
  python3 process_reels.py --urls-file "$f" --collection "$(basename "$f" _NEW.txt)"
done
```

## Scripts Created This Session

| Script | Purpose |
|--------|---------|
| `scripts/extract_saved_collections.py` | Parses saved_collections.json → per-collection JSON + flat CSV + URL .txt |
| `scripts/dedupe_against_kb.py` | Deduplicates collection URLs against existing vault KB |
| `scripts/gen_collection_new_only.py` | Generates per-collection NEW_ONLY.txt files |
| `scripts/download_instagram_collections.py` | **Overnight bulk downloader** with concurrency control, retry logic, resume, metadata sidecars, heartbeat logging, graceful shutdown |

## Download Script Features (download_instagram_collections.py)

- **Per-collection isolation** — failure in one doesn't stop others
- **2 concurrent downloads** — Instagram-safe rate limiting
- **Exponential backoff** — 30s → 60s → 120s → 240s → 480s (max 5 retries)
- **Resume support** — `--continue` + `--no-overwrites` skips existing files
- **Metadata sidecars** — `.meta.json` with caption, hashtags, owner, collection, download timestamp
- **Heartbeat logging** — every 60s: `HEARTBEAT | done/total | ✓✓ ✗✗ ⊘⊘ | elapsed`
- **Graceful shutdown** — SIGTERM finishes current URL, writes final report
- **Final report** — `DOWNLOAD_REPORT.json` + `failed_urls.txt` for manual review

## Output Structure

```
/Volumes/Samsung LED/Instagram Downloads/New Untouched Reels Download/
├── Color_grading/
│   ├── Da6GKgXsmcL.mp4
│   ├── Da6GKgXsmcL.info.json      # yt-dlp raw metadata
│   ├── Da6GKgXsmcL.meta.json      # Enhanced: collection, hashtags, owner, downloaded_at
│   └── Da6GKgXsmcL.jpg
├── Video_Effect/
├── Ideas_for_Shooting_Videos/
├── ...
└── logs/
    ├── master.log
    ├── Color_grading.log
    ├── DOWNLOAD_REPORT.json
    └── failed_urls.txt
```

## Related References

- `references/bugfix-retry-loop-variable.md` — Retry loop variable name fix
- `scripts/download_instagram_collections.py` — Overnight bulk downloader
- `scripts/extract_saved_collections.py` — JSON export parser
- `scripts/gen_collection_new_only.py` — NEW_ONLY generator
- `scripts/dedupe_against_kb.py` — Vault deduplication