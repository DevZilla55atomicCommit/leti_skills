---
name: instagram-saved-collections-pipeline
description: Class-level skill for processing Instagram Saved Collections exports — parsing, deduplication against existing knowledge bases, per-collection URL extraction, and pipeline preparation for batch download/analysis.
category: automation
tags: [instagram, saved-collections, data-export, deduplication, pipeline, yt-dlp, obsidian, davinci-resolve]
version: 1.0.0
---

# Instagram Saved Collections Pipeline

Process Instagram's "Your Activity → Saved → Collections" JSON export into actionable pipeline inputs.

## What This Skill Covers

- **Parse** the nested `saved_collections.json` structure (128 collections, 3,959 items)
- **Extract** clean per-collection URL lists (reel + post URLs)
- **Deduplicate** against existing knowledge bases (Obsidian vault, DaVinci Knowledge Base, Hermes skills)
- **Generate** pipeline-ready artifacts: per-collection `.txt` URL files, master flat list, overlap reports
- **Classify** collections by creative discipline for routing to appropriate vaults

## Input Format

Instagram data export: `saved_collections.json`

Structure:
```json
[
  {
    "timestamp": 1775842668,
    "media": [],
    "label_values": [
      {"label": "Name", "value": "Color grading"},
      {"label": "Type", "value": "Default"},
      {"label": "Privacy", "value": "Private"},
      {"label": "Update time", "timestamp_value": 1780932003},
      {"title": "Media", "dict": [
        {"dict": [
          {"label": "URL", "value": "https://www.instagram.com/reel/CODE/", "href": "..."},
          {"label": "Caption", "value": "..."},
          {"label": "Title", "value": ""},
          {"title": "Hashtags", "dict": [{"dict": [{"label": "Name", "value": "davinciresolve"}]}]},
          {"title": "Owner", "dict": [{"dict": [{"label": "Name", "value": "Creator"}, {"label": "Username", "value": "handle"}]}]},
          {"title": "Brand partner", "dict": []}
        ]}
      ]}
    ]
  }
]
```

## Pipeline Stages

### Stage 1: Parse & Extract
```bash
python3 parse_saved_collections.py \
  --input saved_collections.json \
  --output-dir ./instagram_saved_output/
```
Outputs:
- `instagram_saved_clean.json` — full structured data
- `instagram_saved_clean.csv` — spreadsheet-ready
- `instagram_saved_urls_by_collection.md` — human-readable per-collection URLs
- `instagram_all_urls_flat.txt` — one URL per line (3,959 total)
- `instagram_saved_by_collection/` — 117 individual JSON files

### Stage 2: Deduplicate Against Knowledge Bases
```bash
python3 deduplicate_against_kb.py \
  --urls instagram_all_urls_flat.txt \
  --kb-root "/path/to/DaVinci_Knowledge_Base" \
  --output-dir ./dedup_output/
```
Outputs:
- `instagram_urls_OVERLAP.txt` — already processed (462 URLs)
- `instagram_urls_NEW_ONLY.txt` — fresh to process (3,497 URLs)
- `instagram_urls_KB_ONLY.txt` — in KB but not in this export (17 URLs)
- Per-collection breakdown: `OVERLAP_BY_COLLECTION.json`

### Stage 3: Generate Per-Collection Pipeline Inputs
```bash
python3 generate_collection_inputs.py \
  --new-urls instagram_urls_NEW_ONLY.txt \
  --collection-json instagram_saved_by_collection/ \
  --output-dir ./pipeline_inputs/
```
Outputs: `pipeline_inputs/<Collection_Name>_NEW.txt` (117 files, one per collection)

### Stage 4: Batch Download & Process (Updated 2026-07-20)

```bash
# Test single collection
yt-dlp -a pipeline_inputs/Color_grading_NEW.txt -o "downloads/Color_grading/%(title)s.%(ext)s"

# Or use the bulletproof overnight downloader (NEW — handles retries, resume, logging)
python3 download_instagram_collections.py \
  --urls-dir pipeline_inputs/ \
  --cookies cookies_www.instagram.com_2026-07-19.txt \
  --output instagram_downloads \
  --logs instagram_downloads/logs \
  --max-concurrent 2 --max-retries 5 --timeout 300

# Or use Hermes browser tools fallback (when yt-dlp blocked)
python3 process_with_browser_tools.py --collection Color_grading_NEW.txt
```

**New bulletproof downloader** (`download_instagram_collections.py`):
- Per-collection isolation (one failure doesn't stop others)
- Exponential backoff: 30s → 60s → 120s → 240s → 480s (5 retries)
- Resume-safe: `--continue` + `--no-overwrites` — safe to Ctrl+C and restart
- Structured logs: per-collection log + master log + heartbeat every 60s
- Metadata sidecars: `.meta.json` with collection, hashtags, owner, download timestamp
- Graceful shutdown: SIGTERM/SIGINT finishes current URLs, writes final report
- Final outputs: `DOWNLOAD_REPORT.json` (success rates, timing) + `failed_urls.txt` (manual review)
- Tested: 85/113 DaVinci_Tricks URLs in 3 min (1 failing = deleted post, correctly retried)

### Stage 5: Post-Download Index & Cross-Reference (Added 2026-07-20)

```bash
# Generate master index linking downloaded files to collections + KB overlap
python3 generate_master_index.py \
  --downloads instagram_downloads/ \
  --collections instagram_saved_by_collection/ \
  --output instagram_downloads/MASTER_INDEX.json

# Cross-reference with DaVinci KB for technique tagging
python3 tag_techniques_from_kb.py \
  --index instagram_downloads/MASTER_INDEX.json \
  --kb-root "/path/to/DaVinci_Knowledge_Base" \
  --output instagram_downloads/TECHNIQUE_TAGS.json
```

Outputs:
- `MASTER_INDEX.json` — per-file: collection, URL, local path, size, duration, KB overlap status, KB note path
- `TECHNIQUE_TAGS.json` — per-file: detected techniques (speed_ramp, masking, color_grade, etc.) from KB note content
- `PER_COLLECTION_SUMMARY.csv` — collection, total, downloaded, failed, overlap %, avg size

## 2026-07-20 Session Results

| Metric | Value |
|--------|-------|
| Total collections | 117 (128 in export, 11 empty) |
| Total items | 3,959 |
| Already in DaVinci KB | 462 (11.7%) |
| New to process | 3,497 (88.3%) |
| KB-only (not in export) | 17 |
| **Downloaded in overnight run** | **~1,030 (29%) in 2+ hours** |
| Failed URLs (total) | 2 (both AI collection — deleted/private posts) |
| Disk used | 52 GB / 120 GB (Samsung LED) |
| Process | PID 15880, 2+ hours running, stable |

### Top Collections by Volume
1. **Ideas for Shooting Videos** — 410 (12 done, 398 new)
2. **Photography/Videography** — 395 (0 done, 395 new)
3. **Video Effect** — 394 (28 done, 366 new)
4. **Color grading** — 362 (176 done, 186 new)
5. **Videographer** — 275 (213 done, 62 new)
6. **Gimbal Moves** — 238 (1 done, 237 new)
7. **Fitness** — 201 (0 done, 201 new)
8. **Lightroom** — 192 (1 done, 191 new)

### Collections with High Overlap (Already Largely Processed)
- **Videographer** — 77% done (213/275)
- **Color grading** — 49% done (176/362)
- **Video Effect** — 7% done (28/394) — large fresh batch

### Collections with Zero Overlap (Fresh Territory)
- Photography/Videography (395), Fitness (201), Lightroom (191), Ideas for Shooting Videos (398), Gimbal Moves (237), DaVinci Tricks (113), Poses (110), Drone (57), Text Effects (57), Pickleball (57)

### Big Collections Remaining
| Collection | URLs |
|------------|------|
| Ideas for Shooting Videos | 398 |
| Photography/Videography | 395 |
| Video Effect | 366 |
| Gimbal Moves | 237 |
| Lightroom | 191 |
| Fitness | 201 |
| DaVinci Tricks | 113 |
| Videographer | 62 |
| Poses | 110 |
| Drone | 57 |
| Pickleball | 57 |
| Text Effects | 57 |
| Cinematic | 78 |

## Full Pipeline Execution (Added 2026-07-20)

### Complete Pipeline Outputs Generated
```
PIPELINE_OUTPUT/
├── DaVinci_Knowledge_Base/
│   ├── csv/           # all_videos.csv, collections_summary.csv, by_technique.csv, by_creator.csv
│   ├── db/            # videos.db (composite PK: video_id + collection)
│   ├── obsidian/      # Index + 55 collection notes + technique notes
│   └── resolve/       # DaVinci Resolve bin structure (planned)
└── Other_Content/
    ├── csv/
    ├── db/
    ├── obsidian/
    └── resolve/
```

### DaVinci vs Other Content Separation
- **DaVinci-related collections**: 55 (Color_grading, DaVinci_Tricks, Cinematic, Video_Effect, Ideas_for_Shooting_Videos, Videographer, Gimbal_Moves, Drone, etc.)
- **Other collections**: 61 (Fitness, Life, Lens, Lightroom, Photography_Videography, Food_for_thoughts, etc.)
- **Separation logic**: Collection name matching against `DAVINCI_COLLECTIONS` set

### SQLite Schema (Composite Key Fix)
```sql
CREATE TABLE videos (
    video_id TEXT,
    collection TEXT,
    -- all metadata columns...
    PRIMARY KEY (video_id, collection)  -- Composite key allows same video in multiple collections
);
```

### Obsidian Notes Structure (Both Outputs)
```
DaVinci_Knowledge_Base/obsidian/
├── 📚 Instagram Reels Index.md          # Master index with collections table
├── Color_Grading_&_Looks.md             # Collection note with frame table + techniques
├── Technique: color-grading.md          # Technique-specific index
└── ... (55 collections)

Other_Content/obsidian/
├── 📚 Instagram Reels Index.md
├── Fitness.md
├── Life.md
└── ... (61 collections)
```

### Technique Tagging System (Auto-applied)
18 technique categories with keyword matching: color-grading, speed-ramp, masking, gimbal, drone, lighting, composition, camera-settings, skin-tones, luts, noise-reduction, transitions, editing, sound-design, motion-graphics, vfx, camera-theory

---

## 2026-07-20 Session Results

## Key Findings (2026-07-20 Session)

| Metric | Value |
|--------|-------|
| Total collections | 117 (128 in export, 11 empty) |
| Total items | 3,959 |
| Already in DaVinci KB | 462 (11.7%) |
| New to process | 3,497 (88.3%) |
| KB-only (not in export) | 17 |

### Top Collections by Volume
1. **Ideas for Shooting Videos** — 410 (12 done, 398 new)
2. **Photography/Videography** — 395 (0 done, 395 new)
3. **Video Effect** — 394 (28 done, 366 new)
4. **Color grading** — 362 (176 done, 186 new)
5. **Videographer** — 275 (213 done, 62 new)
6. **Gimbal Moves** — 238 (1 done, 237 new)
7. **Fitness** — 201 (0 done, 201 new)
8. **Lightroom** — 192 (1 done, 191 new)

### Collections with High Overlap (Already Largely Processed)
- **Videographer** — 77% done (213/275)
- **Color grading** — 49% done (176/362)
- **Video Effect** — 7% done (28/394) — large fresh batch

### Collections with Zero Overlap (Fresh Territory)
- Photography/Videography (395), Fitness (201), Lightroom (191), Ideas for Shooting Videos (398), Gimbal Moves (237), DaVinci Tricks (113), Poses (110), Drone (57), Text Effects (57), Pickleball (57)

## Usage Notes

- **Cookie handling**: Use local browser cookies (Netscape format) — never share cookies
- **Rate limits**: Instagram API ~40 RPM — use browser tools fallback for blocked reels
- **Frame extraction**: Use 99.9% instead of 100% for last frame; accept ≥7/8 frames
- **Metadata**: Capture caption, hashtags, owner, brand partner for vault notes
- **Classification**: Auto-classify by collection name + caption keywords

## References

- [references/parse_saved_collections.py](references/parse_saved_collections.py) — Main parser script (JSON export)
- [references/parse_saved_collections_html.py](references/parse_saved_collections_html.py) — Parser for Instagram's HTML export format (saved_collections.html)
- [references/deduplicate_against_kb.py](references/deduplicate_against_kb.py) — KB overlap checker
- [references/generate_collection_inputs.py](references/generate_collection_inputs.py) — Per-collection pipeline file generator
- [references/instagram_export_structure.md](references/instagram_export_structure.md) — Documented JSON schema
- [references/instagram_html_export_structure.md](references/instagram_html_export_structure.md) — Documented HTML export schema
- [references/generate_remaining_urls.py](references/generate_remaining_urls.py) — Cross-references HTML export against master index to produce remaining URLs markdown

## Related Skills

- `automation/instagram-reels-pipeline` — Downstream download/frame extraction/vault creation
- `creative/davinci_color_grading` — Color science analysis for downloaded reels
- `creative/davinci_workflows` — DaVinci Resolve MCP integration