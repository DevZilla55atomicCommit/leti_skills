# Workspace Trust Automation

## The Problem

Claude Code's print mode (`-p`) **hangs indefinitely** if the workspace hasn't been trusted via the interactive trust dialog first.

### Error Signature

```bash
$ claude -p "task" --model qwen3.5:9b --dangerously-skip-permissions
# ... waits 60+ seconds ...
# Stderr:
Ignoring 2 permissions.allow entries from .claude/settings.local.json: this workspace has not been trusted. Run Claude Code interactively here once and accept the trust dialog, or set projects["/path"].hasTrustDialogAccepted: true in /Users/alfredkamisese/.claude.json.
```

### Root Cause

- Print mode skips the trust dialog entirely
- If trust was never accepted, the process waits for a dialog that never appears
- This is a **one-time per directory** requirement

---

## Solution 1: Manual One-Time Trust (Simplest)

```bash
# For each project directory, run ONCE:
cd ~/myapp && claude
# Press Enter for "Yes, I trust this folder"
# Type /exit
```

After this, print mode works instantly in that directory.

---

## Solution 2: Pre-Configure via ~/.claude.json

Add trust acceptance to the global config:

```json
{
  "projects": {
    "/Users/alfredkamisese/myapp": {
      "hasTrustDialogAccepted": true
    },
    "/Users/alfredkamisese/other-project": {
      "hasTrustDialogAccepted": true
    }
  }
}
```

**Location:** `~/.claude.json` (not `~/.claude/settings.json`)

### Automated Script

```bash
#!/bin/bash
# trust_workspace.sh - Add workspace trust to ~/.claude.json

PROJECT_PATH="${1:-$(pwd)}"
CLAUDE_JSON="$HOME/.claude.json"

# Read existing
if [[ -f "$CLAUDE_JSON" ]]; then
    json=$(cat "$CLAUDE_JSON")
else
    json='{}'
fi

# Add/update project trust
json=$(echo "$json" | jq --arg path "$PROJECT_PATH" '
    .projects[$path] = {"hasTrustDialogAccepted": true}
')

# Write back
echo "$json" > "$CLAUDE_JSON"
echo "Added trust for: $PROJECT_PATH"
```

---

## Solution 3: Automation in Delegate Task Context

When using `delegate_task` to spawn Claude Code workers, include trust setup:

```python
delegate_task(
    goal="Build feature X",
    context="""
    Project at ~/myapp. 
    
    FIRST: Ensure workspace is trusted:
    cd ~/myapp && claude --dangerously-skip-permissions -p "trust check" --max-turns 1 2>/dev/null || true
    
    THEN run the actual task:
    claude -p "Build feature X" --model claude-sonet-4.6:latest --dangerously-skip-permissions --output-format json --max-turns 10
    """
)
```

---

## Solution 4: CI/CD Friendly (No Interactive Step)

For headless environments, pre-populate `~/.claude.json`:

```bash
# In your setup script / Dockerfile / CI:
mkdir -p ~/.claude
cat > ~/.claude.json << 'EOF'
{
  "projects": {
    "/workspace": {"hasTrustDialogAccepted": true},
    "/home/user/project": {"hasTrustDialogAccepted": true}
  }
}
EOF
```

---

## Verification

Test that trust works:

```bash
# Should complete in <2 seconds, not hang
claude -p "echo test" --model qwen3.5:9b --dangerously-skip-permissions --max-turns 1 --output-format json
```

Expected output: JSON with `"subtype": "success"`

---

## Related Files

- `~/.claude.json` — Global config with project trust flags
- `~/.claude/settings.local.json` — Per-project permissions (gitignored)
- `~/.claude/projects/<project>/` — Auto-memory, includes trust state