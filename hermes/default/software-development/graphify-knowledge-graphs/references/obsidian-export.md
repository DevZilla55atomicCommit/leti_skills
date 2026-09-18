---
title: "Graphify Obsidian Export Reference"
source: "Graphify repository (graphify/export.py - to_obsidian, to_canvas functions)"
version: "0.9.9"
---

# Graphify Obsidian Export Reference

## Export Commands

```bash
# Basic export to default location (graphify-out/obsidian)
graphify export obsidian

# Export to custom directory (existing vault)
graphify export obsidian --dir ~/MyVault/Graphify-Project

# Via slash command (includes HTML viz)
/graphify . --obsidian --obsidian-dir ~/MyVault/Graphify-Project
```

## Generated Files

```
Graphify-Project/
├── .obsidian/
│   └── graph.json          # Graph view color groups by community tag
├── _COMMUNITY_<Name>.md    # One per community (overview notes)
├── <NodeLabel>.md          # One per node (with wikilinks)
├── graph.canvas            # Visual canvas (communities as groups)
└── .graphify_obsidian_manifest.json  # Tracks owned files
```

## Node Note Format

Each node becomes a `.md` file with:

```markdown
---
source_file: "src/auth.py"
type: "code"
community: "Auth System"
location: "L42"
tags:
  - graphify/code
  - graphify/EXTRACTED
  - community/auth_system
---

# AuthModule

## Connections
- [[DatabasePool]] - `uses` [EXTRACTED]
- [[RateLimiter]] - `calls` [INFERRED]

#graphify/code #graphify/EXTRACTED #community/auth_system
```

**Frontmatter fields:**
- `source_file` - original file path (relativized)
- `type` - `code`, `document`, `paper`, `image`, `rationale`
- `community` - community name (from labels)
- `location` - source location (line number, heading)
- `tags` - structured tags for filtering

**Body:**
- `# Label` - node label as heading
- `## Connections` - outgoing edges as wikilinks with relation + confidence
- Inline tags at bottom for Obsidian tag panel

---

## Community Overview Notes

Named `_COMMUNITY_<Name>.md` (underscore prefix sorts to top):

```markdown
---
type: community
cohesion: 0.72
members: 47
---

# Auth System

**Cohesion:** 0.72 - tightly connected
**Members:** 47 nodes

## Members
- [[AuthModule]] - code - src/auth.py
- [[RateLimiter]] - code - src/middleware.py
...

## Live Query (requires Dataview plugin)
```dataview
TABLE source_file, type FROM #community/auth_system
SORT file.name ASC
```

## Connections to other communities
- 12 edges to [[_COMMUNITY_Database]]

## Top bridge nodes
- [[AuthModule]] - degree 34, connects to 2 communities
```

---

## Canvas Export (graph.canvas)

Obsidian Canvas file with:
- **Groups** = communities (colored boxes in grid layout)
- **Cards** = nodes (file cards linking to `.md` notes)
- **Edges** = connections between nodes (capped at 200 highest-weight)

Layout algorithm:
1. Communities arranged in grid (sqrt(n) columns)
2. Nodes within community in ceil(sqrt(n)) column grid
3. Group boxes sized to fit all member cards
4. Colors cycled from Obsidian's 6 canvas colors

---

## Graph View Configuration (.obsidian/graph.json)

Auto-generated color groups for Obsidian's native graph view:

```json
{
  "colorGroups": [
    {
      "query": "tag:#community/auth_system",
      "color": { "a": 1, "rgb": 16711680 }
    },
    {
      "query": "tag:#community/database",
      "color": { "a": 1, "rgb": 65280 }
    }
  ]
}
```

Each community gets a distinct color. Nodes tagged with `community/<name>` appear in that color in graph view.

---

## Manifest Protection

File: `.graphify_obsidian_manifest.json`

```json
{
  "files": [
    "_COMMUNITY_Auth_System.md",
    "AuthModule.md",
    "DatabasePool.md",
    "graph.canvas",
    ".obsidian/graph.json"
  ]
}
```

**Behavior:**
- On re-export, Graphify reads manifest
- Only overwrites files listed in manifest (its own files)
- Pre-existing files NOT in manifest are NEVER touched
- Warning printed if any files skipped
- Safe to point `--obsidian-dir` at existing vault

---

## Tag System

| Tag Pattern | Purpose |
|-------------|---------|
| `graphify/code` | Node from code file |
| `graphify/document` | Node from markdown/doc |
| `graphify/paper` | Node from PDF/paper |
| `graphify/image` | Node from image |
| `graphify/EXTRACTED` | Dominant edge confidence |
| `graphify/INFERRED` | Dominant edge confidence |
| `graphify/AMBIGUOUS` | Dominant edge confidence |
| `community/<name>` | Community membership (for graph view colors) |

---

## Dataview Integration

Community notes include live Dataview queries:

```dataview
TABLE source_file, type FROM #community/auth_system
SORT file.name ASC
```

Requires **Dataview plugin** in Obsidian. Shows all nodes in that community as a table.

---

## Filename Sanitization

Node labels → filenames:
1. Remove unsafe chars: `\/*?:"<>|#^[]`
2. Strip trailing `.md`, `.mdx`, `.qmd`, `.markdown`
3. Require at least one word character (fallback: `unnamed`)
4. Deduplicate: `Label` → `Label_1`, `Label_2` if collision
5. Case-folded dedup for communities (prevents `API` vs `Api` collision on macOS)

---

## Command Line Options

```bash
graphify export obsidian [OPTIONS]

Options:
  --dir PATH          Output directory (default: graphify-out/obsidian)
  --graph PATH        Custom graph.json path
  --no-labels         Skip community labeling (use "Community N")
  --help              Show help
```

---

## Integration with TamaZila Vault

For Alfred's setup:

```bash
# Vault path from memory
VAULT="/Users/alfredkamisese/TamaZila Obsidian Vault"

# Map a project into a subfolder of the vault
/graphify ./my-project --obsidian --obsidian-dir "$VAULT/Graphify-my-project"

# Map the entire vault (markdown files as corpus)
/graphify "$VAULT" --obsidian --obsidian-dir "$VAULT/Graphify-VaultMap"
```

---

## Verification Checklist

After export, verify in Obsidian:
- [ ] Open vault folder → see `.md` files for nodes
- [ ] Graph view (Ctrl+G) → nodes colored by community
- [ ] Canvas (Ctrl+Shift+P → "Open canvas") → `graph.canvas` shows groups
- [ ] Search `#community/auth_system` → shows community members
- [ ] Dataview query in community note → renders table
- [ ] Click wikilink `[[AuthModule]]` → opens node note
- [ ] Community note `_COMMUNITY_Auth_System.md` shows members + connections