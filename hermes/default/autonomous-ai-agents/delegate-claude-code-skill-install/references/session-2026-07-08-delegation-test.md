# Session Reference: Delegate Skill Installation Test (2026-07-08)

## Overview
Tested delegating skill file creation to Claude Code via `delegate_task` with Ollama backend.

## What Worked

### Delegation Command
```python
delegate_task(
    goal="Create a comprehensive code review checklist skill at ~/.claude/skills/code-review-checklist.md",
    context="""
    Create a skill file at ~/.claude/skills/code-review-checklist.md that provides a comprehensive code review checklist. 
    Include sections for security, performance, code quality, testing, documentation, and architecture.
    Make it detailed and practical with specific checklists.
    
    Use this exact command pattern:
      claude -p "Create a comprehensive code review checklist skill at ~/.claude/skills/code-review-checklist.md..." \
        --model qwen3.5:9b \
        --dangerously-skip-permissions \
        --output-format json \
        --max-turns 8 \
        --bare \
        --workdir /tmp
    """
)
```

### Execution Details
- **Model**: `qwen3.5:9b` (Ollama)
- **Duration**: ~235 seconds (3m 55s)
- **API calls**: 5
- **Status**: Completed successfully
- **Output**: 213-line skill file created at `~/.claude/skills/code-review-checklist.md`

### Verification
```bash
ls -la ~/.claude/skills/
# -rw-------@ 1 alfredkamisese  staff  6750 Jul  8 12:42 code-review-checklist.md

wc -l ~/.claude/skills/code-review-checklist.md
# 213 lines
```

## Key Findings

### Ollama Model Selection
| Model | Use Case | Notes |
|-------|----------|-------|
| `qwen3.5:9b` | General coding tasks | Good balance of speed/quality |
| `claude-sonet-4.6:latest` | Complex reasoning | Slower, higher quality |
| `claude-opus-4.8:latest` | Heavy reasoning | Slowest, best for architecture |

### Required Flags for Print Mode with Ollama
```bash
--model qwen3.5:9b              # Exact Ollama name (NOT aliases like sonnet/haiku)
--dangerously-skip-permissions  # Auto-approve all tools
--output-format json            # Structured result
--max-turns 8                   # Prevent runaway loops
--bare                          # Skip hooks/plugins/MCP (critical for speed)
--workdir /tmp                  # Working directory
```

### Common Pitfalls Avoided
1. **Model aliases don't work with Ollama** - Must use exact name from `ollama list`
2. **`--workdir` flag not supported in older Claude Code versions** - Use `cd /path && claude ...` instead
3. **Print mode hangs if workspace not trusted** - First run `claude` interactively in the directory
4. **Timeouts** - Set generous timeout (120-180s) for complex tasks

## Skills vs Plugins Clarification

| Aspect | Skills | Plugins |
|--------|--------|---------|
| Location | `~/.claude/skills/*.md` | `~/.claude/plugins/` (npm packages) |
| Format | Markdown with frontmatter | Node.js packages |
| Invocation | Automatic (natural language) | Slash commands / explicit |
| Installation | Write file directly | `claude plugin install <pkg>` or `npm install -g` |
| This workflow | ✅ Works via delegation | ❌ Requires terminal/npm |

## Reproduction Recipe

```bash
# 1. Verify Ollama has the model
ollama list | grep qwen3.5:9b

# 2. Test basic print mode
cd /tmp && claude -p "Reply with: OK" --model qwen3.5:9b --dangerously-skip-permissions --output-format json --max-turns 1 --bare

# 3. Run delegation via Hermes
hermes chat -q "Delegate: Create skill at ~/.claude/skills/test.md with content..."
```

## Related Files Created
- `~/.claude/skills/code-review-checklist.md` (213 lines, 6.7KB)
- `/Users/alfredkamisese/.hermes/skills/autonomous-ai-agents/delegate-claude-code-skill-install/SKILL.md` (this skill)