# Obsidian Vault Export — Deep Dive

## What Gets Generated

```
Graphify-Project/
├── ClassName.md                    # One per code node (classes, functions, modules)
├── function_name.md                # 
├── ModuleName.md                   #
├── _COMMUNITY_DatabasePool.md      # One per community (overview + Dataview query)
├── _COMMUNITY_AuthManager.md       #
├── graph.canvas                    # Visual canvas: groups + cards + edges
├── .obsidian/
│   └── graph.json                  # Graph View color groups by community tag
└── .graphify_obsidian_manifest.json # Protection manifest
```

## Node Notes (per concept)

**YAML frontmatter:**
```yaml
---
source_file: "database.py"
type: "code"
community: "DatabasePool"
location: "L8"
tags:
  - graphify/code
  - graphify/EXTRACTED
  - community/DatabasePool
---
```

**Body:**
```markdown
# DatabasePool

## Connections
- [[._init_pool]] - `method` [EXTRACTED]
- [[.execute]] - `method` [EXTRACTED]
- [[Thread-safe SQLite connection pool.]] - `rationale_for` [EXTRACTED]
- [[api.py]] - `imports` [EXTRACTED]
- [[create_app()]] - `references` [EXTRACTED]
- [[main()]] - `calls` [EXTRACTED]

#graphify/code #graphify/EXTRACTED #community/DatabasePool
```

## Community Overview Notes

Each `_COMMUNITY_Name.md` contains:
- **Cohesion score** (0.0–1.0) with description (tightly/moderately/loosely connected)
- **Members list** as wikilinks with type + source file
- **Dataview live query** (requires Dataview plugin):
  ```dataview
  TABLE source_file, type FROM #community/DatabasePool
  SORT file.name ASC
  ```
- **Connections to other communities** (edge counts)
- **Top bridge nodes** (high degree + cross-community reach)

## Canvas (`graph.canvas`)

Obsidian Canvas format with:
- Communities as **groups** (colored boxes, arranged in grid)
- Nodes as **file cards** (linked to `.md` notes, laid out in rows within group)
- **Edges** as labeled connections between cards (capped at 200 highest-weight)

Open in Obsidian → infinite canvas with drag/rearrange.

## Graph View Colors (`.obsidian/graph.json`)

Auto-generated color groups:
```json
{
  "colorGroups": [
    {"query": "tag:#community/DatabasePool", "color": {"a": 1, "rgb": 5142951}},
    {"query": "tag:#community/AuthManager", "color": {"a": 1, "rgb": 15896107}},
    ...
  ]
}
```

Open Graph View in Obsidian → nodes colored by community.

## Manifest Protection (`.graphify_obsidian_manifest.json`)

Tracks files Graphify owns. On re-export:
- **Graphify-owned files** → overwritten
- **Pre-existing files NOT in manifest** in manifest → **skipped with warning**

This allows exporting into an existing vault safely.

## Practical Tips

1. **Export to empty directory first** to get full graph, then move/merge into main vault
2. **Use Dataview plugin** for live community queries in community notes
3. **Canvas** is best for visual exploration; Graph View for global structure
4. **Search** works across all frontmatter + body content
5. **Tags panel** shows `graphify/*` and `community/*` hierarchies