---
name: instagram-saved-collections-parser
description: Parse Instagram data export saved_collections.json into structured data (CSV, JSON, per-collection files) with hashtag/creator analytics
category: automation
tags: [instagram, data-export, saved-collections, json-parsing, analytics, csv-export]
version: 1.0.0
author: Maddie (Hermes Pipeline)
created: 2026-07-20
---

# Instagram Saved Collections Parser

Parses Instagram's `your_instagram_activity/saved/saved_collections.json` export into clean, structured formats for analysis and vault integration.

## Problem Solved

Instagram's data export saves saved posts/reels in a deeply nested JSON structure that's unusable directly. This parser extracts:
- 3,959+ media items across 128 collections
- URLs, captions, hashtags, creators, brand partners
- Per-collection and global analytics (top hashtags, top creators)
- Clean CSV/JSON exports for downstream use

## Quick Start

```bash
# Parse a saved_collections.json export
python3 parse_saved_collections.py \
  --input /path/to/saved_collections.json \
  --output-dir /path/to/output
```

## Output Files

| File | Description |
|------|-------------|
| `instagram_saved_clean.json` | Full structured data + global analytics |
| `instagram_saved_clean.csv` | Spreadsheet-ready (Collection, URL, Caption, Hashtags, Owner, Username, Brand) |
| `by_collection/{Collection_Name}.json` | Per-collection JSON files |
| `analytics_summary.md` | Human-readable markdown report |

## JSON Structure (Input)

```json
[
  {
    "timestamp": 1775842668,
    "media": [],
    "label_values": [
      {"label": "Name", "value": "Project Ideas"},
      {"label": "Type", "value": "Default"},
      {"label": "Privacy", "value": "Private"},
      {"label": "Update time", "timestamp_value": 1780932003},
      {
        "dict": [
          {
            "dict": [
              {"label": "URL", "value": "https://...", "href": "https://..."},
              {"label": "Caption", "value": "..."},
              {"label": "Title", "value": ""},
              {"dict": [...], "title": "Hashtags"},
              {"dict": [...], "title": "Owner"},
              {"dict": [...], "title": "Brand partner"}
            ],
            "title": ""
          }
        ],
        "title": "Media"
      }
    ],
    "fbid": "..."
  }
]
```

## Parsed Output Structure (Per Item)

```json
{
  "collection": "Color grading",
  "url": "https://www.instagram.com/reel/Da6GKgXsmcL/",
  "href": "https://www.instagram.com/reel/Da6GKgXsmcL/",
  "caption": "If you want my top 24 Cinematic Presets FOR FREE...",
  "hashtags": ["magimir", "curvestutorial", "colorgrading", "photoeditor"],
  "owner": "Some Creator Name",
  "owner_username": "creator_handle",
  "brand_partner": "Brand Name"
}
```

## Analytics Generated

- **Top 100 hashtags** with counts (e.g., `#davinciresolve: 559`, `#videography: 383`)
- **Top 100 creators** with save counts
- **Items per collection** distribution
- **Date ranges** (collection creation, last update)

## Use Cases

1. **Vault ingestion** — Import per-collection JSON into Obsidian as structured notes
2. **Content audit** — Find your most-saved creators, hashtags, topics
3. **Pipeline feed** — Extract reel URLs for `instagram-reels-pipeline` download
4. **Research** — Analyze saved content patterns across disciplines

## Requirements

- Python 3.8+
- Standard library only (json, csv, collections, datetime, os, argparse)

## Script Location

`scripts/parse_saved_collections.py`

## Example Output

```
Total media items: 3,959
Total collections: 128
Top collection: "Ideas for Shooting Videos" (410 items)
Top hashtag: #davinciresolve (559)
Top creator: RESOLVED (109 saves)
Date range: 2023-08-09 to 2026-07-12
```

## Integration with Other Skills

| Skill | Integration |
|-------|-------------|
| `instagram-reels-pipeline` | Feed extracted reel URLs to download pipeline |
| `vault-setup` | Import per-collection JSON as Obsidian notes |
| `davinci_color_grading` | Filter Color Grading collection for technique replication |

## Changelog

### 1.0.0 (2026-07-20)
- Initial release
- Handles Instagram's nested `label_values → dict → dict → dict` structure
- Correctly extracts hashtags from `value` field (not `label`)
- Exports JSON, CSV, per-collection JSON, and markdown summary
- Zero dependencies

### 2026-07-20 Session Integration
- **Parsed 14.9 MB export**: 3,959 items across 128 collections
- **Top hashtags**: #davinciresolve (559), #videography (383), #colorgrading (365)
- **Top creators**: RESOLVED (109), Julian Woldan (101), Pedro Mello (82)
- **Export structure parsed**: Deeply nested `label_values → dict → dict → dict` correctly handled
- **Integration**: Output feeds directly into `instagram-reels-pipeline` and `instagram-saved-collections-pipeline`
- **Per-collection NEW_ONLY files generated**: 116 files for batch processing
- **DaVinci KB deduplication**: 425 overlap, 3,504 new URLs identified