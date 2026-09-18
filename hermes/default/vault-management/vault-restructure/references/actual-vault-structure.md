# Actual Vault Structure (Discovered 2026-08-06)

## Root Location
- **Physical**: `/Volumes/PNY128GBLED/TamaZila Obsidian Vault/`
- **Symlink**: `/Users/alfredkamisese/TamaZila_Obsidian_Vault` → above

## Domain Folders (Nested Under DaVinci_Knowledge_Base)
All expected domain folders exist but are **one level deeper** than cron job config assumes:

| Domain | Actual Path |
|--------|-------------|
| Color Grading & Looks | `Hermes Agent/DaVinci_Knowledge_Base/Color Grading & Looks/` |
| Camera Theory | `Hermes Agent/DaVinci_Knowledge_Base/Camera Theory/` |
| Cinematic Grading Workflows | `Hermes Agent/DaVinci_Knowledge_Base/Cinematic Grading Workflows/` |
| Video_Effects | `Hermes Agent/DaVinci_Knowledge_Base/Video_Effects/` |
| Fusion | `Hermes Agent/DaVinci_Knowledge_Base/Fusion/` |
| Lighting | `Hermes Agent/DaVinci_Knowledge_Base/Lighting/` |
| Masking & Power Windows | `Hermes Agent/DaVinci_Knowledge_Base/Masking & Power Windows/` |
| Node Structures & Templates | `Hermes Agent/DaVinci_Knowledge_Base/Node Structures & Templates/` |
| Post_Production | `Hermes Agent/DaVinci_Knowledge_Base/Post_Production/` |
| Color Management & Pipeline | `Hermes Agent/DaVinci_Knowledge_Base/Color Management & Pipeline/` |
| Learning Resources & Guides | `Hermes Agent/DaVinci_Knowledge_Base/Learning Resources & Guides/` |
| Photography_Videography | `Hermes Agent/DaVinci_Knowledge_Base/Photography_Videography/` |
| Videographer | `Hermes Agent/DaVinci_Knowledge_Base/Videographer/` |

## Cron Job Path Mismatch
The cron job `696058de26a8` ("Vault Organizer — Dry Run") references:
- Script: `/Users/alfredkamisese/vault_organizer.py` → **DOES NOT EXIST**
- Domain roots at vault root → **WRONG** (they're under `Hermes Agent/DaVinci_Knowledge_Base/`)

## Existing Organizer Script
Specialized reorganizer exists at:
- `/Users/alfredkamisese/vision_pipeline/reorganize_vault.py`
- Targets `DaVinci_Knowledge_Base/` structure
- Uses `VISION_PROGRESS.json` + `techniques/` + `skills/` + `media/` + `analysis/`
- Maps by `resolve_page` + `collection` frontmatter

## Backup Evidence
Vault organizer backups exist at:
- `/Volumes/PNY128GBLED/TamaZila Obsidian Vault/.vault-organizer-backups/` (4 runs)
- `/Volumes/PNY128GBLED/TamaZila Obsidian Vault/.vault-organizer-manifests/` (empty)

This suggests prior organizer runs (possibly `vision_pipeline/reorganize_vault.py` or manual).

## Forex Center & Developer Workflows Drift
- **Forex Center actual path**: `Hermes Agent/Forex Center/` (not vault root). Contains `Memory.md` + `Momentum/` only; the four folders promised in `Memory.md` (`Market_Dynamics/`, `Technical_Indicators/`, `Automated_Strategy/`, `Trading_Logics/`) do not exist, notes carry no frontmatter and zero wikilinks, and the Momentum notes reference a wrong stored path plus a `Developer Workflows/Python_Automation` folder that also does not exist.
- **Audit rule from this**: a zero-result filename search on a large vault is not conclusive — verify with `find <vault> -maxdepth N -type d -iname '*name*'` before declaring a folder missing.