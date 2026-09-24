# Graphify Integration with TONY

## Your Existing Graphify Setup

Your project has Graphify at:
- **Vault**: `/Users/alfredkamisese/TamaZila Obsidian Vault`
- **Output**: `graphify-out/graph.json` (god nodes, communities, edges)
- **Wiki**: `graphify-out/wiki/index.md`

## Connect to TONY

### 1. Configure Obsidian Vault Path

In `.env`:
```bash
OBSIDIAN_VAULT_PATH=/Users/alfredkamisese/TamaZila Obsidian Vault
OBSIDIAN_BRAIN_FOLDER=Agentic Brain
```

### 2. TONY's Graphify Module

`src/brain/graphify.js`:
- `buildFromWorkspace()` — scans `src/`, `skills/`, `integrations/` for JS/TS/Python/MD
- Extracts: imports, exports, functions, classes, comments
- Builds: nodes (files, symbols), edges (imports, calls, references)
- Outputs: `data/graphify.json` (97 nodes, 236 edges in our test)

### 3. Query Your Vault from TONY

Once vault path is configured:
```bash
# TONY will index vault markdown files
npm run charlie:graph

# Query via API
curl "http://localhost:8787/api/brain/graph?q=graphify&token=tony-hermes-local-2026"
```

### 4. Architectures of Mind Integration

`src/brain/architectures.js` assembles context from:
1. **Perception** — Voice STT, user message
2. **Working** — Current session history
3. **Episodic** — SQLite conversation DB
4. **Semantic** — JSON facts/preferences
5. **Procedural** — Playbooks, skills
6. **Graph** — Graphify code relationships ← YOUR DATA
7. **Obsidian** — Vault markdown notes ← YOUR VAULT

The `assembleContext({sessionId, userMessage})` pulls relevant nodes from both Graphify and Obsidian.

## Merge Strategy: Your Graphify + TONY's Graphify

| Source | Content | Use Case |
|--------|---------|----------|
| **Your Graphify** (`graphify-out/`) | Project codebase, Obsidian notes, research | Domain knowledge, business logic |
| **TONY's Graphify** (`data/graphify.json`) | TONY internal codebase | Self-awareness, tool locations |

### Option A: Symlink (Simple)
```bash
cd ~/tony-ai-agent
ln -s /Users/alfredkamisese/TamaZila\ Obsidian\ Vault ./vault
```

### Option B: Configure Both Paths
In `.env`:
```bash
# Your project
OBSIDIAN_VAULT_PATH=/Users/alfredkamisese/TamaZila Obsidian Vault

# TONY also reads its own workspace via graphify.buildFromWorkspace()
```

### Option C: Custom Graphify Build
Create a script that merges both graphs:
```javascript
// scripts/merge-graphs.js
const fs = require('fs');
const yourGraph = JSON.parse(fs.readFileSync('/path/to/graphify-out/graph.json'));
const tonyGraph = JSON.parse(fs.readFileSync('./data/graphify.json'));

// Merge nodes/edges, deduplicate by ID
const merged = { ... };
fs.writeFileSync('./data/graphify-merged.json', JSON.stringify(merged));
```

Then point TONY to merged graph.

## Query Examples

### Query Your Research
```bash
curl "http://localhost:8787/api/brain/graph/query?q=forex&token=tony-hermes-local-2026"
# Returns nodes/edges from your Forex research notes
```

### Query TONY Internals
```bash
curl "http://localhost:8787/api/brain/graph/query?q=paul&token=tony-hermes-local-2026"
# Returns Paul builder agent files in TONY
```

### Cross-Reference
```bash
curl "http://localhost:8787/api/brain/graph/query?q=agent&token=tony-hermes-local-2026"
# Returns BOTH your agent research + TONY's agent files
```

## Hermes Agent Bridge

Your Hermes Agent already has Graphify skill loaded. To share:

### Hermes → TONY
```python
# In Hermes skill
import requests

def query_tony_graph(term):
    resp = requests.get(
        "http://localhost:8787/api/brain/graph/query",
        params={"q": term, "token": "tony-hermes-local-2026"}
    )
    return resp.json()
```

### TONY → Hermes (via MCP)
If Hermes exposes MCP server:
```bash
# In .env
HERMES_MCP_URL=http://localhost:XXXX/mcp
```

Then TONY's `mcp_call` tool can invoke Hermes skills.

## Health Check: Graphify Status

```bash
curl http://localhost:8787/health | jq .mind.graphify
# {
#   "path": "/Users/.../data/graphify.json",
#   "nodes": 97,
#   "edges": 236,
#   "builtAt": "2026-07-08T23:42:36.852Z"
# }
```

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Vault not indexed | Check `OBSIDIAN_VAULT_PATH` exists; run `npm run charlie:graph` |
| 0 nodes from vault | Ensure `.md` files in vault; check `OBSIDIAN_BRAIN_FOLDER` |
| Graph outdated | `npm run charlie:graph` rebuilds from workspace |
| Merge conflicts | Use Option C script; deduplicate by `id` field |

## Next Steps

1. Add vault path to `.env`
2. Run `npm run charlie:graph` to build combined graph
3. Test queries against your Forex/creative research
4. Wire Hermes MCP for bidirectional skill access