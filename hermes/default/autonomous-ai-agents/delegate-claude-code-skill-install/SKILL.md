---
name: delegate-claude-code-skill-install
description: "Delegate to Claude Code to install skills into its own ~/.claude/skills/ directory via print mode"
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [delegation, claude-code, skills, orchestration, automation]
    related_skills: [claude-code, hermes-claude-code-bridge, hermes-claude-code-orchestration]
---

# Delegate Claude Code Skill Installation

This skill documents the workflow for using Hermes to delegate skill creation/installation to Claude Code, which writes the skill file directly into its own `~/.claude/skills/` directory.

## When to Use

- You want to add a new skill to Claude Code's auto-invocation system
- You have skill content (markdown instructions) and want it installed without manual copy-paste
- You want to automate skill creation as part of a larger workflow

## Prerequisites

- Claude Code installed and configured with Ollama backend
- `ANTHROPIC_BASE_URL=http://localhost:11434` in `~/.claude/settings.json`
- Ollama running with required models (e.g., `qwen3.5:9b`, `claude-sonet-4.6:latest`)
- Hermes `delegate_task` tool available

## Workflow Overview

```
Hermes (orchestrator)
    │
    ▼ delegate_task(goal, context)
    │
    ▼ Claude Code (worker) - print mode (-p)
    │
    ▼ Writes skill file to ~/.claude/skills/<name>.md
    │
    ▼ Returns JSON result with session info
    │
    ▼ Hermes verifies file exists
```

## Step-by-Step Process

### 1. Prepare Skill Content

Create the markdown content for the skill. It should follow Claude Code's skill format:

```markdown
# Skill Name

When asked to <trigger condition>:
1. Step one
2. Step two
3. Step three
```

**Key points:**
- Skills are **natural language invocation** - Claude auto-invokes when task matches
- Place in `~/.claude/skills/<kebab-case-name>.md`
- No frontmatter required (unlike Hermes skills)
- Should be practical, checklist-style instructions

### 2. Construct the Delegate Task

Use `delegate_task` with this context template:

```python
delegate_task(
    goal="Create a Claude Code skill at ~/.claude/skills/<skill-name>.md",
    context="""## Task: Install a Claude Code Skill

Create a skill file at ~/.claude/skills/<skill-name>.md with the following content:

## Skill Content

<PASTE THE FULL MARKDOWN SKILL CONTENT HERE>

## Execution Command

Use this exact command pattern:
  claude -p "Create a skill file at ~/.claude/skills/<skill-name>.md with the following content: <ESCAPED_CONTENT>" \\
    --model qwen3.5:9b \\
    --dangerously-skip-permissions \\
    --output-format json \\
    --max-turns 8 \\
    --bare \\
    --workdir /tmp

## Requirements

- File must be created at ~/.claude/skills/<skill-name>.md
- Content must match exactly what's provided above
- Verify by reading the file back
- Return success/failure in JSON output"""
)
```

### 3. Model Selection

| Task Complexity | Model | Max Turns |
|-----------------|-------|-----------|
| Simple skill creation | `qwen3.5:9b` | 5-8 |
| Complex skill with research | `claude-sonet-4.6:latest` | 10-15 |
| Heavy reasoning needed | `claude-opus-4.8:latest` | 15-20 |

**Critical:** Always use exact Ollama model names. Never use aliases (`sonnet`, `haiku`, `opus`).

### 4. Command Flags Explained

| Flag | Purpose |
|------|---------|
| `-p` / `--print` | Non-interactive, exits when done |
| `--model <name>` | Exact Ollama model name |
| `--dangerously-skip-permissions` | Auto-approve all file writes |
| `--output-format json` | Structured result parsing |
| `--max-turns N` | Prevent runaway loops |
| `--bare` | Skip hooks/plugins/MCP (faster) |
| `--workdir /tmp` | Neutral working directory |

### 5. Verification

After delegation completes, verify:

```bash
# Check file exists
ls -la ~/.claude/skills/<skill-name>.md

# Verify content
cat ~/.claude/skills/<skill-name>.md

# Test auto-invocation
claude -p "test the <skill-name> skill" --model qwen3.5:9b --bare --max-turns 3
```

## Complete Example

### Input: Skill to Create

**Name:** `api-design-review`  
**Content:**
```markdown
# API Design Review Skill

When asked to review an API design or OpenAPI spec:
1. Check REST conventions (nouns not verbs, plural collections)
2. Verify proper HTTP status codes
3. Validate request/response schemas
4. Check versioning strategy
5. Review authentication/authorization design
6. Ensure pagination for list endpoints
7. Validate error response format consistency
8. Check rate limiting headers
```

### Hermes Delegation Code

```python
delegate_task(
    goal="Create Claude Code skill for API design review",
    context="""## Task: Install a Claude Code Skill

Create a skill file at ~/.claude/skills/api-design-review.md with the following content:

## Skill Content

# API Design Review Skill

When asked to review an API design or OpenAPI spec:
1. Check REST conventions (nouns not verbs, plural collections)
2. Verify proper HTTP status codes
3. Validate request/response schemas
4. Check versioning strategy
5. Review authentication/authorization design
6. Ensure pagination for list endpoints
7. Validate error response format consistency
8. Check rate limiting headers

## Execution Command

Use this exact command pattern:
  claude -p "Create a skill file at ~/.claude/skills/api-design-review.md with the following content: [ESCAPED_CONTENT]" \\
    --model qwen3.5:9b \\
    --dangerously-skip-permissions \\
    --output-format json \\
    --max-turns 8 \\
    --bare \\
    --workdir /tmp

## Requirements

- File must be created at ~/.claude/skills/api-design-review.md
- Content must match exactly what's provided above
- Verify by reading the file back
- Return success/failure in JSON output"""
)
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `claude: command not found` | Use full path: `/Users/alfredkamisese/Library/Application Support/claude/claude-code/<version>/claude.app/Contents/MacOS/claude` |
| `--workdir` not recognized | Remove `--workdir` flag; `cd /tmp && claude ...` instead |
| Model not found | Run `ollama list` to verify exact model name |
| Print mode hangs | Workspace not trusted. Run `claude` interactively once in the directory first |
| Skill not auto-invoking | Ensure file is in `~/.claude/skills/` with `.md` extension; restart Claude Code |

## Important Notes

### Skills vs Plugins

| | Skills | Plugins |
|---|--------|---------|
| **Format** | Markdown (`.md`) | NPM package |
| **Install** | Write file to `~/.claude/skills/` | `claude plugin install <pkg>` or `npm install -g` |
| **Invocation** | Automatic (natural language) | Slash commands / explicit |
| **This workflow** | ✅ Works via delegation | ❌ Requires terminal/npm |

### Content Escaping

When embedding skill content in the prompt, escape:
- Backticks: `` \` ``
- Quotes: `\"`
- Newlines: `\\n`
- Backslashes: `\\\\`

Or use a heredoc approach with `--workdir /tmp` and write to a temp file first.

## Related Skills

- `claude-code` - Full Claude Code CLI reference
- `hermes-claude-code-bridge` - Bidirectional integration patterns
- `hermes-claude-code-orchestration` - Orchestration architecture

## Support Files

| File | Type | Purpose |
|------|------|---------|
| `references/session-2026-07-08-delegation-test.md` | Reference | Session transcript with execution details, model findings, and troubleshooting |
| `templates/delegate-skill-install-context.md` | Template | Ready-to-use delegate_task context template with examples |
| `scripts/verify-delegation-setup.sh` | Script | Verification script for prerequisites (Hermes, Claude Code, Ollama, models) |

## Version History

- 1.0.1 (2026-07-08): Added support files from session testing
- 1.0.0 (2026-07-08): Initial version based on successful delegation test