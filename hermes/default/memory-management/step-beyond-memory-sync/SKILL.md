---
name: step-beyond-memory-sync
description: Bidirectional memory sync between Hermes builtin memory and Obsidian vault for Step Beyond user-patterns.md format. Ensures durable, structured memory that survives context compression and session restarts.
version: 1.0.0
license: MIT
author: Alfred (Maddie)
---

# Step Beyond Memory Sync

Automated sync protocol for Step Beyond user patterns between Hermes Agent's builtin memory and the Obsidian vault.

## Architecture

```
┌──────────────────┐     --pull (session start)     ┌──────────────────┐
│  Obsidian Vault  │ ─────────────────────────────▶ │  Hermes Memory   │
│  step-beyond-    │                                │  user.json       │
│  user-patterns.md│                                │  (builtin)       │
└──────────────────┘                                 └──────────────────┘
        ▲                                                   │
        │                                                   │
        │     --push (session end / cron 30m)              │
        └───────────────────────────────────────────────────┘
```

## Files

| File | Purpose |
|------|---------|
| `sync_step_beyond_memory.py` | Core sync logic (pull/push/status) |
| `session_start_step_beyond.sh` | Session start hook (pull) |
| `session_end_step_beyond.sh` | Session end hook (push) |
| `~/.hermes/scripts/sync_step_beyond_memory.py` | Installed script for cron |

## References

| File | Purpose |
|------|---------|
| `references/fix-history.md` | Full fix history for sync issues |
| `references/cron-script-arg-fix.md` | Cron script argument parsing fix details |

## Usage

### Manual Commands
```bash
# Pull from Obsidian → Hermes (session start)
python3 ~/.hermes/scripts/sync_step_beyond_memory.py --pull

# Push from Hermes → Obsidian (session end)
python3 ~/.hermes/scripts/sync_step_beyond_memory.py --push

# Check sync status
python3 ~/.hermes/scripts/sync_step_beyond_memory.py --status
```

### Session Hooks
Add to your shell/profile for automatic sync:
```bash
# In ~/.zshrc or similar
alias hermes-start='~/TamaZila\ Obsidian\ Vault/Hermes\ Agent/session_start_step_beyond.sh'
alias hermes-end='~/TamaZila\ Obsidian\ Vault/Hermes\ Agent/session_end_step_beyond.sh'
```

### Cron Job (Automatic Push)
Auto-configured: `step-beyond-memory-sync` runs every 30 minutes, pushing Hermes memory to Obsidian.

```bash
# View cron jobs
hermes cron list

# Manual trigger
hermes cron run step-beyond-memory-sync
```

## Memory Format (Obsidian)

The `step-beyond-user-patterns.md` follows the Step Beyond template:

```markdown
# Step Beyond — User Patterns
updated: YYYY-MM-DD

## Profile
<!-- Stable facts. Read every session. Feed into intent briefs + L1 constraints. -->
- stack:
- brand:
- language:
- tone:
- platforms:

## Reinforced
<!-- Accepted 2×+. Default L2 for their domain. Format: domain: +name (accepted N×, last DATE) -->

## Banned
<!-- Rejected 2×+ or explicit "never". Hard filter — checked before every addition. -->

## Watching
<!-- Single signals. One more accept → Reinforced. One more reject → Banned. Ignored 3× → delete. -->

## Trajectories
<!-- Multi-session request sequences. Fuel for L3 prediction. Format: A → B → C (seen N×) -->

## Open Loops
<!-- Optional. Unfinished threads awaiting user input. Next session: close these before adding anything new. Delete when closed. -->

## Session Context
<!-- Transient working context for current session. Cleared on session end. -->
```

## Integration with Step Beyond Protocol

| Step Beyond Concept | Sync Implementation |
|---------------------|---------------------|
| **User-model entries** | Typed as `profile` kind with `scope: step-beyond-patterns` |
| **Open Loops** | Explicit section in patterns file — survives compression |
| **Trajectories** | Multi-session patterns persisted across restarts |
| **Namespace isolation** | Separate from Hermes general memory via scope tag |
| **Audit trail** | Hermes JSONL entries + Obsidian file history (git) |
| **No guess promotion** | Protocol enforced by Step Beyond skill, not sync |

## Why This Survives Compression

1. **Obsidian is the source of truth** — file persists independently of Hermes context
2. **Session start pulls** — full patterns loaded before any task begins
3. **Session end pushes** — any new Open Loops/Trajectories captured
4. **Cron every 30m** — catches mid-session changes even if session doesn't end cleanly
5. **Scope-tagged in Hermes** — `scope: step-beyond-patterns` isolates from other memory

## Configuration

| Setting | Value |
|---------|-------|
| Obsidian vault | `/Users/alfredkamisese/TamaZila Obsidian Vault/Hermes Agent/Hermes Memory/` |
| Patterns file | `step-beyond-user-patterns.md` |
| Hermes memory | `~/.hermes/profiles/default/memories/user.json` |
| Cron schedule | `every 30m` |
| Cron job ID | `7e54178aa1b0` |

## Verification

```bash
# Check both sides match
python3 ~/.hermes/scripts/sync_step_beyond_memory.py --status

# Expected: same hash on both sides after sync
```

## Troubleshooting

| Issue | Fix |
|-------|-----|
| "No patterns in Obsidian" | Run initial setup: copy template to Obsidian path |
| "Hermes memory file not found" | First run creates it; check `~/.hermes/profiles/default/memories/` |
| "Hash mismatch after push" | Manual edit in Obsidian — run `--pull` to refresh Hermes |
| Cron not running | `hermes cron list` → check job enabled, `hermes cron run step-beyond-memory-sync` |

## Observed Cron Behavior (Verified 2026-07-16)

| Pattern | Detail |
|---------|--------|
| **Schedule** | Every 30 minutes (00:04, 00:34, 01:04, 01:34... or similar offset) |
| **Default action** | No-argument run defaults to `--push` (Hermes → Obsidian) |
| **Hour/half-hour runs** | Execute `--push` + `--status` (10 messages, visible delivery) |
| **Other runs** | `--status` only; emits `[SILENT]` when in sync (no delivery) |
| **Last verified sync** | Hermes memory last synced 2026-07-15 18:42; in sync since |
| **Silent suppression** | Cron job configured with `SILENT: If there is genuinely nothing new to report, respond with exactly "[SILENT]"` — working correctly |