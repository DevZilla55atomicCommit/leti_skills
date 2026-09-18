# Compaction Tuning for Claude Code on Local Models

Topical depth for `local-coding-agents`. Distilled from official docs
(code.claude.com/docs: env-vars, context-window, settings) plus verified
local-model behavior. No per-model threshold setting exists upstream —
control comes from three knobs plus serving alignment.

## Trigger formula

- Effective window = `min(CLAUDE_CODE_AUTO_COMPACT_WINDOW if set, model window)`.
- Fires at `min(CLAUDE_AUTOCOMPACT_PCT_OVERRIDE, ~83%)` of that window — the
  percent override only ever LOWERS the trigger; above-default values are
  silently ignored. Applies to main conversations and subagents.
- Status-line `used_percentage` always measures against the FULL model
  window, so it diverges from the real trigger whenever a custom compact
  window is set.
- Window range 100K–1M, plain integer only (`500k` parses as `500` and clamps
  to the 100K floor); always capped at the model's window.

## Precedence (highest wins, silently)

`CLAUDE_CODE_AUTO_COMPACT_WINDOW` env > `--autocompact` launch flag >
`/autocompact` command ≈ `autoCompactWindow` setting (managed-settings scope
can preempt the command, never the flag). `/autocompact auto` returns to the
model-tuned window; `/autocompact` with no args reports the winning scope.

## Disable switches

- `DISABLE_AUTO_COMPACT=1` kills auto-compaction, keeps manual `/compact`.
- `DISABLE_COMPACT=1` kills both — risks a 100% deadlock with no recovery.
- `CLAUDE_CODE_MAX_CONTEXT_TOKENS` corrects the assumed window for
  `ANTHROPIC_BASE_URL`-routed models but is legacy beside the window var;
  don't set both.

## Serving alignment (the usual real cause of 'early' compaction)

- Unrecognized/gateway model IDs compact at an ASSUMED window, not the real
  one; verify with `/autocompact` (it names the winning scope).
- Ollama `num_ctx` must be baked into the model (Modelfile `PARAMETER
  num_ctx`); server defaults truncate silently, so percentages compute
  against a window the server never honors.
- No per-model setting exists — use a shell wrapper switching the window by
  model tag (`case $1 in *32k*) export ...32000 ...`) since one flat value
  underuses big models or overflows small ones.

## Subagent costs

- Subagents run in separate windows; only their returned summary lands in
  main (the `↓ N tokens` line) — but a verbose return can itself push main
  over the compact line. Cap returns (~15 lines: verdict + files + gates).
- A subagent can fill ITS window while main looks healthy, then stall the
  project with a truncated return; timebox subagents and split on stall.
