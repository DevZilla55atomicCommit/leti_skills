# Obsidian Export Structure Reference

## What Graphify Creates in Your Vault

When you run `graphify export obsidian --dir /path/to/vault` or `/graphify . --obsidian --obsidian-dir /path/to/vault`, Graphify creates a **self-contained subfolder** that you open as a vault in Obsidian.

### File Manifest (from test run on 4-file Python project)

```
Graphify-Test/
├── .graphify_obsidian_manifest.json    # Tracks Graphify-owned files (protection)
├── .obsidian/
│   └── graph.json                      # Graph view color groups by community
├── graph.canvas                        # Canvas: communities=groups, nodes=cards
├── *.md                                # 1 file per graph node (~40-50 files)
└── _COMMUNITY_*.md                     # 1 overview per community (~10 files)
```

## Node Notes (One Per Graph Node)

**Filename**: Sanitized node label + `.md` (deduplicated with numeric suffixes)

**Frontmatter**:
```yaml
---
source_file: "database.py"        # Origin file
type: "code"                       # code | document | paper | image | rationale
community: "DatabasePool"          # Community name
location: "L8"                     # Source line (code only)
tags:
  - graphify/code                  # File type tag
  - graphify/EXTRACTED             # Confidence: EXTRACTED | INFERRED | AMBIGUOUS
  - community/DatabasePool         # Community membership
---
```

**Body**:
```markdown
# Node Label

## Connections
- [[TargetNode]] - `relation` [CONFIDENCE]
- [[AnotherNode]] - `calls` [EXTRACTED]

#graphify/code #graphify/graphify/EXTRACTED #community/DatabasePool
```

**Relation Types**: `method`, `imports`, `references`, `calls`, `contains`, `rationale_for`, `semantically_similar_to`

**Confidence Tags**: `EXTRACTED` (explicit in source), `INFERRED` (deduced), `AMBIGUOUS` (uncertain)

## Community Overview Notes (`_COMMUNITY_Name.md`)

**Filename**: `_COMMUNITY_` + sanitized community name + `.md` (underscore prefix sorts to top)

**Frontmatter**:
```yaml
---
type: community
cohesion: 0.28
members: 9
---
```

**Sections**:
1. **Cohesion score** + description (tightly/moderately/loosely connected)
2. **Members table** - `[[NodeName]] - type - source_file`
3. **Dataview Live Query** - Requires Dataview plugin:
   ```dataview
   TABLE source_file, type FROM #community/DatabasePool
   SORT file.name ASC
   ```
4. **Cross-community edges** - Count + `[[_COMMUNITY_Other]]` links
5. **Top Bridge Nodes** - Highest degree nodes connecting to other communities

## Canvas File (`graph.canvas`)

Obsidian Canvas format with:
- **Groups** = Communities (colored, grid layout)
- **Cards** = Nodes (type: `file`, pointing to `.md` notes)
- **Edges** = Top 200 weighted connections with labels

Open in Obsidian → infinite canvas with community groupings visible.

## Graph View Colors (`.obsidian/graph.json`)

Auto-generated color groups by community tag:
```json
{
  "colorGroups": [
    {
      "query": "tag:#community/DatabasePool",
      "color": { "a": 1, "rgb": 5142951 }
    },
    ...
  ]
}
```

Enable in Obsidian: **Graph View → Groups → + New Group** (auto-populated from this file).

## Manifest Protection (`.graphify_obsidian_manifest.json`)

```json
{
  "files": [
    "DatabasePool.md",
    "_COMMUNITY_DatabasePool.md",
    ".obsidian/graph.json",
    "graph.canvas",
    ...
  ]
}
```

**Behavior**:
- Graphify **only overwrites files listed in manifest**
- Pre-existing files in vault **outside manifest are never touched**
- Safe to export into an existing vault with your own notes
- Re-runs update Graphify files, preserve your files

## Opening in Obsidian

1. Open Obsidian
2. "Open folder as vault" → Select the Graphify export directory (e.g., `Graphify-Test/`)
3. Enable core plugins: **Canvas**, **Graph View**, **Dataview** (for live queries)
4. Open `graph.canvas` for visual layout
5. Open Graph View → Groups should show community colors
6. Search `#community/DatabasePool` in tag pane to filter

## Tips for Your TamaZila Vault

```bash
# Export to subfolder of your main vault
graphify export obsidian --dir "/Users/alfredkamisese/TamaZila Obsidian Vault/Graphify-MyProject"

# Or use skill command in Hermes:
/graphify . --obsidian --obsidian-dir "/Users/alfredkamisese/TamaZila Obsidian Vault/Graphify-MyProject"

# The subfolder becomes a self-contained vault you can open separately
# Or keep it inside main vault and use "Open graph view" from any note
```

## File Count Estimation

| Project Size | Nodes | Communities | Notes Created |
|-------------|-------|-------------|---------------|
| Small (4 files) | ~40 | ~10 | ~50 |
| Medium (50 files) | ~500 | ~30 | ~530 |
| Large (500 files) | ~5000 | ~100 | ~5100 |

Each node = 1 note. Each community = 1 overview + 1 canvas group.