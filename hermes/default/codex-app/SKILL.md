---
name: codex-app
description: 'Use when operating the Codex app backed by Ollama.'
version: 1.0.0
tags: [codex, ollama, mcp, sandbox, local-models]
---

# Codex App (Local-Model Backend)

Run the Codex desktop app routed to a local Ollama daemon: register MCP servers, grant write access, and diagnose denials from session logs.

## Config Location

- `~/.codex/config.toml` holds model selection, provider routing, MCP servers, and project trust.
- Copy-backup before every edit: `cp ~/.codex/config.toml ~/.codex/config.toml.bak-<yyyymmdd>`.
- Local routing looks like `model = "<ollama-tag>"` with `openai_base_url = "http://127.0.0.1:11434/api/codex/v1"`.

## Skills vs Plugins vs Tools

- Standalone skill: a `SKILL.md` folder under `~/.codex/skills/<name>/` — copy the whole folder in with `mkdir -p` then restart the app.
- When bulk-installing, back up any same-named existing dir first (`mv <dst> <dst>.bak-<yyyymmdd>`) and verify every destination contains `SKILL.md` afterwards — a copy that lands files one level deep surfaces only as a skill that never loads.
- Discover skills in a cloned repo with `find <repo> -name SKILL.md`, never bare `ls` — curated collections hide under dot-directories (e.g. `skills/.curated/`) that plain `ls` silently omits.
- `github.com/openai/skills` is deprecated — for current Codex skill and plugin examples use `github.com/openai/plugins`.
- Plugin: a bundled skills+agents package from a marketplace (lives under `~/.codex/plugins/cache/`) — install with `codex plugin add <name>@<marketplace>`, list with `codex plugin list`.
- Tool (MCP server): an external server registered in `config.toml` — install with `codex mcp add`, list with `codex mcp list`.
- Ask which layer the user means when they say "install X to Codex" — the three paths are not interchangeable.

## CLI Catalog Override

- The CLI parses `model_catalog_json` with an older schema than the desktop app and its generator write — `codex plugin`/`codex mcp` fail with `unknown variant` or `missing field` while the app itself runs fine, so treat a CLI-only catalog parse error as version skew, never as a corrupt config.
- Never edit the generated catalog to satisfy the CLI — the app needs the new-schema fields and the generator rewrites the file, so the edit evaporates on relaunch and can degrade the app.
- Keep a minimal schema-valid one-model catalog (one entry shaped like a `models_cache.json` entry) at `~/.codex/ollama-launch-models.cli-min.json` and pass it per invocation:

```bash
codex -c model_catalog_json='"/Users/<you>/.codex/ollama-launch-models.cli-min.json"' plugin list
```

- The `-c` value is parsed as TOML so the inner path needs its own quotes; `-c model_catalog_json=null` does not clear it (it parses as the literal path `null`).

## Register an MCP Server

- Prefer the CLI over hand-editing TOML — it avoids silent typos that surface only as a missing server:

```bash
codex mcp add <name> -- /abs/path/to/venv/bin/python /abs/path/to/server.py
codex mcp add <name> --url http://127.0.0.1:8000/mcp
codex mcp list
```

- TOML fallback — append one block per server with absolute paths (quote paths containing spaces, never use `~`):

```toml
[mcp_servers.<name>]
command = "/abs/path/to/venv/bin/python"
args = ["/abs/path/to/server.py"]
cwd = "/abs/path/to/server/dir"
enabled = true
startup_timeout_sec = 60
```

Restart the Codex app afterwards — MCP servers load at startup, there is no hot-reload.

## Verify Before Announcing

- Parse check: reload the TOML and confirm the block reads back with `enabled = true` — a silent typo here surfaces only as a missing server.
- Handshake check: spawn `[command, args[0]]` under `cwd`, send an MCP `initialize` request over stdio, and require a result carrying `serverInfo` — a clean handshake proves the server runs independent of the app.
- Pin the MCP SDK major to the server's API generation in the server's own venv — bare `pip install mcp` resolves to 2.x, which removed `mcp.server.fastmcp`, so v1 `FastMCP` servers need `pip install "mcp<2"` or they die at import.

## Pick the Local Model Variant

- A `model:tag` and its `model:tag-mlx` twin share base weights but differ in backend (GGUF/llama.cpp vs Apple MLX), quantizer (the `quantization` field in `ollama show`), and resident footprint (the `SIZE` column in `ollama ps`).
- Diff `ollama show <a>` against `ollama show <b>` (parameters, quantization, context length) before pulling a multi-GB second copy — pull only for a measured reason (speed shootout, RAM fit), never out of curiosity.

## Tool Invocation Model

- MCP tools fire automatically: the model reads each tool's name and description and calls it when the request matches — no slash command exists unless the server also ships prompts or skills.
- Name the tool in the prompt to force it ("using the flux tools, ..."); otherwise let the model decide.
- Bias every session with one standing line in the project's `AGENTS.md` (e.g. always use a given MCP tool for a given artifact type).
- Confirm visibility by asking the app to list its tools or checking Settings → MCP — a dead server errors there instead of failing silently.

## Sandbox and Write Access

- The default `sandbox_mode` is `workspace-write`: the filesystem reads broadly but writes land only inside the session's working directory — repeated grants and approvals never widen this, so stop re-asking and re-root instead.
- Grant a folder in this order: root the chat at the target directory so it becomes the workspace; mark it trusted via a `[projects."<abs-path>"] trust_level = "trusted"` config entry; have the app persist access through its own `request_permissions` tool; reserve full-access sandbox modes for explicit user approval since they remove the guardrail entirely.
- Prove access with a test-file write before starting real work.

## Session Forensics

- Rollouts live under `~/.codex/sessions/<yyyy>/<mm>/<dd>/rollout-*.jsonl`.
- Grep the latest rollout for `sandbox_mode`, `file_system_sandbox_policy`, and `"cwd"` to distinguish a sandbox denial from a missing approval or a wrong path — diagnose from the log before changing configuration.
- When the rollout shows `Could not resolve host` on git/curl, run `git ls-remote <url> HEAD` and `nslookup <host>` OUTSIDE the sandbox before touching config — success outside proves a sandbox network denial, not a real outage, so fix by fetching outside into a workspace path and pointing the session at local files instead of widening sandbox network.
