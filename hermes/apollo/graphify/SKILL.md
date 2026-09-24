---
name: graphify
description: Use when building or querying a graphify knowledge graph.
version: 1.0.0
author: Apollo
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    tags: [graphify, knowledge-graph, obsidian, vault]
    related_skills: [obsidian]
---

# Graphify — knowledge-graph extraction, completion, and querying

Binary: the Hermes venv graphify (`~/.hermes/hermes-agent/venv/bin/graphify`,
`graphify --help` lists all commands). Vault path (this machine): resolve the
symlink `~/TamaZila_Obsidian_Vault` to `/Volumes/PNY128GBLED/TamaZila Obsidian Vault`
before passing concrete absolute paths to tools. Report findings in English.

## 0. Query order — vault direct first, graphify for relationships

- Answer daily-workflow questions from the vault files first (source of truth for the user's own setup); use `query`, `path`, and `explain` second for cross-file relationships plain search misses.
- Pass `--graph <vault>/graphify-out/graph.json` explicitly — the default `graphify-out/graph.json` resolves to the cwd, not the vault.
- A `query` that reports N nodes found but shows far fewer hit the `--budget` cap — raise `--budget` or narrow with a context filter / single-node lookup before concluding the answer is missing.

## 1. Diagnose state first (read-only, fast)

- `ls -la <vault>/graphify-out/` — a complete graph has `graph.json`,
  `.graphify_labels.json`, `GRAPH_REPORT.md` (missing `graph.html`/`wiki/` alone is normal for 10k+ node graphs — viz is unusable and intentionally skipped).
  Missing `GRAPH_REPORT.md` with only `graph.json` + `cache/` present means
  extraction ran but clustering/report never completed.
- Inspect shape with python (never `cat` a 100 MB graph): top-level keys are
  `directed, multigraph, graph, nodes, links, hyperedges` — edges live under
  `links`, not `edges`. Count nodes, links, hyperedges, communities, and the
  `file_type` / `_origin` distributions.
- Health signals: label count in `.graphify_labels.json` should equal the community
  count; `god-nodes --top 15` should show domain concepts — minified single-letter
  JS functions (`e()`, `r()`) as top hubs means `.obsidian/` plugin/theme internals
  polluted the graph; `diagnose multigraph` should show 0 missing/dangling/duplicates.
- `check-update <vault>` empty output is normal (no semantic re-extraction pending).

## 2. Setup — exclude machine state before any rebuild

- If no `.graphifyignore` exists at the vault root, propose one from
  `templates/vault.graphifyignore` (covers `.obsidian/`, AppleDouble `._*`,
  `*sync-conflict*`, vault-organizer state/logs, sync metadata, previous
  `graphify-out/` and `Graphify-*/` outputs, media binaries). The ignore file only
  filters extraction — it never deletes notes, but never add an ignore that
  excludes `.obsidian/` without the user's explicit approval: the full corpus
  including plugin nodes is kept by standing rule, so offer a filtered query
  view instead of pruning.
- Pitfall: nearly half the nodes can be `.obsidian/` internals (workspace sync
  conflicts, themes, plugins) when no ignore file was in place — measure the
  share via `source_file` containing `.obsidian` (node keys are `label, file_type,
  source_file, source_location, _origin, community, id`), not via `src`/`id`,
  before recommending any rebuild.
- An ignore file can exist while the graph is still polluted — the ignore only takes effect on a `--force` rebuild, so high `.obsidian` share with `.graphifyignore` present means the forced rebuild never ran since the ignore was added.

## 3. Rebuild — backup, then AST update in background

- Back up `graph.json`, `.graphify_labels.json`, `.graphify_root` into
  `graphify-out/graphify-out_archived/<date>_pre-cleanup/` before anything
  destructive. Never skip the backup when `--force` will be used: excluding
  junk shrinks the node count and `update` refuses a smaller rebuild without it.
- Run `graphify update <vault> --force` (AST-only, no API cost, incremental via
  `cache/` + `stat-index.json`) as a background process with completion notify —
  a full vault walk takes many minutes. In cron / one-shot sessions completion
  notify is unavailable and foreground caps force background promotion: wait with
  ONE blocking wait (or sparse polls minutes apart), never a tight poll loop —
  rapid polling burns the run's tool-iteration budget and ends the session
  mid-extraction with cluster/label/verify never run. `manifest.json` is a per-file stat-index (mtime/ast_hash per path), not a timing report — never estimate duration from it. Delete a stale `.rebuild.lock` in `graphify-out/` before retrying, and verify afterward with the node/link counts
  from step 1 plus the `graph.json` mtime — scheduler status `ok` does not prove
  the graph was rewritten; unchanged mtime with identical counts means the
  rebuild never landed.
- The rebuild writes to the vault drive, not internal SSD — confirm free space on the vault volume for the backup (~size of `graph.json` + labels) plus the new graph; internal disk only takes temp files.
- For multi-phase unattended work (update → cluster → label → verify), write the
  whole pipeline as one script file and launch it once as a single background
  process with completion notify — chaining phases across turns or polls lets a
  stalled phase strand the rest with no runner left to continue it.
- The `[graphify watch] pruned N node(s)` log line counts only the incremental
  pruner, not the full `--force` exclusion — measure what an ignore rule removed
  by recounting `source_file` before/after, never by that line.
- Debug a fired-but-suspect run from its own transcript, not the scheduler status:
  the run lives as its own session (`hermes sessions list` shows it as
  `cron_<job>_<timestamp>`; read it with `hermes sessions export --session-id`).
  Per-profile cron state (executions.db, jobs.json) sits under
  `~/.hermes/profiles/<profile>/cron/`, not the default `~/.hermes/cron/` —
  querying the wrong profile's DB shows no trace of the run.
- An overnight one-shot cron only fires while the Hermes gateway is running and only notifies when `deliver` points at a reachable channel — a saved job with the gateway stopped stays `scheduled` forever, so verify gateway state and delivery target before promising a morning report.
- For overnight runs on this Mac also check `pmset -g` first: system `sleep 0` means Never (display sleep after N minutes only blanks the screen and is harmless) — full system sleep would miss the run window, so confirm the sleep setting before promising morning results.
- Pitfall: the vault lives on an ExFAT USB drive where `find` returns 0 results —
  count files with `python3 -c "os.walk"` instead of debugging the filesystem.
  Expect ~275k files (mostly AppleDouble `._*` sidecars) and size the rebuild
  timeout accordingly.

## 4. Finish — cluster, label, verify

- `cluster-only <vault> --no-viz --no-label` regenerates communities +
  `GRAPH_REPORT.md` without invoking the LLM (unpinned clustering auto-detects a
  labeling backend, which can land on cloud) — labeling happens in the next step.
  Skip `graph.html` for 10k+ node graphs (viz is unusable and slow).
- `label <vault>` with the local Ollama backend (`qwen3.5` variants are installed)
  names placeholder communities; `--missing-only` preserves existing labels.
  Always pin `--backend=ollama --model=<installed-tag>` (e.g. `qwen3.5-32k`) —
  the backend default model comes from `OLLAMA_MODEL` or falls back to
  `qwen2.5-coder:7b`, which may not be installed, failing every labeling call.
  Local Ollama labeling is forced to concurrency 1, so thousands of communities
  mean a long slow tail that warms a 16GB Mac — keep it inside the same
  background script, never as a separate attended phase.
- Verify with `god-nodes`, one `query "<question>"`, and one
  `explain "<concept>"`; after code edits run `graphify update .` (no `--force`)
  to keep the graph current per repo AGENTS.md rules.
