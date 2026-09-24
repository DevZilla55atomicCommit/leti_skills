---
name: vault-setup
type: skill
description: Comprehensive guide for setting up EMAI Starter Vault with Obsidian
status: active
tags: [vault, setup, emai, starter]
---

# EMAI Starter Vault Setup

This skill documents the complete procedure for setting up the EMAI Starter Vault without modifying the user's main vault.

## Vault Structure

The EMAI Starter Vault follows this structure:
- `00 Human/` — Your territory containing personal notes, tasks, and projects
- `Machine/` — AI territory with workflows, templates, and script outputs
- `System/` — Operating documentation and configuration files

## Setup Procedure

1. Open the vault directory in Obsidian as a new vault
2. Allow community plugins to load (17 plugins pre-configured)
3. Verify key folders exist:
   - `00 Human/`
   - `Machine/`
   - `System/`
4. Install recommended plugins if not auto-loaded:
   - lean-terminal
   - dataview
   - obsidian-git
   - templater
   - other specified plugins

## Core Workflow

The vault includes these core commands

## User Preferences (Embedded from Session)

- Quick path preference: prioritize streamlined setup and immediate value
- Workflow focus: tooling/infrastructure projects, platform-specific workflows
- Task style: priority list over time blocks
- Avoidance pattern: avoids ad-hoc/administrative tasks; concentrates on avoided/overdue work

The vault includes these core commands:
- `/start` — Orientation and setup verification
- `/interview` — Personalizes the vault for your workflow
- `/today` — Daily planning using compiled prompts
- `/closeday` — Daily closure and reflection
- `/new` — Captures brain dumps in appropriate locations
- `/meeting-notes` — Structures meeting capture

## Verification Steps

To verify proper setup:
1. Check that all key folders exist
2. Confirm plugins load without errors
2. Run `/start` command to verify orientation workflow
4. Check that `/interview` executes without errors

## Known Issues & Workarounds

- When using Claude Code CLI with Ollama, ensure the API endpoint is correctly configured
- Avoid accidentally modifying files outside the vault structure
- For large vaults, allow extra time for plugin initialization

## Support Files

This skill includes supporting files:
- `references/setup-steps.md` — Condensed step-by-step setup guide
- `templates/vault-config.yaml` — Example configuration template
- `scripts/verify-setup.py` — Automated verification script
- `references/connection-strategy.md` — Documented connection strategy for linking starter and main vaults
- `references/external-vault-migration.md` — Diagnostic, classification, and transfer plan for moving large vaults to external APFS volumes