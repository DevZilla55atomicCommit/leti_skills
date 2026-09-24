---
name: hermes-ecosystem-integration
description: "Integrate agent ecosystems (ECC) into Hermes via installers."
version: 1.0.0
author: Maddie
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    tags: [hermes, ecosystem, integration, ecc, agent-frameworks]
    related_skills: [hermes-agent, github-repo-management]
---

# Hermes Ecosystem Integration

Guide for evaluating and integrating large AI agent ecosystems (like ECC — Everything Claude Code / Engineering Control Center) into Hermes. These are **not single skills** but entire frameworks with agents, skills, commands, hooks, rules, and security scanning.

## Trigger

Use when:
- User asks to "install X as a skill" where X is a large repo (ECC, Agentic OS, etc.)
- Evaluating whether an external framework belongs in Hermes as-is or needs adaptation
- Need to cherry-pick components from a large ecosystem rather than full install

---

## Core Distinction: Ecosystem vs Skill

| Aspect | Single Skill | Agent Ecosystem (ECC, etc.) |
|--------|--------------|----------------------------|
| Scope | One workflow/domain | 67 agents, 281 skills, 94 commands, hooks, rules, AgentShield |
| Install | `skill_manage create` or copy to `~/.hermes/skills/` | Platform-specific installer (`install.sh --target hermes`) |
| Structure | Self-contained directory with SKILL.md | Multi-directory repo (agents/, skills/, commands/, rules/, hooks/) |
| Maintenance | Update individually | Versioned releases, plugin marketplace, sync flows |

**Rule:** Never try to "install an ecosystem as a skill." Use the ecosystem's own install path for the target harness.

---

## ECC-Specific Integration (Reference Pattern)

ECC (github.com/affaan-m/ECC) is the primary ecosystem with Hermes support. This pattern applies to similar frameworks.

### 1. Evaluate First

```bash
# Clone and inspect structure
git clone https://github.com/affaan-m/ECC.git
ls ECC/
# Look for: .hermes/README.md, docs/HERMES-SETUP.md, install.sh, package.json
```

**Key indicators of Hermes support:**
- `.hermes/README.md` with install instructions
- `docs/HERMES-SETUP.md` with architecture guide
- `install.sh` accepting `--target hermes`
- `.codex-plugin/plugin.json` (shows skill packaging pattern)

### 2. Choose Install Profile

| Profile | Use When |
|---------|----------|
| `minimal` | Rules + core skills only, no hook runtime (recommended for Hermes) |
| `core` | Standard install with baseline hooks |
| `full` | Everything (avoid on Hermes — duplicates plugin-managed hooks) |

```bash
# Minimal (recommended)
cd ECC
./install.sh --target hermes --profile minimal
# or without cloning:
npx ecc-install --profile minimal --target hermes
```

### 3. What Gets Installed (Minimal Profile)

```
~/.hermes/
├── skills/ecc-imports/        # 281 ECC skills → Hermes skills
├── rules/ecc/                 # Rule packs (common + your stack)
├── commands/                  # 94 slash-commands
├── AGENTS.md                  # Agent instructions
└── plugins/                   # Bridge plugins for hooks/reminders
```

**Hermes config files (`config.yaml`, `.env`) are NOT touched.**

### 4. Cherry-Pick Alternative (When Full Install Is Overkill)

If you only need specific skills (e.g., `tdd-workflow`, `security-review`, `verification-loop`):

```bash
# From cloned repo:
cp -r .agents/skills/tdd-workflow ~/.hermes/skills/
cp -r .agents/skills/security-review ~/.hermes/skills/
cp -r .agents/skills/verification-loop ~/.hermes/skills/
```

Each ECC skill in `.agents/skills/` is a standalone skill directory compatible with Hermes' skill loader.

### 5. Post-Install Verification

```bash
# Health check
npx ecc doctor --target hermes

# Verify skills loaded
ls ~/.hermes/skills/ecc-imports/ | head -20

# Test a skill
# (In Hermes chat) use the skill name directly
```

### 6. Rule Packs (Add Separately)

ECC rules are always-loaded context. Install only what you use:

```bash
mkdir -p ~/.hermes/rules/ecc
cp -r ECC/rules/common ~/.hermes/rules/ecc/
cp -r ECC/rules/typescript ~/.hermes/rules/ecc/  # or python, go, rust, etc.
```

Start with `common` + one language pack. Rules are additive — more rules = more context window usage.

---

## General Pattern for Other Ecosystems

When evaluating a new ecosystem (Agentic OS, custom frameworks, etc.):

1. **Check for harness-specific install** — look for `--target hermes`, `.hermes/`, `docs/HERMES-*.md`
2. **Identify component boundaries** — agents vs skills vs commands vs rules vs hooks
3. **Prefer minimal/profile-based install** — avoid "full" unless you need hooks/runtime
4. **Verify config isolation** — ecosystem should not overwrite `config.yaml`, `.env`, or existing skills
5. **Test skill discovery** — installed skills must appear in Hermes skill list and be invokable

---

## Pitfalls

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| Installing ecosystem as single skill | `skill_manage create` fails or creates unusable monster skill | Use ecosystem's `--target hermes` installer |
| Running full install on Hermes | Duplicate hooks, plugin conflicts, bloated context | Use `--profile minimal` |
| Copying raw hooks.json to settings.json | Duplicate hook execution, cross-platform conflicts | Use installer's `--modules hooks-runtime` |
| Installing all 281 skills | Context window bloat, slow skill discovery | Cherry-pick only needed skills |
| Ignoring rule pack selection | Unnecessary always-loaded context | Install only `common` + your stack |
| Expecting "full" to install all 280 skills | Only 134 skills in `~/.hermes/skills/`; 17 modules skipped | Check installer output for "Skipped modules" list; cherry-pick from npm package |
| Assuming `.agents/skills/` = all skills | Only 39 Hermes-native skills (with `agents/openai.yaml`); rest in `skills/` | Use `~/.npm-global/lib/node_modules/ecc-universal/skills/` for full set |
| Missing `ecc-install` binary | `ecc-install: command not found` after `npm i -g ecc-universal` | Use `node scripts/install-apply.js` directly from package or add npm bin to PATH |

---

## Related Skills

- `hermes-agent` — Hermes configuration, tools, providers (bundled, protected)
- `github-repo-management` — Cloning, inspecting repos (used to fetch ECC)
- `hermes-desktop-plugins` — Writing plugins for Hermes UI panes/commands

---

## References

- `references/ecc-hermes-install.md` — ECC-specific install notes from session
- `references/ecosystem-evaluation-checklist.md` — Checklist for evaluating new ecosystems
- `references/ecc-install-session-2026-08-04.md` — Detailed session log of minimal→full ECC install into Hermes, actual commands, module mapping, and cherry-pick guidance