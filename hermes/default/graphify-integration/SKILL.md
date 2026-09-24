---
name: graphify-integration
description: Auto-query Graphify knowledge graph for relevant context before coding tasks
category: development
tags: [graphify, knowledge-graph, context, rag, codebase]
---

# Graphify Integration Skill

## Purpose
Automatically inject relevant codebase context from Graphify knowledge graph into agent prompts before and during coding tasks.

## When to Use
- **Before** starting any non-trivial coding task
- **During** debugging to trace relationships
- **When** exploring unfamiliar codebases
- **For** impact analysis before refactoring

### Graphify Commands Reference

### Query (Natural Language)
```bash
# From project root
uvx --from graphifyy graphify query "How does authentication work in this project?"

# From any directory with --root
uvx --from graphifyy graphify query "Find all components that use the UserContext" --root /path/to/project
```

### Path (Relationship Between Two Nodes)
```bash
uvx --from graphifyy graphify path "src/lib/auth.ts" "src/app/api/auth/route.ts"
```

### Explain (Focused Concept)
```bash
uvx --from graphifyy graphify explain "Server Actions pattern in this codebase"
```

### Update (After Code Changes)
```bash
# From project root
uvx --from graphifyy graphify update .

# Or with explicit path (positional — there is no --root flag)
uvx --from graphifyy graphify update /path/to/project
```

## Agent Integration Pattern

### Pre-Task Context Injection
```python
# Before starting a task, agent runs:
def get_graphify_context(task_description: str, project_path: str = "."):
    """Get relevant context from Graphify for a task."""
    # 1. Query for task-relevant nodes
    query_result = graphify_query(task_description, project_path)
    
    # 2. If specific files mentioned, get paths
    path_results = []
    for file in extract_mentioned_files(task_description):
        path_results.append(graphify_path(file, "related", project_path))
    
    # 3. Format for injection
    return format_context(query_result, path_results)
```

### During-Task Exploration
```python
# When agent needs to understand a specific symbol
def explore_symbol(symbol_name: str, project_path: str = "."):
    return graphify_explain(symbol_name, project_path)
```

## Hermes Integration

### Auto-Load in Skills
Add to skill frontmatter:
```yaml
# In any coding skill
load_order:
  - graphify-integration
  - project-conventions
  - coding-workflow
```

### Kanban Task Enhancement
When Kanban creates a coding task:
1. Extract key terms from task description
2. Run `graphify query` with those terms
3. Inject top 5-10 results as context
4. Agent starts with codebase awareness

## Context Format for Injection

```markdown
## 📊 Graphify Context (Auto-Injected)

### Relevant Nodes (from query: "user authentication")
| Node | Type | File | Summary |
|------|------|------|---------|
| `authenticateUser` | Function | `src/lib/auth.ts` | Validates credentials, returns session |
| `UserProvider` | Component | `src/components/providers/UserProvider.tsx` | React context for user state |
| `useUser` | Hook | `src/hooks/useUser.ts` | Access user from context |
| `authMiddleware` | Middleware | `src/middleware.ts` | Protects routes, redirects to login |

### Relationships
- `UserProvider` → provides → `useUser` (context consumer)
- `authMiddleware` → calls → `authenticateUser` (validation)
- `loginAction` → calls → `authenticateUser` → sets → `UserProvider` state

### Suggested Exploration
- `graphify path "src/lib/auth.ts" "src/app/(auth)/login/page.tsx"`
- `graphify explain "session management pattern"`
```

## Best Practices

### Do
- Run `graphify update` after significant changes
- Use specific queries ("payment webhook handling" not "payments")
- Combine with file reads for full picture
- Share context across agent handoffs

### Don't
- Skip update after refactoring (graph becomes stale)
- Over-inject (limit to top 10 most relevant nodes)
- Trust graph 100% — verify with file reads
- Use for trivial tasks (overhead not worth it)

## Project Setup

### Initialize Graphify for a Project
```bash
cd /Users/alfredkamisese/projects/my-project
uvx --from graphifyy graphify init .                    # Creates graphify-out/
uvx --from graphifyy graphify update .                  # Builds initial graph
```

### Default Vault Graph (TamaZila Obsidian Vault)
```bash
# Already indexed at:
# ~/TamaZila Obsidian Vault/graphify-out/graph.json
# Query it directly:
uvx --from graphifyy graphify query "question" --root "~/TamaZila Obsidian Vault"
```

### Add to Project's CLAUDE.md
```markdown
## Graphify
- Knowledge graph at `graphify-out/`
- Run `graphify update .` after significant changes
- Agents auto-query before coding tasks
- Use `graphify query "..."` for exploration
```

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Graph empty | Run `graphify update .` in project root |
| Stale results | Run `graphify update .` after code changes |
| No results | Broaden query terms, check `graphify-out/wiki/index.md` |
| Large project slow | Use `graphify query` with specific terms, not broad |
| `update` slow on USB vault (7+ min) | Run in background with notify; a foreground timeout kills it pre-write (graph.json left intact, safe to retry) |

## Integration with Other Skills

| Skill | Integration Point |
|-------|-------------------|
| `project-conventions` | Graphify knows project structure conventions |
| `coding-workflow` | Run `graphify update` as post-commit hook |
| `model-router` | Route exploration queries to Ollama (tools) |
| `mcp-filesystem` | Graphify complements filesystem MCP |

## Quick Commands Card

```
┌─────────────────────────────────────────────────────────────┐
│  GRAPHIFY QUICK REFERENCE                                  │
├─────────────────────────────────────────────────────────────┤
│  uvx --from graphifyy graphify query "question"            │
│  uvx --from graphifyy graphify path "A" "B"                │
│  uvx --from graphifyy graphify explain "concept"           │
│  uvx --from graphifyy graphify update .                    │
│  uvx --from graphifyy graphify update /path                │
└─────────────────────────────────────────────────────────────┘
```