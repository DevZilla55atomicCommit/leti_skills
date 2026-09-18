# Vault Organizer Validation Patterns & Pitfalls

## Context
The `vault_organizer.py` script runs daily dry-runs and validates vault integrity. Its `run_validation()` function checks:
1. Broken wikilinks (`[[target]]` references to missing files)
2. Orphan files (technique files not linked from any index)
3. Missing indexes (folders without `INDEX.md`)
4. Link chain integrity (MASTER_MAPPING.md, Memory.md, Hero_index.md)

## Critical Pitfalls Discovered (2026-08-10)

### 1. Graphify Binary Path Mismatch
- **Problem**: `vault_organizer.py` hardcoded `/Users/alfredkamisese/.local/share/uv/tools/graphifyy/bin/graphify`
- **Actual location**: `/Users/alfredkamisese/.hermes/hermes-agent/venv/bin/graphify`
- **Fix**: Updated both occurrences in `run_validation()` to use the correct path

### 2. Structural "Broken Wikilinks" — Analysis JSON References
- **Problem**: Index tables (e.g., `Color Grading & Looks/index.md`) have an "Analysis" column with links like `[[analysis/CwNVpUJpQUL/analysis.json]]`
- **Reality**: These `analysis/VIDEO_ID/analysis.json` files **never exist** — they were planned but not generated
- **Impact**: 11,000+ false "broken wikilinks" in validation
- **Fix**: Skip validation for targets matching `analysis/.../analysis.json` pattern and `analysis/...` (non-.md) patterns

### 3. Over-Broad Orphan Counting
- **Problem**: Original code counted ALL `.md` files in vault (20,895 files) as potential orphans
- **Reality**: Only DaVinci KB technique/skill folders should be indexed:
  - `skills/`
  - `techniques/`
  - `Color Grading & Looks/`
  - `Video_Effects/`
  - `Fusion/`
  - `Lighting/`
  - `Camera Theory/`
  - `Cinematography/`
- **Impact**: 18,000+ false orphans (including `.obsidian/`, `graphify-out/`, `analysis/`, etc.)
- **Fix**: Restrict orphan counting to technique folders only

### 4. Wikilink Resolution Strategy
- **Correct approach**: Index all `.md` filenames → map name → check if target exists anywhere in vault by filename
- **Don't**: Try to resolve relative paths from source file (wikilinks in index tables use bare filenames like `Advanced-Color-Grading-...md`)

## Validation Logic (Current)

```python
# Build name-to-path index
name_to_paths = {}
for md_file in VAULT_ROOT.rglob("*.md"):
    name_to_paths[md_file.name].append(md_file.relative_to(VAULT_ROOT).as_posix())

# Check wikilinks - skip analysis/... patterns
if target.startswith("analysis/") and (target.endswith("/analysis.json") or not target.endswith(".md")):
    continue

# Check by filename
found = target in name_to_paths \
     or (target.endswith('.md') and target[:-3] in name_to_paths) \
     or (not target.endswith('.md') and f"{target}.md" in name_to_paths)

# Orphan counting - restricted to technique folders
technique_folders = [DAVINCI_KB / "skills", DAVINCI_KB / "techniques", ...]
for folder in technique_folders:
    if folder.exists():
        for md_file in folder.rglob("*.md"):
            if md_file.name not in linked_names:
                orphan_count += 1
```

## Expected Healthy Numbers (Post-Fix)
- **Broken wikilinks**: ~0 (after skipping analysis/... patterns)
- **Orphan files**: ~0 (after restricting to technique folders and indexing them)
- **Missing indexes**: 0
- **Link chain**: OK

## Running Validation Manually
```bash
cd /Volumes/PNY128GBLED/TamaZila\ Obsidian\ Vault
python3 ~/vault_organizer.py
```

## Cron Integration
The Vault Organizer runs via cron job `Vault Organizer — Dry Run` (job_id: `696058de26a8`) at 03:00, 11:00, 23:00 daily.