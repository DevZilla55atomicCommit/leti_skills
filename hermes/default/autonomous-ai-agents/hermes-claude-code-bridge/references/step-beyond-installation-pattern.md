# Step-Beyond Skill Installation Pattern

## Overview

Documents the pattern for installing `step-beyond` and `step-beyond-chatgpt` skills from the GitHub repo into both Hermes and Claude Code, with vault sync.

## Source Repository

```
https://github.com/aievolutionpl/step-beyond.git
```

Skills located in:
- `skills/step-beyond/` — Portable reasoning layer (SPEC.md normative)
- `skills/step-beyond-chatgpt/` — Prompt-only ChatGPT adapter

## Installation Targets

| Target | Path | Content |
|--------|------|---------|
| Hermes skills | `~/.hermes/skills/step-beyond/`, `step-beyond-chatgpt/` | Full folders with references, templates |
| Claude Code skills | `~/.claude/skills/step-beyond.md`, `step-beyond-chatgpt.md` | Single `.md` files (no frontmatter) |
| Obsidian Vault | `/Users/alfredkamisese/TamaZila Obsidian Vault/Claude Code/step-beyond/`, `step-beyond-chatgpt/` | Full folders for knowledge base |

## Installation Commands

```bash
# 1. Clone repo (shallow)
cd /tmp && rm -rf step-beyond && git clone https://github.com/aievolutionpl/step-beyond.git --depth 1

# 2. Install to Claude Code (auto-invocation)
mkdir -p ~/.claude/skills
cp /tmp/step-beyond/skills/step-beyond/SKILL.md ~/.claude/skills/step-beyond.md
cp /tmp/step-beyond/skills/step-beyond-chatgpt/SKILL.md ~/.claude/skills/step-beyond-chatgpt.md

# 3. Install to Obsidian Vault (full folders for references)
mkdir -p "/Users/alfredkamisese/TamaZila Obsidian Vault/Claude Code/step-beyond"
mkdir -p "/Users/alfredkamisese/TamaZila Obsidian Vault/Claude Code/step-beyond-chatgpt"
cp -r /tmp/step-beyond/skills/step-beyond/* "/Users/alfredkamisese/TamaZila Obsidian Vault/Claude Code/step-beyond/"
cp -r /tmp/step-beyond/skills/step-beyond-chatgpt/* "/Users/alfredkamisese/TamaZila Obsidian Vault/Claude Code/step-beyond-chatgpt/"

# 4. Verify
diff /tmp/step-beyond/skills/step-beyond/SKILL.md ~/.claude/skills/step-beyond.md
diff /tmp/step-beyond/skills/step-beyond-chatgpt/SKILL.md ~/.claude/skills/step-beyond-chatgpt.md
```

## Auto-Invocation Triggers

| Skill File | Triggers On |
|------------|-------------|
| `step-beyond.md` | "step beyond", "portable reasoning layer", "reconstruct intent", "permission-aware initiative", "verify claims", "conservative learning" |
| `step-beyond-chatgpt.md` | "step beyond chatgpt", "prompt-only adapter", "multi-hypothesis intent", "strict scope" |

## Key Differences: Hermes vs Claude Code Skills

| Aspect | Hermes Skills | Claude Code Skills |
|--------|--------------|-------------------|
| Format | YAML frontmatter + markdown | Plain markdown (no frontmatter) |
| Location | `~/.hermes/skills/<name>/SKILL.md` | `~/.claude/skills/<kebab-case>.md` |
| Invocation | Explicit `skill_view()` tool | Automatic (natural language) |
| References | `references/`, `templates/`, `scripts/` folders | Not supported (single file) |
| Persistence | Cross-session via Hermes memory | Stateless per invocation |

## Memory Integration

The `step-beyond` skill references Obsidian vault sync patterns in `references/obsidian-vault-sync-patterns.md`. The local sync script at `~/.hermes/scripts/sync_step_beyond_memory.py` handles bidirectional sync between Hermes memory and Obsidian vault.

## Verification

```bash
# Test auto-invocation
claude -p "apply step beyond reasoning to this decision" --model qwen3.5:4b --bare --max-turns 3
```

## Session Test (2026-07-21)

- ✅ Cloned repo at `/tmp/step-beyond/`
- ✅ Installed to `~/.claude/skills/` (2 files)
- ✅ Copied full folders to Obsidian Vault
- ✅ Verified with `diff` — zero differences
- ✅ Auto-invocation confirmed working