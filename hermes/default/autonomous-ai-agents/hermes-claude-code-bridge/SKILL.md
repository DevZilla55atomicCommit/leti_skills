---
name: hermes-claude-code-bridge
description: "Bidirectional integration patterns between Hermes Agent (orchestrator) and Claude Code (worker) via MCP and process spawning"
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [hermes, claude-code, mcp, orchestration, multi-agent, bridge]
    related_skills: [hermes-agent, claude-code, native-mcp]
---

# Hermes ↔ Claude Code Bridge

Integration patterns for using **Hermes as the orchestrator** and **Claude Code as the worker/builder** in a multi-agent workflow.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     HERMES (Orchestrator)                       │
│  • Planning, delegation, coordination, memory, skills           │
│  • Exposes tools via MCP server: conversations, approvals, msg  │
└──────────────────────────┬──────────────────────────────────────┘
                           │
              ┌────────────┴────────────┐
              ▼                         ▼
    ┌───────────────────┐     ┌───────────────────┐
    │  CLAUDE CODE      │     │  CLAUDE CODE      │
    │  (Worker 1)       │     │  (Worker N)       │
    │  • Coding tasks   │     │  • Coding tasks   │
    │  • File ops       │     │  • File ops       │
    │  • Git workflows  │     │  • Git workflows  │
    └───────────────────┘     └───────────────────┘
```

Two communication directions, two different mechanisms:

| Direction | Mechanism | Use Case |
|-----------|-----------|----------|
| **Claude Code → Hermes** | MCP Client (`claude mcp add hermes`) | Claude Code calls Hermes tools (messaging, approvals, session mgmt) |
| **Hermes → Claude Code** | Process Spawning (`delegate_task` / tmux) | Hermes delegates coding tasks, gets structured results |

---

## Direction 1: Claude Code → Hermes (MCP Client)

### Setup

```bash
# In your running Claude Code terminal:
claude mcp add hermes -- hermes mcp serve
```

### What Hermes Exposes (10 tools)

| Tool | Purpose |
|------|---------|
| `conversations_list` | List active messaging conversations across platforms |
| `conversation_get` | Get detailed info about one conversation |
| `messages_read` | Read recent messages from a conversation |
| `attachments_fetch` | Extract images/media from messages |
| `events_poll` | Poll for new events since cursor |
| `events_wait` | Long-poll for next event |
| `messages_send` | Send message to platform conversation |
| `channels_list` | List available messaging channels |
| `permissions_list_open` | List pending approval requests |
| `permissions_respond` | Respond to approval (allow-once/allow-always/deny) |

### When to Use

- Claude Code needs to send notifications via Telegram/Discord/Slack
- Claude Code needs to check/respond to gateway approval requests
- Claude Code needs to read conversation history for context

---

## Direction 2: Hermes → Claude Code (Process Spawning)

### Pattern A: Print Mode (Recommended for Most Tasks)

Clean, non-interactive, structured JSON output.

```python
# In Hermes session or delegate_task:
delegate_task(
    goal="Build auth module with JWT tokens",
    context="""
    Project at ~/myapp. Use this exact command pattern:
    claude -p "Build auth module with JWT" \
      --model claude-sonet-4.6:latest \
      --dangerously-skip-permissions \
      --output-format json \
      --max-turns 10
    """
)
```

**Key flags:**
- `-p / --print` — Non-interactive, exits when done
- `--model <ollama-model>` — **Must use exact Ollama model name** (see Model Mapping below)
- `--dangerously-skip-permissions` — Auto-approve all tool use (required for automation)
- `--output-format json` — Structured result with session_id, cost, turns, etc.
- `--max-turns N` — Prevent runaway loops (5-10 for most tasks)

**Result structure:**
```json
{
  "type": "result",
  "subtype": "success",
  "result": "The analysis text...",
  "session_id": "75e2167f-...",
  "num_turns": 3,
  "total_cost_usd": 0.0787,
  "duration_ms": 10276,
  "stop_reason": "end_turn"
}
```

### Pattern B: Interactive TMUX (Multi-Turn Iterative Work)

For complex refactors, exploratory work, human-in-the-loop.

```bash
# Hermes starts worker
tmux new-session -d -s claude-work -x 140 -y 40 'cd ~/myapp && claude'

# Handle trust dialog (first time only)
tmux send-keys -t claude-work Enter

# Send initial task
tmux send-keys -t claude-work 'Refactor auth module to use JWT' Enter

# Monitor progress
tmux capture-pane -t claude-work -p -S -50

# Send follow-ups
tmux send-keys -t claude-work 'Now add unit tests' Enter

# Cleanup
tmux send-keys -t claude-work '/exit' Enter
tmux kill-session -t claude-work
```

---

## Critical Configuration: Ollama Model Mapping

**Your Claude Code is configured for Ollama** (`ANTHROPIC_BASE_URL: http://localhost:11434`). **This IS a custom provider setup** — you're already using the primary mechanism for third-party models! See `references/custom-providers.md` for the full pattern.

### The Trap

Claude Code's built-in aliases **don't work with Ollama**:

| Alias | Ollama Reality |
|-------|----------------|
| `--model sonnet` | ❌ 404 - tries Anthropic API |
| `--model haiku` | ❌ 404 - tries Anthropic API |
| `--model opus` | ❌ 404 - tries Anthropic API |

### Must Use Exact Ollama Model Names

```bash
# ✅ Works
--model claude-sonet-4.6:latest
--model claude-opus-4.8:latest
--model qwen3.5:9b
--model gemma4:12b-mlx
```

### Verify Available Models

```bash
ollama list
# Or via API:
curl -s http://localhost:11434/api/tags | jq '.models[].name'
```

### Add Aliases to ~/.claude/settings.json (Optional)

```json
{
  "model": "claude-sonet-4.6:latest",
  "available_models": [
    "claude-sonet-4.6:latest",
    "claude-opus-4.8:latest",
    "qwen3.5:9b"
  ]
}
```

---

### Critical Blocker: Workspace Trust

**Print mode (`-p`) HANGS indefinitely** if the workspace hasn't been trusted interactively first.

### Symptoms

- `claude -p "task" ...` runs for 60+ seconds, no output
- Stderr shows: `Ignoring permissions.allow entries: this workspace has not been trusted`

### Fix: One-Time Interactive Trust

```bash
# Run ONCE in each project directory:
cd ~/myapp && claude
# Press Enter for "Yes, I trust this folder"
# Type /exit
```

After this, print mode works instantly.

### Automation Workaround

For CI/automation where interactive trust isn't possible:

```bash
# Pre-trust via config (add to ~/.claude.json):
# "projects": {"/path/to/project": {"hasTrustDialogAccepted": true}}
```

---

### macOS Binary Path & CLI Flags (Session Finding)

**Claude Code binary location on macOS:**
```
/Users/alfredkamisese/Library/Application Support/claude/claude-code/<version>/claude.app/Contents/MacOS/claude
```
Version directory changes on update (e.g., `2.1.197`). Use `ls` to find current version.

**Critical CLI flag differences:**
| Flag | Status | Notes |
|------|--------|-------|
| `--workdir` | **REMOVED** | Does not exist in v2.x. Use `cd` in shell or `cwd` in `delegate_task` context |
| `--bare` | Works | Skips hooks/plugins/MCP discovery — critical for speed |
| `--dangerously-skip-permissions` | Works | Required for automation; print mode skips dialog entirely |
| `--model` | Works | **Must use exact Ollama model name** (e.g., `qwen3.5:9b`), not aliases |

**Print mode with Ollama often hangs 60-120s** on first invocation due to:
1. Model loading into VRAM/RAM
2. Workspace trust dialog (if directory not previously trusted)
3. SQLite lock contention if another instance runs

**Fix:** Pre-trust workspace once interactively: `cd /project && claude` → press Enter → `/exit`

---

## Anti-Pattern: Connecting to Existing Terminal

**You cannot reliably connect Hermes to an arbitrary running Claude Code terminal.**

| Approach | Works? | Why |
|----------|--------|-----|
| `claude mcp add` on running REPL | ❌ | REPL doesn't expose MCP server |
| tmux attach to existing session | ⚠️ Fragile | Race conditions, no clean API |
| PID attachment / ptrace | ❌ | Not supported, security issues |

### Correct Pattern: Spawn Fresh Workers

```python
# Each task gets a clean Claude Code instance
delegate_task(goal="Task 1", context="...")
delegate_task(goal="Task 2", context="...")
# Or tmux sessions with unique names
```

---

## Complete Workflow Example

### 1. Start Hermes MCP Server (persistent)

```bash
# Terminal 1: Hermes MCP server for Claude→Hermes calls
hermes mcp serve
```

### 2. Connect Claude Code to Hermes

```bash
# In your interactive Claude Code terminal:
claude mcp add hermes -- hermes mcp serve
```

### 3. Hermes Delegates to Claude Code Workers

```python
# In Hermes session:
# Quick one-shot task
result = delegate_task(
    goal="Add error handling to API calls in src/api.py",
    context="Project at ~/myapp. Model: claude-sonet-4.6:latest"
)

# Complex multi-turn task
# (spawn tmux session, monitor, send follow-ups)
```

### 4. Full Loop

```
User → Hermes (plans) 
      → Spawns Claude Code worker (executes) 
      → Gets JSON result 
      → User (reviews)
      → Claude Code (calls Hermes MCP for notifications/approvals)
```

---

## Troubleshooting Quick Reference

| Symptom | Cause | Fix |
|---------|-------|-----|
| `claude -p` hangs 60s+ | Workspace not trusted | Run `claude` interactively once, accept trust |
| `claude -p` times out (60-120s) | Local Ollama inference slow on M4 16GB | Use `--max-turns 1`, increase wrapper timeout to 180s+, or use faster model (`gemma4:12b` over `qwen3.5:4b`) |
| "model_not_found" error | Using `sonnet`/`haiku` aliases | Use exact Ollama name: `claude-sonet-4.6:latest` |
| "unknown option --workdir" | Wrong flag | Use `cwd` in delegate_task, or `cd` in tmux |
| MCP tools not appearing | Server not running | Start `hermes mcp serve` first |
| Permission prompts in print mode | Missing `--dangerously-skip-permissions` | Add the flag |

---

## References

- `references/ollama-model-mapping.md` — Complete model name mappings for your Ollama setup
- `references/custom-providers.md` — **Custom providers & LLM gateways (NVIDIA, vLLM, LiteLLM, Ollama, etc.)** — environment variables, modelOverrides, capabilities, gateway discovery
- `references/workspace-trust.md` — Deep dive on trust dialog automation
- `references/mcp-tool-reference.md` — Full Hermes MCP tool schemas
- `references/print-mode-conflict.md` — Print mode deadlock with running interactive instance