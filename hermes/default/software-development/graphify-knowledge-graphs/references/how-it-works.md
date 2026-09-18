---
title: "How Graphify Works - Technical Deep Dive"
source: "Graphify repository (docs/how-it-works.md)"
version: "0.9.9"
---

# How Graphify Works - Technical Deep Dive

## The Three Passes

Graphify processes files in three distinct passes:

### Pass 1 — Code Structure (Free, No API Calls)
- **Tree-sitter AST parsing** for 36+ languages
- Extracts: classes, functions, imports, call graphs, inline comments
- Runs locally with no LLM involved
- SQL files get special treatment: tables, views, foreign keys, JOIN relationships
- Code files are **not sent to LLM** semantic extractor in normal pipeline
- If corpus is code-only, Pass 3 is skipped entirely

### Pass 2 — Video and Audio (Local, No API Calls)
- **faster-whisper** transcription
- Transcription prompt seeded with top god nodes (most-connected concepts in code graph)
- Transcripts cached - re-runs skip already-processed files

### Pass 3 — Docs, Papers, Images (LLM, Costs Tokens)
- **Claude subagents** run in parallel over markdown, PDFs, images, transcripts
- Each subagent reads batch of files → outputs JSON fragment (nodes, edges, group relationships)
- Fragments merged into single graph
- Optional converters turn pointer/binary formats → Markdown sidecars under `graphify-out/converted/`
  - Office files (`.docx`, `.xlsx`) require `[office]` extra
  - Google Workspace shortcuts (`.gdoc`, `.gsheet`, `.gslides`) opt-in with `--google-workspace` + authenticated `gws` CLI

---

## Community Detection

- **Leiden algorithm** - graph clustering by edge density
- Nodes with many connections between them end up in same community
- **No embeddings needed** - semantic similarity edges (`semantically_similar_to`) already in graph
- Graph structure IS the similarity signal - no separate embedding step or vector DB

---

## Confidence Tagging

| Tag | Meaning | Confidence Score |
|-----|---------|------------------|
| `EXTRACTED` | Found directly in source (function call, import) | 1.0 (always) |
| `INFERRED` | Reasonable deduction by Claude | 0.55-0.95 (discrete rubric) |
| `AMBIGUOUS` | Uncertain - flagged for human review | N/A |

**INFERRED confidence rubric:**
- 0.95 — near-certain (explicit cross-file reference, one plausible target)
- 0.85 — strong evidence (naming + context align)
- 0.75 — reasonable (contextual but not explicit)
- 0.65 — weak (naming similarity only)
- 0.55 — speculative

---

## Token Benchmark

| Corpus | Files | Reduction |
|--------|-------|-----------|
| Karpathy repos + papers + images | 52 | **71.5x** |
| graphify source + Transformer paper | 4 | **5.4x** |
| httpx (synthetic Python library) | 6 | ~1x |

Token reduction scales with corpus size. At 6 files, value is structural clarity, not compression.

---

## Parallel Extraction

- Code files: `ProcessPoolExecutor` - bypasses Python GIL for genuine multiprocessing
- Doc/paper/image batches: parallel Claude subagents
- 84 code files: ~1.66x speedup vs sequential

---

## SHA256 Cache

- Every extracted file fingerprinted by content hash
- Re-runs skip unchanged files entirely - only new/modified go through extraction
- Cache lives in `graphify-out/cache/`

---

## Graph Format (graph.json)

NetworkX node-link format.

**Node properties:**
- `id` - stable identifier
- `label` - human-readable name
- `file_type` - `code`, `document`, `paper`, `image`, `rationale`
- `source_file` - where it came from

**Edge properties:**
- `source`, `target` - node IDs
- `relation` - verb phrase (`calls`, `imports`, `implements`, `semantically_similar_to`)
- `confidence` - `EXTRACTED`, `INFERRED`, `AMBIGUOUS`
- `confidence_score` - float (INFERRED only)
- `source_file` - where relationship found

**Hyperedges** (group relationships 3+ nodes): `G.graph["hyperedges"]`