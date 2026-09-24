---
name: local-model-compaction
description: "Use to tune Claude Code compaction on local models."
---

# Local-Model Compaction (Claude Code v2.1.x, Ollama-routed runs)

Auto-compact fires earlier than the status-line percentage suggests when any
input is misread. Check them in this order.

## Trigger formula

`effective_window = min(CLAUDE_CODE_AUTO_COMPACT_WINDOW or tuned default, model window)` then `trigger = PCT_OVERRIDE clamped to ≤ default (~83%) of that window`, minus a hardcoded buffer (~33K tokens) that is NOT overridable.

- `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` (1–100) only ever LOWERS the trigger.
  Values above the default are silently ignored — there is no raise knob.
- The window var accepts a plain integer 100000–1000000 only. `500k` parses
  as `500` and clamps to the 100K floor without complaint.
- While the window var is set, the status line keeps measuring against the
  FULL model window — the displayed % no longer marks the real trigger.

## The output-reserve elephant

The compaction buffer scales with `CLAUDE_CODE_MAX_OUTPUT_TOKENS`. Setting
max-output near the context size (e.g. 128000 on a 131072 window) leaves ~zero
headroom, so compaction fires at ~50% no matter what the window says. Keep
max-output modest (16K is plenty for code); the buffer follows it down.
Diagnose via `/context` — a giant buffer line next to a small message line is
this bug, not a threshold bug.

## Precedence (silent winner takes all)

env `CLAUDE_CODE_AUTO_COMPACT_WINDOW` > `--autocompact` flag > `/autocompact`
command (`autoCompactWindow` in settings) — except a higher-priority managed
scope can preempt the command (never the flag). `/autocompact` with no args
reports the winning source in parentheses; if it says 'default for this model'
while the env var is set, the var isn't exported in that shell. Unrecognized
(gateway/local) model IDs compact at an assumed tuned window, not the real
one — pin the window explicitly for routed models.

## Disable pair

- `DISABLE_AUTO_COMPACT=1` — kills auto-compact, keeps manual `/compact`.
  The sane escape hatch.
- `DISABLE_COMPACT=1` — kills manual too; the session then deadlocks at 100%.
  Never set unattended.

## Verify (fresh session — running processes keep old env)

- `/autocompact` — must name your source, not 'default'. Some builds do
  nothing on bare `/autocompact` (no report at all) — fall back to `/context`.
- `/context` — breakdown by category; buffer vs messages tells reserve vs bloat.
- `ollama show <model>` must report the serving `num_ctx` assumed
  (Ollama defaults to 4K; an under-provisioned server truncates and every
  percentage becomes a lie). Confirm the LOADED model too (`GET /api/ps` →
  `context_length`) — runtimes silently load a different variant than the
  settings assume, and every percentage lies the same way.
- Managed/desktop runtimes may clamp, override, or hold stale copies of user
  settings — a session message quoting a setting back at you is not proof the
  value took effect. Confirm by behavior change after a fresh session, never
  by quotation alone.
- On memory-constrained hosts, rule out RAM exhaustion before tuning numbers:
  near-zero free pages means the session is starved, not hung — free memory
  and re-seat the harness before touching the window math.
- Prefer a fresh-session reboot from files over `/compact` — compaction is
  lossy, so surviving thrash via reboot beats surviving it via summarize.

## Per-model correctness (no native per-model knob exists)

Window and `MAX_CONTEXT_TOKENS` are flat globals. For multi-size rotations
(32k/48k/96k/128k aliases), wrap the launcher so each model sets its own
window — never 'pick the smallest window and forget it', which compacts the
big model at half capacity to babysit the small one.
