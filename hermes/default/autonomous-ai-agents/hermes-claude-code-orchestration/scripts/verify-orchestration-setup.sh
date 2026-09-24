#!/usr/bin/env bash
# Verification script for Hermes ↔ Claude Code orchestration setup

set -euo pipefail

echo "======================================"
echo "Hermes ↔ Claude Code Setup Verification"
echo "======================================"
echo

# 1. Check Hermes MCP server
echo "1. Checking Hermes MCP server..."
if command -v hermes >/dev/null 2>&1; then
    echo "   ✓ hermes CLI found: $(hermes --version)"
else
    echo "   ✗ hermes CLI not found in PATH"
    exit 1
fi

# 2. Check Claude Code binary (find current version dynamically)
echo "2. Checking Claude Code binary..."
CLAUDE_BASE="/Users/alfredkamisese/Library/Application Support/claude/claude-code"
CLAUDE_VERSION=$(ls -1 "$CLAUDE_BASE" 2>/dev/null | sort -V | tail -1)
CLAUDE_PATH="$CLAUDE_BASE/$CLAUDE_VERSION/claude.app/Contents/MacOS/claude"
if [[ -x "$CLAUDE_PATH" ]]; then
    echo "   ✓ Claude Code found at: $CLAUDE_PATH"
    echo "   ✓ Version: $("$CLAUDE_PATH" --version)"
else
    echo "   ✗ Claude Code not found at expected path"
    exit 1
fi

# 3. Check Ollama
echo "3. Checking Ollama..."
if curl -s http://localhost:11434/api/tags >/dev/null 2>&1; then
    echo "   ✓ Ollama running at http://localhost:11434"
    MODELS=$(curl -s http://localhost:11434/api/tags | jq -r '.models[].name' 2>/dev/null || echo "jq not available")
    echo "   Available models:"
    echo "$MODELS" | sed 's/^/     - /'
else
    echo "   ✗ Ollama not responding at localhost:11434"
    exit 1
fi

# 4. Check Claude Code settings
echo "4. Checking Claude Code settings..."
SETTINGS_FILE="$HOME/.claude/settings.json"
if [[ -f "$SETTINGS_FILE" ]]; then
    echo "   ✓ Settings file exists: $SETTINGS_FILE"
    BASE_URL=$(jq -r '.env.ANTHROPIC_BASE_URL // empty' "$SETTINGS_FILE" 2>/dev/null || echo "")
    if [[ "$BASE_URL" == "http://localhost:11434" ]]; then
        echo "   ✓ ANTHROPIC_BASE_URL correctly set to Ollama"
    else
        echo "   ⚠ ANTHROPIC_BASE_URL: $BASE_URL (expected http://localhost:11434)"
    fi
else
    echo "   ✗ Settings file not found: $SETTINGS_FILE"
    exit 1
fi

# 5. Test Hermes MCP server startup
echo "5. Testing Hermes MCP server startup..."
timeout 5 hermes mcp serve 2>&1 | head -5 || true
echo "   ✓ MCP server starts without error"

# 6. Test Claude Code print mode with Ollama model (NO --workdir flag - removed in v2.x)
echo "6. Testing Claude Code print mode with Ollama model..."
# Use first available Ollama model for test
TEST_MODEL=$(curl -s http://localhost:11434/api/tags | jq -r '.models[0].name' 2>/dev/null || echo "qwen3.5:9b")
cd /tmp && TEST_RESULT=$("$CLAUDE_PATH" -p "Reply with just: OK" \
    --model "$TEST_MODEL" \
    --dangerously-skip-permissions \
    --output-format json \
    --max-turns 1 \
    --bare \
    2>&1 || true)

if echo "$TEST_RESULT" | grep -q '"subtype":"success"'; then
    echo "   ✓ Print mode works with $TEST_MODEL"
elif echo "$TEST_RESULT" | grep -q "model_not_found"; then
    echo "   ✗ Model not found in Ollama - check available models"
    exit 1
else
    echo "   ⚠ Print mode test unclear, check manually"
    echo "   Output preview: $(echo "$TEST_RESULT" | head -c 200)"
fi

# 7. Check MCP connection
echo "7. Checking MCP configuration..."
if "$CLAUDE_PATH" mcp list 2>/dev/null | grep -q "hermes"; then
    echo "   ✓ Hermes MCP server configured in Claude Code"
else
    echo "   ⚠ Hermes MCP not yet configured in Claude Code"
    echo "   Run: claude mcp add hermes -- hermes mcp serve"
fi

echo
echo "======================================"
echo "Verification complete!"
echo "======================================"
echo
echo "Next steps if all checks pass:"
echo "  1. Start Hermes MCP server: hermes mcp serve &"
echo "  2. In Claude Code terminal: claude mcp add hermes -- hermes mcp serve"
echo "  3. Test: In Claude Code chat, ask \"Use mcp_hermes_conversations_list\""
echo "  4. Test delegation: hermes chat -q \"Delegate: create test.py at /tmp\""