# Lock File Handling and Session Persistence Fixes

## Problem: Claude Code `-p` hangs indefinitely when another interactive session exists.

### Root Cause
- Shared SQLite session DB (`~/.claude/.session.lock`) creates file-level lock
- Concurrent access causes deadlock when one session tries to acquire lock while another holds it
- Print mode commands (`claude -p`) wait for lock release but never get it

## Permanent Fixes

### 1. Environment Variable Mitigation
```bash
export NO_CLAUDE_SESSION_HOOK=1
```
- Disables automatic session DB locking
- Prevents lock contention between sessions
- Must be set **before** launching any `claude -p` command

### 2. Lock File Management
```bash
# Check for existing lock
ls -la ~/.claude/.session.lock

# Safe removal (only if no active interactive session)
rm -f ~/.claude/.session.lock
```

**Warning**: Only remove if you're certain no interactive session is active. Doing so while another session has unsaved state may cause data loss.

### 3. Command Line Flags
Add to all print mode invocations:
```bash
--no-session-persistence
```
- Forces isolated execution environment
- Prevents lock sharing with other sessions
- Particularly important for cron jobs and automated workflows

### 4. Pre-Task Session Validation
```bash
if [ -f ~/.claude/.session.lock ]; then
  echo "Warning: Existing session lock detected. Removing..."
  rm -f ~/.claude/.session.lock
fi
```

## Best Practices

1. **Always set environment variable first**:
   ```bash
   export NO_CLAUDE_SESSION_HOOK=1 && claude -p "Your task"
   ```

2. **Use `--no-session-persistence` on all automated commands**:
   - CI/CD pipelines
   - Cron jobs
   - Background delegations
   - Batch processing

3. **Manual interactive sessions**:
   - If you need an interactive session, launch it explicitly
   - Close it properly with `/exit` or `Ctrl+C`
   - Verify lock file is gone before starting automated work

4. **Debugging hangs**:
   ```bash
   # Check active Claude processes
   ps aux | grep "claude"
   
   # Verify lock status
   lsof | grep .session.lock
   ```

## Related Fixes in Skill Library
This fix is documented in:
- `hermes-claude-code-orchestration` skill, "Print Mode Conflict with Running Interactive Instance" section