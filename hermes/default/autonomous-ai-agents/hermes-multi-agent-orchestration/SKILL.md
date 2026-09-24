---
name: hermes-multi-agent-orchestration
description: "Run Hermes profiles as agents via tmux, kanban, cron."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [hermes, multi-agent, profiles, orchestration, tmux, delegation, kanban, cron, gateway]
    related_skills: [hermes-agent, kanban-orchestrator, subagent-driven-development, hermes-profile-sync-management]
---

# Hermes Multi-Agent Profile Orchestration

## Overview

In Hermes, **each profile IS a fully independent agent/bot** with isolated:
- `config.yaml` — model, providers, toolsets, MCP servers
- `.env` — API keys and secrets
- `skills/` — installed skills (built-in + hub)
- `memories/` — `MEMORY.md`, `USER.md`, `SOUL.md`
- `sessions/` — conversation history
- `cron/` — scheduled jobs
- `logs/` — agent + gateway logs

This skill covers the patterns for creating specialized profiles and orchestrating them as a multi-agent fleet.

## When to Use

- You need specialized agents for different domains (coding, research, creative, trading, etc.)
- You want parallel autonomous workers that survive restarts
- You need scheduled autonomous agents (cron)
- You want to route messages to different bots on Telegram/Discord
- You need to coordinate multiple agents via Kanban

---

## Creating Specialized Profiles

### Basic Patterns

```bash
# Fresh profile with bundled skills
hermes profile create forex-analyst

# Clone current profile's config, .env, SOUL.md, skills, memories
hermes profile create colorist --clone

# Full clone (all state except per-profile history)
hermes profile create web-dev --clone-all

# With description for kanban routing
hermes profile create creative-dir --clone --description "Storyboards, shot lists, camera theory"
```

### Recommended Specialized Profiles for Your Workflow

| Profile | Purpose | Key Config |
|---------|---------|------------|
| `forex-analyst` | Forex technical analysis, macro indicators, automated alerts | `toolsets: [web, terminal, file, skills, memory, cronjob]` |
| `colorist` | DaVinci Resolve grading, node workflows, LUT design | `mcp_servers.davinci-resolve.enabled: true` |
| `web-dev` | Next.js, React, TypeScript, Tailwind, Framer Motion | `toolsets: [web, terminal, file, code_execution, coding, skills, memory]` |
| `creative-dir` | Storyboards, shot lists, camera theory, lighting design | `skills: [videography, photography, davinci-resolve]` |
| `researcher` | Deep research, paper analysis, market data | `toolsets: [web, terminal, file, skills, memory, browser]` |

### Configure Each Profile

```bash
# Set model per profile
hermes -p forex-analyst config set model.default "openai/gpt-5.5"
hermes -p forex-analyst config set model.provider "openrouter"

# Enable specialized toolsets
hermes -p web-dev config set toolsets "[web, terminal, file, code_execution, coding, skills, memory]"

# Add MCP servers
hermes -p colorist config set mcp_servers.davinci-resolve.enabled true
```

---

## Orchestration Patterns

### Pattern A: Parallel tmux Workers (Long Autonomous Missions)

Use for **hours/days** of independent work with full tool access and interactive PTY.

```bash
# Backend agent
tmux new-session -d -s backend 'hermes -p backend-coder'
tmux send-keys -t backend 'Build REST API for user management' Enter

# Frontend agent
tmux new-session -d -s frontend 'hermes -p frontend-coder'
tmux send-keys -t frontend 'Build React dashboard for user management' Enter

# Cross-pollinate context
tmux capture-pane -t backend -p | tail -30
tmux send-keys -t frontend 'API schema from backend: ...' Enter

# Monitor
tmux capture-pane -t backend -p
tmux capture-pane -t frontend -p

# Cleanup
tmux send-keys -t backend '/exit' Enter && tmux kill-session -t backend
```

**When to use:** Long coding missions, independent feature work, when agents need full interactive terminal access.

**Key flags:** Use `-w` (worktree mode) when spawning agents that edit code — prevents git conflicts.

### Pattern B: `delegate_task` (Quick Parallel Subtasks)

Use for **minutes** of parallel work within a single conversation. Subagents share process but have isolated context.

```python
# From within a Hermes session
delegate_task(
    tasks=[
        {"goal": "Research GRPO papers and write summary", "context": "Focus on recent arxiv, technical depth"},
        {"goal": "Analyze forex EUR/USD technical setup", "context": "Daily timeframe, key levels, risk/reward"},
        {"goal": "Create DaVinci node template for teal-orange", "context": "Parallel nodes, CST workflow, skin protection"}
    ]
)
```

**When to use:** Quick research, analysis, or generation tasks that benefit from parallel fresh contexts.

**Limitation:** Not durable — if parent process exits, children are lost.

### Pattern C: Kanban Board (Durable Multi-Agent Collaboration)

Use for **multi-session, crash-survivable** work with human-in-the-loop and audit trail.

**Setup:**
```bash
# Initialize board (run once)
hermes kanban init

# Create specialist profiles first (Step 0 of kanban-orchestrator)
hermes profile list
```

**Decompose and route:**
```python
# Discover profiles first
profiles = terminal(command="hermes profile list")  # or kanban_list()

# Create parallel research lanes
t1 = kanban_create(title="research: forex macro indicators", assignee="forex-analyst", body="...")
t2 = kanban_create(title="research: DaVinci 20.2 new features", assignee="colorist", body="...")

# Synthesis depends on both
t3 = kanban_create(title="synthesize: cross-domain insights", assignee="creative-dir", body="...", parents=[t1, t2])

# Final deliverable
t4 = kanban_create(title="draft: weekly creative report", assignee="web-dev", body="...", parents=[t3])
```

**When to use:** Work that must survive crashes, needs human review, involves multiple specialists over days, or requires audit trail.

**Reference:** See `kanban-orchestrator` skill for full decomposition playbook.

### Pattern D: Cron Jobs (Scheduled Autonomous Agents)

Use for **recurring autonomous work** on a schedule.

```bash
# Daily forex digest at 9 AM
hermes -p forex-analyst cron add daily-digest "0 9 * * *" \
  --prompt "Summarize today's forex news, technical setups for major pairs, and risk events" \
  --skills research,market-analysis

# Weekly color grading tips
hermes -p colorist cron add weekly-tips "0 10 * * 1" \
  --prompt "Extract one DaVinci Resolve technique from recent Instagram reels and document as a skill" \
  --skills davinci-resolve,instagram-reels-pipeline

# Hourly system health check
hermes -p system-monitor cron add health-check "0 * * * *" \
  --prompt "Check disk space, GPU memory, Ollama status, and Hermes gateway health" \
  --skills devops/monitoring \
  --no-agent true \
  --script "health_check.sh"
```

**When to use:** Recurring research, monitoring, content generation, scheduled analysis.

### Pattern E: Gateway Profile Routing (Telegram/Discord Bots)

Run **one gateway process** serving multiple isolated bot personalities per channel/server.

**Config (`config.yaml`):**
```yaml
gateway:
  multiplex_profiles: true
  profile_routes:
    - name: "forex-bot"
      platform: telegram
      chat_id: "-1001234567890"
      profile: forex-analyst
    - name: "color-support"
      platform: discord
      guild_id: "1234567890"
      chat_id: "9876543210"
      profile: colorist
    - name: "dev-assistant"
      platform: discord
      guild_id: "1234567890"
      profile: web-dev
    - name: "creative-director"
      platform: telegram
      chat_id: "-1009876543210"
      profile: creative-dir
```

**Matching rules:** Most specific route wins (thread_id > chat_id > guild_id > platform-only).

**When to use:** Multiple communities/channels needing different bot personalities from a single gateway.

---

## Profile Management Commands

| Task | Command |
|------|---------|
| List profiles | `hermes profile list` |
| Switch default | `hermes profile use forex-analyst` |
| Show profile details | `hermes profile show forex-analyst` |
| Set description | `hermes profile describe forex-analyst --text "Forex specialist"` |
| Create wrapper alias | `hermes profile alias forex-analyst` → then run `forex-analyst` directly |
| Export profile | `hermes profile export forex-analyst -o forex.tar.gz` |
| Import profile | `hermes profile import forex.tar.gz --name forex-analyst-v2` |
| Delete profile | `hermes profile delete forex-analyst` |

---

## Cross-Profile Memory Sync

If you run profiles across multiple machines (Mac mini + MBP), sync memories but isolate configs:

```bash
# On each machine: exclude config.yaml from Syncthing
echo "config.yaml" >> ~/.hermes/profiles/.stignore

# Memories auto-sync via Syncthing
# Each machine keeps its own config.yaml with local Ollama endpoints, API keys
```

**Reference:** See `hermes-profile-sync-management` skill.

---

## Pattern F: Bot Mode (Desktop-Native Multi-Agent Chat)

**New in Hermes v0.21+** — Built into the Desktop app as a default-on plugin. Each profile becomes a **Bot** with:
- Persistent **canonical Bot Chat** (never forks, `/new` → `/compact`)
- **@mention handoffs** in any chat: `@colorist grade this clip`
- **Group chats** (2–6 bots, up to 3 rounds of turns per message)
- **Bot-initiated DMs** via `message_agent(target="coder", message="...")` tool
- **Cross-machine messaging** via Desktop relay (Settings → Connections) or `hermes peer`
- **Routines** = namespaced cron jobs `[bot:<name>] <routine>` landing in bot's own chat
- **Avatars, sections, hide/unhide** for roster management

### Bot Mode Quick Start

```bash
# 1. Create profiles with descriptions (for teammate roster)
hermes profile create creative-dir --clone --description "Creative Director — storyboards, shot lists, camera theory"
hermes profile create colorist --clone --description "DaVinci Resolve colorist — CDL, node trees, PowerGrades"
hermes profile create coder --clone --description "Code Architect — Next.js, React, TypeScript, APIs"

# 2. Open Desktop → Bots tab → right-click each → Edit Profile
#    Add Title, Description, Avatar (blob/geometric/uploaded/AI-generated)

# 3. Create group chat: right-click bot → Manage groups → New group
#    Add bots, name room (e.g., "Feature: Payment Refactor")

# 4. In group chat: @mention bots to trigger up to 3 rounds
#    @creative-dir @coder @reviewer Break down the payment refactor

# 5. Bot-to-bot DM (in canonical Bot Chat):
#    message_agent(target="coder", message="Implement retry logic per spec")
```

### Cross-Machine Bot Communication

| Path | Use Case | Setup |
|------|----------|-------|
| **Desktop Relay** | Human-driven, Desktop running | Settings → Connections (add SSH/remote/Cloud) |
| **`hermes peer`** | Always-on, no Desktop | `hermes peer add vps --url http://vps.lan:8377 --key $KEY` then `hermes peer dm vps/coder "task"` |

```bash
# Peer commands
hermes peer add spark --url http://spark.lan:8377 --key <API_SERVER_KEY>
hermes peer dm spark/researcher "Analyze this data"
hermes peer run spark --idempotency-key ticket-123 "Long task"
hermes peer status spark run_abc123
hermes peer stop spark run_abc123
```

### CLI Parity (Everything Works in Terminal)

| Bot Mode Action | CLI Equivalent |
|-----------------|----------------|
| Chat with a bot | `hermes -p <bot> chat` |
| Bot's files/skills/memory | `~/.hermes/profiles/<bot>/` |
| Routines | `hermes cron list` (jobs named `[bot:<name>] …`) |
| Create/inspect profiles | `hermes profile create`, `hermes profile list` |
| @mention in chat | Type `@botname message` in `hermes -p <bot> chat` |
| Group chat | Not directly in CLI (use Desktop) |

### Bot Mode Group Chat Creation (v0.21+)

**Desktop flow (the only way to create groups):**

1. Open **Bots tab** in Desktop sidebar
2. **Right-click a LOCAL bot** → **Manage groups** → **New group chat**
3. **Name** the group (e.g., `team`)
4. **Checkboxes appear** — check all desired members (2–6 bots)
5. **Create** — group exists with all members immediately

**Important:** You create the group *from a bot's context*, not as a standalone empty group. The bot you right-click becomes a member automatically.

**After creation:**
- Group row appears in Bots pane with member count: `team (5)`
- Click group row → opens `Group: <name>` shared room
- Each bot gets a persistent `Group: <name>` session in their history
- In the room: `@team` addresses all, `@botname` addresses one
- Up to **3 rounds** of turns per message, 10 messages/turn cap

**Pre-seeding group history via CLI (optional):**
```bash
# Run once per bot to establish group context before Desktop creation
for bot in apollo helios hephaestus hestia kairos; do
  hermes -p "$bot" chat -q "GROUP INIT: You are now part of the 'team' group. Awaiting tasks."
done
```

**Common pitfall:** Right-clicking the *group row* (not a bot) shows no "Manage groups" — must right-click a bot row.

---

## Quick Reference: Choosing Your Pattern

| Need | Pattern | Durability | Isolation |
|------|---------|------------|-----------|
| Quick parallel research | `delegate_task` | Process-life | Context-only |
| Long coding missions | tmux workers | Hours/days | Full process |
| Multi-day collaboration | Kanban | Indefinite | Full profile |
| Scheduled recurring work | Cron | Indefinite | Full profile |
| Chat platform bots | Gateway routing | Indefinite | Full profile |
| **Desktop multi-bot chat** | **Bot Mode** | **Indefinite** | **Full profile** |
| **Cross-machine bot chat** | **Bot Mode + peer** | **Indefinite** | **Full profile** |

---

## Pitfalls to Avoid

1. **Inventing profile names** — Kanban dispatcher silently fails unknown assignees. Always `hermes profile list` first.
2. **Forgetting `-w` flag** — Without worktree mode, parallel code-editing agents conflict on git.
3. **Over-using `delegate_task` for long work** — Children die with parent. Use tmux or cron for durability.
4. **Cloning `.env` with API keys** — `--clone` copies `.env`. Rotate keys or use per-profile secrets.
5. **Not setting descriptions** — Kanban orchestrator uses descriptions to route tasks. Add `--description` at creation.
6. **Running gateway without `multiplex_profiles: true`** — Profile routing is ignored entirely without it.
7. **Ghost `delegation.model`** — every child boots on this model; if it names an ID that isn't installed or reachable, all children fail in seconds with 404. Verify with `hermes config get delegation.model`, probe it with one cheap call, fix with `hermes config set delegation.model <working-id>`. Children also require ≥64K context — smaller-window models are rejected at dispatch. Probe cloud IDs the same way before fanning out; paid-only models fail fast with 402.
8. **Research children that present plans instead of results** — planning skills hijack research dispatches into asking for approval. Instruct in context: deliver the final report directly, no plan, no approval ask.
9. **Handing files to weaker agents** — mark direction docs READ-ONLY in their instructions, commit a baseline before delegating so overwrites show as diffs, and add an anti-loop line ("once you have read the file, your next call must be Write/Edit/Bash, not another Read").

---

## Related Skills

- **`hermes-agent`** — Core Hermes configuration, spawning, surfaces
- **`kanban-orchestrator`** — Deep decomposition playbook for Kanban routing
- **`subagent-driven-development`** — Two-stage review pattern for `delegate_task` workflows
- **`hermes-profile-sync-management`** — Multi-machine profile sync with config isolation

---

## References

- `references/profile-templates.md` — Ready-to-use profile configurations for common roles
- `references/ad-hoc-tmux-agents.md` — Quick tmux agent setup without profile creation (same profile, role prompts)
- `references/orchestration-comparison.md` — Detailed comparison matrix of all patterns
- `references/gateway-routing-examples.md` — Complete gateway config examples for Telegram/Discord/Slack