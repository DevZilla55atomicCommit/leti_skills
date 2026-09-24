# Repo Assessment Template

Fill in after investigation. One page max.

---

## Repo: `{owner}/{repo}`

**Upstream:** `{upstream_owner}/{upstream_repo}` (if fork)
**License:** `{license}`
**Language:** `{primary_language}`

---

## Verdict: `[GO / ADAPT / PASS]`

---

## What It Is

{One paragraph: actual technical purpose, not marketing tagline.}

---

## Integration Path

| Your Layer | How | Effort |
|------------|-----|--------|
| Hermes Skill | `{import pattern or wrapper}` | L/M/H |
| MCP Server | `{server config or "not available"}` | L/M/H |
| Cron/Background | `{CLI command or script}` | L/M/H |
| Claude Code | `{plugin or MCP URL}` | L/M/H |
| Obsidian | `{markdown output pattern}` | L/M/H |

---

## Costs

| Factor | Estimate |
|--------|----------|
| Install size | `{MB}` / deps: `{heavy deps list}` |
| LLM tokens | `~$X per 1K docs` / `{per-request}` |
| First-run migration | `{Y/N}` — alembic / schema init |
| Ongoing maintenance | `{your time per month}` |

---

## Risks

- `{Risk 1: specific, from code inspection}`
- `{Risk 2: fork staleness / cloud dependency / token cost}`
- `{Risk 3: migration churn / breaking changes}`

---

## Evidence

| Check | Result |
|-------|--------|
| Upstream resolved | `{Y/N} — {commits behind}` |
| `pyproject.toml` read | `{Y/N}` |
| Core module inspected | `{module.py}` |
| MCP/CLI entrypoint found | `{Y/N} — {command}` |
| Minimal test run | `{Y/N} — {output}` |
| Issue search | `{keywords found}` |

---

## Recommendation

`{Concrete next step: "Add as MCP server", "Write Hermes skill wrapper", "Extract pattern X into skill", "Skip — no current pain"}`

---

## Notes

`{Any context for future self: quirks, env vars needed, config tips}`