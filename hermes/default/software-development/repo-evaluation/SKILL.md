---
name: repo-evaluation
description: Class-level skill for evaluating external GitHub repositories and tools for potential integration into the local AI stack (Hermes, Claude Code, local models). Covers discovery, technical assessment, integration mapping, and go/no-go decision framework.
category: software-development
---

# Repository Evaluation Skill

Systematic approach to assessing whether an external repo/tool is worth integrating into the local AI orchestration stack.

## When to Use

- User asks "check this repo out and tell me if it's good"
- Considering a new MCP server, CLI tool, Python package, or framework
- Evaluating forks vs. upstreams
- Deciding between build vs. buy vs. adapt

## Evaluation Framework

### 1. Identity & Provenance

| Check | Method |
|-------|--------|
| **Actual upstream** | Follow "forked from" links; compare commit counts |
| **License** | `LICENSE` file + `pyproject.toml`/`package.json` license field |
| **Maintenance** | Recent commits, release frequency, issue/PR responsiveness |
| **Community** | Stars, forks, contributors, Discord/Slack activity |
| **Governance** | Single maintainer vs. org; CLA requirements |

**Red flag**: Fork significantly behind upstream (like DevZilla55/loop-engineering: 21 commits behind) — prefer upstream.

### 2. Technical Architecture

| Dimension | What to Extract |
|-----------|-----------------|
| **Core purpose** | One-sentence summary from README + `__init__.py` exports |
| **Dependencies** | `pyproject.toml`/`package.json` — heaviness, conflicts, version pins |
| **Entry points** | CLI (`[project.scripts]`), Python API (`__init__.py`), MCP tools |
| **Data stores** | Required databases (Postgres, Neo4j, Redis, embedded SQLite/LanceDB/Kuzu) |
| **Deployment modes** | Local, Docker, cloud, serverless (Modal, Railway, Fly.io) |
| **Auth/tenancy** | API keys, multi-user, per-dataset isolation, ACLs |

### 3. Integration Mapping

For each candidate, map to your stack:

| Your Layer | Integration Pattern |
|------------|---------------------|
| **Hermes skills** | Python SDK → `import pkg; await pkg.fn()` inside skill code |
| **MCP servers** | Add to Hermes MCP config → tools appear natively |
| **Claude Code** | Plugin marketplace or `--mcp-config` |
| **Local models** | `litellm` / `ollama` provider config in tool |
| **Obsidian vault** | Tool writes markdown → vault indexes it |
| **Cron/scheduler** | Tool has CLI → wrap in Hermes cron job |

### 4. Cost & Risk Assessment

| Factor | Estimation Method |
|--------|-------------------|
| **LLM token cost** | Check if tool calls LLM per chunk/request (e.g., `cognify()` = ~$0.01–0.10/doc) |
| **Install size** | `pip install` / `docker pull` — disk, deps, compile steps |
| **Migration risk** | DB schema churn (alembic migrations on first run = surprise) |
| **Vendor lock-in** | Proprietary formats vs. open standards (MCP, JSON, SQLite) |
| **Maintenance burden** | You own adaptations; upstream changes = manual port |

### 5. Decision Matrix

```
┌─────────────────────────────────────────────────────────────┐
│  GO if:                                                      │
│  • Solves a real pain point you feel TODAY                   │
│  • Clean integration path (MCP, Python SDK, CLI)             │
│  • Local-first or self-hostable                              │
│  • Active upstream, Apache/MIT license                       │
│  • Token cost predictable / budgetable                       │
├─────────────────────────────────────────────────────────────┤
│  ADAPT if:                                                   │
│  • Good patterns but wrong runtime (e.g., GH Actions → cron) │
│  • Fork is stale — use upstream + cherry-pick                │
│  • Need only subset — extract patterns, not whole tool       │
├─────────────────────────────────────────────────────────────┤
│  PASS if:                                                    │
│  • No current pain (speculative ROI)                         │
│  • Heavy deps / cloud-only / proprietary                     │
│  • You'd be the only maintainer of the integration           │
│  • Existing stack already covers 80%                         │
└─────────────────────────────────────────────────────────────┘
```

## Investigation Checklist (Run in Order)

1. **Resolve upstream** — `git log --oneline -5` on both fork + upstream
2. **Read `pyproject.toml` / `package.json`** — deps, scripts, optional groups
3. **Check `__init__.py` / main entry** — public API surface
4. **Read 1–2 core modules** — understand data flow (e.g., `remember.py`, `cognify.py`)
5. **Check MCP/CLI entrypoints** — `cognee-mcp/README.md`, `pyproject.toml [project.scripts]`
6. **Test minimal install** — `pip install pkg` → `python -c "import pkg; pkg.hello()"`
7. **Search issues** — "breaking change", "migration", "memory leak", "token cost"

## Common Pitfalls

| Pitfall | Prevention |
|---------|------------|
| **Fork confusion** | Always check "forked from" badge; use upstream for evaluation |
| **Marketing ≠ reality** | Read source, not just README; run the quickstart yourself |
| **Hidden cloud dependency** | Search for `serve()`, `cloud`, `api_url` — does it *require* remote? |
| **Migration surprise** | Look for `alembic` + `run_migrations_and_block()` in code |
| **Token budget blind spot** | Grep for `llm.call`, `instructor`, `completion` — estimate per doc |
| **Integration mismatch** | Tool assumes GH Actions; you run local cron — adapt or pass |

## Output Format

Deliver a **one-page assessment** with:

```
## Verdict: [GO / ADAPT / PASS]

### What It Is
One paragraph: actual purpose, not marketing.

### Integration Path
| Your Layer | How |
|------------|-----|
| Hermes skill | `import pkg` in skill |
| MCP | Add to `mcp.servers` |
| Cron | Wrap CLI in cron job |

### Costs
- Install: ~XXX MB, deps: [list heavy ones]
- LLM: ~$X per 1K docs (if applicable)
- Migration: alembic on first run (Y/N)

### Risks
- [Specific risks found]

### Recommendation
[Concrete next step or "skip"]
```

## References

- `references/fork-vs-upstream-checklist.md` — Quick commands to resolve fork status
- `references/dependency-weight-guide.md` — Heuristics for dep heaviness by ecosystem
- `references/integration-patterns.md` — Mapping table: tool type → your stack integration

## Templates

- `templates/repo-assessment.md` — Fill-in assessment template
- `templates/minimal-test.py` — Boilerplate for `pip install` smoke test