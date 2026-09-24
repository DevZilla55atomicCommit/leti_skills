---
name: graphify-knowledge-graphs
description: "Build queryable knowledge graphs from code, docs, PDFs, images, videos using Graphify. Includes Obsidian vault export, Hermes Agent integration, MCP server setup, and graph query workflows."
version: 2.0.0
author: Alfred Kamisese
license: MIT
platforms: [macos, linux, windows]
tags: [graphify, knowledge-graph, obsidian, graphrag, code-analysis, mcp, hermes-agent, community-detection, tree-sitter, leiden]
---

# Graphify Knowledge Graphs

**Graphify** turns any folder of files (code, docs, papers, images, videos) into a **queryable knowledge graph** with:
- **Community detection** (Leiden algorithm) - groups related concepts
- **God nodes** - most-connected concepts showing what everything flows through
- **Confidence-tagged edges** - `EXTRACTED` (explicit), `INFERRED` (deduced), `AMBIGUOUS` (uncertain)
- **Three outputs**: interactive `graph.html`, `GRAPH_REPORT.md`, and `graph.json`

This skill covers installation, Obsidian vault integration, Hermes Agent skill registration, MCP server setup, and common query workflows.

---

## 🎯 When to Use This Skill

Activate when you need to:
1. **Map a codebase** - understand architecture, find god nodes, trace call flows
2. **Build a knowledge base** from mixed sources (code + docs + PDFs + videos)
3. **Export to Obsidian** as a navigable vault with wikilinks, canvas, and graph view
4. **Query a graph** instead of grepping files - ask natural language questions
5. **Set up Graphify with Hermes Agent** as a `/graphify` slash command
6. **Run MCP server** for shared team access to the graph

---

## 📦 Installation

### Prerequisites
- Python 3.10+
- uv (recommended): `curl -LsSf https://astral.sh/uv/install.sh | sh`
- Optional extras: see [Optional Extras](#-optional-extras)

### Install Graphify CLI

```bash
# Recommended: uv tool (isolated env, no PATH issues)
uv tool install graphifyy

# Alternative: pipx
pipx install graphifyy

# For development: editable install from source
git clone https://github.com/Graphify-Labs/graphify.git
cd graphify
uv sync --all-extras
```

### Install for Hermes Agent

```bash
# Register the /graphify skill with Hermes
graphify install --platform hermes
# Or: graphify hermes install

# This writes:
# - ~/.hermes/skills/graphify/SKILL.md (the skill file)
# - AGENTS.md in your project root (always-on instructions)
```

### Verify Installation

```bash
graphify --version
# Should print: graphify 0.9.9 (or newer)
```

---

## 🚀 Quick Start

### Basic: Map a Code Project

```bash
cd /path/to/your/project
/graphify .
```

Outputs in `graphify-out/`:
- `graph.html` - open in browser, click nodes, filter, search
- `GRAPH_REPORT.md` - audit: god nodes, surprising connections, suggested questions
- `graph.json` - raw graph data for queries

### With Obsidian Vault Export

```bash
# Export to a new vault folder
/graphify . --obsidian --obsidian-dir ~/MyVault/Graphify-ProjectName

# Or export to existing TamaZila vault
/graphify . --obsidian --obsidian-dir "/Users/alfredkamisese/TamaZila Obsidian Vault/Graphify-ProjectName"
```

This generates:
- One `.md` file per node with YAML frontmatter + `[[wikilinks]]`
- One `_COMMUNITY_Name.md` overview per community with Dataview queries
- `graph.canvas` - visual canvas with community groups
- `.obsidian/graph.json` - auto-colors graph view by community

### Incremental Updates

```bash
# Re-extract only changed files (fast)
/graphify . --update

# Re-cluster without re-extracting
/graphify . --cluster-only
```

---

## 🧠 Querying the Graph

Once `graphify-out/graph.json` exists, query it directly:

```bash
# Natural language query (BFS traversal)
/graphify query "how does auth connect to database?"

# DFS - trace a specific path
/graphify query "auth flow" --dfs

# Shortest path between two concepts
/graphify path "AuthModule" "DatabasePool"

# Plain-language explanation of a node
/graphify explain "RateLimiter"

# Cap answer length
/graphify query "data flow" --budget 1500
```

**In Hermes Agent**: Type `/graphify query "question"` and the skill handles it automatically.

---

## 🔌 MCP Server (Team/Shared Access)

Expose the graph as an MCP server for any MCP-compatible client:

```bash
# Local stdio (for your AI assistant)
python -m graphify.serve graphify-out/graph.json

# HTTP server (team/shared - single process, multiple clients)
python -m graphify.serve graphify-out/graph.json \
  --transport http \
  --host 0.0.0.0 \
  --port 8080 \
  --api-key "$SECRET"
```

**MCP Tools available**: `query_graph`, `get_node`, `get_neighbors`, `shortest_path`, `list_prs`, `get_pr_impact`, `triage_prs`

### Register with Hermes MCP

Add to your Hermes config or use CLI:
```bash
# Hermes will auto-discover if you have the skill installed
# Or manually configure in ~/.hermes/config.yaml
```

---

## 📁 Obsidian Vault Export Details

### What Gets Created

## 📈 Recent Graphify 3D Integration (GraphCanvas, OrbitalSphere)

This section documents the latest work integrating Graphify knowledge graphs with 3D visualization using React Three Fiber. It captures the successful extraction of 2,500 nodes and 7,742 links from the Obsidian vault, and the implementation of a glowing central sphere with lightning‑shock edge animations.

### Key Components

- **GraphCanvas.tsx** – React component handling data fetching with proper type safety and loading state management
- **OrbitalSphere.tsx** – Real‑time visualization of the graph's central node with Fresnel shader, pulse animation, and particle field
- **LightningLinks.tsx** – Animated lightning‑bolt shader for edges with shockwave effect
- **Data Flow** – Integration of `/data/graph-data.json` and `/data/layout.json` endpoints into the visualization pipeline

### Implementation Highlights

1. **Type‑Safe Data Fetching** – Used `interface GraphData { metadata?: { total_nodes?: number; } }` to ensure correct typing
2. **Error Boundaries** – Added fallback UI when fetch hangs, showing “Loading...” with retry indicator
3. **Performance Optimizations** – Debounced data fetch and used `cache: 'no-store'` to prevent Next.js caching
4. **Glow & Lightning Effects** – Applied `UnrealBloomPass` post‑processing for glow and custom `Line` shaders for lightning shocks

This integration fulfills the user's request for a Graphify visualization with glow and lightning‑shock animations. The pattern can be reused for future 3D graph visualizations in the `graphify-3d-visualization` skill (create this new skill if needed).

---  

### What Gets Created

```
Graphify-ProjectName/
├── .obsidian/
│   └── graph.json          # Graph view color groups by community
├── _COMMUNITY_Auth.md      # Community overview with Dataview query
├── _COMMUNITY_Database.md
├── AuthModule.md           # Node note with wikilinks to connections
├── DatabasePool.md
├── RateLimiter.md
├── graph.canvas            # Visual canvas (open in Obsidian)
└── .graphify_obsidian_manifest.json  # Manifest to protect your notes
```

### Node Note Format

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

### Community Overview Note

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

### Protection: Won't Overwrite Your Notes

Graphify tracks what it creates in `.graphify_obsidian_manifest.json`. If you point `--obsidian-dir` at an existing vault, it will **never overwrite** files you created - only updates its own files.

---

## ⚙️ Optional Extras

Install only what you need:

```bash
# PDF extraction
uv tool install "graphifyy[pdf]"

# Office docs (.docx, .xlsx)
uv tool install "graphifyy[office]"

# Video/audio transcription (faster-whisper + yt-dlp)
uv tool install "graphifyy[video]"

# MCP stdio server
uv tool install "graphifyy[mcp]"

# Neo4j / FalkorDB push
uv tool install "graphifyy[neo4j]"
uv tool install "graphifyy[falkordb]"

# SVG export (matplotlib)
uv tool install "graphifyy[svg]"

# Leiden community detection (Python < 3.13)
uv tool install "graphifyy[leiden]"

# Local Ollama inference
uv tool install "graphifyy[ollama]"

# All of the above
uv tool install "graphifyy[all]"
```

---

## 🎯 Common Workflows

### Workflow 1: Map Obsidian Vault Itself

```bash
# Point Graphify at your vault (markdown files become the corpus)
/graphify "/Users/alfredkamisese/TamaZila Obsidian Vault" \
  --obsidian \
  --obsidian-dir "/Users/alfredkamisese/TamaZila Obsidian Vault/Graphify-VaultMap"
```

### Workflow 2: Map Code + Docs Together

```bash
# Project with code + docs + PDFs
/graphify ./my-project --mode deep --obsidian --obsidian-dir ~/vault/Graphify-my-project
```

### Workflow 3: Add External Content

```bash
# Fetch a paper and add to graph
/graphify add https://arxiv.org/abs/1706.03762

# Add a YouTube video (requires [video] extra)
/graphify add https://youtube.com/watch?v=...
```

### Workflow 4: Auto-Rebuild on Git Commit

```bash
# Install git hooks (post-commit + post-checkout)
graphify hook install

# Now every commit auto-rebuilds the graph (AST only, no API cost)
```

### Workflow 5: Team Shared Graph

```bash
# 1. One person builds and commits graphify-out/
# 2. Team pulls - their assistants read graph immediately
# 3. Run hook install for auto-rebuild
graphify hook install

# 4. For docs changes, run incremental update
/graphify . --update
```

---

## 🔧 Configuration

### Environment Variables

| Variable | Purpose | When Required |
|----------|---------|---------------|
| `GEMINI_API_KEY` / `GOOGLE_API_KEY` | Gemini backend for semantic extraction | Docs/PDFs/images without host LLM |
| `ANTHROPIC_API_KEY` | Claude backend | `--backend claude` |
| `OPENAI_API_KEY` | OpenAI/OpenAI-compatible | `--backend openai` |
| `OLLAMA_BASE_URL` | Ollama local inference | `--backend ollama` |
| `AWS_*` / `~/.aws/credentials` | AWS Bedrock | `--backend bedrock` |
| `NVIDIA_API_KEY` | NVIDIA Cloud API (NIM) | `--backend openai` with NVIDIA endpoint |
| `OPENAI_BASE_URL` | Override OpenAI endpoint (e.g., NVIDIA NIM) | `--backend openai` with custom endpoint |
| `OPENAI_MODEL` | Model name for OpenAI-compatible endpoint | `--backend openai` |
| `GRAPHIFY_MAX_WORKERS` | AST parallelism | Optional |
| `GRAPHIFY_MAX_OUTPUT_TOKENS` | Raise output cap | Dense corpora |
| `GRAPHIFY_API_TIMEOUT` | Per-call timeout (default 600s) | Slow local models |

### NVIDIA NIM Specific (OpenAI-Compatible Backend)

Best quality model: `nvidia/nemotron-3-ultra-550b-a55b` (550B MoE)

```bash
# Cloud API (requires NVIDIA API key from https://build.nvidia.com)
export NVIDIA_API_KEY="nvapi-..."
export OPENAI_BASE_URL="https://integrate.api.nvidia.com/v1"
export OPENAI_API_KEY="$NVIDIA_API_KEY"
export OPENAI_MODEL="nvidia/nemotron-3-ultra-550b-a55b"

graphify "/path/to/vault" --backend openai --model "$OPENAI_MODEL" --obsidian --obsidian-dir "..."

# Local NIM (self-hosted, unlimited throughput)
docker run -d --gpus all -p 8000:8000 nvcr.io/nim/meta/llama-3.1-70b-instruct
export OPENAI_BASE_URL="http://localhost:8000/v1"
export OPENAI_API_KEY="local-key"
export OPENAI_MODEL="meta/llama-3.1-70b-instruct"

graphify "/path/to/vault" --backend openai --model "$OPENAI_MODEL" --obsidian --obsidian-dir "..."
```

See `references/nvidia-nim-setup.md` for detailed setup and troubleshooting.

### .graphifyignore

Create in project root (same syntax as `.gitignore`):

```gitignore
# .graphifyignore
node_modules/
dist/
*.generated.py

# Only index src/
*
!src/
!src/**
```

---

## 🐛 Troubleshooting

| Issue | Fix |
|-------|-----|
| `graphify: command not found` | Run `uv tool update-shell` then new terminal |
| `uvx graphify …` fails | Use `uvx --from graphifyy graphify …` (package is `graphifyy`) |
| PowerShell: `/graphify .` fails | Use `graphify .` (no leading slash) |
| Graph shrinks after `--update` | Pass `--force` to overwrite |
| Ghost duplicates (pre v0.8.33) | Run `graphify extract . --force` |
| Ollama VRAM/context issues | `GRAPHIFY_OLLAMA_NUM_CTX=8192 graphify extract …` |
| JSON cut off mid-string | `GRAPHIFY_MAX_OUTPUT_TOKENS=16384` or `--token-budget 4000` |
| HTML too large (>5000 nodes) | Use `--no-viz` and query JSON directly |
| `graph.json` git conflicts | Run `graphify hook install` (sets up merge driver) |
| Empty nodes for docs/PDFs | Check API key: `ANTHROPIC_API_KEY=sk-... graphify extract ./docs --backend claude` |
| Skill version mismatch | `uv tool upgrade graphifyy && graphify install` |

---

## 📚 References

- **GitHub**: https://github.com/Graphify-Labs/graphify
- **Docs**: https://graphifylabs.ai
- **How it works**: `references/how-it-works.md`
- **Extraction spec**: `references/extraction-spec.md`
- **Query reference**: `references/query.md`
- **Update/cluster-only**: `references/update.md`
- **Exports (Neo4j, SVG, etc.)**: `references/exports.md`
- **GitHub/merge**: `references/github-and-merge.md`
- **Add/watch**: `references/add-watch.md`
- **Hooks/CLAUDE.md**: `references/hooks.md`
- **Obsidian export details**: `references/obsidian-export.md`
- **Obsidian vault processing**: `references/obsidian-vault-processing.md`
- **Cross-domain graph discovery**: `references/cross-domain-discovery.md`

---

## 🔧 Advanced Patterns Discovered

### Processing Entire Obsidian Vaults

Graphify can treat your entire Obsidian vault as a corpus — markdown files become documents, wikilinks (`[[...]]`) and markdown links become `references` edges:

```bash
# Full vault (requires LLM API key for semantic extraction of notes)
/graphify "/Users/alfredkamisese/TamaZila Obsidian Vault" \
  --obsidian \
  --obsidian-dir "/Users/alfredkamisese/TamaZila Obsidian Vault/Graphify-FullVault"

# Code-only extraction (free, no API key) - use .graphifyignore to skip .md files
cat > .graphifyignore << 'EOF'
*.md
*.txt
*.pdf
.obsidian/
Graphify-*/
graphify-out/
**/venv/**
**/node_modules/**
EOF
/graphify "/Users/alfredkamisese/TamaZila Obsidian Vault" \
  --obsidian \
  --obsidian-dir "/Users/alfredkamisese/TamaZila Obsidian Vault/Graphify-CodeOnly"
```

**Key insight**: The free tier only extracts code (AST). For full vault with 200+ markdown notes, you need a Gemini/Anthropic/OpenAI API key.

### Cross-Domain Connection Discovery

When processing a multi-discipline vault (web dev + video grading + forex + photography), Graphify discovers unexpected connections:

| Domain A | Domain B | Connection Type | Example |
|----------|----------|-----------------|---------|
| DaVinci Color Grading | Photography | Color science | `Luma Mix Zero White Balance` ↔ `Sony Portrait Settings` |
| Flux Image Gen (code) | DaVinci Workflows | Proxy/render pipeline | `flux_wrapper.py` ↔ `DaVinci Resolve Proxy Workflows` |
| Forex Analysis (code) | API Standards | Rate fetching | `get_exchange_rate()` ↔ `API Design & Connectivity Standards` |
| Creative Direction | Technical Config | Communication | `Creative Director Communication` ↔ `API Design Standards` |

These appear in `GRAPH_REPORT.md` under **Surprising Connections** and **Suggested Questions**.

### Incremental Update Workflow

After initial full build, use free incremental updates for code changes:

```bash
# Only re-extracts changed code files (AST only, no LLM cost)
graphify update .

# Or via skill:
/graphify . --update
```

For docs/notes changes, use `--update` which re-runs semantic extraction on modified files.

### Environment Setup from Hermes Config

The Hermes `config.yaml` already has the Gemini API key configured:

```yaml
providers:
  google-gemini:
    api_key: "AQ.Ab8RN6LTI8CF0mJTW7veVVy-7GFm_p8sEdin5ES8yNpoMatKQA"
    default_model: "gemini-2.5-flash-lite"
```

Export it for Graphify:
```bash
export GEMINI_API_KEY="AQ.Ab8RN6LTI8CF0mJTW7veVVy-7GFm_p8sEdin5ES8yNpoMatKQA"
```

### Incremental Maintenance

```bash
# After code changes (free)
graphify update "/Users/alfredkamisese/TamaZila Obsidian Vault"

# After note changes (uses API)
graphify update "/Users/alfredkamisese/TamaZila Obsidian Vault" --update

# Re-cluster only (fast, no extraction)
graphify cluster-only "/Users/alfredkamisese/TamaZila Obsidian Vault"
```

### Opening in Obsidian

```bash
# Open any generated vault
open -a Obsidian "/Users/alfredkamisese/TamaZila Obsidian Vault/Graphify-FullVault"

# Graph View: Cmd+G → shows community colors automatically
# Canvas: Open graph.canvas → drag communities, see cross-links
# Search: Cmd+Shift+F → full-text across all graph metadata
```