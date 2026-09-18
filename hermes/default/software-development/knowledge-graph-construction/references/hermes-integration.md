# Hermes Agent Integration

## Installation

```bash
# Global skill (available in all Hermes sessions)
graphify hermes install

# Or project-scoped (writes .hermes/skills/graphify/ in project root)
graphify hermes install --project
```

**What it writes:**
- `AGENTS.md` in project root — always-on rules for Hermes to use graphify
- `~/.hermes/skills/graphify/SKILL.md` — the skill definition Hermes loads

## AGENTS.md Content

```markdown
## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

When the user types `/graphify`, use the installed graphify skill or instructions before doing anything else.

Rules:
- For codebase questions, first run `graphify query "<question>"` when graphify-out/graph.json exists. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- Dirty graphify-out/ files are expected after hooks or incremental updates; dirty graph files are not a reason to skip graphify. Only skip graphify if the task is about stale or incorrect graph output, or the user explicitly says not to use it.
- If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost).
```

## Using in Hermes

### Build Graph
```
/graphify .
/graphify ./my-project --obsidian --obsidian-dir "~/TamaZila Obsidian Vault/MyProject"
```

### Query Existing Graph
```
/graphify query "how does authentication connect to the database?"
/graphify path "AuthManager" "DatabasePool"
/graphify explain "RateLimiter"
```

### Update After Changes
```
/graphify update .
```

## Key Differences from Claude Code

| Feature | Claude Code | Hermes |
|---------|-------------|--------|
| Hooks | `PreToolUse` hook fires before Read/Glob/Bash | No hook equivalent — AGENTS.md is the always-on mechanism |
| Skill location | `~/.claude/skills/` | `~/.hermes/skills/` |
| Config | `CLAUDE.md` | `AGENTS.md` |
| Skill trigger | `/graphify` slash command | `/graphify` slash command (same) |

## Workflow in Hermes

1. **First run**: `/graphify .` → builds graph, exports to vault if `--obsidian`
2. **Daily coding**: Ask questions → Hermes runs `graphify query` automatically via AGENTS.md rules
3. **After edits**: `/graphify update .` → fast AST-only refresh
4. **New docs/images**: `/graphify . --update` → incremental semantic extraction
5. **Explore in Obsidian**: Open exported vault → Graph View, Canvas, Search, Wikilinks

## Skill File Location

- Global: `~/.hermes/skills/graphify/SKILL.md`
- Project: `.hermes/skills/graphify/SKILL.md` (when `--project` used)

The skill references `references/` sidecar for progressive disclosure (extraction spec, query patterns, update flow, etc.) — loaded on demand.