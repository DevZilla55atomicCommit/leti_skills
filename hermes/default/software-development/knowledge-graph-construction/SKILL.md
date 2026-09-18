---
name: knowledge-graph-construction
description: Build, query, and export queryable knowledge graphs from codebases, documentation vaults, and mixed corpora using Graphify. Covers installation, AST/semantic extraction, Obsidian vault export, Hermes integration, and common troubleshooting.
---

# Knowledge Graph Construction with Graphify

Graphify transforms any folder (code, docs, PDFs, images, videos) into a **queryable knowledge graph** with community detection, god nodes, and confidence-tagged edges (EXTRACTED/INFERRED/AMBIGUOUS). Outputs: interactive `graph.html`, `GRAPH_REPORT.md`, `graph.json`, and optionally an Obsidian vault.

## Installation

```bash
# Recommended: uv tool (isolated env, handles PATH)
uv tool install graphifyy
uv tool update-shell  # adds ~/.local/bin to PATH

# Alternative: pipx
pipx install graphifyy
pipx ensurepath

# Verify
graphify --version
```

## Core Workflow

### 1. Build Graph (First Time)

```bash
cd /path/to/project
graphify .                    # Full pipeline: AST + semantic + cluster + viz
graphify . --no-cluster       # Skip clustering (faster, no community labels)
graphify . --mode deep        # Aggressive INFERRED edge extraction
```

**Code-only corpus** (no API key needed): AST extraction via tree-sitter, 36 languages.

**Docs/PDFs/images/videos** (needs LLM): Semantic extraction requires one of:
- `GEMINI_API_KEY` / `GOOGLE_API_KEY` (Gemini)
- `ANTHROPIC_API_KEY` (Claude)
- `OPENAI_API_KEY` (OpenAI / OpenAI-compatible)
- `OLLAMA_BASE_URL` + `OLLAMA_MODEL` (local Ollama)
- `AWS_*` credentials (Bedrock)

### 2. Query Existing Graph

```bash
graphify query "how does auth connect to database?"
graphify path "AuthManager" "DatabasePool"   # Shortest path between concepts
graphify explain "RateLimiter"                # Node explanation with connections
```

### 3. Incremental Updates

```bash
graphify update .              # Re-extract changed code files only (AST, free)
graphify update . --force      # Overwrite even if node count decreases
graphify cluster-only .        # Re-run clustering on existing graph
```

### 4. Export to Obsidian Vault

```bash
# One-shot build + export
graphify . --obsidian --obsidian-dir "/path/to/vault/ProjectName"

# Or separate steps
graphify .
graphify export obsidian --dir "/path/to/vault/ProjectName"
```

**Outputs in vault:**
- One `.md` per node with YAML frontmatter + `[[wikilinks]]` to connections
- `_COMMUNITY_Name.md` overview notes (members, cohesion, cross-community links, bridge nodes, Dataview queries)
- `graph.canvas` visual canvas (communities as groups, nodes as cards)
- `.obsidian/graph.json` auto-colors Graph View by community tags
- `.graphify_obsidian_manifest.json` protects your existing notes from overwrite

### 5. Hermes Integration

```bash
graphify hermes install
# Writes AGENTS.md to project root + ~/.hermes/skills/graphify/SKILL.md
```

Then in Hermes: `/graphify .` or `/graphify query "..."` works natively.

## Controlling What Gets Processed

Create `.graphifyignore` (same syntax as `.gitignore`, merged with it):

```gitignore
# Skip all markdown/docs for code-only graph
*.md
*.txt
*.pdf

# Skip vault config
.obsidian/
Graphify-*/

# Skip system/venv
.DS_Store
**/venv/**
**/node_modules/**
**/cache/**
```

**Key insight**: Without `.graphifyignore`, a typical Obsidian vault (200+ `.md` files) will require semantic extraction for each note → needs LLM API key and costs tokens.

## Common Pitfalls & Fixes

| Symptom | Cause | Fix |
|---------|-------|-----|
| `no LLM API key found (N doc files need semantic extraction)` | Vault has `.md`/`.pdf`/images but no API key set | Add `.graphifyignore` to skip docs, or set `GEMINI_API_KEY` / `ANTHROPIC_API_KEY` / `OPENAI_API_KEY` |
| Ollama chunks fail with `404 page not found` | Model doesn't support `/api/generate` endpoint format | Use a model that supports generate (e.g., `llama3.1`, `mistral`), or switch to cloud API |
| `graphify: command not found` after install | `~/.local/bin` not on PATH | Run `uv tool update-shell` or `pipx ensurepath`, restart shell |
| Graph has fewer nodes after `--update` | Refactor deleted files, old nodes linger | Re-run with `--force` flag |
| HTML too large to open (>5000 nodes) | Large corpus | Use `--no-viz` or `graphify cluster-only --no-viz`, then query via CLI |
| Export overwrites your notes | Vault not empty | Graphify uses manifest (`.graphify_obsidian_manifest.json`) — only exports to empty dir or its own files |

## Query Patterns

```bash
# Broad context (BFS)
graphify query "what connects auth to database?"

# Deep trace (DFS)
graphify query "auth flow" --dfs

# Token-bounded
graphify query "data pipeline" --budget 1500

# Cross-repo (merge graphs first)
graphify merge-graphs a.json b.json --out merged.json
graphify query "..." --graph merged.json
```

## MCP Server (Team/Shared Access)

```bash
# Local stdio (for your AI assistant)
python -m graphify.serve graphify-out/graph.json

# HTTP server (team/shared, point IDE MCP config at http://host:8080/mcp)
python -m graphify.serve graphify-out/graph.json --transport http --host 0.0.0.0 --port 8080 --api-key "$SECRET"
```

Tools exposed: `query_graph`, `get_node`, `get_neighbors`, `shortest_path`, `list_prs`, `get_pr_impact`, `triage_prs`.

## References

- `references/obsidian-integration.md` — Vault export details, manifest protection, canvas, graph view colors
- `references/hermes-integration.md` — AGENTS.md, skill install, query flow in Hermes
- `references/common-pitfalls.md` — Detailed troubleshooting, Ollama model compatibility, API key setup
- `references/query-examples.md` — Real query patterns and output interpretation