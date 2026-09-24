---
name: ollama-models
description: Manage local Ollama models and context variants.
version: 1.0.0
author: Apollo (Hermes Agent)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Ollama, Modelfile, Local LLM, Context Window]
    related_skills: []
---

# Ollama Models

## When to use

Use when inspecting, cloning, or creating local Ollama models — especially context-window variants of the same base weights via Modelfile, memory-tuned copies for constrained RAM, or judging whether a large-context model fits the host.

## Standing preference

This user keeps context-window clones of one base model as separate tags in the form `<family>-<N>k:latest` (e.g. `qwen3.5-48k:latest`, `qwen3.5-96k:latest`), all sharing a single weight blob. Match that naming when asked for a new context size.

## Procedure

1. Inspect the base first — never guess the blob or params:
   - `ollama list | grep <family>`
   - `ollama show <base-tag> --modelfile` (source of truth for FROM blob, TEMPLATE, SYSTEM, RENDERER, PARSER, PARAMETERs, LICENSE)
2. Dump the base Modelfile to a file, then derive the new one by changing ONLY what the context size requires:
   - `ollama show <base> --modelfile > /tmp/Modelfile.<new-tag>.base`
   - Replace the context-window mention in SYSTEM (e.g. `48K` -> `96K`).
   - Replace `PARAMETER num_ctx <old>` with `N*1024` (e.g. 48k=49152, 96k=98304, 128k=131072).
   - Keep FROM blob SHA, TEMPLATE, RENDERER, PARSER, all other PARAMETERs, and LICENSE byte-identical so the new tag shares the weight blob (zero extra storage for weights).
   - Write a clean header: `# Modelfile for <new-tag>` + `# Based on <base-tag> but with <N>K context window (<N>*1024=<ctx>)`.
3. Create the model:
   - `ollama create <new-tag> -f /tmp/Modelfile.<new-tag>`
4. Verify with real tool output before claiming success:
   - `ollama list | grep <family>` (new tag present, same GB size as siblings confirms blob sharing)
   - `ollama show <new-tag> --modelfile | head` (SYSTEM + num_ctx correct)
   - `ollama show <new-tag>` Parameters section (num_ctx equals N*1024, arch/quant match base)

## Pitfalls

- Copy the exact `FROM /.../.ollama/models/blobs/sha256-...` line from the base Modelfile — rebuilding FROM a tag name instead of the blob SHA risks resolving to different weights and breaking blob sharing.
- Compute num_ctx as N*1024 with the terminal, never from memory — a wrong num_ctx silently creates a mislabeled model that still reports success.
- Verify with `ollama show`, not `ollama run`, for thinking/reasoning models — a run test can stream a long thinking trace and hang the session while show returns the ground truth instantly.
- Change nothing else between siblings unless asked — temperature, top_k, top_p, repeat/presence penalties, num_predict, and num_thread must stay identical so only context differs.
- Set KV-cache quantization via the server environment, never the Modelfile — `OLLAMA_KV_CACHE_TYPE` is read by `ollama serve` at startup and Modelfile PARAMETERs silently ignore it, so a `-q8kv` name alone saves nothing until the server restarts with the flag.
- Check `ollama ps` before restarting the server — a restart drops loaded models, so confirm the table is empty to make the restart zero-cost.
- Estimate weights + KV before promising a fit — KV cache grows linearly with num_ctx and can exceed physical RAM on 16GB hosts at 96k+ even when weights alone fit; see `references/apple-silicon-sizing.md` for the math.
- Retrieve a prior variant's recipe from session history before rebuilding — the exact FROM blob and PARAMETER set are session-specific ground truth that beats reconstructing from docs.
- Check stock pulls for a baked `num_ctx` before trusting any assumed window — `ollama show <tag> --modelfile | grep num_ctx` returning empty means the real window is the server default, so a client-side trio built for a larger number overshoots on long sessions; clone the tag with the desired `PARAMETER num_ctx` baked in instead of assuming.
- Distinguish cloud-only from downloadable tags before promising a local pull — a `:cloud` tag shows `-` under SIZE in `ollama list` and a huge parameter count in `ollama show`; the Ollama library Models table lists it separately from sized local tags, so verify there first and offer the cloud `ollama run <model>:cloud` path as the workaround.
- Treat identical IDs in `ollama list` as one shared blob, not two downloads — same ID means alias (zero extra disk), so report it as such instead of summing both sizes.
- Check the model README hardware floor and license, not just download GB — a 14GB tag can still require a 32GB host for usable context, and some code tags forbid commercial use; confirm fits / at-limit / exceeds against RAM minus macOS reserve AND `df -h /` free disk before recommending.
- Evict every non-target local before switching models on constrained RAM — Ollama's multi-minute keepalive stacks weights so back-to-back switches load both at once (6.6GB + 4.7GB already exceeds 16GB minus macOS reserve); run `ollama stop` on all other locals at switch time and confirm with `ollama ps`.
- Pair a second local specialist sequentially with capped context, never at full window — a 7B coder at 16K ctx + 2048 out loads ~5GB instead of ~5.6GB+ at full 32K, which is what keeps a two-model rotation survivable on 16GB; full windows are for solo runs only.
- Never rewrite model settings while a task is mid-run — changing the model trio under an active session swaps its context/output budget mid-turn and evicts the model it is using; check `ollama ps` and running clients first, and if a task is active, restore its trio instead of switching.
- Never pass `--num-ctx` to `ollama run` — the flag does not exist and the command errors; set context via Modelfile `PARAMETER num_ctx`, the `OLLAMA_CONTEXT_LENGTH` env var, or the calling client's context setting.

## Memory-tuned variants

When the user asks for a copy that fits constrained RAM, clone the context variant then deliberately cut output buffer and suffix the name (e.g. `<family>-96k-q8kv:latest`):

1. Derive from the context variant's dumped Modelfile, changing ONLY `PARAMETER num_predict 4096` -> `2048`.
2. Write a header comment stating exactly what changed and what it does NOT do (e.g. `# TUNED ... num_predict 2048 (vs 4096) to cut output buffer.` plus a NOTE that the q8kv memory saving requires server env `OLLAMA_KV_CACHE_TYPE=q8_0`).
3. Treat `num_predict` as output-length cap only — lowering it never changes reasoning or knowledge, so prefer cutting it before touching weights or context when RAM is tight.
4. Tell the user the tuned name alone does not halve memory — the q8 KV saving activates only after the server restarts with the env flag; until then the copy's benefit is shorter max answers under a clearly distinct name.

## Server vs client

- The Ollama app (`ollama serve`) is the server and owns all memory behavior; Claude Code CLI, `ollama run`, and curl are interchangeable clients against `localhost:11434`.
- Restarting means quitting/reopening the Ollama app (or its `serve` process), never restarting Claude Code.
- For the GUI app on macOS, shell-exported env does not propagate — use `launchctl setenv OLLAMA_KV_CACHE_TYPE q8_0` then reopen the app; revert with `launchctl unsetenv` plus reopen.

## References

- **[apple-silicon-sizing.md](references/apple-silicon-sizing.md)** — KV-cache math, fit-table method, and q8_0 guidance for 16GB hosts.
- **[claude-code-wiring.md](references/claude-code-wiring.md)** — Claude Code settings for Ollama-backed and multi-provider setups: trio-must-match-model, modelPicker lineup, gateway knobs, server-vs-client env scope, Zen-proxy notes, keychain secrets.
