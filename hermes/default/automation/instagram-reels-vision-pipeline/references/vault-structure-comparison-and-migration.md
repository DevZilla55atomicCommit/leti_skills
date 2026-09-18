# Vault Structure Comparison & Migration Plan (2026-07-31)

**Context:** During vision pipeline processing, discovered the current pipeline vault is INCOMPLETE compared to the existing `DaVinci_Knowledge_Base`.

---

## Comparison: DaVinci_Knowledge_Base vs Current Pipeline Vault

### DaVinci_Knowledge_Base (Existing, Rich Structure)
```
/TamaZila Obsidian Vault/Hermes Agent/DaVinci_Knowledge_Base/
├── Vision_Reports/           # 200+ JSON files — frame-by-frame analysis
│   └── C0Ck90GNfrb.json      # reel_id, collection, frames_analyzed, frame_details[], summary
├── Instagram_Reels/          # 200+ MD files — curated notes per reel
│   └── C2LuR9hxHyo.md        # frontmatter + summary + Quick Grade Recipe + Media + Skill ref + Pipeline Status
├── Domain folders/           # Organized by craft
│   ├── Color Grading & Looks/
│   ├── Camera Theory/
│   ├── Lighting/
│   ├── Fusion/
│   ├── Node Structures & Templates/
│   └── ...
├── skills_export.json        # All skills exported
├── knowledge_base_export.json # All notes exported
└── CROSS_REFERENCE_INDEX.md  # Navigation
```

**Each Instagram Reel note includes:**
- Frontmatter (reel_id, collection, URL, tags, analyzed_at)
- Summary + Key Techniques + Color Grade + Camera & Movement + Lighting + Composition
- **Quick Grade Recipe** (node graph with specific values)
- **Media references** (GIF + keyframes with `![[0001.jpg]]` embeds)
- **Hermes Skill reference** (path to `~/.hermes/skills/creative/davinci-reel-XXXXX/`)
- **Files Generated table** (vision_report, frames, gif, mp4, skill, quick_ref)
- **Pipeline Status checkboxes** (Download, Extract, Vision, Skill, Vault, Cleanup)

---

### Current Pipeline Vault (Samsung LED, Flat & Incomplete)
```
/Volumes/Samsung LED/.../CONTENT_PROCESSING/vault/
├── techniques/               # 985 MD files — flat list
│   └── 3d-camera-tracking-and-asset-integration.md  # Basic frontmatter + steps only
├── media/                    # 81 MB GIFs (referenced in notes)
├── collections/              # Empty stubs
├── tags/                     # Empty stubs
└── index.md                  # Basic index
```

**Each technique note only has:**
- Frontmatter (title, video_id, collection, resolve_page, node_graph, difficulty, tags, source_reel, created)
- Basic description + Node list + Parameters + Steps
- **NO:** Vision report, frame details, grade recipe, skill reference, pipeline status, keyframes

---

## What's Missing from Current Pipeline

| Feature | DaVinci_Knowledge_Base | Current Pipeline |
|---------|------------------------|------------------|
| Frame-by-frame vision JSON | ✅ Vision_Reports/ | ❌ |
| Quick Grade Recipe (node values) | ✅ | ❌ |
| Embedded keyframes in notes | ✅ `![[0001.jpg]]` | ❌ |
| Hermes Skill cross-reference | ✅ | ❌ |
| Pipeline status tracking | ✅ Checkboxes | ❌ |
| Domain organization | ✅ Folders | ❌ Flat |
| Exports (JSON/CSV) | ✅ | ❌ |
| Transcripts folder | ✅ | ❌ Scattered |

---

## The Mess
You have **two incomplete vaults**:
1. **DaVinci_Knowledge_Base** — rich, structured, but only ~200 reels (old pipeline)
2. **Current vault** — flat, missing metadata, 985 notes but shallow

**Neither has:** frames, transcripts, analysis JSON, skills integrated.

---

## Redundant Data on Samsung LED (Storage Crisis)

| Path | Size | Keep? |
|------|------|-------|
| `Instagram Downloads/{collection}/` | ~50 GB | ✅ Original MP4s |
| `CONTENT_PROCESSING/frames/` | 7.9 GB | ⚠️ Regeneratable |
| `CONTENT_PROCESSING/transcripts/` | 1.5 GB | ⚠️ Regeneratable |
| `CONTENT_PROCESSING/analysis/` | 579 MB | ⚠️ Regeneratable |
| `CONTENT_PROCESSING/vault/` | **427 MB** | ✅ **MIGRATE** (346 MB notes + 81 MB embedded GIFs) |
| `CONTENT_PROCESSING/gifs/` | **45 GB** | ❌ **DELETE** (redundant, not linked to vault) |
| `VISION_PROGRESS.json` | 2.6 MB | ✅ **MIGRATE** |

**Critical Finding:** The 45 GB `gifs/` folder is SEPARATE from vault's 81 MB embedded GIFs. Vault notes reference `media/*.gif` (81 MB), NOT `gifs/*`.

---

## Migration Plan (No Regeneration)

### What to Move to Internal (Keep Forever)
| Data | Size | Location |
|------|------|----------|
| **Vault notes + embedded GIFs** | **~427 MB** (346 MB + 81 MB) | `CONTENT_PROCESSING/vault/` |
| **Skills (1,449+)** | ~50 MB | `~/.hermes/skills/davinci-resolve-techniques/` |
| **VISION_PROGRESS.json** | 2.6 MB | `CONTENT_PROCESSING/VISION_PROGRESS.json` |

### What to Delete (Not Needed)
| Data | Size | Why |
|------|------|-----|
| `CONTENT_PROCESSING/gifs/` | **45 GB** | Not linked to vault, redundant |
| `CONTENT_PROCESSING/frames/` | 7.9 GB | Regeneratable from MP4s |
| `CONTENT_PROCESSING/transcripts/` | 1.5 GB | Regeneratable |
| `CONTENT_PROCESSING/analysis/` | 579 MB | Regeneratable from VISION_PROGRESS.json |

### Migration Commands (No Regeneration)
```bash
# 1. Copy vault to internal
cp -r "/Volumes/Samsung LED/Instagram Downloads/New Untouched Reels Download/CONTENT_PROCESSING/vault" ~/DaVinci_Vault

# 2. Copy progress tracking
cp "/Volumes/Samsung LED/Instagram Downloads/New Untouched Reels Download/CONTENT_PROCESSING/VISION_PROGRESS.json" ~/DaVinci_Vault/

# 3. Delete redundant gifs (45 GB)
rm -rf "/Volumes/Samsung LED/Instagram Downloads/New Untouched Reels Download/CONTENT_PROCESSING/gifs"

# 4. Optionally clean completed frames (keep only error/pending)
# Find completed video_ids from VISION_PROGRESS.json, remove their frame dirs

# 5. Verify internal skills already safe
ls ~/.hermes/skills/davinci-resolve-techniques/ | wc -l  # Should be 1449+
```

**Result:** Free ~54 GB on Samsung LED, keep all curated outputs on internal.

---

## Recommended Future Pipeline Updates (v2 Phase 3)

The pipeline should produce **DaVinci_Knowledge_Base-style notes** with:
1. Vision_Reports JSON per reel
2. Quick Grade Recipe with node values
3. Embedded keyframes (`![[frames/{CODE}/frame_XX.png]]`)
4. Hermes Skill cross-reference
5. Pipeline Status checkboxes
6. Domain folder organization
7. Exports (JSON/CSV)
8. Transcripts integration