---
title: "Graphify Git Hooks & CLAUDE.md Integration"
source: "Graphify repository (tools/skillgen/fragments/references/hooks.md)"
version: "0.9.9"
---

# Graphify Git Hooks & CLAUDE.md Integration

## Git Hooks

### Install Hooks
```bash
graphify hook install
```

### What Gets Installed

**`.git/hooks/post-commit`**
- Runs after every commit
- Executes: `graphify update . --no-cluster` (AST only, no LLM)
- Fast - only re-parses changed code files
- Updates `graph.json` and `graph.html` incrementally

**`.git/hooks/post-checkout`**
- Runs after `git checkout`, `git switch`, `git restore`
- Refreshes graph for new branch state

**Git merge driver for `graph.json`**
- Added to `.git/config`:
```ini
[merge "graphify"]
  name = Graphify graph.json union merge
  driver = python -m graphify.merge %O %A %B %P
```
- Union-merges `graph.json` on parallel commits
- Prevents conflict markers in graph.json
- Two devs committing in parallel get graphs auto-merged

### Uninstall Hooks
```bash
graphify hook uninstall
```

### Check Hook Status
```bash
graphify hook status
# Shows: installed/not installed, merge driver configured
```

---

## CLAUDE.md / AGENTS.md Integration

### Install Always-On Instructions

```bash
# For Hermes Agent (this skill's platform)
graphify hermes install
# Writes: ~/.hermes/skills/graphify/SKILL.md + project AGENTS.md

# For other platforms:
graphify claude install      # CLAUDE.md + PreToolUse hook (Claude Code)
graphify codex install       # AGENTS.md + PreToolUse hook (.codex/hooks.json)
graphify opencode install    # AGENTS.md + tool.execute.before plugin
graphify cursor install      # .cursor/rules/graphify.mdc (alwaysApply: true)
graphify gemini install      # GEMINI.md + BeforeTool hook
graphify agents install      # ~/.agents/skills/ + AGENTS.md (cross-framework)
```

### What Gets Written

**AGENTS.md (project-scoped)**
```markdown
# Graphify Knowledge Graph Integration

## Always consult the knowledge graph first

When answering questions about this codebase, prefer:
1. `graphify query "<question>"` - for broad questions
2. `graphify path "A" "B"` - for tracing connections
3. `graphify explain "Concept"` - for node details

Only read source files directly if the graph doesn't contain the answer.

## Graph Location
- `graphify-out/graph.json` - queryable graph
- `graphify-out/GRAPH_REPORT.md` - architecture summary
- `graphify-out/graph.html` - interactive visualization

## Rebuild Commands
- `/graphify . --update` - incremental (changed files only)
- `/graphify . --cluster-only` - re-cluster without re-extracting
- `/graphify . --force` - full rebuild
```

**PreToolUse Hook (Claude Code, Codex, CodeBuddy)**
- Fires before search-style tool calls (Grep, Glob, Task)
- Fires before Read tool (Claude Code)
- Nudges assistant toward `graphify query` instead of grepping
- Hook script: `.claude/hooks/graphify-pretool.sh` or `.codex/hooks.json`

---

## Project-Scoped Installs

```bash
# Install skill into current repo (not user profile)
graphify install --project
graphify install --project --platform codex

# Writes to:
# .claude/skills/graphify/SKILL.md
# .agents/skills/graphify/SKILL.md
# .cursor/rules/graphify.mdc
# etc.

# Prints `git add` hint for commitable files
```

### When to Use Project Scope
- Team wants graphify config in repo
- CI/CD needs the skill
- Sharing across developers without individual installs

---

## Uninstall

```bash
# Remove from all platforms at once
graphify uninstall

# Also delete graphify-out/
graphify uninstall --purge

# Remove project-scoped only
graphify uninstall --project --platform codex
```

---

## Hook Troubleshooting

| Issue | Fix |
|-------|-----|
| Hook not firing | Check `.git/hooks/post-commit` exists and is executable |
| `graphify` not found in hook | Hook embeds Python path at install time; re-run `graphify hook install` after upgrade |
| Merge conflicts in graph.json | Run `graphify hook install` to add merge driver |
| Hook slows down commits | Hook runs `--no-cluster` (AST only); should be <2s for typical repos |
| Want to disable temporarily | `chmod -x .git/hooks/post-commit` or `graphify hook uninstall` |