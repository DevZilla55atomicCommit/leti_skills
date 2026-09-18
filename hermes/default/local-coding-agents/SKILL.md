---
name: local-coding-agents
description: "Drive local-model coding agents and delegated children."
---

# Local Coding Agents

Operating procedure for coding agents that run on local Ollama models or as
Hermes delegated children: how to start them, tell stuck from loading, make
them act, and keep their scaffolding intact.

## Driving an interactive local session

1. Budget cold start before judging: a 7B+ model needs minutes for GPU load
   plus first-turn prefill over the full skill stack before any token streams.
   Allow 10+ minutes and judge by tool-call evidence (Read/Bash/Edit calls in
   the transcript), never by elapsed time or spinner text.
2. When a session reads but never writes, poke once with an imperative naming
   the exact next write call ("proceed with the X edit now, no more reading").
   Open questions and status checks re-enter deliberation instead of ending it.
3. Step/command files must name the next physical action ("your next call must
   be Write/Edit/Bash, not another Read") — otherwise small models satisfy
   themselves with reconnaissance loops.
4. Config changes (settings.json, shell exports, daemon env) apply to NEW
   sessions only. Restart, then resume with `claude -c` to keep the transcript;
   verify the new behavior (e.g. `/autocompact` reporting the env-var window)
   before trusting it.

## Compaction tuning (local models)

- Confirm the serving context matches the assumed window before long runs
  (Ollama `num_ctx` vs the model's window — low defaults silently truncate
  and make compaction fire early against the wrong denominator); keep
  `MAX_OUTPUT_TOKENS` modest (~16k) since the compaction reserve scales
  with it — a value near the context size starves history.
- Full knob reference (trigger formula, precedence, per-model wrapper
  pattern, subagent return costs): `references/compaction-tuning.md`.

## Run discipline (anti-thrash on small windows)

- Tests run in phases, never the full suite in one go: P1 unit, list
  failures, stop, report — P2 one file per subagent with verify each —
  P3 e2e/integration only after unit is green. A full-suite turn floods
  context and forces compaction mid-run.
- Reads in ≤60-line chunks; grep before read, one file per subagent,
  returns ≤15 lines (verdict + files + gate output), one gate per turn.
- Stop assigning new work past 80% context — write state and stop instead.

## Delegation hygiene (Hermes delegate_task)

1. Verify `delegation.model` exists and carries >=64K context BEFORE fan-out
   (`hermes config get delegation.model`; below 64K the runtime refuses).
   A stale default fails every child identically — check this first when a
   whole batch 404s, not each task.
2. Prefer free cloud models for children (they spare local GPU/RAM for the
   main build); confirm paid-vs-free with one cheap probe before a fan-out,
   since billing failures surface per-child as 402s after dispatch.
3. Stop doomed children before relaunching replacements, or both generations
   contend for the same GPU/RAM.

## Scaffolding agents you intend to train

1. Mark direction docs READ-ONLY in both CLAUDE.md and the plan itself, naming
   the exact mutable files (usually only STATUS/CHANGELOG). Agents
   "helpfully" regenerate any doc the instructions leave unprotected —
   including replacing tuned tokens with generic defaults.
2. Commit the scaffolding baseline BEFORE the agent's first write, so any
   overwrite arrives as a reviewable diff instead of silent corruption.

## Verification probes (run, don't trust)

1. Test a statusline with piped sample JSON before installing it; confirm the
   context math against API usage records, not against the TUI's own line.
2. When the CLI says a registry model is missing, check the manifest API
directly (`.../v2/library/<name>/manifests/<tag>` over HTTPS): CLI 'not found'
can mean client/daemon lookup breakage while the model exists upstream.
