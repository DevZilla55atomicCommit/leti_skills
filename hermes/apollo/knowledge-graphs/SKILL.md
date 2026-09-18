---
name: knowledge-graphs
description: Build or refresh a queryable knowledge graph (graphify).
version: 1.0.0
author: Apollo
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [knowledge-graph, graphify, vault, codebase]
    related_skills: []
---

# Knowledge Graphs (graphify)

Full lifecycle for a queryable knowledge graph over a vault or codebase: inspect state, back up, filter junk, rebuild, cluster, label, verify. Safety first: graph data is regenerable, source notes and code are not — never delete or move source content for the graph's sake.

## Procedure (in order)

1. **Inspect before touching.** Check `graphify-out/` contents, parse `graph.json` top-level keys with Python (node/link/community counts, community distribution, `file_type` and `_origin` breakdowns), and quantify junk: `.obsidian/` internals, `sync-conflict` copies, AppleDouble (`._*`) files on ExFAT drives. Run `god-nodes --top N` and `diagnose multigraph` as a read-only baseline.
2. **Back up the current graph.** Copy `graph.json` (plus labels/root markers) into `graphify-out/graphify-out_archived/<date>_<reason>/` before any rebuild that overwrites. Verify the backup size on disk; do not proceed until it exists.
3. **Write `.graphifyignore` first.** Gitignore-style patterns for internals (`.obsidian/`), AppleDouble (`._*`, `**/._*`), `*sync-conflict*`, organizer state/logs, sync metadata (`.stfolder/`), prior graph outputs (`graphify-out/`, test-dump folders), and media binaries. Creating it is safe: it only filters extraction, never deletes notes.
4. **Rebuild AST-only with `graphify update <path> --force`.** No LLM, no API cost, fully local. `--force` is required whenever the rebuild yields fewer nodes (e.g. after adding exclusions) — without it the write is refused.
5. **Regenerate structure with `cluster-only --no-viz` for graphs over ~5000 nodes.** The HTML viz has a hard node limit and the build refuses above it; `--no-viz` still writes `GRAPH_REPORT.md`, which is the actual completion artifact. Confirm the report exists at graph root afterward.
6. **Refresh names with `graphify label --missing-only`.** Labeling keeps existing names and only names new/placeholder communities.
7. **Verify with read-only probes.** `god-nodes` (hubs should be domain concepts, not minified `e()`/`r()` helpers), one `query` traversal, one `explain` on a known concept. If junk nodes dominate results, say so plainly instead of presenting polluted output as success.

## Pitfalls

- `graphify update` merges and does NOT honor a newly added `.graphifyignore` — only a fresh `extract` applies ignore patterns, so junk-node share can stay flat or grow after an update; report the measured share honestly and offer a clean `extract` as the fix, never claim the cleanup worked without re-measuring.
- `graphify label` is a CLI subprocess that only speaks to its own backends (gemini/kimi/claude/openai/deepseek/ollama) — it cannot borrow the agent's session model; check the environment for keys (names only, never values) and default to the local Ollama backend when no keys exist.
- Long rebuilds (tens of minutes on large vaults, worse on ExFAT USB) run in the background with completion notification — never block the session; estimate time from cache-file growth between polls and report progress, not guesses.
- Missing `GRAPH_REPORT.md` at graph root (with only stale dated snapshots present) is the signature of a partially completed run — treat report generation, not just `graph.json`, as the definition of done.
- Expect and report benign warnings without alarm: files skipped as absent (retried on re-run), a few syntax-error files listed by name, and `graph.html` refused over the viz node limit.
