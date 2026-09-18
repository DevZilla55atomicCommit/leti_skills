---
title: Graphify Integration with Mnemo Cortex
description: How Graphify knowledge graphs fit into the three-layer memory architecture
---

# Graphify + Mnemo Cortex Integration

## Where Graphify Fits in the Three Layers

| Mnemo Layer | Graphify Role | Output Location |
|-------------|---------------|-----------------|
| **Raw (Source of Truth)** | Graphify extraction artifacts | `graphify-out/` in project root |
| **Compiled (Wiki Layer)** | Obsidian vault export + community overviews | `Graphify-<Project>/` in TamaZila Vault |
| **Active (Brain Files)** | Live queries, path tracing, GRAPH_REPORT.md | Session context + `graphify query` |

## Integration Patterns

### Pattern 1: Project Onboarding → Compiled Knowledge
```
1. cd /project
2. /graphify . --obsidian --obsidian-dir "~/TamaZila Vault/Graphify-Project"
3. Result: Compiled knowledge base with wikilinks, communities, canvas
4. Use: Navigate via Graph View, Canvas, or Dataview queries
```

### Pattern 2: Cross-Domain Discovery → Raw Facts
```
1. /graphify query "how does X connect to Y?"
2. Result: Scoped subgraph with EXTRACTED/INFERRED edges
3. Action: Capture surprising connections as Raw facts in mnemo-cortex/
```

### Pattern 3: Active Work → Query Instead of Grep
```
Instead of: grep -r "AuthManager" src/
Use: /graphify query "what calls AuthManager?"
Result: Scoped subgraph with source locations, edge types, confidence tags
```

## Vault Organization for Graphify Projects

```
TamaZila Obsidian Vault/
├── Graphify-CodeOnly/           # Code architecture maps (free, no API)
├── Graphify-DaVinci/            # Color grading knowledge base
├── Graphify-Forex/              # Trading analysis graphs
├── Graphify-FluxScripts/        # AI image generation pipeline
├── Graphify-FullVault/          # Cross-domain discovery map
├── Graphify-HermesAgent/        # Hermes config + scripts
└── mnemo-cortex/                # Raw facts captured from graph queries
```

## Capturing Graph Insights as Raw Facts

When a graph query reveals something valuable:

```bash
# Example: "Graphify found that _generate() bridges 3 communities in Flux pipeline"
# Capture in mnemo-cortex:
echo "# Flux Pipeline Bridge Node
- Node: _generate()
- File: flux_wrapper.py:L37
- Bridges: Batch Gen → Metadata, Flux API, MCP Tools
- Centrality: 0.111 (highest in subgraph)
- Discovered: $(date -I)" > "mnemo-cortex/flux-pipeline-bridge-node.md"
```

## Recurring Maintenance as Active Context

Add to your session startup (Brain File):

```markdown
## Graphify Maintenance
- [ ] Check `graphify update .` for code changes (free)
- [ ] Check `graphify update . --update` for doc changes (uses API)
- [ ] Review GRAPH_REPORT.md for new "Surprising Connections"
- [ ] Run `graphify cluster-only . --resolution 1.5` quarterly for finer communities
```

## Cost-Aware Layer Assignment

| Graphify Operation | Mnemo Layer | API Cost | Frequency |
|--------------------|-------------|----------|-----------|
| AST extraction (code) | Raw | $0 | On every code change |
| Semantic extraction (docs) | Compiled | ~$0.15/vault | On note updates |
| Obsidian export | Compiled | $0 | After extraction |
| Query/path/explain | Active | $0 | Per question |
| Incremental update (--update) | Raw/Compiled | Proportional | As needed |

## TamaZila-Specific Commands

```bash
export GEMINI_API_KEY="$(grep -A2 'google-gemini:' ~/.hermes/config.yaml | grep 'api_key:' | cut -d'\"' -f2)"

# Quick vault map (code only, free)
alias graphify-code='cd "/Users/alfredkamisese/TamaZila Obsidian Vault" && graphify . --obsidian --obsidian-dir "/Users/alfredkamisese/TamaZila Obsidian Vault/Graphify-CodeOnly"'

# Full cross-domain (uses API)
alias graphify-full='cd "/Users/alfredkamisese/TamaZila Obsidian Vault" && GEMINI_API_KEY=$GEMINI_API_KEY graphify . --obsidian --obsidian-dir "/Users/alfredkamisese/TamaZila Obsidian Vault/Graphify-FullVault"'

# Query helper
gq() { cd "/Users/alfredkamisese/TamaZila Obsidian Vault" && graphify query "$*"; }
gp() { cd "/Users/alfredkamisese/TamaZila Obsidian Vault" && graphify path "$1" "$2"; }
ge() { cd "/Users/alfredkamisese/TamaZila Obsidian Vault" && graphify explain "$1"; }
```