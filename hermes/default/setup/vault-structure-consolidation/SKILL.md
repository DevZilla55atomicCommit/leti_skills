---
name: vault-structure-consolidation
type: skill
description: Consolidate, index, and link knowledge base vaults with master GPS navigation patterns
status: active
tags: [vault, consolidation, indexing, navigation, obsidian, master-map]
---

# Vault Structure Consolidation & Master GPS Navigation

This skill covers the end-to-end workflow for consolidating fragmented vault structures, creating master navigation maps (Memory.md), and establishing bidirectional index linking so every file is discoverable from a single entry point.

## When to Use

- Multiple duplicate folders exist (spaces vs underscores, root-level aliases)
- Index files don't link back to a central master map
- New content categories added without updating navigation
- Vault structure has grown organically without canonical paths
- Cross-references between categories are missing or stale

## Core Principles

1. **Single Source of Truth**: One `Memory.md` per domain acts as Master GPS
2. **Canonical Paths Only**: Underscore format for folders; remove root-level aliases
3. **Three-Layer Navigation**: Vault Root → Domain Master → Category Indexes
4. **Every Index Links Up**: Each `00-MASTER-INDEX.md` must reference the domain `Memory.md`
5. **Bidirectional Cross-Refs**: `CROSS_REFERENCE_INDEX.md` tracks technique↔technique links

## Consolidation Workflow

### Phase 1: Audit & Map
```bash
# 1. Find all duplicate folders
find . -maxdepth 2 -type d | sort | uniq -d

# 2. Find all index files
find . -name "*INDEX*.md" -o -name "*MASTER*INDEX*.md" -o -name "*master*index*.md"

# 3. Find orphaned folders (no index)
for d in */; do [[ ! -f "$d/00-MASTER-INDEX.md" && ! -f "$d/INDEX.md" ]] && echo "$d"; done
```

### Phase 2: Merge Duplicates (Spaces → Underscores)
```bash
# For each duplicate pair:
cp "Space Folder/"*.md "Underscore_Folder/"
cp -r "Space Folder/assets/" "Underscore_Folder/"
rm -rf "Space Folder/"
```

### Phase 3: Create Missing Indexes
For each category folder without `00-MASTER-INDEX.md`:
1. Count existing technique files
2. Create index with:
   - Navigation links to domain `Memory.md`
   - File table (NN, title, source, technique, focus)
   - Cross-reference table
   - Mastery verification checklist
   - Revision history

### Phase 4: Update Domain Master Map (`Memory.md`)
1. Quick Navigation table with all categories + paths + index links
2. Sub-category breakdown with canonical paths
3. Pipeline summaries (production/learning counts)
4. Known issues section (update as resolved)

### Phase 5: Update Cross-Reference Index
Add new index references table:
```markdown
| Index | Path | Description |
|-------|------|-------------|
| New Category | `Category/00-MASTER-INDEX.md` | X techniques... |
```

### Phase 6: Update Vault Root Index (`Hero_index.md`)
1. Update domain description in Quick Navigation table
2. Expand folder tree under domain section
3. Update Last Updated date

## Standard Index Template

Every `00-MASTER-INDEX.md` must include:
```markdown
# {{CATEGORY}} — Master Index

> **🔗 Master Vault Index:** `../../../../index.md`
> **🔗 DaVinci KB Master:** `../../Memory.md`
> **🔗 Cross-Reference Index:** `../../CROSS_REFERENCE_INDEX.md`

---

## 📊 Summary
| Pipeline | Techniques |
|----------|------------|
| Production | X |
| Learning | Y |

---

## 🎬 Techniques Table
| # | Title | Source | Type | Date |
|---|-------|--------|------|------|

---

## 🔗 Cross-References
| Topic | Related Category | Link |
|-------|------------------|------|

---

## 🏷️ Tags
`#davinci-resolve #{{CATEGORY_TAG}}`

---

*Part of the **DaVinci Knowledge Base** → **{{CATEGORY}}***
*Master GPS: `../../Memory.md`*
```

## Relative Path Standards

| File Location | Path to Domain Memory.md | Path to Vault Root |
|---------------|--------------------------|-------------------|
| `Color Grading & Looks/Category/` | `../../Memory.md` | `../../../../index.md` |
| `Videographer/SubCategory/` | `../../Memory.md` | `../../../../index.md` |
| `Lighting/` | `../Memory.md` | `../../../index.md` |
| Root category | `../Memory.md` | `../../index.md` |

## Pitfalls & Fixes

| Pitfall | Cause | Fix |
|---------|-------|-----|
| Root-level folders duplicate sub-folders | Organic growth | Remove aliases; use canonical paths under parent |
| Space-formatted folder names | Manual creation | Standardize on underscores; merge contents |
| Index files don't link to master | Missing step in workflow | Add mandatory link block to index template |
| Broken relative links | Wrong depth calculation | Use standard depth table above; test in Obsidian |
| CROSS_REFERENCE_INDEX.md stale | Not updated with new indexes | Add step 5 to workflow: update cross-ref table |
| Reel subfolders with frames/GIFs not copied | `cp` doesn't recurse by default | Use `find -maxdepth 1 -type d ! -name assets -exec cp -rn {} DEST \;` |
| Learning/Production pipeline counts mismatch | Index not regenerated after merge | Always regenerate 00-UNIFIED-MASTER-INDEX.md after consolidation |
| Cross-reference table not dated | No timestamp on new entries | Add "Last Structure Sync" date to cross-ref index header |
| Duplicate reel folders across disciplines | Pipeline assigns discipline but same reel appears in multiple folders | Audit for reel_code duplicates across `Post_Production/`, `Fusion/`, `Video_Effects/` — canonical goes in discipline-matching folder, remove from Archive |
| Root-level Archive folders missing Master Index | `Post_Production/` (Archive) has no 00-MASTER-INDEX.md | Create index with `../../Memory.md` link + archive status note even if empty |
| Empty discipline folders in Videographer/ | Created as placeholders but never populated | Decide: (a) populate, (b) remove, or (c) add placeholder index with "awaiting content" note — never leave bare |
| Cross-reference index missing new category indexes | Workflow step 5 skipped | Add verification: grep new index path in CROSS_REFERENCE_INDEX.md before declaring done |
| Relative link depth miscalculated for nested Videographer/ | Depth varies: `../../Memory.md` vs `../../../Memory.md` | Standard: `../../Memory.md` for `Videographer/*/`, `../Memory.md` for root categories, test in Obsidian |
| **Memory.md and index.md merged into MASTER_MAPPING.md** | Consolidation replaces dual navigation | Update all indexes: replace `Memory.md` → `MASTER_MAPPING.md`, `../index.md` → `MASTER_MAPPING.md`; delete old files after merge |
| **140+ index files across vault not updated** | Consolidation creates new structure but old indexes reference deleted files | After merge: scan all `*INDEX*.md`, `*MASTER*.md`, `*MAPPING*`, `*CROSS_REFERENCE*`; update each with new paths, counts, dates, and MASTER_MAPPING.md reference |
| **Support folder indexes missing** | 6 new folders (analysis, media, skills, collections, tags, transcripts) created without indexes | After merge: create index.md in each with full mapping tables; link from MASTER_MAPPING.md |
| **Per-video mapping files not indexed** | 1,156 analysis.json, 206 Vision_Reports, 1,449 skills, 1,121 transcripts, 206 vision reports | Each is a mapping; support folder indexes must catalog them all with video_id, size, date |
| **Per-reel INDEX.md files in Lighting (93) and Videographer (16)** | Deep nested indexes not captured by domain-level audit | Include in audit: `find . -name "*INDEX*.md" -o -name "*MASTER*INDEX*.md"`; update each to reference MASTER_MAPPING.md |
| **Videographer subfolder indexes (16) not updated** | Subfolder structure changes not propagated | Regenerate 00-UNIFIED-MASTER-INDEX.md and all subfolder 00-MASTER-INDEX.md after consolidation |
| **Support folder indexes not linked from MASTER_MAPPING.md** | Created but not integrated | Add support folder table to MASTER_MAPPING.md with paths, entry counts, descriptions |
| **Lighting folder has 93 video-specific INDEX.md files** | Each reel gets its own index; not captured in domain count | These are per-reel mappings; update each to reference MASTER_MAPPING.md; catalog in Lighting/00-MASTER-INDEX.md |
| **Duplicate index files with different naming** | `00-MASTER-INDEX.md`, `00-INDEX_*.md`, `INDEX.md`, `MASTER_INDEX.md`, `00-*-INDEX.md` | Standardize naming; prefer `00-MASTER-INDEX.md` for domain folders, `INDEX.md` for per-item |
| **CROSS_REFERENCE_INDEX.md missing support folder references** | Only tracks technique↔technique, not folder-level mappings | Add support folder mapping table to CROSS_REFERENCE_INDEX.md |

## Verification Checklist

After consolidation:
- [ ] Hero_index.md domain description & tree updated
- [ ] Memory.md Quick Navigation has canonical paths only
- [ ] Every category folder has `00-MASTER-INDEX.md`
- [ ] All indexes link to `Memory.md` as Master GPS
- [ ] CROSS_REFERENCE_INDEX.md has new index references table
- [ ] No space-formatted duplicate folders remain
- [ ] All relative links resolve in Obsidian
- [ ] Production/Learning counts match in Videographer unified index

## Support Files

- `templates/00-MASTER-INDEX-template.md` — Fill-in template for new category indexes
- `templates/00-MASTER-INDEX-archive-template.md` — Template for archive folders with canonical location mapping
- `references/vault-structure-consolidation.md` — This document
- `references/Post_Production_Archive_Index.md` — Example archive index for Post_Production/
- `scripts/merge-duplicate-folders.sh` — Automated duplicate merge script (planned)
- `scripts/verify-vault-links.py` — Automated link verification (planned)

## Related Skills

- `vault-optimize` — Quick-path daily operations
- `vault-setup` — Initial EMAI Starter Vault setup
- `instagram-davinci-learning-workflow` — Content pipeline that feeds this vault