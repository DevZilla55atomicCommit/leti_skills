---
title: "Graphify Extraction Specification"
source: "Graphify repository (tools/skillgen/fragments/references/extraction-spec.md)"
version: "0.9.9"
---

# Graphify Extraction Specification

## Subagent Prompt Template

This is the exact prompt dispatched to each semantic extraction subagent. Load only when at least one chunk holds a doc, paper, or image.

---

## JSON Schema for Subagent Output

```json
{
  "nodes": [
    {
      "id": "unique_stable_string",
      "label": "Human Readable Name",
      "source_file": "relative/path/to/file.md",
      "source_location": "L42-L55 or heading",
      "file_type": "document|paper|image|rationale",
      "metadata": {
        "section": "optional section name",
        "page": "optional page number"
      }
    }
  ],
  "edges": [
    {
      "source": "node_id_a",
      "target": "node_id_b",
      "relation": "calls|imports|uses|references|implements|extends|semantically_similar_to|...",
      "confidence": "EXTRACTED|INFERRED|AMBIGUOUS",
      "confidence_score": 0.85,
      "source_file": "relative/path/to/file.md"
    }
  ],
  "hyperedges": [
    {
      "nodes": ["node_id_a", "node_id_b", "node_id_c"],
      "relation": "group|pattern|workflow",
      "description": "These three nodes form a retry pattern",
      "confidence": "INFERRED",
      "confidence_score": 0.80
    }
  ],
  "input_tokens": 1234,
  "output_tokens": 567
}
```

---

## Node ID Rules

1. **Deterministic** - same entity always gets same ID across runs
2. **Format**: `<type>:<namespace>::<name>` or `<file>::<symbol>`
3. **Examples**:
   - `code:python::AuthModule`
   - `document::README.md::Installation`
   - `paper:arxiv::1706.03762::Attention`
   - `image::architecture.png::Diagram`

4. **Code nodes** (from AST): use fully qualified names
5. **Document nodes**: use file path + heading/section
6. **Paper nodes**: use DOI/arXiv ID + section
7. **Image nodes**: use file path + visual element description

---

## Confidence Rubric

### EXTRACTED (confidence_score: 1.0)
- Direct syntactic evidence in source
- Import statements, function calls, class inheritance
- Explicit markdown links `[[wikilink]]` or `[text](./file.md)`
- Explicit citations in papers

### INFERRED (confidence_score: 0.55-0.95)
- **0.95** - Near-certain: explicit cross-file reference, one plausible target
- **0.85** - Strong: naming + context align (e.g., `UserService` calls `UserRepository`)
- **0.75** - Reasonable: contextual but not explicit
- **0.65** - Weak: naming similarity only
- **0.55** - Speculative: tenuous connection

### AMBIGUOUS (no score)
- Multiple equally plausible targets
- Contradictory evidence
- Flagged in GRAPH_REPORT.md for human review

---

## Frontmatter Extraction

For markdown files, extract YAML frontmatter as node metadata:
```yaml
---
title: "API Reference"
tags: [api, reference]
date: 2024-01-15
---
```

Becomes node metadata: `{ "title": "API Reference", "tags": ["api", "reference"], "date": "2024-01-15" }`

---

## Hyperedge Rules

Hyperedges connect 3+ nodes representing:
- **Group**: Nodes that form a conceptual unit (e.g., "Auth Flow" = Login + Token + Refresh)
- **Pattern**: Repeated structural pattern (e.g., "Retry Pattern" = Try + Catch + Backoff)
- **Workflow**: Sequential process (e.g., "Data Pipeline" = Extract → Transform → Load)

Each hyperedge must have a clear `description` explaining the grouping.

---

## Vision Rules (Images)

For images (PNG, JPG, WebP, GIF):
1. Describe what the image shows (architecture diagram, UI mockup, chart, etc.)
2. Extract any text visible in image (OCR)
3. Identify labeled components and their relationships
4. Create nodes for each significant visual element
5. Edge relations: `contains`, `shows`, `depicts`, `illustrates`

---

## Chunk Processing

- Chunk size: 20-25 files
- Each image gets its own chunk (vision needs separate context)
- Group files from same directory together (related artifacts → same chunk)
- Subagent writes result to `CHUNK_PATH` (absolute path)

---

## Cache Integration

Before subagent dispatch:
1. Run `check_semantic_cache(all_files, root)` → returns `(cached_nodes, cached_edges, cached_hyperedges, uncached_files)`
2. Only dispatch subagents for `uncached_files`
3. After subagent completes, run `save_semantic_cache(new_nodes, new_edges, new_hyperedges, root)`

Cache keyed by file content SHA256 - re-runs skip unchanged files.