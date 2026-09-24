---
name: knowledge-graph
description: Use when rebuilding a graphify knowledge graph.
version: 1.0.0
author: Apollo
license: MIT
---

# Knowledge Graph (graphify) Maintenance

Corpus graphs go stale or half-finished: current graph but no report, fresh files unindexed, or junk paths dominating communities. The fix is always diagnose → back up → rebuild → label → verify, in that order.

## Procedure

1. **Diagnose before touching anything.** Load `graphify-out/graph.json` and count nodes, links, communities, plus the share of state/junk paths (sync conflicts, app-internal dirs, generated copies). Compare label count against community count and check whether `GRAPH_REPORT.md` exists at the graph root. This decides whether you need an update, a label pass, or a clean extract.
2. **Back up first.** Copy `graph.json`, `.graphify_labels.json` (and `.graphify_root` if present) into `graphify-out/graphify-out_archived/<timestamp>/` before any `--force` run. Rebuilds are regenerable; the labels and the pre-change graph are not worth re-deriving.
3. **Ignore hygiene.** Ensure `.graphifyignore` excludes generated/state paths before rebuilding (see `templates/graphifyignore`). Exclusions only affect extraction — they never delete corpus files.
4. **Rebuild with update.** `graphify update <corpus> --force` is AST-only: no LLM, no API cost, fully local. On large corpora (or slow drives) it runs long — launch it in the background with completion notification rather than blocking the session.
5. **Name communities with an available backend.** `graphify label <corpus> --missing-only` names only unlabeled communities. Pick the backend from credentials actually present in the environment; with no cloud keys, use the local Ollama backend and an on-device model.
6. **Run the verification battery.** Fresh file timestamps; a corpus-specific `query` returning exact source files; `path` between two related nodes; `explain` on a known concept; `diagnose multigraph` clean. Every command must exit 0 with corpus-grounded output before calling the graph done.

## Pitfalls

- `graphify update` merges and does not apply a newly added `.graphifyignore` — only a fresh `extract` honors ignore rules. Expect junk nodes to survive an update; plan a clean extract when removal (not just currency) is the goal.
- `update` refuses to overwrite when the rebuild has fewer nodes, and `--force` overrides that guard — which is why the backup step is mandatory, never optional.
- `graph.html` is skipped above the viz node limit on large graphs; treat the skip as expected and navigate via `GRAPH_REPORT.md` plus `query`/`path`/`explain` instead.
- The graphify CLI only speaks to its own backends and cannot borrow the agent session's model — check which keys exist before promising a labeling backend.
- `--missing-only` preserves every existing label, including stale or placeholder-flavored ones; use a full relabel only when renaming existing communities is the point.
- Ambiguous `path` endpoints mean duplicate node names in the corpus (e.g. a file plus a generated copy); retry with `--undirected`, then disambiguate with full node IDs.
