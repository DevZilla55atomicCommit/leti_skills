---
name: overnight-agent-run
description: "Use for unattended overnight agent runs in tmux."
---

# Overnight Agent Run

Unattended agents don't skip work — they either idle on blockers, die on context
limits, or lower the bar and report green. This protocol converts all three
into a readable morning diff plus an honest blocker note.

## Preflight (before leaving)

1. Gates first: the task file must contain explicit, machine-checkable
   acceptance criteria (commands + expected outputs), not vibes.
2. Cap scope: assign implementation tasks only. Hold review, tests-signoff,
   and commits for the morning (e.g. work T-C..T-F, leave review/test/commit).
3. Permissions: `settings.local.json` must pre-allow the run's tools
   (`Bash(npm run *)`, `npm test`, `git add/*` as needed); keep deny narrow
   (`Bash(rm -rf *)`, secrets). Deny beats allow — a blanket `Bash` deny
   silently strangles the run.
4. tmux: run in a named session, report `tmux attach -t <name>` per the
   shared-view convention so the user can follow along.

## Leash prompt (send into the session)

```
Work <SCOPE> only. Commit nothing.
Per task: show verify output. If blocked >15 min or a
verify gate fails twice, write BLOCKED.md with state +
next step, then STOP. Do not mark anything done that
isn't verified. Leave <REVIEW/TEST/COMMIT> for morning.
```

## Steering protocol (send-keys must be verified, never fire-and-forget)

Pasted text can park as queued messages instead of submitting — especially
if it lands during compaction, restart, or a busy turn. After every steer:

1. `send-keys -t <session> 'text' Enter`, wait 15–20s.
2. `capture-pane -e -p` and confirm ALL of: composer empty (no queued
   text), activity signal (spinner, token count rising, or agent task line).
3. If `Press up to edit queued messages` or the text still sits in the box:
   send Enter again, wait, re-check. Repeat until working.
4. Never assume sent from text-appears-in-pane. Submitted = session acts.

## Forcing delivery when running or compacting

A steer sent mid-turn parks as queued text and can die there — especially if
compaction fires while it waits (the queue does not reliably survive it) or
the turn is hung (frozen spend/time/tokens + lama-server idle or spinning
with no UI update for 5+ min = runaway generation, never completing).

Escalation ladder, one rung at a time with verification after each:
1. Enter — flushes the queue when the turn ends. Re-check: composer empty +
   context growth + spend/time moving = delivered.
2. Still parked (`queued` tag or full composer, frozen counters)? Enter again
   after 30–60s. Compaction in flight freezes the display; patience first.
3. Frozen across 5+ min with no inference (or endless inference, no output)?
   ONE Ctrl-C — cancels the hung turn, process survives. The queue then
   flushes into the transcript. Verify the text appears as a submitted user
   message (`❯` + text in scrollback), not just composer content.
4. If a compact fired on top of delivery, the instruction may survive only in
   the summary. Confirm by behavior on the next relevant action; if ignored,
   resend a one-liner in the fresh context. Never stack duplicate long steers
   blindly — one short resend max.
5. Keep steers SHORT when context is >60% or compaction is near: long
   messages parked pre-compact are the ones most likely to be lost.

## Morning verification (never trust overnight green)

1. `tmux capture-pane` the session; check for BLOCKED.md first.
2. Re-run the gates yourself (typecheck, lint, test, build) — do not accept
   the agent's transcript as evidence.
3. `git status/diff`: confirm scope discipline (no surprise files, no
   weakened tests, no skipped baselines).
4. Only then allow review/test/commit phases.
