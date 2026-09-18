---
name: hermes-session-diagnostics
description: "Diagnose stuck, hung, and looped Hermes sessions. Log forensics, slash_worker lifecycle, zombie process cleanup, and session health triage."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [hermes, debugging, sessions, process-cleanup, diagnostics, troubleshooting]
    related_skills: [hermes-agent, debugging-hermes-tui-commands, systematic-debugging]
---

# Hermes Session Diagnostics

Diagnose and clean up Hermes sessions that are stuck in tool-call loops,
hung on incomplete tool calls, or accumulating zombie `slash_worker`
processes. Use this skill when someone reports a session that "isn't
finishing," "seems stuck," or "can't complete its task."

## When to Use

- A session has a very high message count (100+) and doesn't seem to be
  converging.
- The last assistant message was a tool call with no follow-up response.
- The user asks "why is session X stuck?" or "is this session in a loop?"
- Zombie `slash_worker` processes are accumulating on the system after
  days of use.

## Quick Triage

```text
1. session_search(session_id="<target_session>")  → read mode: get message count, last messages
2. Scroll the session end — if the last message is an assistant tool_call
   with no follow-up response → HUNG
3. If message count is very high (100+) and tool calls repeat the same
   pattern → LOOPED
4. ps aux | grep "<session_id>" → find the slash_worker PID
5. Check if the worker is still alive (Ss = idle, R = running)
6. Analyze agent.log for the session to identify the loop pattern
```

For the full log-forensics technique, loop-signature table, and
slash_worker lifecycle details, see:
`skill_view(name="hermes-session-diagnostics", file_path="references/log-forensics.md")`

## Identifying Loop vs Hung vs In Progress

| Symptom | Diagnosis | Action |
|---------|-----------|--------|
| 100+ messages, repeated identical or near-identical tool calls | **Looped** — model stuck in a cycle | Kill the worker; the model is not making forward progress |
| Last message is `assistant` with `tool_calls`, no subsequent `tool` or `assistant` response | **Hung** — tool call never returned or model timed out | Kill the worker; check if a background process died |
| Recent messages show varied tool calls making progress toward a goal | **In progress** — just slow | Do not interfere; wait or check if resources are constrained |
| `ResourceExhausted` warnings in agent.log | Rate-limited by provider (e.g. NVIDIA 32/32 worker limit) | Wait for the limit to clear or reduce concurrent sessions |

## Slash_worker Process Lifecycle

Each active Hermes session spawns a `slash_worker` process:

```text
process: tui_gateway.slash_worker --session-key <session_id> --model <model_name>
```

- **Normal:** Created when the session starts, persists while active,
  reaped when the session closes or the desktop app exits.
- **Zombie:** If a session ends abnormally (hang, crash, context window
  exhaustion, model timeout), the `slash_worker` can linger indefinitely
  with near-zero CPU.
- **Accumulation:** Systems running many sessions over days without
  restart can accumulate 5–10+ zombie workers, each consuming ~8–15 MB RSS.

### Finding All Workers

```bash
ps aux | grep "slash_worker" | grep -v grep
```

### Zombie vs Active

| Signal | Status |
|--------|--------|
| `Ss` status, near-zero CPU, session from hours/days ago | Zombie — safe to kill |
| `Ss` status, recent session (current chat) | Active — do not kill |
| `R` status, consuming CPU | Active and working — do not kill |

### Killing Workers

```bash
kill <PID>
# Verify:
ps aux | grep "slash_worker" | grep -v grep
```

**Always confirm the PID maps to the intended session before killing.**
Never kill the worker for the current session — check the session key
in `ps` output against the session ID of the active chat.

## Cleanup Checklist

1. List all `slash_worker` processes
2. Cross-reference session keys against `session_search` or known active
   sessions
3. Present a table of PID, session ID, age, recommended action
4. Ask the user which to kill (use `clarify` with choices)
5. Kill the selected PIDs
6. Verify remaining workers are only active sessions
7. Check if any background processes (e.g. TONY gateway, LiteLLM) need
   restarting

## Pitfalls

- **Never `re.search(content, re.DOTALL)` on the full `agent.log` file.**
  The file can be 100K+ lines. A full-file regex will hit the 300-second
  `execute_code` timeout. Use line-by-line streaming (`for line in
  f.readlines()`) with a session-ID filter instead.
- **Don't kill the current session's worker.** Always verify the session
  key in the `ps` output against the active chat session ID.
- **Check for background processes that caused the hang.** A session that
  called `terminal(background=true)` then `process(action='poll')` will
  hang if the background process was killed (SIGTERM) before returning.
  The session log will show the poll as the last action — the fix is to
  check whether the background process's output was captured before death.
- **Session_search truncates large sessions.** A session with 159 messages
  will show first 20 + last 10. Use `around_message_id` to scroll the
  middle sections.
- **A session being "stuck" doesn't always mean it's looped.** If it's
  just slow due to rate limits (`ResourceExhausted`), killing it loses
  work. Check agent.log for the error pattern before acting.

## Verification

After cleanup:

1. `ps aux | grep "slash_worker" | grep -v grep` should show only active
   sessions.
2. No `R`-state workers for sessions that should be idle.
3. If a gateway (TONY, LiteLLM) was part of the stuck session's work,
   verify it's still running or restart it:
   ```bash
   ps aux | grep "src/gateway/server" | grep -v grep
   ```
