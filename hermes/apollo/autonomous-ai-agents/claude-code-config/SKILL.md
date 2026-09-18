---
name: claude-code-config
description: "Configure Claude Code agents, skills, and commands."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Claude-Code, Subagents, Skills, Configuration, Verification]
    related_skills: [claude-code, mcp-server-setup]
---

# Claude Code Configuration

Set up and maintain the `~/.claude/` config surface: skills, subagents,
commands, and their wiring. (For driving Claude Code on coding tasks, see
the `claude-code` skill; this skill governs the configuration itself.)

## Installing third-party skills from GitHub

Populate `~/.claude/skills/<name>/SKILL.md` (directory format — one folder
per skill, never flat `.md` files):

1. Shallow-clone candidates to a staging dir (`git clone --depth 1`). Never
guess URLs — a failed clone is the signal to find the real source, not to
improvise paths.
2. Map each repo's SKILL.md layout before copying
(`find <repo> -name SKILL.md`) — layouts differ between repos (flat dirs,
`skills/<name>/`, `.claude/skills/`, marketplaces with no skills at all).
Install from where the files actually are.
3. Dedupe with official-source-wins: upstream repos and official installer
CLIs beat mirrors and copies.
4. Security-sweep staged skills before installing — grep for exfil patterns
(`/etc/passwd`, `authorized_keys`, credential-harvesting posts). Skills
execute with full agent permissions; anything that phones home gets read
line-by-line first.
5. Repos with real guidance but no SKILL.md: copy the topic files plus a
hand-written index-router SKILL.md (name + trigger + topic-to-file map),
labeled with its provenance.
6. YAML-validate every installed SKILL.md: `name` + `description` are
required, and files missing either are silently skipped. Startup cost stays
lean — only frontmatter (~60 tokens/skill) loads until the body is needed.

## Porting skills to Claude Desktop (drag-and-drop pack)

Desktop Upload accepts per-skill folders: ship `skills/<name>/SKILL.md`
(directory format, same as CLI) with valid `name` + `description`
frontmatter — flat `.md` files without frontmatter are rejected with
'SKILL.md missing YAML frontmatter'. Keep flat `<skill-name>.md` copies
in the pack root only as paste-in material for Add skill → Write skill
instructions, plus a README index (source folder, one-line description,
flags for `large` >20k chars and support files left behind). Supporting
files (`references/`, templates) do not travel — the methodology survives,
deep lookups do not. Validate frontmatter programmatically on every output
file the same way as step 6 — a bulk script asserting `name:` +
`description:`, not eyeballing.

Cap the ACTIVE set at ~10–15 skills per session no matter how large the
library is: frontmatter for every active skill loads every session, and
on small local windows that catalog eats a third of usable context while
trigger overlap degrades routing. The folder is the library; the active
set is per-project. Subagents, hooks, and slash commands do not transfer
to Desktop at all — only skill bodies.

## Wiring skills and MCP servers into subagents

Subagent frontmatter beyond `tools`/`model` (all optional, all load-bearing):

```markdown
---
name: reviewer
description: Reviews diffs; report only findings scored >=80
tools: [Read, Grep, Glob]
skills:
  - react-best-practices
  - systematic-debugging
mcpServers:
  - playwright
maxTurns: 10
memory: project
---
```

- `skills:` injects the FULL skill content at subagent startup, not just the
description — cap preloads at 1–3 per agent or the bloat defeats the
specialization.
- Every `skills:` entry must exactly match an installed
`~/.claude/skills/<name>/` directory; every `mcpServers:` entry must match
a `claude mcp list` name. A ghost name resolves to nothing, so the agent
launches without the expertise it was designed around — run
`scripts/verify-agents.py` after every edit and fix all MISSING entries
before shipping.
- `memory: project` gives the subagent a persistent cross-session log
(consult and append); `maxTurns` caps runaway loops.
- Renames: keep identifiers kebab-case (`dr-strange`, never `Dr. Strange`
— spaces break @-mention). Sweep every reference afterward:
sibling-agent rosters, slash commands, CLAUDE.md.
- For scripted verification, frontmatter parsing is the source of truth —
files missing `name`/`description` or with unparseable YAML are silently
skipped at load.

## Model routing and app surfaces

- CLI config (`~/.claude/settings.json`, `~/.claude/agents/`, switcher scripts) and Claude Desktop config (`~/Library/Application Support/Claude-3p/claude_desktop_config.json`) are separate surfaces sharing one Ollama server — both apps hit `localhost:11434`, so the 16GB RAM budget covers both combined; attribute a loaded model with `ollama ps` plus client check, never by config file alone.
- `ANTHROPIC_DEFAULT_HAIKU_MODEL` / `SONNET` / `OPUS` in settings env route subagent `model: haiku|sonnet|opus` aliases; `model: inherit` follows the main model, which means an all-inherit roster has no split to manage.
- Never split parallel subagents across two LOCAL models on 16GB hosts — parallel agents load both weights at once and swap-thrash; keep parallel rosters on one local model (inherit) with cloud tags on the fast-lane alias instead.
- Model-switch scripts must evict non-target locals (`ollama stop <other-tags>`) before rewriting settings — Ollama's ~5min keepalive otherwise stacks the old weights under the new model and the host swap-thrashes despite only one model being 'selected'.

## Verification

Run `python3 scripts/verify-agents.py [--agents-dir D] [--skills-dir D]`
after any agent/skill change. It parses every agents/* frontmatter, checks
name/description validity, and resolves all `skills:` and `mcpServers:`
preload entries. Exit nonzero means fix before shipping.
