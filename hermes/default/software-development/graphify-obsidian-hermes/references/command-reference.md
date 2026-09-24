# Graphify Query & Command Reference

Tested on 4-file Python Flask project (main.py, auth.py, database.py, api.py)

## Graph Build Commands

```bash
# Full pipeline from scratch
graphify .

# Full pipeline with Obsidian export
graphify . --obsidian --obsidian-dir "/path/to/vault/Graphify-Project"

# Incremental update (code changes only, AST only - no LLM cost)
graphify update .

# Re-cluster existing graph (no re-extraction)
graphify cluster-only .

# Re-cluster with custom resolution
graphify cluster-only . --resolution 1.5

# Force rebuild even if graph shrinks
graphify extract . --force
```

## Query Commands (Fast Path - Uses Existing graphify-out/graph.json)

### Natural Language Query
```bash
graphify query "how does auth connect to database?"
graphify query "what connects AuthManager to DatabasePool?"
graphify query "show the authentication flow"
```

**Output**: BFS traversal subgraph with nodes + edges, starting from vocabulary-matched nodes

### Shortest Path Between Concepts
```bash
graphify path "AuthManager" "DatabasePool"
graphify path "create_app" "DatabasePool"
graphify path "main" "AuthManager"
```

**Output**: Shortest path with hops, e.g.:
```
Shortest path (2 hops):
  AuthManager <--imports [EXTRACTED]-- main.py --imports [EXTRACTED]--> DatabasePool
```

### Explain a Node
```bash
graphify explain "AuthManager"
graphify explain "DatabasePool"
graphify explain "create_app"
```

**Output**:
```
Node: AuthManager
  ID:        auth_authmanager
  Source:    auth.py L8
  Type:      code
  Community: AuthManager
  Degree:    11

Connections (11):
  <-- main.py [imports] [EXTRACTED]
  <-- api.py [imports] [EXTRACTED]
  <-- create_app() [references] [EXTRACTED]
  <-- auth.py [contains] [EXTRACTED]
  <-- main() [calls] [EXTRACTED]
  --> .create_session() [method] [EXTRACTED]
  --> .hash_password() [method] [EXTRACTED]
  --> .logout() [method] [EXTRACTED]
  --> .validate_session() [method] [EXTRACTED]
  --> .__init__() [method] [EXTRACTED]
  <-- Manages user authentication and sessions. [rationale_for] [EXTRACTED]
```

## Obsidian Export Commands

```bash
# Export to custom vault directory
graphify export obsidian --dir "/path/to/vault/Graphify-Project"

# Export with skill command (in Hermes)
/graphify . --obsidian --obsidian-dir "/path/to/vault/Graphify-Project"
```

**Output**:
```
Obsidian vault: 49 notes in /path/to/vault/Graphify-Project/
Canvas: /path/to/vault/Graphify-Project/graph.canvas
Open /path/to/vault/Graphify-Project/ as a vault in Obsidian.
```

## Other Export Formats

```bash
# Mermaid architecture diagram (HTML)
graphify export callflow-html
graphify export callflow-html --output docs/arch.html

# Neo4j
graphify export --neo4j              # Generates cypher.txt
graphify export --neo4j-push bolt://localhost:7687

# FalkorDB
graphify export --falkordb
graphify export --falkordb-push falkordb://localhost:6379

# SVG / GraphML (Gephi, yEd)
graphify export --svg
graphify export --graphml

# Agent-crawlable wiki
graphify export --wiki

# MCP Server
python -m graphify.serve graphify-out/graph.json              # stdio
python -m graphify.serve graphify-out/graph.json --transport http --host 0.0.0.0 --port 8080 --api-key "$SECRET"
```

## Git Hooks

```bash
# Install post-commit + post-checkout hooks + merge driver
graphify hook install

# Check status
graphify hook status

# Uninstall
graphify hook uninstall
```

## Skill Commands (Inside Hermes)

```bash
# Build graph
/graphify .

# Build + export to Obsidian
/graphify . --obsidian --obsidian-dir "/path/to/vault/Graphify-Project"

# Query existing graph
/graphify query "your question"
/graphify path "ConceptA" "ConceptB"
/graphify explain "Concept"

# Update
/graphify . --update

# Re-cluster
/graphify . --cluster-only
```

## Test Results Summary (4-file Flask project)

| Metric | Value |
|--------|-------|
| Nodes | 39 |
| Edges | 58 |
| Communities | 10 |
| Extraction | 100% EXTRACTED (code-only = no LLM) |
| Token cost | 0 input / 0 output |
| Obsidian notes | 49 (39 nodes + 10 communities) |
| Canvas nodes | 49 cards in 10 groups |

## Key Graph Insights from Test

**God Nodes** (most connected):
1. `DatabasePool` - 13 edges
2. `AuthManager` - 11 edges
3. `create_app()` - 7 edges

**Communities**:
- `DatabasePool` (cohesion 0.28) - DB connection pool internals
- `.get_connection` (cohesion 0.29) - Connection handling
- `api.py` (cohesion 0.50) - Flask app factory + routes
- `AuthManager` - Auth class + methods
- `main.py` - Entry point
- `database.py` - Module level
- `.create_session`, `.hash_password`, `.logout`, `.validate_session` - Individual auth methods

**Surprising Connections** (cross-file):
- `create_app()` → `AuthManager` (imports)
- `create_app()` → `DatabasePool` (imports)
- `main()` → `AuthManager` (calls)
- `main()` → `DatabasePool` (calls)
- `main()` → `create_app()` (calls)

## Tips for Large Projects

```bash
# Skip HTML for graphs > 5000 nodes
graphify . --no-viz

# Deep extraction (richer INFERRED edges)
graphify . --mode deep

# Directed graph (preserves edge direction)
graphify . --directed

# Watch for changes (auto-rebuild code on file save)
graphify . --watch

# Add external content
graphify add https://arxiv.org/abs/1706.03762  # Paper
graphify add https://youtube.com/watch?v=...   # Video (needs [video] extra)
```