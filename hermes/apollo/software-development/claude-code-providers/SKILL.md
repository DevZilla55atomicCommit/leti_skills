---
name: claude-code-providers
description: Use when routing Claude Code to Ollama or gateways.
version: 1.0.0
author: Apollo (Hermes Agent)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Claude Code, settings.json, Ollama, LLM gateway, modelPicker]
    related_skills: [ollama-models]
---

# Claude Code Providers

## When to use

Use when pointing Claude Code at anything other than api.anthropic.com: local Ollama models, Ollama cloud-streamed models, or third-party Anthropic-compatible gateways (e.g. a localhost translating proxy for a free tier). Covers settings.json rewrites, /model picker lineups, per-model context windows, and provider secrets.

## Standing preferences (this user)

- Default model is qwen3.5-48k:latest on local Ollama; change the default only when explicitly asked.
- Auto-compact fires at 75% of the active model's num_ctx, whichever model is chosen.
- Claude Code reads ONLY settings.json — helper scripts are remote controls that edit that file, never configuration. State this plainly whenever the user confuses the two.
- Variant names must show their difference (e.g. a -q8kv suffix carries what changed, and the header comment states what it does NOT do).

## Procedure

1. Treat settings.json as single-active-model state: `model` plus one context trio (`OLLAMA_CONTEXT_LENGTH`, `CLAUDE_CODE_MAX_CONTEXT_TOKENS`, `CLAUDE_CODE_AUTO_COMPACT_WINDOW`, `CLAUDE_CODE_MAX_OUTPUT_TOKENS`). The trio must match the `model` field's real num_ctx/num_predict — that pair is the session-start state, and matching it is what "correct" means.
2. Rewrite atomically with python json (never sed on JSON): `cp` backup first, load, set fields, `json.dump(indent=2)` plus trailing newline (re-apply the newline on every write — writers that omit it create phantom diffs). Verify by re-loading and asserting model + trio + picker row count; eyeballing is not verification.
3. List every provider's chat-capable models in the native `modelPicker` (`replaceBuiltInOptions: true` when all traffic routes to custom base URLs; requires CLI >= v2.1.242 — check `claude --version`). Each row carries a verbatim model id plus a label/description with ctx, compact point, and max-out so models are distinguishable in the picker. Exclude embedding-only and image models with a stated reason, never silently.
4. Keep canonical picker lineups as `~/.claude/picker-<profile>.json` files; the switch writes the active profile's file into settings.json. Rebuild from these after any external rewrite.
5. Validate with `claude doctor` (zero settings errors) — the CLI accepting the file is ground truth; editor squiggles without a pasted hover message are a stale-extension schema until proven otherwise, so ask for the exact message text before changing anything for them.
6. For a new provider profile, switch base URL + auth + trio + picker together in one rewrite. Never change the model id without moving the trio with it.

## Pitfalls

- A single global trio cannot fit all models — after a mid-session /model switch the numbers stay with the session-start model (conservative for larger windows, overshoot risk on smaller ones); exact per-model numbers require a profile switch, not the picker.
- The native `autoCompactWindow` key only accepts 100000-1000000, so it cannot express 75% for small local windows — use the `CLAUDE_CODE_AUTO_COMPACT_WINDOW` env var, which outranks key and flag.
- `OLLAMA_CONTEXT_LENGTH` in the client env block does nothing to the already-running server (separate process) — the documented client-side knob is `CLAUDE_CODE_MAX_CONTEXT_TOKENS`; per-model server ctx lives in each Ollama Modelfile's baked `num_ctx` (see ollama-models).
- settings.json gets rewritten by outside writers (Claude sessions, IDE extensions) that drop keys like `modelPicker` and add their own — leave foreign keys untouched, manage only your own, and re-verify picker row count after every switch; the canonical picker-*.json files are the restore source.
- Secrets go to macOS Keychain (`security add-generic-password -s <service> -a $USER -w`) or a 600-permission key file owned by the providing service, injected at switch time — never into settings files and never quoted in prose; verify storage by character count, not value.
- Free-tier gateway specifics (protocol probes, allowlist vs catalog, 429 handling, daemon persistence) live in `references/free-tier-gateways.md`.
- Claude Desktop app third-party gateway (config location, :11434 vs :11435 catalogs, discovery bug) lives in `references/desktop-gateway.md`.
