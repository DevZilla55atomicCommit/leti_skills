---
name: claude-live-worker
description: "Spawn and manage live Claude Code workers via tmux for real-time monitoring"
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [claude-code, tmux, live-worker, orchestration]
    related_skills: [claude-code, hermes-agent]
---

# Live Claude Code Worker Pattern

Spawn persistent tmux sessions running Claude Code that you can attach to and monitor in real-time. Perfect for complex multi-turn tasks where you want to watch the agent work and steer it.

## Prerequisites

- tmux installed (`brew install tmux`)
- Claude Code CLI installed and authenticated
- `--dangerously-skip-permissions` flag for unattended operation (use only in trusted directories)

## Quick Commands

```bash
# Start a live worker session
hermes claude-live start my-task

# Attach to watch live (detach with Ctrl+B, D)
hermes claude-live attach my-task

# Send a task to the worker
hermes claude-live send my-task "Build a REST API with FastAPI"

# Check status without attaching
hermes claude-live capture my-task

# List all live workers
hermes claude-live list

# Stop a worker
hermes claude-live stop my-task
```

## Manual tmux Commands (what the wrapper does)

### Start a worker
```bash
SESSION_NAME="claude-live-my-task"
tmux new-session -d -s "$SESSION_NAME" -x 160 -y 50 \
  'cd /path/to/project && claude --dangerously-skip-permissions'
```

### Handle first-run dialogs (trust + bypass permissions)
```bash
# Wait for startup, then accept trust dialog (Enter = Yes)
sleep 4 && tmux send-keys -t "$SESSION_NAME" Enter

# Accept bypass permissions dialog (Down + Enter = "Yes, I accept")
sleep 2 && tmux send-keys -t "$SESSION_NAME" Down && sleep 0.3 && tmux send-keys -t "$SESSION_NAME" Enter
```

### Send a task
```bash
tmux send-keys -t "$SESSION_NAME" "Build a FastAPI auth module with JWT" Enter
```

### Monitor progress (non-attached)
```bash
tmux capture-pane -t "$SESSION_NAME" -p -S -50
```

### Attach to watch live
```bash
tmux attach -t "$SESSION_NAME"
# Detach: Ctrl+B, then D
```

### Clean up
```bash
tmux kill-session -t "$SESSION_NAME"
```

## Integration with Hermes delegate_task

For fire-and-forget tasks, use `delegate_task` (Pattern 1). For interactive live monitoring, use this tmux pattern (Pattern 2).

```python
# Pattern 1: delegate_task (headless, returns JSON)
delegate_task(
    goal="Build auth module",
    context="Use: claude -p --model qwen3.5:4b-mlx --dangerously-skip-permissions --output-format json --max-turns 10"
)

# Pattern 2: tmux live worker (interactive, you watch)
# Hermes spawns via terminal tool, you tmux attach
```

## Worker Lifecycle

```
START → [Trust Dialog] → [Bypass Permissions] → READY
                                    ↓
                              SEND TASK → WORKING
                                    ↓
                              CAPTURE/ATTACH → MONITOR
                                    ↓
                              SEND FOLLOW-UP → WORKING
                                    ↓
                              /exit → STOPPED
```

## Safety Notes

- Only use `--dangerously-skip-permissions` in directories you own/trust
- Workers persist until explicitly killed — clean up with `tmux kill-session`
- Each worker needs its own tmux session name
- For parallel workers: `tmux new-session -d -s worker-1 ...`, `tmux new-session -d -s worker-2 ...`

## Directory Structure

Workers run in a specific working directory. Always specify `cd /your/project` in the tmux command or send `cd /path` as first command.

## Troubleshooting

| Issue | Fix |
|-------|-----|
| "Session not found" | Check `tmux list-sessions` |
| Stuck on dialog | Send correct keys: Enter for trust, Down+Enter for bypass |
| Output garbled | Use `capture-pane -p -S -100` for more history |
| Can't attach | Ensure you're not already attached elsewhere |
| Process died | Check `tmux capture-pane -t session -p` for errors |