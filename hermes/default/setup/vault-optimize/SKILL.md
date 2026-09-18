---
name: vault-optimize
type: skill
description: Optimized workflow for EMAI vault setup and daily operations with quick-start patterns
status: active
tags: [vault, optimization, workflow]
---

# EMAI Vault Optimization

This is the umbrella skill for optimizing EMAI vault setup and daily workflows based on user preferences for speed, separation of concerns, and minimal configuration overhead.

## Core Principles

1. **Quick Path First**: Prioritize immediate value delivery over comprehensive setup
2. **Structural Separation**: Maintain clear boundaries between starter and main vaults
3. **Minimal Configuration**: Avoid unnecessary setup steps unless verified requirements emerge
4. **Daily Operation Ready**: Focus on workflows that generate value immediately

## Setup Optimization Patterns

### Vault Connection Strategy
- Keep starter vault separate using dedicated directory structures
- Use symlinks for shared contexts when merging is desired
- Connection verification: check for duplicate folder names between vaults

### Verification Protocol
- Run `verify-setup.sh` to validate directory structure and plugin status
- Check plugin versions against documented compatibility matrix
- Validate API endpoints before relying on automated workflows

## User-Specific Patterns

### Quick Path Configuration
- Skip non-essential plugin installations
- Use pre-configured prompt templates instead of dynamic generation
- Prioritize `/today` workflow over complex setup rituals

### Ollama Configuration
- Direct API endpoint configuration: `http://localhost:11434/v1`
- Model selection based on task complexity:
  - `qwen3.5-32k:latest` for general workflows
  - `phi4:14b` for lightweight verification tasks

## Workflow Templates

### Daily Operations
- `/today` → Priority list generation with minimal input
- `/closeday` → Reflective metrics tracking with automatic log generation
- `/new` → Brain dump capture in standardized locations

### Connection Management
- `/link-vaults` → Verify and establish connections between vaults
- `/disconnect-vaults` → Safe disconnection without data loss

## Verification Script

### Checklist
1. All required folders present in vault structure
2. Core plugins loaded without errors
3. API endpoints responding correctly
4. No duplicate identifier conflicts between vaults

## Support Files

- `references/quick-start-patterns.md` — Condensed step-by-step setup guide
- `references/external-vault-migration.md` — Diagnostic, classification, and transfer plan for moving large vaults to external APFS volumes

---