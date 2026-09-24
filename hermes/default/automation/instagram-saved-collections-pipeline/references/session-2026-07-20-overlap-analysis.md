# Instagram Saved Collections Overlap Analysis — 2026-07-20

## Executive Summary
Parsed Instagram data export `saved_collections.json` (14.9 MB, 3,959 items across 128 collections) and cross-referenced against existing Obsidian vault (`DaVinci_Knowledge_Base`) to identify already-processed URLs.

**Result**: 408 URLs already in KB, **3,504 new URLs** to download across 116 collections.

## Methodology

### 1. Export Parsing
```python
# Structure: List[Collection]
# Collection: {timestamp, media: [], label_values: [
#   {label: "Name", value: "Color grading"},
#   {label: "Update time", timestamp_value: 1780932003},
#   {title: "Media", dict: [  # <-- actual media container
#     {dict: [  # per reel
#       {label: "URL", value: "https://instagram.com/reel/CODE/"},
#       {label: "Caption", value: "..."},
#       {label: "Title", value: ""},
#       {title: "Hashtags", dict: [{dict: [{label: "Name", value: "davinciresolve"}]}]},
#       {title: "Owner", dict: [{dict: [{label: "Name", value: "Justin"}, {label: "Username", value: "justinaparicio"}]}]},
#       {title: "Brand partner", dict: [{dict: [{label: "Name", value: "Creatortools"}]}]}
#     ]}
#   ]}
# ]}
```

### 2. KB URL Extraction
```bash
grep -r "instagram.com/reel" DaVinci_Knowledge_Base/ | \
  grep -oE 'https://www\.instagram\.com/reel/[A-Za-z0-9_-]+' | \
  sort -u > kb_instagram_urls.txt
```
**Found**: 425 unique Instagram URLs in vault

### 3. Overlap Calculation
```python
kb_urls = set(kb_urls)
saved_urls = set(saved_urls)
overlap = kb_urls & saved_urls        # 408 URLs
new_only = saved_urls - kb_urls       # 3,504 URLs
kb_only = kb_urls - saved_urls        # 17 URLs (from other sources)
```

## Results by Collection

| Collection | Total | Already Done | New | Status |
|------------|-------|--------------|-----|--------|
| Videographer | 275 | 213 | 62 | ✅ 77% done |
| Color grading | 362 | 176 | 186 | 🔶 49% done |
| Video Effect | 394 | 28 | 366 | 🔴 7% done |
| Ideas for Shooting Videos | 410 | 12 | 398 | 🔴 3% done |
| Photography/Videography | 395 | 0 | 395 | 🆕 All new |
| Gimbal Moves | 238 | 1 | 237 | 🆕 All new |
| DaVinci Tricks | 115 | 2 | 113 | 🔴 2% done |
| Lightroom | 192 | 1 | 191 | 🆕 All new |
| Fitness | 201 | 0 | 201 | 🆕 All new |
| Cinematic | 80 | 2 | 78 | 🆕 97% new |
| **... + 106 more** | | | | |

**Total**: 3,959 | 408 done | 3,504 new

## Output Files Generated

| File | Purpose |
|------|---------|
| `instagram_saved_clean.json` | Full structured data (3,959 items) |
| `instagram_saved_clean.csv` | Spreadsheet import |
| `instagram_saved_by_collection/` | 128 per-collection JSON files |
| `instagram_saved_urls_by_collection.md` | Human-readable URL list |
| `instagram_all_urls_flat.txt` | All 3,959 URLs (one per line) |
| `instagram_urls_OVERLAP.txt` | 408 already-processed URLs |
| `instagram_urls_NEW_ONLY.txt` | 3,504 fresh URLs |
| `instagram_urls_KB_ONLY.txt` | 17 KB-only URLs |
| `instagram_new_urls_by_collection/` | 116 `*_NEW.txt` files (pipeline inputs) |

## Key Observations

1. **Videographer** is 77% complete — only 62 remaining
2. **Color grading** is 49% complete — 186 fresh tutorials
3. **Video Effect** (394) and **Ideas for Shooting** (410) are largely untouched
4. **Photography/Videography** (395) and **Gimbal Moves** (237) are entirely fresh
5. **Fitness** (201) and **Pickleball** (57) are personal interest, not DaVinci-related
5. 17 URLs in KB not in this export — likely from manual saves or older exports

## Next Steps

1. Run `download_instagram_collections.py` with 3,504 URLs
2. Prioritize: DaVinci Tricks (113), Color Grading (186), Video Effect (366)
3. Skip Fitness/Pickleball if storage constrained
4. After download: run frame extraction + vault note generation pipeline