# Claude Code wiring for Ollama-backed and multi-provider setups

Claude Code reads ONLY `~/.claude/settings.json`. Helper scripts are remote
controls that rewrite the file — keep the file self-consistent so it stands
without them, and keep canonical picker lineups as separate files so an
external rewrite can be rebuilt, not mourned.

## The trio rule

One global context trio per file, and it must match the `model` field:

- `OLLAMA_CONTEXT_LENGTH` = model's real `num_ctx`
- `CLAUDE_CODE_MAX_CONTEXT_TOKENS` = same value (the documented knob Claude
  Code itself reads when routing through `ANTHROPIC_BASE_URL` to a model
  whose window differs from any built-in size)
- `CLAUDE_CODE_AUTO_COMPACT_WINDOW` = 75% of `num_ctx`
- `CLAUDE_CODE_MAX_OUTPUT_TOKENS` = model's real `num_predict`

Method: read each model's `num_ctx`/`num_predict` from `ollama show`, do the
75% math in the terminal, write one row per model. Never copy a trio from
another model — a 131k envelope around a 49k model truncates context and
breaks auto-compact, and the failure looks like model stupidity rather than
config.

## Env scope pitfall

`env` in Claude Code settings affects the `claude` process ONLY, never the
already-running `ollama serve` process. Server-side behavior (KV-cache type,
effective default context) is owned by the server's own environment:

- Inspect it with `ps eww -p <serve-pid>` split on spaces, grepping `OLLAMA_`.
- Trace mystery vars with `launchctl getenv <NAME>` plus shell-rc grep — a
  value that survives fresh launches with no user config behind it is likely
  the app's own built-in default, so stop hunting once launchd, rc files,
  and agents are ruled out.
- For the macOS GUI app, shell exports do not propagate — use
  `launchctl setenv <NAME> <value>` then reopen the app (lasts until reboot;
  re-apply after restart or automate it).

## Native multi-model list

`modelPicker` (User scope, needs CLI v2.1.242+ — confirm with `claude --version`, since the IDE extension can bundle its own older copy) is the in-file `/model`
lineup: `{replaceBuiltInOptions, options: [{model, label, description}]}`.
Put the ctx/compact/out numbers in each row's description so models are
distinguishable at pick time. `replaceBuiltInOptions: true` hides the
built-in Anthropic lineup when every request routes elsewhere anyway. Do not
add an `availableModels` allowlist for custom gateway IDs — its matching
semantics are built for Anthropic families and can silently narrow or reject
rows, while `modelPicker` alone is sufficient for the lineup.

Do NOT use the native `autoCompactWindow` key for sub-100k models — it is
specced 100,000–1,000,000 tokens, so the env var stays the vehicle for the
75% rule on smaller windows.

Validate structural edits with `claude doctor` (zero settings errors), a
JSON parse plus trailing-newline check, and asserts on the live file (model,
trio values, picker count) instead of eyeballing — scripts that rewrite the
file must preserve the newline or every run dirties the diff.

## Multi-provider switching

Claude Code talks to exactly one `ANTHROPIC_BASE_URL` at a time, so each
provider is a full-profile rewrite: base URL, auth token, trio, and picker
lineup together. Switching back must restore all four — verify both
directions with `--no-launch` runs before declaring done.

- Server-only keys (e.g. `OLLAMA_CONTEXT_LENGTH`) get popped on remote
  profiles and re-set on local ones; leaving a stale one is harmless but
  confusing, so don't leave it.
- Read daemon-minted credentials from the daemon's own key file at switch
  time (e.g. the proxy's `api-keys.json`) — the file is the source of truth
  and survives key rotation without you ever handling the value.
- Remote/cloud rows get a larger max-out (they are not VRAM-bound); local
  rows keep each model's real `num_predict`.
- Add a pre-launch health guard for daemon-backed providers (curl the
  health endpoint; print the restart command on failure instead of failing
  mysteriously inside the session).
- Run provider daemons under a LaunchAgent (RunAtLoad + KeepAlive) so
  selection never implies activation — but verify `state = running` plus an
  HTTP health check after install, since a bound-but-dead port fails silently.

## Solo-load pairing on 16GB hosts

Claude Code serves exactly one local model at a time, so pair a second local as a sequential alternate, never a parallel load: cap its trio below its max (e.g. ctx 16384, compact 12288, out 2048 for a 7B coder) to shrink KV, keep the daily driver at 48k rather than 96k while pairing, and evict all non-target locals in the switch script before rewriting settings (`for m in <locals>; do [[ "$m" == "$MODEL" ]] || ollama stop "$m" ...; done`). Back up `settings.json`, the switch script, and the picker lineup before editing, and verify both switch directions with `--no-launch` plus `ollama ps` (target absent until launch, others evicted).

## Free-tier remotes (Zen-style gateways)

- Confirm the servable set with `GET /v1/models` and one tiny inference
  probe per claim — catalog listings, proxy tables, and live servability are
  three different things, and a model can sit in the catalog while 500ing in
  both dialects or being allowlist-rejected by the proxy.
- A `429` with a free-tier message on multiple models over minutes is
  upstream saturation, not local misconfiguration — probe once, back off
  once, then stop and report; a second 429 on a different model is the
  verdict, not a cue for a third probe, and hammering burns the shared pool.
- Never quote unpublished limits — when the provider publishes no per-model
  numbers, say so plainly and let the observed errors speak; invented quotas
  become load-bearing lies a future session will plan around.
- Expose ONLY free IDs in picker rows; keep paid IDs out of the config
  entirely so there is no spend path to stumble into.
- Mark unverified context numbers in the row description (conservative
  undershoot is safe: early compacts beat window overshoot) and record the
  source next to any claimed window.

## Secrets

API keys go to the OS keychain (`security add-generic-password`), injected
at switch time, never into settings files, scripts, or chat. Verify storage
by length, never by value.
