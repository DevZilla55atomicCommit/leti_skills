# Effective Graphify Query Patterns

## Query Types

### 1. Natural Language Questions (`graphify query`)
Broad context retrieval via BFS traversal.

```bash
graphify query "how does authentication connect to the database?"
graphify query "what connects Flux image generation to video workflows"
graphify query "show me the creative director workflow"
graphify query "trace the data flow from user input to image output"
```

**Tips:**
- Use domain terminology from your codebase
- Questions crossing community boundaries yield richest results
- Add `--dfs` for deep path tracing instead of broad context
- Use `--budget N` to cap token output (default 2000)

### 2. Path Tracing (`graphify path`)
Shortest path between two specific concepts.

```bash
graphify path "AuthManager" "DatabasePool"
graphify path "_generate()" "generate_image()"
graphify path "get_exchange_rate()" "API Design Standards"
```

**Tips:**
- Use exact node labels from `graphify explain` or GRAPH_REPORT.md
- Ambiguous matches warn: "target match was ambiguous"
- Shows hop count and edge relations

### 3. Concept Explanation (`graphify explain`)
Focused node details with all connections.

```bash
graphify explain "RateLimiter"
graphify explain "_generate()"
graphify explain "flux_wrapper.py"
```

**Output includes:**
- Node ID, source file, line number, community, degree
- All connections with relation + confidence
- Directionality (incoming/outgoing)

## Query Formulation Strategies

### Cross-Domain Discovery
```bash
# Find connections between technical domains
graphify query "what connects DaVinci color grading to photography?"
graphify query "how does forex data feed into the API layer?"
graphify query "show me Flux and storyboard integration points"
```

### Architecture Navigation
```bash
# Find god nodes (hubs)
graphify query "what are the most connected components?"

# Trace call chains
graphify query "trace the call chain from MCP tool to Ollama API"

# Find bridge nodes
graphify query "what connects the batch generation to metadata history?"
```

### Debugging & Refactoring
```bash
# Impact analysis
graphify query "what would break if I change _generate()?"
graphify path "old_function" "new_function"

# Find isolated code
graphify query "what nodes have no connections?"
```

## Advanced Patterns

### Combine with Shell
```bash
# List all communities
graphify query "list all communities" --budget 500 | grep "Community"

# Find all MCP tools
graphify query "what MCP tools are exposed?" --budget 300

# Export subgraph for documentation
graphify query "Flux generation pipeline" --budget 1000 > pipeline.md
```

### Iterative Exploration
```bash
# 1. Start broad
graphify query "image generation architecture"

# 2. Drill into interesting node
graphify explain "_generate()"

# 3. Trace specific path
graphify path "_generate()" "generate_image()"

# 4. Explore community
graphify query "what's in the Batch Image Generation community?"
```

## Interpreting Results

### Edge Confidence Tags
| Tag | Meaning | Trust Level |
|-----|---------|-------------|
| `EXTRACTED` | Explicit in source (import, call, wikilink) | 100% |
| `INFERRED` | Deduced by LLM with confidence score | 55–95% |
| `AMBIGUOUS` | Uncertain, flagged for review | Low |

### Community Cohesion
| Score | Interpretation |
|-------|----------------|
| ≥ 0.7 | Tightly connected (clear module) |
| 0.4–0.7 | Moderately connected |
| < 0.4 | Loosely connected (may need refactoring) |

### God Nodes (High Betweenness)
Nodes that bridge communities — changing them has wide impact.
Look for: "High betweenness centrality" in GRAPH_REPORT.md

## Common Query Failures & Fixes

| Problem | Fix |
|---------|-----|
| "No path found" | Concepts in disconnected components; check spelling with `graphify explain` |
| Too many results | Add `--budget 500` or use `--dfs` for focused trace |
| Irrelevant results | Use more specific domain terms; check GRAPH_REPORT.md for vocabulary |
| "Ambiguous match" | Use exact label from `graphify explain` output |

## Vocabulary Expansion

Graphify expands queries against graph vocabulary automatically. If results are poor:
1. Check GRAPH_REPORT.md "Community Hubs" for terminology
2. Run `graphify explain` on a known node to get exact labels
3. Try synonyms from your domain (e.g., "MCP tool" vs "Hermes tool")