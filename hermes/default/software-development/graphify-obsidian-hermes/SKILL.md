---
name: graphify-obsidian-hermes
description: "Complete workflow for installing Graphify, registering it with Hermes Agent, building knowledge graphs from code/docs, and exporting to Obsidian vaults with interactive graph view, canvas, and Dataview queries."
---

# Graphify + Obsidian + Hermes Integration Workflow

Complete end-to-end workflow for knowledge graph generation and Obsidian vault export using Graphify with Hermes Agent.

## Prerequisites

- macOS/Linux with Python 3.10+
- `uv` package manager (recommended) or `pipx`
- Hermes Agent desktop app running
- Obsidian with an existing vault

## Installation

### 1. Install Graphify CLI

```bash
# Recommended (isolated, handles PATH)
uv tool install graphifyy

# Fix PATH if needed
uv tool update-shell
source ~/.zshenv  # or restart shell

# Verify
graphify --version  # Should show graphify 0.9.9+
```

### 2. Register Graphify Skill with Hermes

```bash
# Global install (user-scoped skill)
graphify hermes install
# OR equivalently:
graphify install --platform hermes

# Project-scoped install (writes to ./.hermes/skills/graphify/)
graphify hermes install --project
# OR:
graphify install --platform hermes --project
```

This writes:
- `~/.hermes/skills/graphify/SKILL.md` (global) or `./.hermes/skills/graphify/SKILL.md` (project)
- `AGENTS.md` in project root with always-on graph query rules

## Basic Usage

### Build Knowledge Graph + Export to Obsidian Vault

```bash
# Navigate to your project
cd /path/to/your/project

# Full pipeline: extract → cluster → analyze → export HTML + Obsidian vault
graphify . --obsidian --obsidian-dir "/path/to/your/vault/Graphify-ProjectName"

# Or using the skill command (inside Hermes):
/graphify . --obsidian --obsidian-dir "/path/to/your/vault/Graphify-ProjectName"
```

### Export to Existing Vault (Safe - Won't Overwrite Your Notes)

```bash
# If vault exists, Graphify tracks its own files via manifest
# and refuses to overwrite pre-existing files not created by Graphify
graphify export obsidian --dir "/path/to/your/vault/Graphify-ProjectName"
```

### Query Existing Graph (Fast Path - No Rebuild)

```bash
# When graphify-out/graph.json exists, query directly
graphify query "how does auth connect to database?"
graphify path "AuthManager" "DatabasePool"
graphify explain "RateLimiter"
```

## Obsidian Vault Output Structure

Graphify creates a complete Obsidian vault with:

| File Type | Purpose |
|-----------|---------|
| `*.md` (one per node) | Entity notes with YAML frontmatter, `[[wikilinks]]`, inline `#tags` |
| `_COMMUNITY_Name.md` | Community overview: members, cohesion, cross-community edges, bridge nodes, Dataview query |
| `graph.canvas` | Visual canvas: communities as groups, nodes as cards, edges as connections |
| `.obsidian/graph.json` | Auto-colors graph view by community tags |
| `.graphify_obsidian_manifest.json` | Tracks Graphify-owned files to prevent clobbering user notes |

### Node Note Example (`DatabasePool.md`)

```markdown
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

# DatabasePool

## Connections
- [[.__init__()_1]] - `method` [EXTRACTED]
- [[._init_pool()]] - `method` [EXTRACTED]
- [[api.py]] - `imports` [EXTRACTED]
- [[create_app()]] - `references` [EXTRACTED]
- [[main()]] - `calls` [EXTRACTED]

#graphify/code #graphify/EXTRACTED #community/DatabasePool
```

### Community Overview (`_COMMUNITY_DatabasePool.md`)

```markdown
---
type: community
cohesion: 0.28
members: 9
---

# DatabasePool

**Cohesion:** 0.28 - loosely connected
**Members:** 9 nodes

## Members
- [[DatabasePool]] - code - database.py
- [[._init_pool()]] - code - database.py
- ...

## Live Query (requires Dataview plugin)
```dataview
TABLE source_file, type FROM #community/DatabasePool
SORT file.name ASC
```

## Connections to other communities
- 5 edges to [[_COMMUNITY_.get_connection]]
- 3 edges to [[_COMMUNITY_api.py]]

## Top bridge nodes
- [[DatabasePool]] - degree 13, connects to 4 communities
```

## Advanced Commands

### Incremental Update (Code Changes Only - No LLM Cost)

```bash
graphify update .
# OR
/graphify . --update
```

### Re-cluster Without Re-extraction

```bash
graphify cluster-only .
# With custom resolution (more granular = higher)
graphify cluster-only . --resolution 1.5
# Exclude super-hubs from god nodes
graphify cluster-only . --exclude-hubs 99
```

### Export Formats

```bash
# Mermaid architecture diagram (auto-regenerates on git commit with hook)
graphify export callflow-html

# Neo4j / FalkorDB
graphify export --neo4j
graphify export --neo4j-push bolt://localhost:7687
graphify export --falkordb
graphify export --falkordb-push falkordb://localhost:6379

# SVG / GraphML for Gephi/yEd
graphify export --svg
graphify export --graphml

# Agent-crawlable wiki
graphify export --wiki

# MCP Server (for repeated agent access)
python -m graphify.serve graphify-out/graph.json
# HTTP for team sharing
python -m graphify.serve graphify-out/graph.json --transport http --host 0.0.0.0 --port 8080 --api-key "$SECRET"
```

### Git Hooks (Auto-Rebuild on Commit)

```bash
# Installs post-commit + post-checkout hooks
# Also sets up git merge driver for graph.json (no conflicts)
graphify hook install

# Check status
graphify hook status

# Remove
graphify hook uninstall
```

## Optional Extras (Install Only What You Need)

```bash
# PDF support
uv tool install "graphifyy[pdf]"

# Video/audio transcription (faster-whisper + yt-dlp)
uv tool install "graphifyy[video]"

# Office docs (.docx, .xlsx)
uv tool install "graphifyy[office]"

# All extras
uv tool install "graphifyy[all]"
```

## Environment Variables (For Headless/CI Extraction)

```bash
# Semantic extraction backends (only needed for docs/PDFs/images - code is free)
GEMINI_API_KEY=...        # Google Gemini (priority 1)
ANTHROPIC_API_KEY=...     # Claude (priority 2)
OPENAI_API_KEY=...        # OpenAI-compatible (priority 3)
OLLAMA_BASE_URL=...       # Local Ollama (priority 4)

# Graphify behavior
GRAPHIFY_MAX_WORKERS=16   # AST parallelism
GRAPHIFY_MAX_OUTPUT_TOKENS=32768  # Raise for dense corpora
GRAPHIFY_API_TIMEOUT=900  # For slow local models
```

## Hermes-Specific Notes

- **No PreToolUse hooks** - Unlike Claude Code, Hermes uses `AGENTS.md` as the always-on mechanism
- The `graphify hermes install` command writes both the skill and `AGENTS.md`
- In Hermes, invoke with `/graphify` (not `graphify` bare command)
- Skill loads references on-demand from `~/.hermes/skills/graphify/references/`

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `graphify: command not found` | Run `uv tool update-shell` and restart shell |
| `uvx graphify ...` fails | Use `uvx --from graphifyy graphify ...` (package is `graphifyy`, command is `graphify`) |
| Graph shrinks on rebuild | Use `--force` or `GRAPHIFY_FORCE=1` to overwrite |
| Empty graph | Check `.graphifyignore` / `.gitignore`; ensure supported file types |
| Obsidian graph view not colored | Open vault in Obsidian, enable "Graph view" plugin, check `.obsidian/graph.json` exists |
| Canvas not rendering | Ensure Obsidian Canvas core plugin is enabled |

## Quick Reference Card

```bash
# Install & setup
uv tool install graphifyy && uv tool update-shell
graphify hermes install

# Build + export to vault
cd /my/project
graphify . --obsidian --obsidian-dir "~/Obsidian Vault/Graphify-MyProject"

# Query existing graph
graphify query "question about codebase"
graphify path "ConceptA" "ConceptB"
graphify explain "Concept"

# Maintain
graphify update .              # Incremental (code only)
graphify cluster-only .        # Re-cluster
graphify hook install          # Auto-rebuild on commit

# Extras
graphify export callflow-html  # Architecture diagram
python -m graphify.serve graphify-out/graph.json  # MCP server
```

---

## 🎯 Practical Findings from TamaZila Vault Processing

### Vault Structure Impact

| Approach | Files | Cost | Use Case |
|----------|-------|------|----------|
| **Code-only** (`.graphifyignore` skips `.md`) | 5-30 code files | $0 (free) | Pure code architecture mapping |
| **Selective folders** (DaVinci, Forex, Photography) | 50-200 docs each | $0.05-0.15 each | Domain-specific knowledge bases |
| **Full vault** (452 docs + 30 code) | ~500 files | ~$0.15-0.30 | Cross-domain discovery |

### TamaZila-Specific Commands

```bash
# Export API key from Hermes config
export GEMINI_API_KEY="$(grep -A2 'google-gemini:' ~/.hermes/config.yaml | grep 'api_key:' | cut -d'"' -f2)"

# 1. Code-only vault map (free)
cat > .graphifyignore << 'EOF'
*.md; *.txt; *.pdf; .obsidian/; Graphify-*/; graphify-out/; **/venv/**; **/node_modules/**
EOF
graphify "/Users/alfredkamisese/TamaZila Obsidian Vault" --obsidian --obsidian-dir "/Users/alfredkamisese/TamaZila Obsidian Vault/Graphify-CodeOnly"

# 2. DaVinci Knowledge Base (color grading focus)
graphify "/Users/alfredkamisese/TamaZila Obsidian Vault/Hermes Agent/DaVinci_Knowledge_Base" --obsidian --obsidian-dir "/Users/alfredkamisese/TamaZila Obsidian Vault/Graphify-DaVinci"

# 3. Forex Analysis
graphify "/Users/alfredkamisese/TamaZila Obsidian Vault/Hermes Agent/Forex Center" --obsidian --obsidian-dir "/Users/alfredkamisese/TamaZila Obsidian Vault/Graphify-Forex"

# 4. Full vault cross-domain (requires API key)
graphify "/Users/alfredkamisese/TamaZila Obsidian Vault" --obsidian --obsidian-dir "/Users/alfredkamisese/TamaZila Obsidian Vault/Graphify-FullVault"

# 5. Flux scripts subproject
graphify "/Users/alfredkamisese/TamaZila Obsidian Vault/Hermes Agent/Hermes Image Generates" --obsidian --obsidian-dir "/Users/alfredkamisese/TamaZila Obsidian Vault/Graphify-FluxScripts"
```

### Cross-Domain Connections Discovered

| Domain A | Domain B | Connection | Strength |
|----------|----------|------------|----------|
| DaVinci Color Grading | Photography | Color science (Luma Mix ↔ Sony Settings) | INFERRED 0.85 |
| Flux Image Gen (code) | DaVinci Workflows | Proxy/render pipeline | INFERRED 0.75 |
| Forex Code | API Standards | Rate fetching implementation | EXTRACTED |
| Creative Direction | Technical Config | Communication protocols | INFERRED 0.75 |

### Rate Limit Handling (Gemini Free Tier)

```bash
# Free tier: 250K tokens/min, ~$0.15 per full vault run
# If rate limited (429), wait ~30-60s and retry
# Or reduce concurrency:
GRAPHIFY_MAX_CONCURRENCY=1 graphify extract "/path/to/vault" --backend gemini

# Track costs
graphify extract . --timing  # prints per-stage wall-clock timings
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