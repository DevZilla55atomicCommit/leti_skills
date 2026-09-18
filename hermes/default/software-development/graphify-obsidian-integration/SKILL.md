---
name: graphify-obsidian-integration
description: Create queryable knowledge graphs from codebases and Obsidian vaults using Graphify, with automatic Obsidian export for interactive exploration via Graph View, Canvas, and Dataview.
---

# Graphify + Obsidian Integration Workflow

Graphify transforms any folder (code, docs, markdown, PDFs, images, videos) into a knowledge graph with community detection, god nodes, and confidence-tagged edges. This skill covers the end-to-end workflow for building graphs and exporting them to Obsidian for visual exploration.

## Prerequisites

- Python 3.10+
- `uv` (recommended) or `pipx`
- Obsidian vault path
- **For markdown/docs/PDFs/images**: LLM API key (Gemini, Anthropic, OpenAI, Ollama, etc.)

## Installation

```bash
# Install Graphify CLI
uv tool install graphifyy
uv tool update-shell  # adds ~/.local/bin to PATH

# Register with Hermes Agent
graphify hermes install
# Writes: ~/.hermes/skills/graphify/SKILL.md and project AGENTS.md
```

## Quick Start: Code-Only Graph (Free, No API Key)

```bash
cd /path/to/project
graphify . --obsidian --obsidian-dir "/path/to/vault/Graphify-ProjectName"
```

- Uses tree-sitter AST extraction only (36 languages)
- No LLM calls, no API key needed
- Instant for most codebases

## Full Vault Graph (Needs LLM API Key)

```bash
# Set API key (Gemini free tier works)
export GEMINI_API_KEY="your-key-from-ai.google.dev"

# Process entire Obsidian vault
graphify "/path/to/vault" --obsidian --obsidian-dir "/path/to/vault/Graphify-FullVault"

# Or process a subfolder (e.g., DaVinci knowledge base)
graphify "/path/to/vault/Hermes Agent/DaVinci_Knowledge_Base" \
  --obsidian --obsidian-dir "/path/to/vault/Graphify-DaVinci"
```

## Hybrid: Text-Only + Image References (For Large Media Vaults)

When your vault contains **large media files (GIFs >5 MB, many images)** that exceed vision API rate limits, use the hybrid strategy:

```bash
# Skip ALL images from vision queue; process text/markdown/code fully
graphify "/path/to/vault" \
  --backend openai \
  --model "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning" \
  --obsidian \
  --obsidian-dir "/path/to/vault/Graphify-FullVault" \
  --ignore "*.gif" --ignore "*.jpg" --ignore "*.jpeg" --ignore "*.png" --ignore "*.webp" \
  --ignore ".vault-organizer-backups/**"  # Skip Syncthing conflict copies
```

| Content | In Graph? | Extraction |
|---------|-----------|------------|
| Markdown/notes/docs | ✅ Full | Semantic LLM |
| Code (Python, JS, etc.) | ✅ Full | AST + Semantic |
| PDFs | ✅ Full | Text + LLM |
| **Image files** | ✅ Reference nodes only | **None (skipped)** |
| Vision analysis | ❌ | N/A |

**Time**: ~20–30 min vs 100+ hours for full vision on 200K+ large images.

See `references/hybrid-text-reference-strategy.md` for details.

## Using NVIDIA NIM (Best Quality)

NVIDIA NIM exposes an OpenAI-compatible API. Use the `openai` backend with NVIDIA's endpoint:

```bash
# Get API key from https://build.nvidia.com → API Keys
export NVIDIA_API_KEY="nvapi-..."
export OPENAI_BASE_URL="https://integrate.api.nvidia.com/v1"
export OPENAI_API_KEY="$NVIDIA_API_KEY"
export OPENAI_MODEL="nvidia/nemotron-3-ultra-550b-a55b"  # Best quality: 550B MoE (TEXT ONLY)

# Build with Nemotron 3 Ultra (TEXT-ONLY vaults)
graphify "/path/to/vault" \
  --backend openai \
  --model "nvidia/nemotron-3-ultra-550b-a55b" \
  --obsidian --obsidian-dir "/path/to/vault/Graphify-FullVault"
```

### NVIDIA Cloud Model Tier List

| Model | Params | Vision? | Best For |
|-------|--------|---------|----------|
| **`nvidia/nemotron-3-ultra-550b-a55b`** | 550B MoE | ❌ NO | **Best text quality** — extraction, naming, reasoning (text-only vaults) |
| `nvidia/nemotron-3-super-120b-a12b` | 120B MoE | ❌ NO | Great text quality, faster/cheaper |
| `nvidia/llama-3.1-nemotron-70b-instruct` | 70B | ❌ NO | Solid general text |
| **`nvidia/nemotron-3-nano-omni-30b-a3b-reasoning`** | 30B | ✅ YES | **Images + text** — only Nemotron with vision |
| **`meta/llama-3.2-90b-vision-instruct`** | 90B | ✅ YES | **Images + text** — largest vision model |
| `meta/llama-3.2-11b-vision-instruct` | 11B | ✅ YES | Lightweight vision |

> ⚠️ **Critical**: If your vault contains images, GIFs, or PDFs, you MUST use a vision-capable model (✅ YES above). Text-only models (Nemotron 3 Ultra/Super, Nemotron 70B) will fail on every image chunk with `400: multimodal processing not enabled` errors. The error mentions "--enable-multimodal flag" — THIS FLAG DOES NOT EXIST; it's a model capability.

> **Large GIFs (>5 MB)**: Even with vision models, Graphify auto-skips inline vision for files >5 MB — they become reference nodes only. The TamaZila vault has GIFs 10–100 MB. For full frame analysis, extract key frames as <5 MB JPGs before indexing.

### Local NIM (Self-Hosted)

```bash
# Start local NIM container
docker run -d --gpus all -p 8000:8000 nvcr.io/nim/meta/llama-3.1-70b-instruct

# Point Graphify at local endpoint
export OPENAI_BASE_URL="http://localhost:8000/v1"
export OPENAI_API_KEY="local-key"  # NIM accepts any non-empty string
export OPENAI_MODEL="meta/llama-3.1-70b-instruct"

graphify "/path/to/vault" --backend openai --model "$OPENAI_MODEL" --obsidian --obsidian-dir "..."
```

> **For local vision**: Deploy `nvcr.io/nim/meta/llama-3.2-90b-vision-instruct` or `nvcr.io/nim/nvidia/nemotron-3-nano-omni-30b-a3b-reasoning`.

## TamaZila Vault: Dual Graphs — Use the Right One

The TamaZila Obsidian Vault has two separate Graphify outputs:

| Graph | Location | Contents | Use For |
|-------|----------|----------|---------|
| **Full Vault Graph** (canonical) | `/Volumes/PNY128GBLED/TamaZila Obsidian Vault/Hermes Agent/graphify-out/` | DaVinci KB, Forex, Dev Workflows, Hermes Agent, Projects, Photography — **~98KB, fully queryable** | **All production queries** |
| **Code-Only Graph** (stale test) | `~/TamaZila_Obsidian_Vault/Graphify-CodeOnly/.obsidian/graph.json` | Color groups only, ~23 bytes — **near-empty** | **Ignore** |

```bash
# Query the FULL graph (preferred)
graphify query "question" --graph "/Volumes/PNY128GBLED/TamaZila Obsidian Vault/Hermes Agent/graphify-out/graph.json"

# Via symlink (also works)
graphify query "question" --graph "~/TamaZila_Obsidian_Vault/Hermes Agent/graphify-out/graph.json"
```

> **Note**: The `--graph` flag takes the direct path to `graph.json`. The `--root` flag is for the extraction source directory, not the graph file.

> The symlink `~/TamaZila_Obsidian_Vault` → `/Volumes/PNY128GBLED/TamaZila Obsidian Vault/` is valid.

## Filtering with `.graphifyignore`

Create in the scan root to exclude files (same syntax as `.gitignore`):

```gitignore
# Ignore all markdown for code-only graph
*.md
*.txt
*.pdf

# Ignore vault config
.obsidian/
Graphify-*/

# Ignore system files
.DS_Store
theme.css
```

## Incremental Updates

```bash
# After code changes (free, AST only)
graphify update .

# After docs/markdown changes (needs API key)
graphify . --update

# Re-cluster without re-extracting
graphify cluster-only .
```

## Querying the Graph

```bash
# Natural language question (BFS traversal)
graphify query "how does auth connect to database?" --graph "/Volumes/PNY128GBLED/TamaZila Obsidian Vault/Hermes Agent/graphify-out/graph.json"

# Shortest path between two concepts
graphify path "AuthManager" "DatabasePool" --graph "/Volumes/PNY128GBLED/TamaZila Obsidian Vault/Hermes Agent/graphify-out/graph.json"

# Explain a single concept
graphify explain "RateLimiter" --graph "/Volumes/PNY128GBLED/TamaZila Obsidian Vault/Hermes Agent/graphify-out/graph.json"
```

## What the Obsidian Export Creates

```
/path/to/vault/Graphify-Project/
├── <ConceptName>.md              # One note per node with wikilinks
├── _COMMUNITY_<Name>.md          # Community overview (members, cohesion, bridges)
├── graph.canvas                  # Visual canvas: communities as groups, nodes as cards
├── .obsidian/graph.json          # Auto-colors Graph View by community
└── .graphify_obsidian_manifest.json  # Protection: never overwrites your notes
```

### Node Note Contents
- YAML frontmatter: `source_file`, `type`, `community`, `location`, `tags`
- `## Connections` — wikilinks to related nodes with relation + confidence
- Inline `#tags` for Obsidian tag panel

### Community Note Contents
- Members list as wikilinks
- Cohesion score (0–1)
- Dataview live query (requires Dataview plugin)
- Cross-community connections
- Top bridge nodes (highest degree + cross-community reach)

## Common Pitfalls & Fixes

| Issue | Fix |
|-------|-----|
| `graphify: command not found` | Run `uv tool update-shell` and restart shell |
| `429 quota exceeded` (Gemini free tier) | Wait 30–60s, or use `--max-concurrency 1`, or add billing |
| `no LLM API key found` | Set `GEMINI_API_KEY` or `GOOGLE_API_KEY`, or use `--backend ollama` |
| Ollama 404 errors | Ensure model supports `/api/generate` (try `qwen3.5:9b` not MLX variants) |
| Graph has fewer nodes after `--update` | Re-run with `--force` flag to overwrite |
| HTML too large (>5000 nodes) | Use `--no-viz` or query via `graphify query` instead |
| `error: graph file not found: ~/graphify-out/graph.json` | The graph is NOT at `~/graphify-out/`. Use `--graph "/Volumes/PNY128GBLED/TamaZila Obsidian Vault/Hermes Agent/graphify-out/graph.json"` |
| `error: could not load graph: 'nodes'` | The `.obsidian/graph.json` only has colorGroups. Point `--graph` to the real `graphify-out/graph.json` in the Hermes Agent folder |
| `ValueError: Received multimodal data but multimodal processing is not enabled` | **Model lacks vision**. Use `nvidia/nemotron-3-nano-omni-30b-a3b-reasoning` or `meta/llama-3.2-90b-vision-instruct`. The "--enable-multimodal flag" mentioned in error DOES NOT EXIST — it's a model capability. |
| Large images/GIFs skipped | Log: "over the 5 MB inline-image limit — sending as reference node without inline pixels." Files >5 MB are NOT vision-analyzed. Pre-process large GIFs (extract key frames, compress) before indexing. |

## Large Media Files in TamaZila Vault

The DaVinci Knowledge Base contains **large GIF files (10–70 MB)** from Instagram Reels frame extraction. These exceed the 5 MB inline vision limit:

```bash
# Example from logs:
# image .../CvUV6P0sIiZ.gif is 70645 KB — sent as reference node only
# image .../CzXyM1er54w.gif is 100290 KB — sent as reference node only
```

**Impact**: These files become graph nodes with `source_file` metadata but no visual analysis.

**Workarounds**:
1. **Pre-process**: Extract 1–3 key frames per GIF as <5 MB JPGs before indexing
2. **Accept reference-only**: Graph still links them via filename/wikilinks — useful for navigation
3. **Separate vision pass**: Run a dedicated vision pipeline on extracted frames, merge results later

## Cross-Domain Discovery

When run on a full vault, Graphify automatically connects:
- **Wikilinks** → `references` edges
- **Shared terminology** → `semantically_similar_to` (INFERRED)
- **Code ↔ Docs** → `imports` / `contains` / `references` edges

Example discoveries in a creative/technical vault:
- DaVinci color grading ↔ Photography (color science, LUTs)
- Forex scripts ↔ API standards (shared patterns)
- Flux generation ↔ Storyboard agents (both image pipelines)

## Hermes Agent Integration

After `graphify hermes install`, Hermes will:
1. Check `graphify-out/graph.json` exists before answering codebase questions
2. Prefer `graphify query` over reading raw files
3. Use `graphify update .` after code changes (via AGENTS.md rules)

## MCP Server for Team Access

```bash
# Local stdio (for your AI assistant)
python -m graphify.serve graphify-out/graph.json

# HTTP server (shared team access)
python -m graphify.serve graphify-out/graph.json \
  --transport http --host 0.0.0.0 --port 8080 --api-key "$SECRET"
```

Provides tools: `query_graph`, `get_node`, `get_neighbors`, `shortest_path`, `list_prs`, `get_pr_impact`, `triage_prs`.

## References

- `references/obsidian-export-details.md` — detailed export structure
- `references/query-patterns.md` — effective query formulations
- `references/troubleshooting.md` — common errors and fixes
- `references/nvidia-nim-setup.md` — NVIDIA NIM cloud/local model setup
- `references/hybrid-text-reference-strategy.md` — text-only + image refs for large media vaults