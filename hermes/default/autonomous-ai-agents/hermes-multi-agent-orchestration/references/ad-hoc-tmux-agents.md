# Ad-Hoc Tmux Agents — Quick Setup Without Profile Creation

Reference for `hermes-multi-agent-orchestration` skill.

---

## When to Use This Pattern

Use this **instead of creating specialized profiles** when:
- You need agents *now* for a session or day
- Agents will use the **same toolset/MCP config** (default profile is fine)
- You want to test a role before committing to a profile
- The task is time-boxed (hours, not days/weeks)
- You don't need separate API keys, models, or memory isolation

---

## Pattern: Default Profile + Role Prompt

```bash
# 1. Create tmux sessions (one per agent)
tmux new-session -d -s hermes-research -x 120 -y 40 'hermes'
tmux new-session -d -s hermes-creative -x 120 -y 40 'hermes'
tmux new-session -d -s hermes-dev -x 120 -y 40 'hermes'

# 2. Wait for Hermes startup (8-10s typically)
sleep 10

# 3. Send role-defining prompt to each
tmux send-keys -t hermes-research 'You are the Research Agent. Your role: Forex analysis (EUR/USD, GBP/USD), California polling data, market research, daily briefings. Use terminal tools for data fetching. Confirm your mission.' Enter

tmux send-keys -t hermes-creative 'You are the Creative Agent. Your role: DaVinci Resolve workflows, color grading, Instagram Reels processing, video editing. You have davinci-resolve-mcp and computer-use tools. Confirm your mission.' Enter

tmux send-keys -t hermes-dev 'You are the Dev/Automation Agent. Your role: Code tasks, script maintenance, vault management, GitHub workflows, cron jobs. Confirm your mission.' Enter
```

---

## Verification

```bash
# Check all sessions running
tmux list-sessions

# View any agent's output
tmux capture-pane -t hermes-research -p
tmux capture-pane -t hermes-creative -p
tmux capture-pane -t hermes-dev -p
```

---

## Sending Follow-Up Tasks

```bash
# Research task
tmux send-keys -t hermes-research 'Analyze EUR/USD technical setup for today using macro indicators' Enter

# Creative task  
tmux send-keys -t hermes-creative 'Open current DaVinci project and suggest node structure for cinematic teal-orange grade' Enter

# Dev task
tmux send-keys -t hermes-dev 'Check Obsidian vault for broken links and generate report' Enter
```

---

## Trade-offs vs Profile-Based Agents

| Aspect | Ad-Hoc (This Pattern) | Profile-Based |
|--------|----------------------|---------------|
| Setup time | ~30 seconds | ~2-5 min (create + config) |
| Isolation | Context-only (shared config) | Full (config, .env, skills, memory) |
| Persistence | Dies with tmux session | Survives restarts |
| API keys | Shared | Per-profile |
| Model | Shared | Per-profile |
| MCP servers | Shared | Per-profile |
| Memory | Shared | Isolated |
| Best for | Day tasks, experiments | Long-term specialists |

---

## Graduating to Profiles

If an ad-hoc agent proves valuable long-term:

```bash
# 1. Create profile from current (clones config, skills, memories)
hermes profile create forex-analyst --clone --description "Forex specialist"

# 2. Customize
hermes -p forex-analyst config set model.default "openai/gpt-5.5"

# 3. Future: spawn with profile
tmux new-session -d -s hermes-research 'hermes -p forex-analyst'
```

---

## Pitfalls Specific to This Pattern

1. **No `-w` flag needed** — These agents don't edit code, so worktree mode isn't required. Only add `-w` if the agent will `git commit`.

2. **Startup wait is critical** — `sleep 8-10` before first `send-keys`. Hermes needs time to initialize MCP connections and load skills.

3. **Shared memory** — All ad-hoc agents share `~/.hermes/memories/`. They'll see each other's context. Use profiles for true isolation.

4. **Gateway routing won't distinguish them** — All show as "default" profile in Telegram/Discord routing. Profiles required for multi-bot gateway.

5. **Kill cleanly** — `tmux kill-session -t hermes-research` sends `/exit` gracefully. Avoid `tmux kill-server`.

6. **Verify working state after every steer, not text in the pane** — a fullscreen TUI can display your message while it sits unsubmitted in the queue, so text-present is not proof of delivery; confirm the spinner runs and token/time counters advance.

7. **Flush queued messages with Enter on an idle prompt, then re-check** — input sent during a busy/compacting window parks in the queue ('press up to edit queued messages') instead of submitting, and a second steer piles behind the first.

---

## Steering Fullscreen-TUI Agents (Claude Code)

Plain `capture-pane -p` returns blanks against fullscreen TUIs — the screen lives in escape sequences. Read with `-e` and strip ANSI:

```bash
tmux capture-pane -t <session> -e -p -S -60 | sed 's/\x1b\[[0-9;?]*[a-zA-Z]//g' | grep -v '^$' | tail -25
```

Shared-view rule: whenever you set up a run the user will watch, report the session name plus the exact attach command (`tmux attach -t <name>`) and the detach key (`Ctrl-b d`) in the same message — the user follows along from any terminal, including VS Code's.

---

## Example: Full Day Fleet Setup

```bash
#!/bin/bash
# save as ~/.hermes/scripts/spawn-daily-fleet.sh

SESSIONS=("hermes-research" "hermes-creative" "hermes-dev")

for s in "${SESSIONS[@]}"; do
  tmux new-session -d -s "$s" -x 120 -y 40 'hermes'
done

sleep 10

tmux send-keys -t hermes-research 'You are Research Agent: Forex, polling, market briefings. Confirm.' Enter
tmux send-keys -t hermes-creative 'You are Creative Agent: DaVinci, Reels, video editing. Confirm.' Enter
tmux send-keys -t hermes-dev 'You are Dev Agent: Code, vault, GitHub, cron. Confirm.' Enter

echo "Fleet spawned. Check with: tmux list-sessions"
```