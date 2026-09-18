# Integration Patterns: Tool Type → Your Stack

Mapping table for how different external tool types integrate into your local AI orchestration stack.

## Your Stack Layers

| Layer | What Lives Here | How It's Invoked |
|-------|-----------------|------------------|
| **Hermes Skills** | Python/JS skills in `~/.hermes/skills/` | `skill_view()`, `delegate_task()` |
| **MCP Servers** | Configured in Hermes `config.yaml` → `mcp.servers` | Native tool calls from any agent |
| **Claude Code** | Plugins via marketplace or `--mcp-config` | Slash commands, hooks, MCP tools |
| **Local LLMs** | Ollama / llama.cpp / vLLM endpoints | `litellm` proxy or direct HTTP |
| **Cron/Background** | Hermes `cronjob` tool + `terminal(background=True)` | Scheduled or event-driven |
| **Obsidian Vault** | Markdown files in `TamaZila Obsidian Vault/` | `obsidian` skill read/write/search |

---

## Tool Type → Integration Pattern

### 1. Python Package with SDK (e.g., `cognee`, `cognee-mcp`)

| Your Layer | Pattern |
|------------|---------|
| **Hermes Skill** | ```python\nimport cognee\nasync def my_skill():\n    await cognee.remember("data")\n    results = await cognee.recall("query")\n``` |
| **MCP** | Run `cognee-mcp` as MCP server → add to Hermes `mcp.servers` |
| **Claude Code** | Install plugin: `claude plugin install cognee-memory@cognee` |
| **Cron** | `cognee-cli remember "daily note"` in cron job |

**When to use which:**
- Skill: Need to compose with other skills, use Hermes memory, delegate subagents
- MCP: Want universal access from any MCP client (Cursor, Cline, Roo, etc.)
- Cron: Simple scheduled ingestion (daily logs, weekly summaries)

---

### 2. CLI Tool Only (e.g., `loop-init`, `loop-audit`, `loop-cost`)

| Your Layer | Pattern |
|------------|---------|
| **Hermes Skill** | Wrap in Python: `subprocess.run(["loop-audit", "."])` |
| **Cron** | `cronjob create --schedule "0 8 * * 1-5" --script "loop-audit.sh"` |
| **MCP** | Only if tool has `--mcp` flag or you write wrapper server |

**When to use which:**
- Skill: Need to parse JSON output, chain with other skills
- Cron: Fire-and-forget scheduled runs
- Direct terminal: One-off interactive use

---

### 3. MCP Server (e.g., `davinci-resolve`, `cognee-mcp`, `native-mcp`)

| Your Layer | Pattern |
|------------|---------|
| **Hermes** | Add to `config.yaml`:\n```yaml\nmcp:\n  servers:\n    cognee:\n      command: ["python", "-m", "cognee_mcp"]\n      env:\n        LLM_API_KEY: "${OPENAI_API_KEY}"\n``` |
| **Claude Code** | `claude mcp add cognee -t sse http://localhost:8000/sse` |
| **Cursor/Cline** | Same URL in their MCP config |

**When to use:**
- Always prefer MCP for tools that expose it — universal, no wrapper code

---

### 4. Dockerized Service (e.g., `cognee/cognee:main`, `cognee/cognee-mcp:main`)

| Your Layer | Pattern |
|------------|---------|
| **Local dev** | `docker run -e LLM_API_KEY=... -p 8000:8000 cognee/cognee:main` |
| **MCP (HTTP/SSE)** | `docker run -e TRANSPORT_MODE=sse -p 8000:8000 cognee/cognee-mcp:main` |
| **Hermes cron** | `terminal(background=True, command="docker run ...")` |
| **Production** | Modal/Railway/Fly.io 1-click deploy from repo |

**When to use:**
- Quick test: `docker run` directly
- Persistent: Add to `docker-compose.yml` + systemd/service manager
- Team/shared: Deploy to Modal/Railway → use Cloud mode

---

### 5. GitHub Action / CI-Native Tool (e.g., `loop-engineering` patterns)

| Your Layer | Pattern |
|------------|---------|
| **Adapt to cron** | Extract the action logic → wrap in Hermes cron job + skill |
| **Keep in GH** | If it *only* makes sense on PR events (CI sweeper, PR babysitter) |
| **Hybrid** | GH Action for PR events + local cron for scheduled sweeps |

**When to use:**
- PR-triggered: Keep in GitHub Actions
- Time-triggered: Move to local cron (works offline, uses your local models)

---

### 6. TypeScript/Node Package (e.g., `@cognee/cognee-ts`, `@cobusgreyling/loop-init`)

| Your Layer | Pattern |
|------------|---------|
| **Hermes Skill** | `subprocess.run(["npx", "@cognee/cognee-ts", "remember", "data"])` |
| **MCP** | Only if package exports MCP server entry point |
| **Claude Code** | `npx` in hook or slash command |

---

## Decision Flowchart

```
START: New tool to integrate
│
├─ Does it have MCP server?
│   ├─ YES → Add to Hermes MCP config → DONE
│   └─ NO  → Continue
│
├─ Is it Python with clean SDK?
│   ├─ YES → Write Hermes skill wrapper → DONE
│   └─ NO  → Continue
│
├─ Is it CLI-only?
│   ├─ Scheduled? → Hermes cron job → DONE
│   ├─ Interactive? → Terminal alias / direct use → DONE
│   └─ Needs parsing? → Hermes skill wrapping subprocess → DONE
│
├─ Is it Docker-only?
│   ├─ Persistent? → docker-compose + systemd → DONE
│   └─ Ephemeral? → terminal(background=True) in cron/skill → DONE
│
└─ Is it GH Action only?
    ├─ PR-triggered? → Keep in GitHub → DONE
    └─ Time-triggered? → Extract logic → local cron → DONE
```

---

## Anti-Patterns to Avoid

| Anti-Pattern | Why It Fails | Fix |
|--------------|--------------|-----|
| **Wrap everything in skills** | Skills add overhead; MCP/CLI/cron are simpler | Use lightest layer that works |
| **Assume MCP = magic** | MCP server must be running, healthy, configured | Health-check in cron; fallback to SDK |
| **Duplicate GH Actions locally** | Two sources of truth for same logic | Single source: GH for PR events, local for time events |
| **Ignore token costs** | SDK calls LLM per chunk → surprise bill | Grep for `llm.call` / estimate before cron |
| **Skip migration check** | Alembic runs on first `import` → DB lock | Read code for `run_migrations`; plan first run |