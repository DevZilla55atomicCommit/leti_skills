# Print Mode Hangs Fix

**Problem**: When another interactive Claude Code instance is running (e.g., user's terminal on `s002`), `claude -p` **hangs indefinitely** due to shared resource deadlock (SQLite session DB, lock files).

**Root Cause**: SQLite database locks prevent concurrent access to session metadata. The CLI waits for a lock that may never be released, causing indefinite hangs.

**Mitigations (ordered by preference)**:

1. **Preferred**: Use `delegate_task` for orchestrator→worker delegation — it spawns a fully isolated subprocess that avoids this conflict entirely.

2. **If forced to use `claude -p`**:
   ```bash
   # Set environment variable to disable automatic session DB locking
   NO_CLAUDE_SESSION_HOOK=1 claude -p "Your task" --bare --max-turns 10
   ```

3. **Emergency recovery** (use only if hanging >30s):
   ```bash
   # Check for lock file and remove (with caution)
   ls -la ~/.claude/.session.lock && rm ~/.claude/.session.lock
   # Then retry the command
   ```

4. **Force isolated execution** (adds overhead, use for CI):
   ```bash
   claude -p "Your task" --no-session-persistence
   ```

**Debugging Checklist**:
- [ ] Is there an interactive Claude session? Run `ps aux | grep claude` (macOS) or `lsof | grep session.lock`
- [ ] Does `~/.claude/.session.lock` exist?
- [ ] Test with `NO_CLAUDE_SESSION_HOOK=1` to isolate
- [ ] Check `~/.claude/mcp_state.json` for pending operations

**Permanent Fix Recommendation**:
Add `--no-session-persistence` to all Hermes orchestration print-mode commands to force isolated execution environments.