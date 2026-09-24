---
name: claude-code-local-backends
description: "Use when driving Claude Code on local backends via tmux."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
---

# Claude Code on Local Backends

Operating Claude Code pointed at `ANTHROPIC_BASE_URL=http://localhost:11434`
(or any third-party backend) via tmux. Complements the bundled `claude-code`
skill — the corrections below were verified against v2.1.x where behavior
diverged from it.

## Procedure

1. **Launch in tmux, then verify the session took.** `tmux send-keys -t <s> 'claude' Enter`, sleep, `capture-pane`. A bare `❯` with 0% context is healthy; anything else needs step 2 first.
2. **Trust dialog defaults to refusal.** The workspace-trust dialog opens with the
   cursor on "No, exit" — send `Down`, wait ~0.5s, confirm placement with a
   capture, then `Enter`. If the pane shows a shell prompt instead of Claude,
   the wrong row was accepted: relaunch and retry. Trust caches per directory.
3. **Set effort with the exact level name and confirm scope.** Valid levels are
   `low, medium, high, xhigh, max, ultracode, auto` — bare `ultra` is rejected
   (`ultracode` = xhigh + dynamic workflows). The confirmation states whether
   the level is session-only or saved as default; never assume persistence.
4. **Verify model field matches context trio after any model switch.** Read
   `~/.claude/settings.json`: `model` must agree with `OLLAMA_CONTEXT_LENGTH`,
   `CLAUDE_CODE_MAX_CONTEXT_TOKENS`, and `CLAUDE_CODE_AUTO_COMPACT_WINDOW`.
   A switcher that rewrites only the model name leaves stale trio values, and
   Claude then hits a phantom limit at a fraction of the real window while
   auto-compact guards the wrong line. Re-run the model switcher (it rewrites
   the trio) and re-read the file before launching test sessions.
5. **Keep exactly one dummy credential.** Local backends ignore auth, but the
   CLI warns when both `ANTHROPIC_AUTH_TOKEN` and `ANTHROPIC_API_KEY` are set.
   Keep the token the switcher manages, delete the stale key entirely — a blank
   `""` still counts as set and keeps the warning.
6. **Monitor for action, not just thinking.** `capture-pane` + grep for tool-use
   markers (`⏺`, `Bash(`, `Read(`). Minutes of spinner verbs (Swirling,
   Cogitating, Perambulating) at 0% context with zero tool calls means the
   model is cogitating instead of acting — a model/shim fault, not a prompt or
   config problem. Do not answer it with more context or higher effort; change
   the model or isolate the layer with a print-mode tool-forcing test.
7. **Diagnose stalled desktop sessions from the transcript, not the window.**
   The session JSONL lives at `~/.claude/projects/<cwd-with-/-as-dashes>/`,
   transcript newest by mtime. Count assistant `tool_use` content blocks vs
   `text` blocks and read `message.model` per turn: zero `tool_use` with text
   shaped like `{"name": "...", "arguments": {...}}` means the driving
   model is imitating tool calls instead of invoking them — a model-capability
   fault, not a prompt fault. Small code-only slots (7B-class, short output
   budgets) fail exactly this way. Fix by switching to a larger model and
   starting a fresh session; the poisoned session never recovers.

## Pitfalls

- Sending keystrokes while a turn is still generating queues or drops them —
  confirm each dialog/effort change in a fresh capture before proceeding, because silent non-acceptance looks identical to success.
- New sessions load settings at startup: config fixes never apply to an already
  running tmux session. Kill and recreate after any settings change.
- Desktop sessions bind the driving model at creation: switching the model in
  settings afterwards does not rescue an already-stuck session. Confirm the
  intended model is loaded (`ollama ps`), then abandon the old session and
  start fresh on the same folder — a stuck session that never emitted a
  `tool_use` block changed nothing on disk, so the folder is safe to re-run.
