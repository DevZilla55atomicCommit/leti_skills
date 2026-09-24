# Vault Mapping Update Protocol

**Created:** 2026-08-14
**Source Session:** YouTube → DaVinci Knowledge Base (Video iusBsXNKGPE — Jamie Fenn Relight tutorial)
**Related Skill:** `video-tutorial-extraction`

---

## Purpose

Documents the complete vault mapping update protocol when adding a new technique note from any source (YouTube, Instagram, direct tutorial). This ensures the DaVinci Knowledge Base remains consistent and navigable.

---

## Protocol: Full Mapping Update Chain

**Start at Hero_index.md and walk the chain:**

| Step | File | Update Required |
|------|------|-----------------|
| 1 | `Hero_index.md` | Verify structure, update if folder hierarchy changed |
| 2 | `MASTER_MAPPING.md` | Domain folder technique count, total techniques, regen timestamp |
| 3 | Domain `00-MASTER-INDEX.md` (e.g., `Video_Effects/00-MASTER-INDEX.md`) | Add File entry, update tags, cross-refs, revision history |
| 4 | Domain `index.md` (e.g., `Video_Effects/index.md`) | Add technique entry to table, increment `total_techniques` |
| 5 | `CROSS_REFERENCE_INDEX.md` | Add tool usage counts, cross-ref tables, workflow chains, difficulty/time tags |
| 6 | `tags/*.md` | Create new tag files, update existing tag counts |
| 7 | `collections/index.md` | Add collection entry if new category |
| 8 | `collections/*.md` | Create/update collection files |
| 9 | `analysis/index.md` | Add video entry |
| 10 | `analysis/video_id/analysis.json` | Create structured analysis JSON |
| 11 | `media/index.md` | Add placeholder GIF entry, increment count |

---

## Video Effects Specifics (This Session)

### Folder Structure
```
Video_Effects/
├── 00-MASTER-INDEX.md          # Category TOC + navigation
├── TEMPLATE-Video-Effect.md    # Template for new effects
├── VIDEO_EFFECTS_QUEUE.md      # Processing queue
├── index.md                    # Auto-generated index
├── assets/                     # Visual assets by category
│   ├── transitions/
│   ├── compositing/
│   ├── motion-graphics/
│   ├── vfx/
│   ├── text-effects/
│   ├── stylization/
│   └── time-effects/
├── transitions/
│   ├── 00-MASTER-INDEX.md
│   └── NN-Effect_Name_Source_Tools.md
├── compositing/
├── motion-graphics/
├── vfx/
│   └── NN-Effect_Name_Source_Tools.md
├── text-effects/
├── stylization/
└── time-effects/
```

### New Tags Created (This Session)
- `relight.md` — video_count: 1
- `depth-map.md` — video_count: 1
- `surface-map.md` — video_count: 1
- `3d-lighting.md` — video_count: 1
- `day-for-night.md` — video_count: 1
- `lighting-in-post.md` — video_count: 1
- `jamiefenn.md` — video_count: 1

### Updated Tags
- `vfx.md` — video_count: 3→4

### New Collection
- `vfx.md` — "Visual effects: relighting, depth maps, tracked lights"

### Updated Mapping Files
- `Video_Effects/index.md` — total_techniques: 6→7
- `Video_Effects/00-MASTER-INDEX.md` — Total Techniques: 1→4, File 04 added
- `MASTER_MAPPING.md` — Video_Effects: 7→8, Total: 963→964
- `CROSS_REFERENCE_INDEX.md` — Relight OFX count 1→2, 4 cross-refs, Chain 6 workflow
- `analysis/index.md` — Added iusBsXNKGPE entry
- `analysis/iusBsXNKGPE/analysis.json` — Created structured analysis
- `media/index.md` — total_entries: 405→406, placeholder GIF entry
- `collections/index.md` — Added vfx entry
- `collections/vfx.md` — Created new collection

---

## YouTube-Specific Workflow (This Session)

### Extraction Method
```bash
# 1. Get transcript via yt-dlp (not browser — handles login walls better)
yt-dlp --write-sub --write-auto-sub --sub-lang en --skip-download "https://youtu.be/VIDEO_ID"

# 2. Parse VTT to clean transcript
python3 -c "
import webvtt, re
vtt = webvtt.read('VIDEO_ID.en.vtt')
full = ' '.join([c.text for c in vtt])
clean = re.sub(r'<[^>]+>', '', full)
words = clean.split()
dedup = [w for i,w in enumerate(words) if i==0 or w!=words[i-1]]
print(' '.join(dedup))
"
```

### Vault Note Template
Follow `TEMPLATE-Video-Effect.md` in Video_Effects folder:
- YAML-style frontmatter with vault path, source, video ID, technique
- Node graph diagrams (Color Page workflows)
- Step-by-step procedure tables
- Key principles / pitfalls / verification checklist
- Cross-references to existing vault content
- Visual asset placeholders
- Tags following convention: `#davinci-resolve #video-effects #vfx #relight #depth-map ...`

---

## Quick Reference: Tag Naming Convention

| Pattern | Example |
|---------|---------|
| Technique | `#relight`, `#depth-map`, `#surface-map` |
| Category | `#vfx`, `#transitions`, `#compositing` |
| Source | `#jamiefenn`, `#art3studi0` |
| Feature | `#3d-lighting`, `#day-for-night`, `#node-cache` |
| Tool | `#layer-mixer`, `#effects-tracker`, `#hdr-palette` |

---

## Session Notes

**Source:** YouTube @jamiefenn — "You Can't Fix Lighting in Post. Except You Can." (Video ID: iusBsXNKGPE, 17:21)
**Technique:** Relight Tool with Surface Maps & Depth Maps for 3D Lighting in Post
**Level:** Advanced (Studio 18.5+ required)
**Key Levels Covered:**
1. Basic Relight (single virtual light)
2. Multi-Light Setup (3-point lighting via Layer Mixer)
3. Depth Map Isolation (clean subject-only relighting)
4. Day-for-Night with Tracked Practical Lights

**Time Invested:** ~45 minutes (transcript extraction, cleaning, note creation, mapping updates)
**Files Touched:** 17 files (1 created, 16 updated)