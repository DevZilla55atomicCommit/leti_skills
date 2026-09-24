# Step Beyond — Obsidian Vault Memory Sync Implementation
<!-- Reference implementation of the Step Beyond memory protocol using Obsidian as durable store -->

## Overview

This documents the concrete sync architecture built in session 2026-07-13 for persisting Step Beyond user-patterns.md across Hermes sessions, context compressions, and restarts.

## Architecture

```
┌─────────────────────┐     --pull (session start)      ┌──────────────────┐
│  Obsidian Vault     │ ──────────────────────────────▶ │  Hermes Memory   │
│  step-beyond-       │                                 │  user.json       │
│  user-patterns.md   │                                 │  (builtin)       │
└─────────────────────┘                                 └──────────────────┘
        ▲                                                   │
        │                                                   │
        │     --push (session end / cron 30m)              │
        └───────────────────────────────────────────────────┘
```

## Files

| File | Role |
|------|------|
| `TamaZila Obsidian Vault/Hermes Agent/Hermes Memory/step-beyond-user-patterns.md` | Source of truth (Obsidian) |
| `~/.hermes/scripts/sync_step_beyond_memory.py` | Bidirectional sync logic |
| `TamaZila Obsidian Vault/Hermes Agent/session_end_step_beyond.sh` | Session end hook (push) |
| `~/.hermes/scripts/sync_step_beyond_memory.py` | Cron job entry point (push) |

## Sync Script Interface

```bash
python3 ~/.hermes/scripts/sync_step_beyond_memory.py --pull   # Obsidian → Hermes
python3 ~/.hermes/scripts/sync_step_beyond_memory.py --push   # Hermes → Obsidian
python3 ~/.hermes/scripts/sync_step_beyond_memory.py --status # Verify sync
```

## Cron Job

- **Name**: `step-beyond-memory-sync`
- **Schedule**: `every 30m`
- **Command**: `sync_step_beyond_memory.py --push`
- **Job ID**: `7e54178aa1b0`
- **Delivery**: `local` (no notification)

## Session Hooks

The session end hook pushes current patterns to Obsidian:

```bash
# Session end (run manually or via shell trap)
source ~/TamaZila\\ Obsidian\\ Vault/Hermes\\ Agent/session_end_step_beyond.sh
```

Session start is handled implicitly by the `--pull` command when needed, or run manually:
```bash
python3 ~/.hermes/scripts/sync_step_beyond_memory.py --pull
```

## Memory Format

The patterns file follows the Step Beyond `templates/user-patterns.md` schema:

```markdown
# Step Beyond — User Patterns
updated: YYYY-MM-DD

## Profile          # Stable facts for CONTEXT stage
## Reinforced       # Accepted 2×+ → default L2 initiative
## Banned           # Rejected 2×+ → hard filter
## Watching         # Single signals → Reinforced/Banned
## Trajectories     # Multi-session sequences → L3 prediction
## Open Loops       # Unfinished threads → close next session first
## Session Context  # Transient, cleared on session end
```

## Key Design Decisions

1. **Obsidian is source of truth** — survives Hermes restarts, config changes, compression
2. **Hash-based dedup** — SHA256 prevents redundant writes
3. **Scope-tagged in Hermes** — `scope: step-beyond-patterns` isolates from general memory
4. **Append-only in Obsidian** — Hermes pushes add timestamped sections; manual edits win on pull
5. **Cron catches mid-session drift** — 30m push ensures durability even if session ends uncleanly

## Integration with Step Beyond Protocol

| Protocol Stage | Sync Touchpoint |
|----------------|-----------------|
| CONTEXT | `--pull` loads patterns before any task |
| LEARN | `--push` persists new Open Loops/Trajectories |
| — | Cron provides safety net |

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| "No patterns in Obsidian" | Copy `templates/user-patterns.md` to vault path |
| "Hermes memory file not found" | First `--pull` creates it |
| "Hash mismatch after push" | Manual edit in Obsidian → run `--pull` |
| Cron not running | `hermes cron list` → check enabled, `hermes cron run step-beyond-memory-sync` |
| \"Script not found\" on cron run | Script path in cron job must match actual script location (`~/.hermes/scripts/sync_step_beyond_memory.py`). Fix via `hermes cron edit <job-id>` or recreate job. |

## Extending to Other Vaults/Profiles

The script uses hardcoded paths. To generalize:
1. Parameterize vault path via env var or config
2. Support multiple pattern files (per-project, per-domain)
3. Add conflict resolution UI for simultaneous edits