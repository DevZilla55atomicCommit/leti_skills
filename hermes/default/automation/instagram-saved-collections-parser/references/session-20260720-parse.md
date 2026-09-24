# Session Reference: 2026-07-20 Instagram Saved Collections Parse

## Source File
```
/Users/alfredkamisese/Downloads/instagram-tamazila-2026-07-20-0Ni7mnhM/your_instagram_activity/saved/saved_collections.json
```
- Size: 14.9 MB
- Lines: 444,990
- Top-level collections: 128

## Parsed Results (2026-07-20 Run)

| Metric | Value |
|--------|-------|
| Total media items | 3,959 |
| Total collections | 128 |
| Date range (created) | 2023-08-09 to 2026-07-12 |
| Date range (updated) | 2023-08-10 to 2026-07-20 |

### Top 10 Collections by Item Count
1. **Ideas for Shooting Videos** — 410
2. **Photography/Videography** — 395
3. **Video Effect** — 394
4. **Color grading** — 362
5. **Videographer** — 275
6. **Gimbal Moves** — 238
7. **Fitness** — 201
8. **Lightroom** — 192
9. **Life** — 141
10. **Photograpy** — 133

### Top 10 Hashtags
1. **#davinciresolve** — 559
2. **#videography** — 383
3. **#colorgrading** — 365
4. **#videoediting** — 351
5. **#filmmaking** — 338
6. **#photography** — 326
7. **#tutorial** — 314
8. **#cinematic** — 305
9. **#cinematography** — 284
10. **#editing** — 223

### Top 10 Creators (by saves)
1. **RESOLVED** — 109
2. **Julian Woldan \| FILMMAKER** — 101
3. **Pedro Mello \| Fotógrafo • Videomaker** — 82
4. **Osk 🦦 Photography + Color Grading Tips** — 44
5. **Jihad Konda** — 42
6. **Justin Aparicio** — 29
7. **Justin** — 29
8. **Minh Tran** — 25
9. **Justin Hurley** — 23
10. **GAKU** — 22

## Key Parsing Notes

### Structure Discovered
The JSON uses a deeply nested pattern:
```
collection.label_values[].dict[].dict[].dict[]
```
Specifically:
- `label_values[4]` has `title: "Media"` and contains the array of media items
- Each media item has a `dict` array of 6 elements in fixed order:
  1. URL (label="URL", value=..., href=...)
  2. Caption (label="Caption", value=...)
  3. Title (label="Title", value="")
  4. Hashtags (title="Hashtags", dict[] → dict[] → label="Name", value="hashtag")
  5. Owner (title="Owner", dict[] → dict[] → label="Name"/"Username", value=...)
  6. Brand partner (title="Brand partner", dict[] → dict[] → label="Name", value=...)

### Critical Fix: Hashtag Extraction
**Bug found**: Hashtag value is in the `value` field, NOT the `label` field.
- Inner structure: `{"label": "Name", "value": "actual_hashtag"}`
- Initial parser incorrectly used `h_item.get('label')` which returned "Name" for all
- Fixed by using `h_item.get('value')`

### Collections with Zero Items
Some collections have empty `dict` arrays or missing Media container:
- `Handheld`, `Shooting in Log`, `Xmas Activity Games & more`, `Health` (first one)
- These return 0 items — parser handles gracefully

### Encoding Issues
- Some creator names have UTF-8 encoding artifacts (e.g., `FotÃ³grafo`, `â¥²`)
- Source JSON has these pre-encoded — not a parser issue
- CSV/JSON outputs preserve original encoding

## Output Files Generated
```
/Users/alfredkamisese/Downloads/instagram_saved_clean.json      # Full data + analytics
/Users/alfredkamisese/Downloads/instagram_saved_clean.csv       # Spreadsheet format
/Users/alfredkamisese/Downloads/instagram_saved_by_collection/  # 128 per-collection JSONs
```

## Integration Ideas

### 1. Feed to instagram-reels-pipeline
Extract reel URLs from specific collections:
```bash
# Get all reel URLs from "Color grading" collection
jq -r '.items[] | select(.url | contains("reel")) | .url' \
  instagram_saved_by_collection/Color_grading.json
```

### 2. Vault Ingestion (Obsidian)
Each collection JSON → Obsidian note with:
- Frontmatter: collection, count, date_range
- Table of items with URL, caption preview, hashtags, creator
- Tags from top hashtags

### 3. Discipline Mapping
Map collections to DaVinci Knowledge Base categories:
| Collection | Discipline |
|------------|------------|
| Color grading, DaVinci Tricks, Speed Ramp | Post-Production / Color Grading |
| Gimbal Moves, Car Shooting tips, Drone | Camera Movement |
| Lightroom, Photoshop, Skin Retouch | Photography / Photo Editing |
| Video Effect, Cinematic, Text Effects | Video Effects / VFX |
| Lighting, Wedding Videography | Lighting / Cinematography |

## Command Used
```bash
python3 parse_saved_collections.py \
  --input "/Users/alfredkamisese/Downloads/instagram-tamazila-2026-07-20-0Ni7mnhM/your_instagram_activity/saved/saved_collections.json" \
  --output-dir "/Users/alfredkamisese/Downloads/instagram_saved_output"
```

## Performance
- Parse time: ~2 seconds
- Memory: ~50 MB peak
- Output: ~8 MB JSON, ~6 MB CSV, 128 collection files