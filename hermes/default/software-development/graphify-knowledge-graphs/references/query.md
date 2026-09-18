---
title: "Graphify Query Reference"
source: "Graphify repository (tools/skillgen/fragments/references/query.md)"
version: "0.9.9"
---

# Graphify Query Reference

## Query Modes

### BFS (Default) - Broad Context
```bash
/graphify query "how does auth connect to database?"
```
- Breadth-first traversal from seed nodes
- Returns broad subgraph around the question
- Best for "what connects X to Y?" or "overview of Z"

### DFS - Trace Specific Path
```bash
/graphify query "auth flow" --dfs
```
- Depth-first traversal
- Follows one path deeply
- Best for "trace the flow through X"

### Budget Cap
```bash
/graphify query "data flow" --budget 1500
```
- Caps answer at N tokens
- Prevents overwhelming context

---

## Vocabulary Expansion

Before traversal, the question is expanded against the graph's own vocabulary:
1. Extract key terms from question
2. Find matching node labels (fuzzy match via rapidfuzz)
3. Expand to synonyms/aliases in graph
4. Use expanded terms as BFS/DFS seeds

This prevents wording mismatch collapsing answer to noise.

---

## CLI Commands

### graphify query
```bash
graphify query "question"                    # BFS
graphify query "question" --dfs              # DFS
graphify query "question" --budget 1500      # Token cap
graphify query "question" --graph path/to/graph.json  # Custom graph
```

### graphify path
```bash
graphify path "NodeA" "NodeB"
# Shortest path between two concepts
# Output: A --relation--> B --relation--> C
```

### graphify explain
```bash
graphify explain "NodeName"
# Plain-language explanation of a node
# Shows: source file, community, degree, connections
```

---

## NetworkX Fallback (if CLI unavailable)

```python
import networkx as nx
import json

with open("graphify-out/graph.json") as f:
    data = json.load(f)

G = nx.node_link_graph(data)

# BFS query
def bfs_query(G, question, budget=1500):
    # Expand question to seed nodes
    seeds = expand_question(question, G)
    
    # BFS from seeds
    subgraph_nodes = set()
    for seed in seeds:
        if seed in G:
            subgraph_nodes.update(nx.bfs_tree(G, seed, depth_limit=2).nodes())
    
    # Build answer from subgraph
    return format_subgraph(G.subgraph(subgraph_nodes), budget)
```

---

## save-result Feedback Loop

Record how a Q&A turned out for learning:

```bash
graphify save-result \
  --question "How does auth work?" \
  --answer "AuthModule calls TokenService..." \
  --nodes AuthModule TokenService \
  --outcome useful  # useful|dead_end|corrected
```

### reflect - Aggregate Lessons
```bash
graphify reflect                    # Write to reflections/LESSONS.md
graphify reflect --if-stale         # No-op if LESSONS.md is fresh
graphify reflect --out docs/LESSONS.md
graphify reflect --graph graphify-out/graph.json
# Groups lessons by community, writes .graphify_learning.json overlay
# Overlay tags nodes: preferred/tentative/contested (recency-weighted)
# graphify explain/query then show "Lesson:" hint
```

---

## Answer Format

Query answers should:
1. Use ONLY what graph output contains
2. Quote `source_location` when citing specific facts
3. Reference confidence tags: `[EXTRACTED]`, `[INFERRED]`, `[AMBIGUOUS]`
4. Show community boundaries crossed
5. End with natural follow-up: "this connects to X - want to go deeper?"

---

## Hermes Agent Integration

In Hermes, the skill handles `/graphify query "..."` automatically:
1. Checks `graphify-out/graph.json` exists
2. Runs `graphify query "..."` via CLI
3. Formats response with graph structure
4. Offers follow-up exploration

The skill prompt includes the full query workflow from `references/query.md`.