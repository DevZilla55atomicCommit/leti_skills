---
name: claude-code-auto-compact
description: Configure auto-compact for Claude Code with Ollama/local models
category: automation
author: alfredkamisese
tags: claude-code, auto-compact, settings, ollama, token-limit
---

# Claude Code Auto-Compact Settings

This skill documents the recommended configuration for enabling automatic conversation compaction in Claude Code, particularly when using local models via Ollama.

## Recommended Settings

Add the following to your `~/.claude/settings.json`:

```json
{
  "env": {
    "CLAUDE_CODE_MAX_OUTPUT_TOKENS": "36000",
    "CLAUDE_CODE_MAX_CONTEXT_TOKENS": "48000",
    "CLAUDE_CODE_DISABLE_UNKNOWN_MODEL_WINDOW_ENFORCEMENT": "1",
    "ANTHROPIC_BASE_URL": "http://localhost:11434",
    "ANTHROPIC_AUTH_TOKEN": "ollama",
    "ANTHROPIC_API_KEY": "ollama"
  },
  "autoCompactEnabled": true,
  "model": "qwen3.5-48k:latest",
  "statusLine": {
    "type": "command",
    "command": "~/.claude/statusline.sh"
  }
}
```

Set `CLAUDE_CODE_MAX_OUTPUT_TOKENS` to **75%** of your model's context window for reliable auto-compact triggering with Ollama (75% is safer than 80% — compact fires at ~80% of this value, so 75% compacts at ~60% of real context while 80% compacts at ~64%, later, where proxy undercounting overflows):
- qwen3.5-32k:latest → 24000
- qwen3.5-48k:latest → 36000
- qwen3.5-64k:latest → 48000
- qwen3.5-96k:latest → 72000
- qwen3.5-128k:latest → 96000

**Also set `CLAUDE_CODE_MAX_CONTEXT_LENGTH`** to the full window (96000 for qwen3.5-96k) so Claude Code knows the actual window size.

**Set `CLAUDE_CODE_AUTO_COMPACT_WINDOW`** to match `CLAUDE_CODE_MAX_OUTPUT_TOKENS` (75% of context = 72000 for qwen3.5-96k) so the compaction window aligns with the output token limit.

**Env vars are GLOBAL, not per-model** — anchor the three token values to the default `model`, never to the largest window present. Anchoring to a 1M cloud window starves nothing but breaks every local model; anchoring to the smallest model strangles large ones. Default pattern: anchor to the daily-driver model and accept early (safe) compaction on larger models when switching via the picker.

**Size from `num_ctx`, not native context** — `ollama show` reports architecture context (e.g. 262144) plus effective `num_ctx` (e.g. 32768); always compute 75% from `num_ctx`. Set `OLLAMA_CONTEXT_LENGTH` to the default model's `num_ctx` to avoid over-allocating RAM.

**Set `CLAUDE_CODE_DISABLE_UNKNOWN_MODEL_WINDOW_ENFORCEMENT=1`** when using Ollama/local models to prevent Claude Code from enforcing its default 200k window assumption.

**Set `ANTHROPIC_BASE_URL`, `ANTHROPIC_AUTH_TOKEN`, `ANTHROPIC_API_KEY`** for Ollama's Anthropic-compatible endpoint.

**Expose models via gateway discovery, never modelOverrides** — `modelOverrides`/`behavesAs` are not real Claude Code keys; unknown settings keys are silently ignored, so they never populate any picker. Set `CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY=1` (v2.1.129+) so `/model` lists what `GET /v1/models` returns, and map tiers with `ANTHROPIC_DEFAULT_HAIKU/SONNET/OPUS_MODEL` (locals → sonnet, small/fast → haiku, large reasoners → opus). Exclude non-chat models (embeddings, image) at selection time, not in config.

**Set `statusLine.command` to `~/.claude/statusline.sh`** — tilde expansion works; absolute path `bash /path/` does NOT.

## Multi-model switching (one trio, many windows)

Token env vars are global, so one file cannot hold correct per-size values for 32k through 128k simultaneously — and project `.claude/settings.json` `env` silently overrides the global trio for sessions launched in that folder. Two rules:
- Strip token keys (`CLAUDE_CODE_MAX_OUTPUT_TOKENS`, `CLAUDE_CODE_MAX_CONTEXT_TOKENS`, `OLLAMA_CONTEXT_LENGTH`, `CLAUDE_CODE_AUTO_COMPACT_WINDOW`) from every project settings file so one global trio governs everywhere. Project-level `model` pinning is fine; wrong-size numbers fail safe only in the early-compact direction — never run a small-window model on large-window numbers.
- Switch models with a script that rewrites the four window values plus `model` to the target size's set (75% set for the safe trigger, 100% set for an 80%-of-real trigger), backs up first, and validates JSON — then restart Claude Code. Per-size values live in `references/auto-compact-env-vars.md`.

## When Using Ollama Proxy

Because token counting may not be accurately reported through a local proxy, consider:

1. **Explicit Token Limit**: Set `CLAUDE_CODE_MAX_OUTPUT_TOKENS` to 94% of your model's context window (e.g., 45000 for qwen3.5-48k:latest). This allows auto-compact to trigger before hitting the hard limit.

2. **Manual Management**: If auto-compact doesn't work reliably, set `DISABLE_AUTO_COMPACT=true` and manage context manually via subagents or `/compact` commands.

## Desktop App vs CLI Settings

The Claude Desktop app reads `~/.claude/settings.json` (launches with `--setting-sources=user,project,local`), but:
- **Values may be clamped** — the app enforces a 100k floor on `CLAUDE_CODE_AUTO_COMPACT_WINDOW`; a 65536 value reports as 100k in the app's `/autocompact` message.
- **Stale env in running processes** — settings changes only apply to fresh sessions; the Desktop app's managed worker holds the old trio until quit + reopen.
- **Managed settings can override** — the app injects `--managed-settings` and `--model` flags that may shadow user values. Verify with `/autocompact` in the app session (it names the winning source) before assuming the file governs.
- **Model picker drift** — the app's picker silently loads a different variant than the pinned `model` (e.g., `qwen3.5:9b` at 131k instead of `qwen3.5-96k` at 98k). Always confirm with `curl localhost:11434/api/ps` that the serving model matches the settings trio.
- **Provider port bug** — the app maintains its own provider registry (separate from Hermes `config.yaml`). A typo like `http://127.0.0.1:11435` instead of `11434` yields "Gateway returned no usable models" even when Ollama is healthy. Fix in the app's Settings → Providers UI.
- **Gateway vs Hermes config** — Hermes `config.yaml` (port 11434) and Desktop app provider settings are independent. Both must point to 11434.

## RAM Pressure on 16 GB Machines

Large local models (9b+ at 128k+ context) consume 6–10 GB VRAM/RAM. On 16 GB:
- `qwen3.5:9b` at 131072 ctx → ~9.4 GB resident → 8% free, heavy swap, model overload errors.
- `qwen3.5-96k` at 98304 ctx → ~6 GB resident → stable headroom for app renderers.
**Rule:** anchor the default model + settings trio to the largest model that leaves ≥20% free RAM. Accept early compaction on larger models when switching via picker; do not size the trio to a model that starves the system.

## Auto Is the Stable Default

Remove `CLAUDE_CODE_AUTO_COMPACT_WINDOW` and `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` entirely. Let `auto` tune to whatever model is actually loaded (the app's message: "The auto setting picks a window tuned for your model and is strongly recommended"). This eliminates the half-finished-switch problem (four keys on old size, one on new) and survives model-picker drift. Keep `MAX_OUTPUT_TOKENS` modest (16384) so the output reserve doesn't eat the trigger.

## Qwen3.5 96k Streaming Bug — Non-Streaming Workaround

When `qwen3.5-96k:latest` streaming is broken (returns empty NDJSON), force non-streaming:
- **Non-streaming endpoint works** — returns valid JSON, no `StreamNoEventsError` retry loop.
- **Gateway config** (litellm proxy):
  ```yaml
  model_list:
    - model_name: qwen3.5-96k
      litellm_params:
        model: ollama/qwen3.5-96k:latest
        api_base: http://localhost:11434
        stream: false
  ```
- **RAM win**: 96k non-streaming = ~6 GB (stable). 9b streaming = ~9.4 GB (OOM on 16 GB).
- **Trade-off**: lose "typing" effect, gain complete diffs/code blocks, stability.

## Verification

After updating settings, run `/status` to confirm the settings loaded. Look for the "Auto-compact" line in the settings sources output.

## Common Pitfalls

- After any model switch, print all five token keys (`OLLAMA_CONTEXT_LENGTH`, `CLAUDE_CODE_MAX_OUTPUT_TOKENS`, `CLAUDE_CODE_MAX_CONTEXT_TOKENS`, `CLAUDE_CODE_MAX_CONTEXT_LENGTH`, `CLAUDE_CODE_AUTO_COMPACT_WINDOW`) plus `ollama show <serving-model>` `num_ctx` and confirm they agree — a half-finished switch (some keys on the old size, some on the new) produces early-compact thrash at a fraction of the real window.
- When compaction misbehaves in the Desktop app, run `/autocompact` in that session before touching `~/.claude/settings.json` — it names the winning source (env var, flag, command, or model default), and the CLI file may not govern the app runtime at all.

- Using a `CLAUDE_CODE_MAX_OUTPUT_TOKENS` value larger than the model's actual context window prevents auto-compact from triggering.
- Keep `CLAUDE_CODE_MAX_OUTPUT_TOKENS` and `CLAUDE_CODE_AUTO_COMPACT_WINDOW` equal — mismatched values delay compaction unpredictably.
- Keep `OLLAMA_CONTEXT_LENGTH` equal to the default model's `num_ctx` — a larger value wastes RAM with no benefit.
- Local proxies may not report token usage correctly, affecting auto-compact's ability to assess context.
- Disabling auto-compact without an alternative context management strategy can lead to frequent token limit errors.

## Related Skills

- [[claude-code-settings-overview]] - Comprehensive guide to all Claude Code settings
- [[ollama-proxy-configuration]] - Best practices for using Ollama with Claude Code

### Support Files

- `references/auto-compact-troubleshooting.md` - Troubleshooting token counting issues with local proxies
- `references/auto-compact-env-vars.md` - Environment variable reference table with model-specific values
- `templates/auto-compact-check.sh` - Script to verify auto-compact status
- `scripts/check-auto-compact.sh` - Verify auto-compact configuration