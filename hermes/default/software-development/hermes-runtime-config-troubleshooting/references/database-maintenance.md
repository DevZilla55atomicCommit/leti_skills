---
session: 2026-08-22
profile: default
issue: "Keyboard lag / UI freezes in Hermes desktop with large conversation history"
root_cause: "Fragmented 1.1GB state.db + missing indexes + 375MB request dumps + empty fallback chain + aggressive compression"
---

# Database Maintenance for Hermes Desktop Lag

## Problem

Hermes desktop app exhibits keyboard input lag and UI freezes when:
- `state.db` grows beyond 500MB with fragmentation
- Missing critical indexes on `messages` table (`idx_messages_session_ts`, `idx_messages_role_session`)
- `~/.hermes/sessions/` accumulates 200MB+ of request dump files
- Combined with empty fallback chain + aggressive compression (threshold ≤ 0.65)

## Symptoms

- Keystroke-to-character delay (100-500ms per character)
- UI freezes during model streaming
- High CPU in Electron renderer process (~30%)
- Model "falls off track" after NVIDIA rate limit hit

## Diagnosis Commands

```bash
# Check database size
ls -lh ~/.hermes/state.db

# Check indexes on messages table
sqlite3 ~/.hermes/state.db "PRAGMA index_list(messages);"
# Should include: idx_messages_session_ts, idx_messages_role_session

# Check session dumps size
du -sh ~/.hermes/sessions/

# Check fallback chain
hermes fallback list
# Should show at least 2 entries (local + cloud)

# Check compression settings
grep -A 10 '^compression:' ~/.hermes/config.yaml
# threshold should be 0.75-0.8 for complex tasks
```

## Fix Procedure

**REQUIRED: Quit Hermes desktop completely first (Cmd+Q)**

```bash
# 1. Vacuum - reclaims space, defragments
sqlite3 ~/.hermes/state.db "VACUUM;"

# 2. Reindex - rebuilds FTS5 indexes
sqlite3 ~/.hermes/state.db "REINDEX;"

# 3. Add missing indexes for fast session/message lookups
sqlite3 ~/.hermes/state.db "CREATE INDEX IF NOT EXISTS idx_messages_session_ts ON messages(session_id, timestamp);"
sqlite3 ~/.hermes/state.db "CREATE INDEX IF NOT EXISTS idx_messages_role_session ON messages(role, session_id);"

# 4. Prune old request dumps (older than 30 days)
find ~/.hermes/sessions -name "request_dump_*.json" -mtime +30 -delete
```

## Verification

```bash
# Database should shrink significantly (1.1GB → ~700MB typical)
ls -lh ~/.hermes/state.db

# Indexes should now exist
sqlite3 ~/.hermes/state.db "PRAGMA index_list(messages);"

# Session dumps reduced
du -sh ~/.hermes/sessions/

# Fallback chain should show 2+ entries
hermes fallback list
```

## Results from This Session

| Metric | Before | After |
|--------|--------|-------|
| state.db size | 1.1 GB | 702 MB |
| Indexes on messages | 5 auto | 7 (2 new custom) |
| ~/.hermes/sessions/ | 375 MB | 375 MB (no files >30 days) |
| Fallback chain | 0 entries | 2 entries (ollama + openrouter) |
| Compression threshold | 0.5 | 0.8 |
| protect_last_n | 20 | 350 |
| protect_first_n | 3 | 50 |

## Prevention

- Run database maintenance quarterly or when `state.db` > 500MB
- Monitor `~/.hermes/sessions/` size monthly
- Keep fallback chain configured (local Ollama + cloud)
- Keep compression threshold ≥ 0.75 for complex workflows