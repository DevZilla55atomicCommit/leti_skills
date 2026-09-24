---
name: ecc-installation
description: Install ECC into Hermes, Codex, and other agent harnesses.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [ECC, installation, harness, plugin, setup]
    related_skills: [hermes-agent, configure-ecc]
---

# ECC Installation

Install the **Engineering Control Center (ECC)** ecosystem into your agent harness. ECC provides 67 agents, 281+ skills, 94 commands, hooks, rules, and AgentShield security scanning.

## Supported Harnesses

| Harness | Install Method | Notes |
|---------|---------------|-------|
| **Hermes** | `ecc-install --profile minimal --target hermes` | Via ecc-universal npm package |
| **Claude Code** | `/plugin marketplace add https://github.com/affaan-m/ECC` + `/plugin install ecc@ecc` | Plugin-first (recommended) |
| **Codex** | `git clone ... && npm install && bash scripts/sync-ecc-to-codex.sh` | Sync flow (preserves existing config) |
| **Cursor** | `./install.sh --profile minimal --target cursor` | Project-local `.cursor/` adapter |
| **Others** | See `docs/MANUAL-ADAPTATION-GUIDE.md` | OpenCode, Gemini, Zed, Qwen, etc. |

## Quick Start (Hermes)

### Prerequisites
- Node.js + npm
- Hermes installed and configured

### Install
```bash
# 1. Install ECC universal CLI
npm install -g ecc-universal

# 2. Run minimal install for Hermes
ecc-install --profile minimal --target hermes
# Or if ecc-install not on PATH:
node $(npm root -g)/ecc-universal/scripts/install-apply.js --profile minimal --target hermes
```

### What Gets Installed (Minimal Profile)
```
~/.hermes/
├── agents/                    # 67 specialist agents
├── .agents/skills/            # 281+ skills (Hermes-native format with agents/openai.yaml)
├── skills/                    # 281+ skills (standard format)
├── commands/                  # 94 slash-commands
├── rules/                     # 23 language packs (common, typescript, python, etc.)
├── mcp-configs/
│   └── mcp-servers.json      # MCP server definitions (opt-in)
├── scripts/                   # Helper scripts
└── ecc-install-state.json    # Install state for upgrades/uninstall
```

**Preserved:** Your existing `config.yaml`, `.env`, skills, memories, and Hermes setup are **not modified**.

### Verify Installation
```bash
ecc doctor --target hermes
# Status: OK
# Issues: none
```

## Profiles

| Profile | Components | Use Case |
|---------|------------|----------|
| `minimal` | rules-core, agents-core, commands-core, platform-configs, skill-unified-memory, workflow-quality | **Recommended default** — no hook runtime |
| `core` | minimal + hooks-runtime | Adds automated enforcement hooks |
| `full` | All components | Everything including legacy command shims |

### Add Components Later
```bash
# Add hook runtime to existing minimal install
ecc-install --target hermes --modules hooks-runtime

# Add specific skills
ecc-install --target hermes --skills tdd-workflow,security-review

# Add capability pack
ecc-install --target hermes --with capability:machine-learning
```

## Hermes-Specific Notes

### Skill Formats
ECC installs skills in **two locations** for Hermes compatibility:

1. **`~/.hermes/.agents/skills/<skill>/`** — Hermes-native format with `agents/openai.yaml` for agent delegation
2. **`~/.hermes/skills/<skill>/`** — Standard skill format (SKILL.md only)

Both are usable. The `.agents/skills/` format enables Hermes' agent delegation features.

### Rules
Rules are installed to `~/.hermes/rules/<language>/`. Start with:
```bash
# Already installed by minimal profile
~/.hermes/rules/common/
~/.hermes/rules/typescript/   # or your stack
```

### MCP Servers
Only `chrome-devtools` is enabled by default. Others in `~/.hermes/mcp-configs/mcp-servers.json` are opt-in. Copy desired entries to your harness MCP config.

### Memory Vault (Cross-Harness Handoffs)
```bash
# Install separately
npm install -g ecc-universal
ecc memory init --scope project --scope team
```
Then register `ecc-memory-mcp` in each harness that needs tool access.

## Troubleshooting

### `ecc-install` Not Found After `npm install -g ecc-universal`
The binary may not be on PATH. Use the direct script path:
```bash
node $(npm root -g)/ecc-universal/scripts/install-apply.js --profile minimal --target hermes
```

### Doctor Reports Issues
```bash
ecc doctor --target hermes
# Or direct:
node $(npm root -g)/ecc-universal/scripts/ecc.js doctor --target hermes
```

### Upgrade ECC
```bash
npm update -g ecc-universal
ecc-install --target hermes --profile minimal  # Re-runs with new version
```

### Uninstall
```bash
ecc-install --target hermes --uninstall
# Or manually remove ~/.hermes/ecc-install-state.json and the installed files
```

## Pitfalls

- **Do not stack install methods** — e.g., don't run both plugin install AND manual install for the same harness
- **Minimal profile excludes hooks** — Add `hooks-runtime` module only if you want automated enforcement
- **MCP servers are opt-in** — Default `.mcp.json` only includes `chrome-devtools`
- **Config files untouched** — Your `config.yaml`, `.env`, existing skills are preserved
- **PATH issues** — Use `$(npm root -g)/ecc-universal/scripts/` prefix if binaries not linked

## References

- `references/hermes-install.md` — Detailed Hermes installation log and verification steps
- `references/harness-comparison.md` — Profile and component matrix across harnesses