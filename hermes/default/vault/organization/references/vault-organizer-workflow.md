# Vault Organizer Workflow Reference

## Tool: vault_organizer.py

**Location:** `/Users/alfredkamisese/vault_organizer.py`

**Purpose:** Organizes Obsidian vault structure by classifying misplaced .md files based on frontmatter `collection` field, moving them to correct subfolders, maintaining indexes, and validating link integrity.

## Key Features

- **Dry-run by default** — use `--apply` to execute moves
- **Delta scanning** — only processes files changed since last run (via manifest)
- **No backup** — space efficient (uses manifest for rollback tracking)
- **MAX_MOVES_PER_RUN** — safety limit (default 10, set to 1000 for bulk)
- **Comprehensive logging** — JSONL log + state file + end-of-run manifest

## Classification Rules (from script)

```python
COLLECTION_RULES = {
    "Cinematic": "Cinematic Grading Workflows",
    "Color_grading": "Color Correction Fundamentals",
    "Ideas_for_Shooting_Videos": "Educational Resources",
    "DaVinci_Tricks": "Educational Resources",
    "Export_Videos": "Educational Resources",
    "Drone": "Cinematic Grading Workflows",
    "Car_Shooting_tips": "Automotive & Specialty",
}

VIDEOGRAPHER_COLLECTIONS = {
    "Gimbal_Moves": "Videographer/Camera_Movement",
    "Gimbal": "Videographer/Camera_Movement",
    "Dji_Gimbals_Tips": "Videographer/Camera_Movement",
}
```

## Domain Roots Scanned

- `Color Grading & Looks`
- `Video_Effects`
- `Post_Production`
- `Fusion`
- `Lighting`
- `Camera Theory`

## Validation Checks

- Broken wikilinks
- Orphan files (requires `graphify` tool)
- Missing indexes (00-MASTER-INDEX.md)
- Link chain integrity (requires Memory.md in KB root)

## Typical Workflow

```bash
# Dry-run to preview
python3 /Users/alfredkamisese/vault_organizer.py

# Bulk execute (increase limit first if needed)
python3 /Users/alfredkamisese/vault_organizer.py --apply

# Background for large batches
python3 /Users/alfredkamisese/vault_organizer.py --apply --background
```

## Cron Integration

Runs automatically at 03:00 and 11:00 daily via cron job. Delta scanning keeps subsequent runs fast.

## Known Dependencies

- `graphify` (uv tool install graphifyy) — for code analysis; **NOT** for wikilink validation (see below)
- `Memory.md` in KB root — for link chain validation

## Validation Fix (2026-08-10)

The original `run_validation()` used graphify queries:
- `"broken wikilinks in DaVinci_Knowledge_Base"` → returns code symbols, not actual broken wikilinks
- `"files not linked from any index"` → returns code symbols, not orphan markdown files

**Fix applied:** Replaced with native Python regex-based validation in `vault_organizer.py`:

```python
# Broken wikilinks: scan all .md for [[target]] and verify file exists
wikilink_pattern = re.compile(r'\[\[([^\]]+)\]\]')
# Orphan files: scan index files (INDEX.md, MASTER_*.md, Hero_*.md) for links,
# then find .md files not referenced by any index
```

This correctly identifies actual broken wikilinks and true orphan files.

## Graphify Binary Path

**Corrected:** `/Users/alfredkamisese/.hermes/hermes-agent/venv/bin/graphify` (not `~/.local/share/uv/tools/graphifyy/bin/graphify`)

## Syncthing Conflict Cleanup

Regular cleanup needed for `.obsidian/*.sync-conflict-*` files — they accumulate during concurrent edits across machines.