#!/usr/bin/env bash
# Verification script for delegate-claude-code-skill-install workflow
# Tests that Claude Code print mode works with Ollama backend

set -euo pipefail

echo "======================================"
echo "Claude Code + Ollama Delegation Test"
echo "======================================"
echo

# 1. Check Hermes CLI
echo "1. Checking Hermes CLI..."
if command -v hermes >/dev/null 2>&1; then
    echo "   ✓ hermes found: $(hermes --version)"
else
    echo "   ✗ hermes not found in PATH"
    exit 1
fi

# 2. Check Claude Code binary
echo "2. Checking Claude Code..."
CLAUDE_PATH="/Users/alfredkamisese/Library/Application Support/claude/claude-code/2.1.197/claude.app/Contents/MacOS/claude"
if [[ -x "$CLAUDE_PATH" ]]; then
    echo "   ✓ Claude Code found at: $CLAUDE_PATH"
    echo "   ✓ Version: $("$CLAUDE_PATH" --version)"
else
    echo "   ✗ Claude Code not found at expected path"
    echo "   Check: ls -la ~/Library/Application\\ Support/claude/claude-code/"
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

# 4. Check required model
echo "4. Checking for qwen3.5:9b model..."
if echo "$MODELS" | grep -q "qwen3.5:9b"; then
    echo "   ✓ qwen3.5:9b available"
else
    echo "   ⚠ qwen3.5:9b not found - install with: ollama pull qwen3.5:9b"
fi

# 5. Test basic print mode
echo "5. Testing basic print mode..."
TEST_RESULT=$(
    cd /tmp && "$CLAUDE_PATH" -p "Reply with exactly: OK" \
        --model qwen3.5:9b \
        --dangerously-skip-permissions \
        --output-format json \
        --max-turns 1 \
        --bare \
        2>&1 || true
)

if echo "$TEST_RESULT" | grep -q '"subtype":"success"'; then
    echo "   ✓ Print mode works with qwen3.5:9b"
    TURNS=$(echo "$TEST_RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('num_turns', '?'))")
    COST=$(echo "$TEST_RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('total_cost_usd', '?'))")
    echo "     Turns: $TURNS, Cost: \$$COST"
elif echo "$TEST_RESULT" | grep -q "model_not_found"; then
    echo "   ✗ Model not found in Ollama"
    exit 1
elif echo "$TEST_RESULT" | grep -q "unknown option"; then
    echo "   ⚠ Flag not supported in this Claude Code version"
    echo "     Try without --bare and --workdir flags"
else
    echo "   ⚠ Print mode test unclear"
    echo "     Output preview: $(echo "$TEST_RESULT" | head -c 200)"
fi

# 6. Check Claude Code settings
echo "6. Checking Claude Code settings..."
SETTINGS_FILE="$HOME/.claude/settings.json"
if [[ -f "$SETTINGS_FILE" ]]; then
    echo "   ✓ Settings file exists"
    BASE_URL=$(jq -r '.env.ANTHROPIC_BASE_URL // empty' "$SETTINGS_FILE" 2>/dev/null || echo "")
    if [[ "$BASE_URL" == "http://localhost:11434" ]]; then
        echo "   ✓ ANTHROPIC_BASE_URL correctly set to Ollama"
    else
        echo "   ⚠ ANTHROPIC_BASE_URL: ${BASE_URL:-not set} (expected http://localhost:11434)"
    fi
else
    echo "   ⚠ Settings file not found: $SETTINGS_FILE"
fi

# 7. Check skills directory
echo "7. Checking skills directory..."
SKILLS_DIR="$HOME/.claude/skills"
if [[ -d "$SKILLS_DIR" ]]; then
    echo "   ✓ Skills directory exists: $SKILLS_DIR"
    SKILL_COUNT=$(ls -1 "$SKILLS_DIR"/*.md 2>/dev/null | wc -l | tr -d ' ')
    echo "   Installed skills: $SKILL_COUNT"
    ls -1 "$SKILLS_DIR"/*.md 2>/dev/null | sed 's/^/     - /'
else
    echo "   ⚠ Skills directory not found (will be created on first install)"
fi

echo
echo "======================================"
echo "Verification complete!"
echo "======================================"
echo
echo "If all checks pass, you can use delegate_task to install skills:"
echo "  delegate_task(goal=\"Create skill: my-skill\", context=\"...\")"
echo
echo "If any checks fail, see the skill's references/session-2026-07-08-delegation-test.md"
echo "for troubleshooting details."