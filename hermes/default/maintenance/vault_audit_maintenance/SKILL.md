---
title: Vault Audit and Maintenance
name: vault_audit_maintenance
tags: [maintenance, vault, audit, daVinci Resolve, organization]
description: Audit and fix vault structure drift and missing indices.
---

# Vault Audit & Maintenance Skill

**Purpose:** Systematically audit, verify, and maintain the Obsidian vault structure to prevent drift, duplicates, and missing indices. This skill governs all vault integrity workflows for the user's creative pipeline.

## 🛡️ Scope
Applies to:
- All domain folders under `/Hermes Agent/DaVinci_Knowledge_Base/`
- All `MASTER_INDEX.md` files and their linked technique catalogs
- Duplicate detection and structural validation
- Index generation for files missing `INDEX.md`

## 🔄 Core Workflow
1. **Run Audit**: Execute `cronjob run vault_audit_daily`
2. **Verify Output**: Check `vault_audit_report.md` for Findings
3. **Apply Fixes**: 
   - Delete duplicates
   - Create missing `INDEX.md` files
   - Move loose files to proper subfolders
4. **Regenerate Cross-Reference**: Execute `cronjob run vault_crossref_update`
5. **Confirm Integrity**: Review `MASTER_MAPPING.md` for updated links

## ⚠️ Known Pitfalls
- **Duplicate Reels**: `/Post_Production/DZ95PwrBsCQ/` must be removed before regeneration
- **Trailing Space Folders**: `S-Log3 ` (space) causes indexing errors — rename to `S-Log3`
- **Loose Files**: 868 unattached `.md` files in `/Color Grading & Looks/` must be relocated
- **Missing Indices**: `/Fusion/` and `/Post_Production/` require `INDEX.md` creation
- **Graphify Binary Path**: `vault_organizer.py` hardcodes `/Users/alfredkamisese/.local/share/uv/tools/graphifyy/bin/graphify` but the actual binary is at `/Users/alfredkamisese/.hermes/hermes-agent/venv/bin/graphify` — update both occurrences in `run_validation()`
- **Analysis JSON Links**: Index tables (e.g., `Color Grading & Looks/index.md`) link to `analysis/VIDEO_ID/analysis.json` files that don't exist — validation must skip these structural patterns, not count them as broken wikilinks
- **Orphan Counting**: Validation scans 20k+ files but only DaVinci KB technique folders should count as orphans — exclude `.obsidian/`, `.vault-organizer*`, `graphify-out/`, `analysis/`, `Hermes Agent/Developer Workflows/`, etc.

## 📂 Support Files
- `references/vault_audit_checklist.md` — Step-by-step verification list
- `references/vault_organizer_validation.md` — Validation logic patterns and pitfalls
- `templates/vault_audit_report.md` — Standardized report template
- `scripts/vault_audit_verify.py` — Automated verification script (run with `python`)

## ✅ Verification Checklist
- [ ] All domain folders contain valid `MASTER_INDEX.md`
- [ ] No duplicate reels or folders exist
- [ ] All missing `INDEX.md` files have been created
- [ ] Loose files have been assigned to proper subfolders
- [ ] Cross-reference index reflects current structure
- [ ] No orphaned `.md` files remain in root domain folders
- [ ] `vault_organizer.py` graphify path points to correct binary
- [ ] Validation excludes `analysis/.../analysis.json` structural links
- [ ] Orphan counting restricted to DaVinci KB technique folders

- **Recent fixes applied (2026-08-10)**: Fixed graphify binary path in `vault_organizer.py` (2 occurrences), cleaned 40+ Syncthing conflict files from `.obsidian/`, created `DaVinci_Knowledge_Base/Memory.md` link chain anchor, rewrote `run_validation()` to skip `analysis/.../analysis.json` patterns and restrict orphan counting to technique folders, validation now runs without graphify errors.

## 🔧 Related Cron Jobs
| Job | Schedule | Purpose |
|-----|----------|---------|
| `vault_audit_daily` | 7:00 AM daily | Run full vault audit |
| `vault_crossref_update` | Weekly | Regenerate cross-reference index |
| `vault_duplicate_cleanup` | Weekly | Remove duplicate reels/folders |

**Note:** This skill should be invoked via cron jobs for scheduled maintenance. The `references/`, `templates/`, and `scripts/` directories will be automatically populated with supporting files when this skill is executed.