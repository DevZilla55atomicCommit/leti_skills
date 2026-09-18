---
name: hermes-claude-code-orchestration
description: "Orchestrate Hermes as planner and Claude Code as builder/worker with bidirectional communication via MCP and delegate_task."
version: 1.0.0
author: Alfred Kamisese
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    tags: [orchestration, multi-agent, claude-code, mcp, delegation]
---
# Hermes ↔ Claude Code Orchestration Pattern

This skill documents the architecture for using **Hermes as the orchestrator** and **Claude Code as the builder/worker**, with bidirectional communication.

## Architecture Overview

``` 
┌─────────────────────────────────────────────────────────────┐
│                    HERMES (Orchestrator)                    │
│  • Planning & task decomposition                            │
│  • Multi-agent coordination                                 │
│  • Persistent memory & skills                               │
│  • Gateway messaging (Telegram, Discord, etc.)              │
│  • Cron scheduling & kanban boards                          │
└──────────────────────┬──────────────────────────────────────┘
                       │
         ┌─────────────┴─────────────┐
         │                           │
    ┌────▼────┐               ┌───────▼──────┐
    │ MCP     │               │ delegate_task │
    │ Bridge  │               │ (spawn CC)    │
    └────┬────┘               └───────┬──────┘
         │                           │
    ┌────▼────┐               ┌───────▼──────┐
    │ Claude  │               │  Claude Code  │
    │ Code    │               │  (Worker)     │
    │ Client  │               │               │
    └─────────┘               └───────────────┘
```

## Two Communication Directions

### 1. Hermes → Claude Code (Orchestrator to Worker)

**Primary method: `delegate_task` with print mode**
```python
delegate_task(
    goal="Build auth module with JWT tokens",
    context="Project at ~/myapp. Use: claude -p --model claude-sonet-4.6:latest --dangerously-skip-permissions --output-format json --max-turns 10 --bare --workdir ~/myapp"
)
```

**Alternative: tmux interactive for multi-turn work**
```bash
# Hermes spawns tmux session
tmux new-session -d -s cc-build -x 140 -y 40
tmux send-keys -t cc-build 'cd ~/myapp && claude --dangerously-skip-permissions' Enter
# Handle dialogs, then send tasks via send-keys
# Monitor via capture-pane
```

**Multi-client watching (user observes from a second terminal such as VS Code):** tmux is server-side, so any terminal attaching with `tmux attach -t <session>` sees the same live pane. Give the watcher independent window sizing with a grouped session (`tmux new -s <session>-vscode -t <session>`) so a narrow panel doesn't shrink the main view — or set `tmux set -g aggressive-resize on`. Detach with `Ctrl-b d`, never by killing the pane. Dismiss a blocking Claude Code startup dialog with `Escape` (returns to shell) rather than `Ctrl-C`, which the dialog swallows.

### Interactive TUI Pitfalls (tmux-driven sessions)

- **Trust dialog defaults to refusal** — the startup highlight sits on `No, exit`, so a bare Enter aborts back to shell. Send Down, verify the `❯` moved via `capture-pane`, then Enter.
- **Verify prompt submission** — send-keys text with trailing Enter can sit in the compose buffer unsent; confirm empty input plus a working spinner via `capture-pane` before waiting, otherwise send Enter again.
- **Killing the last session kills the server** — chaining `kill-session` and `new-session` in one terminal call fails against the dead server; recreate the session in a follow-up call.
- **Stale `ANTHROPIC_API_KEY` triggers the dual-auth warning** — settings env carrying both the token and a real key warns at startup; keep only the credential in active use (backup first, never print values). Harmless when routed at local Ollama, billing-breaking on cloud.

### 2. Claude Code → Hermes (Worker to Orchestrator)

**Method: Hermes MCP Server + Claude Code MCP Client**
```bash
# Terminal 1: Start Hermes MCP server
hermes mcp serve

# Terminal 2 (Claude Code): Connect to Hermes
claude mcp add hermes -- hermes mcp serve
```

Claude Code can then call Hermes tools:
- `conversations_list`, `messages_send` — communicate via gateway
- `delegate_task` — spawn sub-agents
- `terminal`, `read_file`, `write_file` — file operations
- `cronjob` — schedule tasks

## Skill Availability Across Runtimes (verify before delegating)

A skill installed for the CLI is not automatically visible to the Desktop app (separate managed runtime, own toggles) — and a bare skill name may not resolve where the namespaced `plugin:skill` form does. An unresolvable skill name fails silently: the worker claims it lacks the skill and skips that phase. Never write prompts that depend on a skill name without probing first:
1. Enumerate: `claude -p "List every skill available to you right now. Reply with ONLY a comma-separated list."` — confirm the exact `plugin:skill` name appears.
2. Sentinel probe: `claude -p "Use the <plugin:skill> skill. Quote back its <unique section> verbatim. If you do not have it, say SKILL NOT FOUND."` — a plausible-sounding description is a hallucination; only a verbatim quote of content unique to that skill counts as resolved.
3. If the bare name returns NOT FOUND, retry namespaced — then write all downstream prompts using the form that resolved, with a fallback line ("if the name fails to resolve, continue from <vendored doc> and note it in your report") so one missing skill degrades instead of skipping a phase.
4. Re-probe on EACH runtime that will execute the work — CLI-verified never transfers to the Desktop app.

Portable install mechanism is the plugin marketplace (recipe: `references/plugin-marketplace-packaging.md`): registry repo with `.claude-plugin/marketplace.json`, one `plugins/<name>/` dir per plugin with `.claude-plugin/plugin.json` + `skills/<skill>/SKILL.md`. Legacy single-file `~/.claude/skills/*.md` entries are CLI-only — never copy those files as the install mechanism.

## Ollama Backend Critical Configuration

When Claude Code uses Ollama (common in offline/local setups):

### `~/.claude/settings.json`
```json
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "ollama",
    "ANTHROPIC_API_KEY": "",
    "ANTHROPIC_BASE_URL": "http://localhost:11434"
  },
  "model": "qwen3.5:9b",
  "available_models": [
    "claude-sonet-4.6:latest",
    "claude-opus-4.8:latest",
    "qwen3.5:9b",
    "qwen3.5:4b-mlx",
    "gemma4:e4b-mlx",
    "gemma4:12b-mlx"
  ]
}
```

### Model Selection Rules

| Task Type | Model | Flags |
|-----------|-------|-------|
| Complex coding | `claude-sonet-4.6:latest` | `--max-turns 10 --bare` |
| Heavy reasoning | `claude-opus-4.8:latest` | `--max-turns 15 --bare` |
| Fast/lightweight | `qwen3.5:9b` | `--max-turns 3 --bare` |

**NEVER use aliases `sonnet`, `haiku`, `opus` — they don't exist in Ollama.**

### Print Mode Optimization for Ollama

```bash
# Template for reliable execution
claude -p "YOUR TASK" \
  --model claude-sonet-4.6:latest \
  --dangerously-skip-permissions \
  --output-format json \
  --max-turns 10 \
  --bare \
  --workdir /path/to/project
```

- `--bare`: Skips hooks/plugins/MCP discovery (critical for speed)
- `--output-format json`: Structured result parsing
- `--max-turns`: Prevents runaway loops
- Test model first: `ollama run claude-sonet-4.6:latest "test"`

### Local 9B Sampling for Tool-Use (Ollama)

Cold, penalty-heavy sampling makes small reasoning models ruminate without ever emitting tool calls. When a local 7–14B session thinks for minutes with zero tool calls and ample context remaining, check the Modelfile before anything else:
- `temperature 0.4` over 0.2 — near-zero temperature collapses the distribution onto continued reasoning instead of low-probability action tokens.
- `top_k 20`, `top_p 0.85` — narrow the field without freezing it.
- `presence_penalty 0.6` over 1.5 — high presence distorts rigid tool-call syntax; keep repeat_penalty ≈ 1.2.
- Keep `num_ctx` at what RAM actually fits (KV math in the Ollama troubleshooting skill); a window the machine can't serve buys nothing.

### Context Trio Parity Check

Claude-side accounting must match the serving side, or the session hits phantom limits: `OLLAMA_CONTEXT_LENGTH` = `CLAUDE_CODE_MAX_CONTEXT_TOKENS` = the model's loaded `num_ctx` (confirm via `ollama ps` CONTEXT column), and `CLAUDE_CODE_AUTO_COMPACT_WINDOW` at the intended fraction. A model field switched without its trio shadows the real window (e.g., 96k model on 48k accounting caps the session at half capacity).

### Compact-Tuning Precedence

Shell-exported `CLAUDE_CODE_AUTO_COMPACT_WINDOW` / `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` beat `settings.json` env for new launches (same layered setup on every machine); running sessions keep old behavior until restarted. Verify in a fresh session with bare `/autocompact` — it must cite the env-var window, not a model default.

### ⚠️ Print Mode Conflict with Running Interactive Instance (Critical)

**When another interactive Claude Code instance is running** (e.g., user's terminal on `s002`), `claude -p` **hangs indefinitely** due to shared resource deadlock (SQLite session DB, lock files).

**Additional mitigation:** Set `NO_CLAUDE_SESSION_HOOK=1` in the environment if you must run `claude -p` in contexts where another interactive session might be active, and always verify `~/.claude/.session.lock` is absent before launching.

**Permanent fix:** When launching Hermes, add `--no-session-persistence` flag to print-mode commands to force isolated execution. **Also** set `NO_CLAUDE_SESSION_HOOK=1` in the environment if you must run `claude -p` in contexts where another interactive session might be active, and always verify `~/.claude/.session.lock` is absent before launching.