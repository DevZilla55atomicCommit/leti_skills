---
title: "Graphify Export Formats Reference"
source: "Graphify repository (tools/skillgen/fragments/references/exports.md)"
version: "0.9.9"
---

# Graphify Export Formats Reference

## Available Export Commands

```bash
# All exports run from project root or with explicit --graph path

# Obsidian vault (detailed in references/obsidian-export.md)
graphify export obsidian [--dir PATH] [--graph PATH]

# HTML call-flow architecture diagram
graphify export callflow-html [--max-sections N] [--output PATH] [GRAPH_DIR]

# SVG graph visualization
graphify export svg [--graph PATH] [--output PATH]

# GraphML for Gephi / yEd
graphify export graphml [--graph PATH] [--output PATH]

# Neo4j Cypher script
graphify export neo4j [--graph PATH] [--output PATH]
graphify export neo4j-push bolt://host:7687 [--graph PATH] [--user USER] [--password PASS]

# FalkorDB Cypher script
graphify export falkordb [--graph PATH] [--output PATH]
graphify export falkordb-push falkordb://host:6379 [--graph PATH]

# Agent-crawlable wiki (markdown)
graphify export wiki [--graph PATH] [--output PATH]
```

---

## HTML Call-Flow Architecture Diagram

**Command:**
```bash
graphify export callflow-html
# Output: graphify-out/<project>-callflow.html
```

**Features:**
- Mermaid.js architecture diagrams
- Auto-regenerates on git commit if hook installed
- Sections: overview, call flows, data flows, community maps
- `--max-sections 8` caps generated sections
- Embeddable in Notion, GitHub, Confluence

---

## SVG Export

**Command:**
```bash
graphify export svg
# Requires: uv tool install "graphifyy[svg]"
# Output: graphify-out/graph.svg
```

**Features:**
- Matplotlib-based force-directed layout
- Node colors by community
- Edge width by weight
- Scalable vector - zoom without quality loss
- Embed in docs, presentations, GitHub README

---

## GraphML Export

**Command:**
```bash
graphify export graphml
# Output: graphify-out/graph.graphml
```

**Use with:**
- **Gephi** - network analysis, layout algorithms
- **yEd** - graph editor, auto-layout
- **Cytoscape** - biological networks
- **NetworkX** - `nx.read_graphml()`

---

## Neo4j Export

### Generate Cypher Script
```bash
graphify export neo4j
# Output: graphify-out/cypher.txt
```

### Push Directly to Neo4j
```bash
graphify export neo4j-push bolt://localhost:7687 \
  --user neo4j --password secret
```

**Schema:**
- Nodes: `:Concept {id, label, file_type, source_file, community}`
- Relationships: `[:RELATION {relation, confidence, confidence_score, source_file}]`
- Communities: `:Community {id, name, cohesion}`

---

## FalkorDB Export

### Generate Cypher Script
```bash
graphify export falkordb
# Output: graphify-out/cypher.txt (FalkorDB dialect)
```

### Push Directly to FalkorDB
```bash
graphify export falkordb-push falkordb://localhost:6379
```

---

## Wiki Export (Agent-Crawlable)

**Command:**
```bash
graphify export wiki
# Output: graphify-out/wiki/
```

**Structure:**
```
wiki/
├── index.md                 # Entry point with community TOC
├── community_Auth_System.md # Community overview + member links
├── community_Database.md
├── AuthModule.md            # Node page with connections
├── ...
```

**Features:**
- One markdown file per community + node
- Relative links between pages
- No wikilinks (standard markdown) - works in any viewer
- Designed for AI agents to crawl (follow links, read pages)

---

## Slash Command Flags (All Exports)

```bash
/graphify . --svg              # Also export graph.svg
/graphify . --graphml          # Also export graph.graphml
/graphify . --neo4j            # Also generate cypher.txt
/graphify . --neo4j-push URI   # Also push to Neo4j
/graphify . --falkordb         # Also generate falkordb cypher
/graphify . --falkordb-push URI # Also push to FalkorDB
/graphify . --wiki             # Also build wiki
/graphify . --callflow-html    # Also generate callflow.html
```

---

## Callflow HTML Auto-Regeneration

With git hook installed:
```bash
graphify hook install
```

On every commit:
1. Runs AST extraction on changed files (free, no API)
2. Regenerates `graphify-out/<project>-callflow.html`
3. Commits updated HTML alongside code

Result: Architecture diagram always in sync with codebase.

---

## Choosing an Export Format

| Need | Format |
|------|--------|
| Obsidian knowledge base | `--obsidian` / `export obsidian` |
| Team architecture diagram | `export callflow-html` |
| Network analysis (Gephi) | `export graphml` |
| Graph database (Neo4j) | `export neo4j-push` |
| Graph database (FalkorDB) | `export falkordb-push` |
| AI agent crawlable docs | `export wiki` |
| Publication figure | `export svg` |
| Custom analysis (Python) | Use `graph.json` directly |