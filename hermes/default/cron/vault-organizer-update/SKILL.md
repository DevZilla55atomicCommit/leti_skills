---
name: vault-organizer-update
description: Tracks organizer script and cron schedule updates.
category: cron
---

# Enhanced Tracker

This skill now covers not only cron job scheduling but also comprehensive vault structural analysis, ensuring all domain maps are synchronized with Hero_index.md and identifying structural drift.

## Core Functions

1. **Cron Job Monitoring**  
   - Daily verification of scheduled jobs (e.g., `Vault Organizer — Dry Run` at `0 3,11,23 * * *`)  
   - Alerts on job failures or missed runs  

2. **Structural Mapping Validation**  
   - Cross-references all vault domains against `Hero_index.md` navigation entries  
   - Detects unlinked files and unmapped top-level domains (e.g., `00 Human/`, `App Development/`)  
   - Validates that referenced files (Security Audit, Technical SOP) exist in correct paths  

3. **Structural Drift Reporting**  
   - Generates `references/structural-audit.md` with findings  
   - Updates `references/vault-structural-fix-template.md` for recurring fixes  
   - Flags unmapped domains and file path mismatches  

4. **Auto-Correction Protocol**  
   - Recommends moving files to correct locations (e.g., relocating `Security Audit Master Index.md` to root)  
   - Updates `Hero_index.md` links or files to root as needed  
   - Creates `references/unmapped-domains.md` for tracking unmapped folders  

5. **Maintenance Schedule**  
   - Daily dry-run at 3am, weekly deep audit on Sundays  
   - Reports findings in `vault-structural-report.md` for user review  

## Vault Path (verified 2026-09-13)

- Canonical vault: `/Volumes/PNY128GBLED/TamaZila Obsidian Vault` (via `~/TamaZila_Obsidian_Vault` symlink). `~/.hermes/scripts/vault_path.txt` must point here.
- `~/TamaZila Obsidian Vault` (with spaces) is a STALE HUSK (2 md files, no graphify-out). Any script resolving to it reports meaningless healthy results. If Keeper/monitor output looks suspiciously small, check the resolved path first.

- Created missing `00-MASTER-INDEX.md` files in:
  - Color Grading & Looks
  - Camera Theory (renamed from `00-INDEX_Camera-Theory.md`)
  - Fusion
  - Post Production
- Fixed broken `[[Collection]]` reference: updated to `[[footage-collection]]` → `collections/footage-collection.md`
- Updated `MASTER_MAPPING.md` cross-references to point to new index files.
- Identified ~1,000+ broken wikilinks in index files, primarily:
  - Analysis JSON references in `INDEX.md` tables (Fusion, Color Grading, Lighting, Video Effects, Masking, Node Structures, Cinematic Grading, Camera Theory)
  - Videographer reel technique links in `00-UNIFIED-MASTER-INDEX.md` (364 broken links)

## Required Data Migration

- **Analysis JSON files**: Verify and migrate missing files from `.vault-organizer-backups/`.
- **Videographer technique files**: Restore missing files from backup or regenerate as needed.
- After migration, run vault structural audit to resolve remaining broken links.

## Ongoing Maintenance

- Monitor `references/unmapped-domains.md` for newly identified unmapped folders.
- Schedule weekly deep audit to keep structural integrity up to date.

## Vault Script Pitfalls

- Verify a configured vault path EXISTS before trusting it — a config file can silently point at a stale directory while every check reports green. Fall back through known-good candidates in order.
- Exclude AppleDouble `._*` files from every vault scan, count, and glob — they match `*.md` and roughly double apparent file counts, poisoning drift reports and change hashes.
- Prefer `no_agent:true` for cron jobs whose script is self-contained (reads inputs, writes outputs, prints one status line) — the wrapping agent call is pure overhead.
- Gate agent cron jobs with a deterministic `monitor` script (sorted full-corpus hash, no timestamps) so the agent wakes only on real change; exclude timestamp-churned files (e.g. memory-sync outputs rewritten every tick) from the monitor corpus or the gate never closes.

## Cron Job UI Limitation (Observed 2026-08-28)

Cron jobs run in **isolated background sessions** — they cannot drive the user's active desktop app UI.

- Actions like `open_preview`, `focus_pane`, `apply_layout`, or any desktop app manipulation **only affect the cron session's own ephemeral environment**, not the user's live Hermes desktop window.
- The cron agent may report "opened in preview pane" as text output, but no tab appears in the user's actual preview pane.
- **Workaround**: For UI actions that must affect the user's live session, run them directly in the foreground chat (not via cron), or use `deliver='all'` / gateway targets to send a notification the user can click.
- Manual `cronjob(action='run')` test runs also execute in isolated sessions — they verify the prompt logic but cannot test UI side effects on the user's desktop.

*Prepared by vault-organizer-update skill on 2026-08-10.*