# Obsidian Export Structure Details

## File Naming & Deduplication

Graphify sanitizes node labels for filenames:
- Removes: `\`, `/`, `*`, `?`, `:`, `"`, `<`, `>`, `|`, `#`, `^`, `[`, `]`
- Strips trailing `.md`, `.mdx`, `.qmd`, `.markdown`
- Requires at least one word character (fallback: `unnamed`)
- Deduplicates with numeric suffix: `Concept.md`, `Concept_1.md`, `Concept_2.md`

## Community Naming

Communities get `_COMMUNITY_<SanitizedName>.md`:
- Same deduplication logic as nodes
- Case-insensitive collision protection
- Example: `_COMMUNITY_Batch Image Generation.md`

## YAML Frontmatter (Per Node)

```yaml
---
source_file: "flux_wrapper.py"
type: "code"
community: "Batch Image Generation"
location: "L59"
tags:
  - graphify/code
  - graphify/EXTRACTED
  - community/Batch_Image_Generation
---
```

- `type`: `code`, `document`, `paper`, `image`, `rationale`
- `confidence` tag: `graphify/EXTRACTED`, `graphify/INFERRED`, `graphify/AMBIGUOUS`
- `community` tag: `community/<Community_Name>` (spaces → underscores)

## Wikilink Format

```
- [[TargetNode]] - `relation` [CONFIDENCE]
```

Relations extracted:
- Code: `contains`, `imports`, `calls`, `method`, `references`
- Docs: `references`, `semantically_similar_to`, `conceptually_related_to`
- Rationale: `rationale_for`

## Community Overview Note

```markdown
---
type: community
cohesion: 0.50
members: 4
---

# Batch Image Generation

**Cohesion:** 0.50 - moderately connected
**Members:** 4 nodes

## Members
- [[_generate()]] - code - flux_wrapper.py
- [[batch_generate()]] - code - flux_wrapper.py

## Live Query (requires Dataview plugin)
```dataview
TABLE source_file, type FROM #community/Batch_Image_Generation
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_Image Metadata and History]]
- 1 edge to [[_COMMUNITY_generate_flux]]

## Top bridge nodes
- [[_generate()]] - degree 5, connects to 3 communities
```

## Canvas Structure (graph.canvas)

```json
{
  "nodes": [
    {"id": "g0", "type": "group", "label": "Community Name", "x": 0, "y": 0, "width": 600, "height": 400, "color": "1"},
    {"id": "n_<hash>", "type": "file", "file": "Concept.md", "x": 20, "y": 80, "width": 180, "height": 60}
  ],
  "edges": [
    {"id": "e_<hash>", "fromNode": "n_<hash>", "toNode": "n_<hash>", "label": "calls [EXTRACTED]"}
  ]
}
```

- Communities as groups (colored boxes)
- Nodes as file cards (linked to `.md` notes)
- Edges as labeled connections (capped at 200 highest-weight)
- Color codes: 1=red, 2=orange, 3=yellow, 4=green, 5=cyan, 6=purple

## Graph View Auto-Coloring (.obsidian/graph.json)

```json
{
  "colorGroups": [
    {
      "query": "tag:#community/Batch_Image_Generation",
      "color": {"a": 1, "rgb": 15896107}
    }
  ]
}
```

- One entry per community
- Queries by `#community/<Name>` tag
- Colors cycle through Obsidian's 6 palette colors

## Manifest Protection (.graphify_obsidian_manifest.json)

```json
{
  "files": ["Concept.md", "_COMMUNITY_Name.md", "graph.canvas", ".obsidian/graph.json"]
}
```

- Tracks all files Graphify created
- On re-export: refuses to overwrite files NOT in manifest
- Prevents clobbering user's existing notes
- Warning printed to stderr if skips occur

## Incremental Update Behavior

- Re-export reads manifest
- Updates Graphify-owned files in place
- Adds new nodes/communities as new files
- Never deletes user files
- Orphaned Graphify files (from deleted nodes) remain but are harmless