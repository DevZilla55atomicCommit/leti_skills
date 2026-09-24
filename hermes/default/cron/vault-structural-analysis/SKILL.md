---
name: vault-structural-analysis
description: Syncs domain maps for vault integrity. (60 chars)
category: cron
tags: [structural, audit, vault-management]
---

# Vault Structural Analysis

## Overview
Ensures all vault directories are correctly mapped in Hero_index.md, detecting unmapped top-level folders and path mismatches.

## Core Functions
1. Structural mapping validation via cross-referencing
2. Drift detection with audit-report.md output
3. Auto-correction protocol for file relocations
4. Maintenance reporting in vault-structural-report.md

## Triggers
- Manual execution: /vault-structural-analyze
- Scheduled: daily @ 3am, weekly deep audit Sundays

## Support Files
references/audit-report.md - Current audit findings
templates/audit-template.md - Standard report template
scripts/audit-check.sh - Validation execution wrapper

## Dependencies
Requires vault_organizer.py at /Users/alfredkamisese/TamaZila Obsidian Vault/vault_organizer.py
Relies on graphify for knowledge graph analysis

## Execution
vault-structural-analyze --mode=daily | --mode=deep