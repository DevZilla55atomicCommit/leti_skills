---
source: session evaluation of https://github.com/affaan-m/ECC.git
date: 2026-08-04
harness: hermes
ecosystem: ECC (Everything Claude Code / Engineering Control Center)
version: 2.1.0
---

# ECC-Hermes Install Notes

## Repo Structure (Cloned to /tmp/ECC)

```
ECC/
├── .hermes/README.md          # Hermes-specific install guide
├── docs/HERMES-SETUP.md       # Full architecture guide
├── install.sh                 # Multi-target installer (--target hermes)
├── .codex-plugin/plugin.json  # Shows skill packaging pattern
├── .agents/skills/            # 281 skills (Hermes-compatible)
├── agents/                    # 67 agent definitions
├── commands/                  # 94 slash-commands
├── rules/                     # Rule packs (common, typescript, python, etc.)
├── mcp-configs/               # MCP server definitions
├── ecc2/                      # Rust control plane (alpha)
└── docs/                      # Extensive per-harness guides
```

## Hermes Install Path

Per `.hermes/README.md`:
```bash
bash ./install.sh --target hermes --profile minimal
# or
npx ecc-install --profile minimal --target hermes
```

## What Minimal Profile Installs

```
~/.hermes/
├── skills/ecc-imports/        # 281 ECC skills → Hermes skills
├── rules/ecc/                 # Rule packs (common + your stack)
├── commands/                  # 94 slash-commands
├── AGENTS.md                  # Agent instructions
└── plugins/                   # Bridge plugins for hooks/reminders
```

**Config isolation:** Hermes config files (`config.yaml`, `.env`) are NOT touched.

## Cherry-Pick Skills (Alternative)

Individual ECC skills are standalone directories in `.agents/skills/` compatible with Hermes:
```bash
cp -r .agents/skills/tdd-workflow ~/.hermes/skills/
cp -r .agents/skills/security-review ~/.hermes/skills/
cp -r .agents/skills/verification-loop ~/.hermes/skills/
```

## Rule Packs (Add Separately)

```bash
mkdir -p ~/.hermes/rules/ecc
cp -r ECC/rules/common ~/.hermes/rules/ecc/
cp -r ECC/rules/typescript ~/.hermes/rules/ecc/  # pick your stack
```

## Post-Install Verification

```bash
npx ecc doctor --target hermes
ls ~/.hermes/skills/ecc-imports/ | head -20
```

## Key ECC Stats (v2.1.0)

- 67 agents (planner, architect, code-reviewer, security-reviewer, etc.)
- 281 skills (TDD, security, research, docs, frontend, ML, ops)
- 94 commands (/plan, /tdd, /security-scan, /code-review, /build-fix)
- Hooks runtime (pre-compact, session summaries, verification loops)
- AgentShield security scanner
- Memory Vault (cross-harness handoff: Hermes ↔ Codex ↔ Claude)

## npm Package

`ecc-universal@2.1.0` — provides `ecc`, `ecc-control-pane`, `ecc-install`, `ecc-memory-mcp`, `ecc-plan-canvas` binaries.