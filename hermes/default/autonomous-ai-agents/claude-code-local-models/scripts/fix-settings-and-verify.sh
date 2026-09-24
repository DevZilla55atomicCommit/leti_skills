#!/usr/bin/env bash
# fix-settings-and-verify.sh — Fix ~/.claude/settings.json and verify it works with local Ollama model
# Usage: ./fix-settings-and-verify.sh [model-name]
# Example: ./fix-settings-and-verify.sh qwen3.5:4b

set -euo pipefail

MODEL="${1:-qwen3.5:4b}"
SETTINGS_FILE="$HOME/.claude/settings.json"
CLAUDE_BIN="$HOME/.npm-global/bin/claude"

echo "=== Fixing settings.json for model: $MODEL ==="

# 1. Check if claude binary exists
if [[ ! -x "$CLAUDE_BIN" ]]; then
    echo "ERROR: Claude Code not found at $CLAUDE_BIN"
    echo "Install with: npm install -g @anthropic-ai/claude-code"
    exit 1
fi

# 2. Check if model exists in Ollama
echo "Checking Ollama for model: $MODEL ..."
if ! ollama list | grep -q "^$MODEL "; then
    echo "WARNING: Model '$MODEL' not found in ollama list"
    ollama list
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    [[ ! $REPLY =~ ^[Yy]$ ]] && exit 1
fi

# 3. Backup existing settings
if [[ -f "$SETTINGS_FILE" ]]; then
    cp "$SETTINGS_FILE" "${SETTINGS_FILE}.bak.$(date +%s)"
    echo "Backed up existing settings"
fi

# 4. Write correct settings.json with valid statusLine schema
cat > "$SETTINGS_FILE" <<EOF
{
  "env": {
    "ANTHROPIC_BASE_URL": "http://localhost:11434",
    "ANTHROPIC_AUTH_TOKEN": "ollama",
    "ANTHROPIC_API_KEY": "",
    "CLAUDE_CODE_MAX_OUTPUT_TOKENS": "",
    "DISABLE_TELEMETRY": "1",
    "DISABLE_BUG_COMMAND": "1",
    "DISABLE_ERROR_REPORTING": "1"
  },
  "model": "$MODEL",
  "effortLevel": "medium",
  "promptSuggestionEnabled": false,
  "theme": "dark",
  "verbose": false,
  "switchModelsOnFlag": true,
  "statusLine": {
    "type": "command",
    "command": "echo 'Claude Code'",
    "enabled": true
  }
}
EOF

echo "✓ Wrote $SETTINGS_FILE"

# 5. Validate JSON
if python3 -m json.tool "$SETTINGS_FILE" > /dev/null 2>&1; then
    echo "✓ JSON is valid"
else
    echo "✗ JSON is INVALID"
    python3 -m json.tool "$SETTINGS_FILE" 2>&1
    exit 1
fi

# 6. Test with a quick print-mode call
echo ""
echo "=== Testing with claude -p ==="
export PATH="$PATH:$HOME/.npm-global/bin"
export ANTHROPIC_BASE_URL=http://localhost:11434
export ANTHROPIC_AUTH_TOKEN=ollama
export ANTHROPIC_API_KEY=""

# First test: --model flag (bypasses cached state)
echo "Test 1: --model $MODEL (bypasses ~/.claude.json cache)"
timeout 120 "$CLAUDE_BIN" --model "$MODEL" --print "Say hello briefly" 2>&1
RESULT=$?

if [[ $RESULT -eq 0 ]]; then
    echo "✓ Test 1 passed: --model flag works"
elif [[ $RESULT -eq 124 ]]; then
    echo "✗ Test 1 TIMEOUT: Model loading into VRAM (first run can take 60-180s)"
    echo "  Pre-load with: ollama run $MODEL 'warm up' &"
    exit 1
else
    echo "✗ Test 1 FAILED: Exit code $RESULT"
    exit 1
fi

if [[ $RESULT -eq 0 ]]; then
    echo ""
    echo "✓ SUCCESS: Settings work with model $MODEL"
elif [[ $RESULT -eq 124 ]]; then
    echo ""
    echo "✗ TIMEOUT: Model took too long to respond (likely loading into VRAM)"
    echo "  Try a smaller model like qwen3.5:4b or gemma4:12b"
    exit 1
else
    echo ""
    echo "✗ FAILED: Exit code $RESULT"
    exit 1
fi

# 7. Also test without --model (using settings.json)
echo ""
echo "=== Testing WITHOUT --model flag (uses settings.json) ==="
timeout 120 "$CLAUDE_BIN" --print "Say hello briefly" 2>&1
RESULT=$?

if [[ $RESULT -eq 0 ]]; then
    echo ""
    echo "✓ SUCCESS: settings.json model works without --model override"
else
    echo ""
    echo "✗ FAILED: Exit code $RESULT"
    echo "  This is expected if ~/.claude.json has a different cached model."
    echo "  Fix: claude --settings '{\"model\":\"$MODEL\"}' -p \"test\""
fi

echo ""
echo "=== Done ==="
echo "Settings file: $SETTINGS_FILE"
echo "Model: $MODEL"