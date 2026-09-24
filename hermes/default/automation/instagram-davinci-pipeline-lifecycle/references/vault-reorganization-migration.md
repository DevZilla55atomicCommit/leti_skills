# Vault Reorganization & Migration (2026-07-31)

## Summary
Migrated Instagram → DaVinci pipeline outputs from Samsung LED to TamaZila Obsidian Vault, reorganized flat techniques into domain folders, created domain indexes, regenerated all mapping files, and cleaned storage.

## Before: Flat Structure
```
CONTENT_PROCESSING/
├── vault/
│   ├── techniques/ (1,023 flat .md files)
│   ├── media/ (2,096 GIFs)
│   ├── collections/ (40 stubs)
│   ├── tags/ (500 stubs)
│   └── index.md
├── analysis/ (1,165 dirs with analysis.json)
├── transcripts/ (1,165 files)
├── frames/ (7.9 GB)
├── gifs/ (45 GB - redundant)
└── VISION_PROGRESS.json
```

## After: Domain-Organized Vault
```
DaVinci_Knowledge_Base/
├── Color Grading & Looks/ (854 techniques) + index.md
├── Camera Theory/ (5) + index.md
├── Lighting/ (2) + index.md
├── Fusion/ (75) + index.md
├── Photography_Videography/ (1) + index.md
├── Post_Production/ (98) + index.md
├── Video_Effects/ (7) + index.md
├── media/ (2,096 GIFs)
├── skills/ (1,449 Hermes skills)
├── tags/ (907 tag files)
├── collections/ (58 collection files)
├── analysis/ (1,165 dirs)
├── transcripts/ (6,699 files)
├── techniques/ (empty - all moved)
├── VISION_PROGRESS.json
├── knowledge_base_export.json
├── knowledge_base_export.csv
├── skills_export.json
├── skills_export.csv
└── index.md (master index)
```

## Migration Scripts
1. `reorganize_vault.py` — Moves techniques to domain folders based on `resolve_page` + `collection`, updates frontmatter with `domain`, `moved_at`, `skill`, `analysis` links
2. `create_domain_indexes.py` — Generates `index.md` in each domain with technique table (title, video_id, collection, page, tags, skill, analysis, difficulty)
3. `regenerate_mappings.py` — Regenerates all export files (JSON + CSV)

## Frontmatter Updates
Each technique note now includes:
```yaml
domain: "Color Grading & Looks"
moved_at: "2026-07-31"
skill: "technique-name.md"
analysis: "analysis/video_id/analysis.json"
```

## Domain Mapping Logic
| resolve_page | collection | → Domain |
|--------------|------------|----------|
| Color | Color_grading, DaVinci_Tricks, etc. | Color Grading & Looks |
| Camera | Camera, Cinematic, etc. | Camera Theory |
| Lighting | Lighting, Ideas_for_Shooting_Videos | Lighting |
| Fusion | Fusion, DR_Making_CG, DaVinci_Tricks | Fusion |
| Videography | Videography, etc. | Photography_Videography |
| Post | Post_Production, Export_Videos | Post_Production |
| Video | Video_Effects, DaVinci_Tricks | Video_Effects |

## Domain Index.md Format
Each domain folder gets `index.md`:
```markdown
---
title: "Color Grading & Looks Index"
folder: "Color Grading & Looks"
generated: "2026-07-31T14:33:59"
total_techniques: 854
---

# Color Grading & Looks — Technique Index

| Technique | Video ID | Collection | Page | Tags | Skill | Analysis | Difficulty |
|-----------|----------|------------|------|------|-------|----------|------------|
| [[Technique Name]] | VID123 | Collection | Page | tags | [[skill]] | [[analysis]] | intermediate |
```

## Mapping Files Regenerated
- `knowledge_base_export.json` (5,368 files)
- `knowledge_base_export.csv` (5,369 lines)
- `skills_export.json` (1,449 skills)
- `skills_export.csv` (1,450 lines)
- Domain `index.md` files (7 folders)

## Storage Cleanup After Migration
| Deleted | Size |
|---------|------|
| `CONTENT_PROCESSING/gifs/` | 45 GB |
| `CONTENT_PROCESSING/frames/` (1,030 complete) | 7.4 GB |
| `~/Downloads/instagram_downloads/` | 407 MB |

## Result
- **Techniques organized**: 963 techniques in 7 domain folders (1,025 total, some without domain match)
- **Domain indexes**: 7 `index.md` files with wiki-linked technique tables
- **All mapping files**: Regenerated and current
- **Samsung LED**: 5.4 GB → 61 GB free
- **Internal**: 2.5 GB → 12 GB free