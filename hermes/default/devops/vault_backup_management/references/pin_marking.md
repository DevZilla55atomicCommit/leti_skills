# Pin Marking & Session Retention (Hermes Desktop)

## Purpose
Mark sessions that must NOT be deleted or pruned automatically. This ensures:
- Pinned sessions (e.g., critical workflows, ongoing tasks) survive cleanup passes
- Accidental deletion of active cron jobs or in-progress work is prevented
- Session lineage (source, purpose) remains traceable

## How to Apply
1. **Identify**: When reviewing sessions, look for `pinned=1` flag in `state.db` or explicit `@session:<profile>/<id>` markers.
2. **Mark**: Use `hermes curator pin <session_id>` to lock the session.
3. **Verify**: Before any deletion or pruning, run `hermes session_search --filter pinned` to list protected sessions.
4. **Delete Safely**: Only delete sessions that are NOT in the pinned list.

## Command Reference
- `hermes curator pin <session_id>`: Marks a session as pinned.
- `hermes curator unpin <session_id>`: Removes the pin.
- `hermes session_search --filter pinned`: Lists all pinned sessions.

## Example
```bash
# Pin the current session
hermes curator pin $(hermes session_current)

# Verify pinned sessions
hermes session_search --filter pinned
# Output includes: session_id, title, pinned=1
```

## Link to This Skill
This guidance lives in `vault_backup_management` skill under `references/pin_marking.md`.