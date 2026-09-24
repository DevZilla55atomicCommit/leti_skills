---
title: "Graphify Update & Cluster-Only Workflows"
source: "Graphify repository (tools/skillgen/fragments/references/update.md)"
version: "0.9.9"
---

# Graphify Update & Cluster-Only Workflows

## --update: Incremental Re-extraction

Re-extracts only new or changed files since last run. Uses manifest for change detection.

### How It Works

1. **Manifest comparison**: Reads `graphify-out/.graphify_manifest.json` (saved at end of full build)
2. **Detect changes**: Compares current file hashes vs manifest
3. **Extract delta**: Runs Pass 1 (AST) + Pass 3 (semantic) only on changed files
4. **Merge**: Combines new extractions with cached unchanged extractions
5. **Rebuild graph**: Full graph rebuild from merged extractions
6. **Re-cluster**: Runs Leiden clustering on updated graph

### Usage

```bash
# Basic incremental update
/graphify . --update

# With deep mode for richer extraction on changes
/graphify . --update --mode deep

# Force overwrite even if graph shrinks
/graphify . --update --force
```

### Manifest Format

```json
{
  "files": {
    "code": { "src/auth.py": "sha256:abc123...", ... },
    "document": { "docs/api.md": "sha256:def456...", ... },
    "paper": { "papers/attention.pdf": "sha256:ghi789...", ... },
    "image": { "diagrams/arch.png": "sha256:jkl012...", ... },
    "video": { "recordings/demo.mp4": "sha256:mno345...", ... }
  },
  "scan_root": "/absolute/path/to/project"
}
```

Keys are relativized to `scan_root` for portability across machines/clones.

### When to Use --update

- ✅ After adding/modifying a few files
- ✅ After pulling git changes
- ✅ When docs/papers updated but code unchanged
- ❌ After massive refactor (use full rebuild)
- ❌ When `.graphify_manifest.json` missing (falls back to full rebuild)

---

## --cluster-only: Re-cluster Without Re-extracting

Reruns Leiden community detection on existing `graphify-out/graph.json`. Skips all extraction passes.

### How It Works

1. Loads `graphify-out/graph.json`
2. Runs `cluster(G)` - Leiden algorithm
3. Runs `score_all(G, communities)` - cohesion scores
4. Regenerates community labels (if backend configured)
5. Updates `GRAPH_REPORT.md` and `.graphify_analysis.json`
6. Optionally regenerates HTML viz

### Usage

```bash
# Basic re-clustering
/graphify . --cluster-only

# More granular communities (higher resolution = more, smaller communities)
/graphify . --cluster-only --resolution 1.5

# Exclude hub nodes from partitioning (suppress utility super-hubs)
/graphify . --cluster-only --exclude-hubs 99

# Keep "Community N" placeholders (skip LLM labeling)
/graphify . --cluster-only --no-label

# Custom backend for community naming
/graphify . --cluster-only --backend gemini --model gemini-2.5-pro

# Parallel labeling for large graphs
/graphify . --cluster-only --max-concurrency 16 --batch-size 200

# Use custom graph file
graphify cluster-only ./my-project --graph path/to/graph.json
```

### Resolution Parameter

| Value | Effect |
|-------|--------|
| 0.5 | Fewer, larger communities |
| 1.0 | Default (balanced) |
| 1.5 | More, smaller communities |
| 2.0 | Many small communities |

### Exclude Hubs

- `--exclude-hubs 99` - excludes nodes at 99th percentile degree from partitioning
- Prevents utility super-hubs (e.g., `Object`, `Error`, `logger`) from dominating communities
- These nodes still exist but don't pull others into their community

---

## graphify label: Rename Communities On-Demand

```bash
# Rename with configured backend
graphify label ./my-project

# Force specific backend/model
graphify label ./my-project --backend openai --model gpt-4o
```

---

## Combined Workflows

### After Adding Docs to Existing Code Graph

```bash
# 1. Add new paper
/graphify add https://arxiv.org/abs/1706.03762

# 2. Incremental update (extracts paper, merges, re-clusters)
/graphify . --update
```

### After Refactoring Code Structure

```bash
# 1. Full rebuild with force (structure changed significantly)
/graphify . --force

# OR if you just want new communities on same extraction
/graphify . --cluster-only --resolution 1.5
```

### Tuning Communities for Exploration

```bash
# Start with default
/graphify .

# Too broad? More granular
/graphify . --cluster-only --resolution 1.5

# Still too broad? Even more granular
/graphify . --cluster-only --resolution 2.0

# Utility nodes polluting communities?
/graphify . --cluster-only --exclude-hubs 99
```

---

## Automation: Git Hooks

```bash
# Install post-commit + post-checkout hooks
graphify hook install

# Hooks do:
# - Post-commit: auto-rebuild (AST only, no API cost)
# - Post-checkout: refresh graph for new branch
# - Git merge driver: union-merge graph.json (no conflicts)
```

After hook install, `--update` runs automatically on commit for code changes.

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `--update` says "no manifest" | Run full `/graphify .` first to create manifest |
| Graph shrinks after `--update` | Use `--force` (intentional deletions) |
| Communities look wrong | Run `--cluster-only --resolution X` to tune |
| Labels are generic "Community N" | Run `graphify label` or `--cluster-only` without `--no-label` |
| `--update` slow | Check if video files changed (re-transcription); use `--no-cluster` if only code changed |

---

## Files Involved

| File | Purpose |
|------|---------|
| `graphify-out/graph.json` | Main graph (read/written) |
| `graphify-out/.graphify_manifest.json` | File hashes for `--update` |
| `graphify-out/.graphify_analysis.json` | Communities, cohesion, gods, surprises |
| `graphify-out/.graphify_labels.json` | Community name labels |
| `graphify-out/GRAPH_REPORT.md` | Human-readable report |
| `graphify-out/.graphify_root` | Scan root path for manifest relativization |