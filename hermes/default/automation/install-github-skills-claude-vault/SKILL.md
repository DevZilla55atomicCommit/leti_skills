---
name: install-github-skills-claude-vault
description: Install skills from a GitHub repo into both Claude Code (~/.claude/skills/) and an Obsidian vault folder, preserving full skill structure (references/, templates/) in the vault
version: 1.0.0
author: Maddie (Hermes Agent)
license: MIT
---

# Install GitHub Skills to Claude Code + Obsidian Vault

Install skills from a GitHub repository into both:
1. **Claude Code auto-invocation system** (`~/.claude/skills/`) — just the SKILL.md files
2. **Obsidian vault** (user-specified path) — full skill folders with references/, templates/, scripts/

## When to Use

- You have a GitHub repo with skills (like `https://github.com/aievolutionpl/step-beyond.git`)
- You want them available in Claude Code for auto-invocation
- You want full skill structure preserved in your Obsidian knowledge base
- You want a repeatable, delegated workflow

## Prerequisites

- GitHub repo with skills in `skills/<skill-name>/SKILL.md` structure
- Claude Code installed with Ollama backend (`qwen3.5:9b` recommended for simple installs)
- Obsidian vault path exists and is writable
- Hermes `delegate_task` tool available

## Workflow

### 1. Clone Repo (one-time or CI)

```bash
cd /tmp && git clone https://github.com/<owner>/<repo>.git --depth 1
```

### 2. Discover Skills

```bash
ls /tmp/<repo>/skills/
# Lists skill folders, each containing SKILL.md + optional references/, templates/
```

### 3. Delegate to Claude Code (single command)

```bash
claude -p "
Install skills from /tmp/<repo>/skills/ to both targets:

TARGET 1 - Claude Code skills (~/.claude/skills/):
- For each skill folder, copy SKILL.md to ~/.claude/skills/<skill-name>.md
- Filename = kebab-case skill name + .md extension
- No subdirectories, just flat .md files

TARGET 2 - Obsidian Vault (<vault-path>/Claude Code/):
- Copy ENTIRE skill folder to <vault-path>/Claude Code/<skill-name>/
- Preserves references/, templates/, scripts/, SKILL.md
- Creates directory structure matching repo

VERIFICATION:
- ls -la ~/.claude/skills/*.md
- ls -la '<vault-path>/Claude Code/'/
- Test: claude -p 'test the <skill-name> skill' --model qwen3.5:9b --bare --max-turns 3
" --model qwen3.5:9b --dangerously-skip-permissions --output-format json --max-turns 10 --bare
```

### 4. Verify Installation

```bash
# Check Claude Code skills
ls -la ~/.claude/skills/step-beyond.md ~/.claude/skills/step-beyond-chatgpt.md

# Check Vault copies
ls -la "/Users/alfredkamisese/TamaZila Obsidian Vault/Claude Code/step-beyond/SKILL.md"
ls -la "/Users/alfredkamisese/TamaZila Obsidian Vault/Claude Code/step-beyond-chatgpt/SKILL.md"

# Test auto-invocation
claude -p "test the step-beyond skill" --model qwen3.5:9b --bare --max-turns 3
```

## Example: step-beyond Repo

**Repo:** `https://github.com/aievolutionpl/step-beyond.git`
**Skills found:** `step-beyond`, `step-beyond-chatgpt`
**Vault path:** `/Users/alfredkamisese/TamaZila Obsidian Vault/Claude Code/`

### Result

```
~/.claude/skills/
├── step-beyond.md              # From skills/step-beyond/SKILL.md
└── step-beyond-chatgpt.md      # From skills/step-beyond-chatgpt/SKILL.md

/Users/alfredkamisese/TamaZila Obsidian Vault/Claude Code/
├── step-beyond/
│   ├── SKILL.md
│   ├── references/...
│   └── templates/...
└── step-beyond-chatgpt/
    ├── SKILL.md
    ├── templates/...
    ├── CARD.md
    └── INSTALL.md
```

## Delegation Template (for Hermes)

```python
delegate_task(
    goal="Install GitHub skills to Claude Code and Obsidian vault",
    context=f"""
## Task: Install Skills from GitHub Repo

**Repo:** {repo_url}
**Cloned to:** /tmp/{repo_name}/
**Skills dir:** /tmp/{repo_name}/skills/
**Claude Code target:** ~/.claude/skills/
**Vault target:** {vault_path}/Claude Code/

## Instructions

For each skill folder in /tmp/{repo_name}/skills/:

1. **Claude Code** - Copy SKILL.md to ~/.claude/skills/<skill-name>.md
2. **Vault** - Copy entire folder to {vault_path}/Claude Code/<skill-name>/

Use: cp, mkdir -p, ls for verification
Return JSON with success/failure per skill
""",
    role="leaf"
)
```

## Model Selection

| Task | Model | Max Turns |
|------|-------|-----------|
| Simple skill copy | `qwen3.5:9b` | 8-10 |
| Complex multi-skill | `claude-sonet-4.6:latest` | 12-15 |

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `claude: command not found` | Use full path: `~/Library/Application Support/claude/claude-code/<version>/claude.app/Contents/MacOS/claude` |
| `--workdir` not recognized | `cd /tmp && claude ...` instead |
| Model not found | `ollama list` to verify exact name |
| Skill not auto-invoking | Check `~/.claude/skills/<name>.md` exists; restart Claude Code |
| Vault path with spaces | Quote path: `"/Users/.../TamaZila Obsidian Vault/..."` |

## Related Skills

- `delegate-claude-code-skill-install` — single-skill installation pattern
- `claude-code` — full CLI reference
- `hermes-claude-code-orchestration` — orchestration architecture