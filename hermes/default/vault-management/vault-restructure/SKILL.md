---
name: vault-restructure
description: Fix vault drift via metadata audit
status: active
tags: [vault, organization, cleaning, restructuring]
related_skills: ["vault-audit", "vault-setup"]
---
This skill implements a production-grade process for resolving vault structural drift by systematically auditing, cleaning, and reorganizing content based on frontmatter metadata and mapping requirements.

## Trigger Condition
Run when:
- Vault shows missing indices
- Files exist outside expected folders
- Cross-references are broken
- Structural drift is detected

## Core Workflow
1. Scan content for metadata
2. Identify orphaned/orphaned items
3. Resolve conflicts
4. Create missing indices
5. Migrate items appropriately

## P0 Fixes
- Delete sync‐conflict files
- Delete macOS metadata junk (`._*` AppleDouble files, `.DS_Store`) — exFAT/USB vaults accumulate them and they inflate audits
- Remove empty folders

## P1 Fixes
- Regenerate master indexes
- Verify link integrity

## Support Files
- `references/vault-restructure-protocol.md` - Fix steps
- `references/actual-vault-structure.md` - Discovered vault layout & cron job path mismatches
- `references/vault-organizer-cron-fix.md` - Vault Organizer cron job root cause & fixes (wrong VAULT_ROOT, overbroad PROTECTED_PATHS)
- `scripts/vrf-maintenance.md` - Maintenance script

## Integration
Use when user requests vault restructuring, reorganizing folders, or fixing indexing issues.

- Requires explicit user context specifying vault root and current structural issues
- Confirm rebuild scope (cleanup-only vs structure-only vs full rebuild with content stubs) before any deletion or folder creation — vault moves are hard to undo on external drives
- When user clarifies vault location (e.g., '/Users/alfredkamisese/TamaZila Obsidian Vault'), embed that path in all subsequent vault operations.
- When user provides machine specs (e.g., 'MacBook Pro M2, 16 GB RAM'), reference them in performance-sensitive steps (e.g., indexing may be CPU-bound).
- When user requests backup cleanup, verify file patterns (e.g., state.db.pre-update-emergency-*.bak) and confirm before deletion.
- When user emphasizes safety around pinned sessions, check session pin status (source=cron or source=desktop) before performing delete or cleanup actions.
- When user reports storage pressure, prioritize removal of cron dump artifacts and emergency backup files, as demonstrated in recent cleanup of request_dump_*.json and *.bak files.

for broader vault coverage, also consult domain-specific index files (e.g., `DaVinci_Knowledge_Base/MASTER_MAPPING.md`, `Developer Workflows/Memory.md`, `Forex Center/Memory.md`, `Photography/Memory.md`).\n\nSee also: references/vault-storage-optimization.md\n\n---