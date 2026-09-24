---
title: Processing Entire Obsidian Vaults with Graphify
---

# Obsidian Vault Processing Patterns

## Understanding the Corpus Types

| File Type | Graphify Classification | Extraction Method | API Key Required |
|-----------|------------------------|-------------------|------------------|
| `.py`, `.js`, `.ts`, `.go`, `.rs`, etc. | **code** | Tree-sitter AST (deterministic) | ❌ No |
| `.md`, `.txt`, `.rst` | **document** | Semantic LLM extraction | ✅ Yes |
| `.pdf` | **paper** | Semantic LLM + PDF parsing | ✅ Yes |
| `.png`, `.jpg`, `.webp` | **image** | Vision LLM | ✅ Yes |
| `.mp4`, `.mov`, `.mp3` | **video** | Whisper transcription + LLM | ✅ Yes (or local faster-whisper) |

## Code-Only Extraction (Free)

For vaults with mixed content where you only want code relationships:

```bash
# Create .graphifyignore in vault root
cat > /path/to/vault/.graphifyignore << 'EOF'
# Skip all markdown/docs
*.md
*.mdx
*.txt
*.pdf

# Skip Obsidian config
.obsidian/

# Skip Graphify's own outputs
Graphify-*/
graphify-out/

# Skip Python venvs
**/venv/**
**/__pycache__/**

# Skip Node modules
**/node_modules/**
EOF

# Run code-only extraction
graphify "/path/to/vault" --no-cluster --obsidian --obsidian-dir "/path/to/vault/Graphify-CodeOnly"
```

**Result**: Only code files (Python, JS, etc.) are extracted. Wikilinks in markdown are ignored.

## Full Vault Extraction (Requires LLM)

For semantic extraction of markdown notes, wikilinks, and cross-references:

```bash
# Option A: Use Gemini from Hermes config
export GEMINI_API_KEY="$(grep -A2 'google-gemini:' ~/.hermes/config.yaml | grep 'api_key:' | cut -d'\"' -f2)"

graphify "/path/to/vault" \
  --obsidian \
  --obsidian-dir "/path/to/vault/Graphify-FullVault" \
  --mode deep
```

```bash
# Option B: NVIDIA NIM (Best Quality - Nemotron 3 Ultra 550B MoE)
export NVIDIA_API_KEY="nvapi-..."  # from https://build.nvidia.com
export OPENAI_BASE_URL="https://integrate.api.nvidia.com/v1"
export OPENAI_API_KEY="$NVIDIA_API_KEY"
export OPENAI_MODEL="nvidia/nemotron-3-ultra-550b-a55b"

graphify "/path/to/vault" \
  --backend openai \
  --model "$OPENAI_MODEL" \
  --obsidian \
  --obsidian-dir "/path/to/vault/Graphify-FullVault" \
  --mode deep
```

**Cost estimate**: ~200-500 .md files ≈ 300K-500K input tokens ≈ $0.15-0.30 with Gemini Flash (NVIDIA Cloud free tier available)

## Selective Folder Extraction

Process only specific domains from your vault:

```bash
# Only DaVinci color grading knowledge base
graphify "/path/to/vault/Hermes Agent/DaVinci_Knowledge_Base" \
  --obsidian \
  --obsidian-dir "/path/to/vault/Graphify-DaVinci"

# Only Forex analysis
graphify "/path/to/vault/Hermes Agent/Forex Center" \
  --obsidian \
  --obsidian-dir "/path/to/vault/Graphify-Forex"

# Only Photography notes
graphify "/path/to/vault/Hermes Agent/Photography" \
  --obsidian \
  --obsidian-dir "/path/to/vault/Graphify-Photography"
```

## Cross-Domain Graph Merging

Build separate graphs then merge:

```bash
# Build each domain
graphify "/path/to/vault/Hermes Agent/DaVinci_Knowledge_Base" --no-viz
graphify "/path/to/vault/Hermes Agent/Forex Center" --no-viz
graphify "/path/to/vault/Hermes Agent/Photography" --no-viz

# Merge into unified graph
graphify merge-graphs \
  "/path/to/vault/Hermes Agent/DaVinci_Knowledge_Base/graphify-out/graph.json" \
  "/path/to/vault/Hermes Agent/Forex Center/graphify-out/graph.json" \
  "/path/to/vault/Hermes Agent/Photography/graphify-out/graph.json" \
  --out "/path/to/vault/Graphify-Unified/graph.json"
```

## Wikilink Handling

Graphify automatically converts Obsidian wikilinks to `references` edges:

```markdown
# In your vault notes:
See [[DaVinci Resolve Color Management]] for details.
Related: [[Sony Portrait Settings]] and [[Color Warper Tool]].
```

Becomes edges:
```
Note_A --references [EXTRACTED]--> DaVinci Resolve Color Management
Note_A --references [EXTRACTED]--> Sony Portrait Settings
Note_A --references [EXTRACTED]--> Color Warper Tool
```

## Incremental Updates for Vaults

```bash
# After adding/editing notes, re-extract only changed files
graphify update "/path/to/vault" --update

# Re-cluster without re-extracting (fast)
graphify cluster-only "/path/to/vault"
```

## Common Pitfalls

| Issue | Cause | Fix |
|-------|-------|-----|
| "no LLM API key found" | .md files need semantic extraction | Set `GEMINI_API_KEY` or use `--backend ollama` |
| Rate limited (429) | Free tier quota exceeded | Wait, upgrade plan, or use `--max-concurrency 1` |
| Graph too sparse | Too many isolated nodes | Add more wikilinks; use `--mode deep` for richer INFERRED edges |
| Duplicate nodes | Re-extraction without cache clear | Run `graphify extract . --force` |
| Obsidian graph.json not updating | Manifest blocks overwrite | Delete `.graphify_obsidian_manifest.json` or export to new folder |

## TamaZila Vault: Exact Commands

```bash
# Option A: Export API key from Hermes config (Gemini)
export GEMINI_API_KEY="$(grep -A2 'google-gemini:' ~/.hermes/config.yaml | grep 'api_key:' | cut -d'\"' -f2)"

# Option B: NVIDIA NIM (Best Quality - Nemotron 3 Ultra 550B)
export NVIDIA_API_KEY="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"
export OPENAI_BASE_URL="https://integrate.api.nvidia.com/v1"
export OPENAI_API_KEY="$NVIDIA_API_KEY"
export OPENAI_MODEL="nvidia/nemotron-3-ultra-550b-a55b"

# 1. Code-only vault map (free, no API key)
cat > .graphifyignore << 'EOF'
*.md; *.txt; *.pdf; .obsidian/; Graphify-*/; graphify-out/; **/venv/**; **/node_modules/**
EOF
graphify "/Users/alfredkamisese/TamaZila Obsidian Vault" \
  --obsidian --obsidian-dir "/Users/alfredkamisese/TamaZila Obsidian Vault/Graphify-CodeOnly"

# 2. DaVinci Knowledge Base (color grading focus)
graphify "/Users/alfredkamisese/TamaZila Obsidian Vault/Hermes Agent/DaVinci_Knowledge_Base" \
  --obsidian --obsidian-dir "/Users/alfredkamisese/TamaZila Obsidian Vault/Graphify-DaVinci"

# 3. Forex Analysis
graphify "/Users/alfredkamisese/TamaZila Obsidian Vault/Hermes Agent/Forex Center" \
  --obsidian --obsidian-dir "/Users/alfredkamisese/TamaZila Obsidian Vault/Graphify-Forex"

# 4. Photography
graphify "/Users/alfredkamisese/TamaZila Obsidian Vault/Hermes Agent/Photography" \
  --obsidian --obsidian-dir "/Users/alfredkamisese/TamaZila Obsidian Vault/Graphify-Photography"

# 5. Full vault cross-domain with Nemotron 3 Ultra (best quality)
graphify "/Users/alfredkamisese/TamaZila Obsidian Vault" \
  --backend openai \
  --model "$OPENAI_MODEL" \
  --obsidian --obsidian-dir "/Users/alfredkamisese/TamaZila Obsidian Vault/Graphify-FullVault"

# 6. Full vault cross-domain with Gemini (alternative)
# export GEMINI_API_KEY="..."
# graphify "/Users/alfredkamisese/TamaZila Obsidian Vault" \
#   --obsidian --obsidian-dir "/Users/alfredkamisese/TamaZila Obsidian Vault/Graphify-FullVault"

# 7. Flux scripts subproject
graphify "/Users/alfredkamisese/TamaZila Obsidian Vault/Hermes Agent/Hermes Image Generates" \
  --obsidian --obsidian-dir "/Users/alfredkamisese/TamaZila Obsidian Vault/Graphify-FluxScripts"
```

## Incremental Maintenance

```bash
# After code changes (free)
graphify update "/Users/alfredkamisese/TamaZila Obsidian Vault"

# After note changes (uses API)
graphify update "/Users/alfredkamisese/TamaZila Obsidian Vault" --update

# Re-cluster only (fast, no extraction)
graphify cluster-only "/Users/alfredkamisese/TamaZila Obsidian Vault"
```

## Opening in Obsidian

```bash
# Open any generated vault
open -a Obsidian "/Users/alfredkamisese/TamaZila Obsidian Vault/Graphify-FullVault"

# Graph View: Cmd+G → shows community colors automatically
# Canvas: Open graph.canvas → drag communities, see cross-links
# Search: Cmd+Shift+F → full-text across all graph metadata
```