#!/bin/bash
# Test script for claude-code-statusline
# Tests the statusline script with various mock inputs including local model context override, RAM, TPS

set -e

STATUSLINE_SCRIPT="$(dirname "$0")/statusline.sh"

if [ ! -f "$STATUSLINE_SCRIPT" ]; then
    echo "Error: statusline.sh not found at $STATUSLINE_SCRIPT"
    exit 1
fi

chmod +x "$STATUSLINE_SCRIPT"

echo "=== Testing claude-code-statusline ==="
echo

# Test 1: Anthropic model (200K context) - 45%
echo "=== Test 1: Anthropic model (200K) - 45% ==="
echo '{"model":{"display_name":"claude-sonnet-4"},"workspace":{"current_dir":"/test"},"context_window":{"used_percentage":45},"cost":{"total_cost_usd":0.12,"total_duration_ms":180000},"session_id":"test-1"}' | bash "$SCRIPT"
echo

# Test 2: 32K model - 14% Anthropic → 85% true
echo "=== Test 2: 32K model (qwen3.5-32k) - 14% Anthropic → 85% true ==="
echo '{"model":{"display_name":"qwen3.5-32k:latest"},"workspace":{"current_dir":"/test"},"context_window":{"used_percentage":14},"cost":{"total_cost_usd":0.05,"total_duration_ms":60000},"session_id":"test-2"}' | bash "$SCRIPT"
echo

# Test 3: 128K model - 50% Anthropic → 76% true
echo "=== Test 3: 128K model (qwen3.5-128k) - 50% Anthropic → 76% true ==="
echo '{"model":{"display_name":"qwen3.5-128k:latest"},"workspace":{"current_dir":"/test"},"context_window":{"used_percentage":50},"cost":{"total_cost_usd":0.25,"total_duration_ms":300000},"session_id":"test-3"}' | bash "$SCRIPT"
echo

# Test 4: 64K model via env override - 50% Anthropic → 100% true
echo "=== Test 4: 64K model (env override) - 50% Anthropic → 100% true ==="
LOCAL_MODEL_CONTEXT=65536 echo '{"model":{"display_name":"custom-model"},"workspace":{"current_dir":"/test"},"context_window":{"used_percentage":50},"cost":{"total_cost_usd":0.25,"total_duration_ms":240000},"session_id":"test-4"}' | bash "$SCRIPT"
echo

# Test 5: TPS calculation - simulate two calls 1s apart
echo "=== Test 5: TPS calculation (first call) ==="
rm -f /tmp/statusline-tps-cache-test-5 /tmp/statusline-git-cache-test-5
echo '{"model":{"display_name":"qwen3.5-32k:latest"},"workspace":{"current_dir":"/test"},"context_window":{"used_percentage":10},"cost":{"total_cost_usd":0.01,"total_duration_ms":60000},"session_id":"test-5"}' | bash "$SCRIPT"
echo

sleep 1
echo "=== Test 5: TPS calculation (second call, 1s later) ==="
echo '{"model":{"display_name":"qwen3.5-32k:latest"},"workspace":{"current_dir":"/test"},"context_window":{"used_percentage":20},"cost":{"total_cost_usd":0.02,"total_duration_ms":120000},"session_id":"test-5"}' | bash "$SCRIPT"
echo

# Test 6: Warning thresholds - 75%
echo "=== Test 6: 75% warning threshold ==="
echo '{"model":{"display_name":"qwen3.5-32k:latest"},"workspace":{"current_dir":"/test"},"context_window":{"used_percentage":12},"cost":{"total_cost_usd":0.1,"total_duration_ms":120000},"session_id":"test-6"}' | bash "$SCRIPT"
echo

# Test 7: Warning threshold - 90%
echo "=== Test 7: 90% warning threshold ==="
echo '{"model":{"display_name":"qwen3.5-32k:latest"},"workspace":{"current_dir":"/test"},"context_window":{"used_percentage":18},"cost":{"total_cost_usd":0.15,"total_duration_ms":180000},"session_id":"test-7"}' | bash "$SCRIPT"
echo

# Test 8: qwen3-coder (auto-detect 128K) - 40% Anthropic → 61% true
echo "=== Test 8: qwen3-coder (auto 128K) - 40% Anthropic → 61% true ==="
echo '{"model":{"display_name":"qwen3-coder"},"workspace":{"current_dir":"/test"},"context_window":{"used_percentage":40},"cost":{"total_cost_usd":0.3,"total_duration_ms":240000},"session_id":"test-8"}' | bash "$SCRIPT"
echo

# Test 9: Original color threshold tests
echo "=== Test 9: Original color threshold tests ==="
test_cases=(
    "13:green"
    "25:green"
    "50:green"
    "69:green"
    "70:yellow"
    "75:yellow"
    "89:yellow"
    "90:red"
    "100:red"
)

for test in "${test_cases[@]}"; do
    PCT="${test%:*}"
    EXPECTED_COLOR="${test#*:}"
    echo "--- Testing $PCT% (expect $EXPECTED_COLOR) ---"
    echo "{\"model\":{\"display_name\":\"qwen3.5-32k:latest\"},\"workspace\":{\"current_dir\":\"/Users/alfredkamisese/Projects/test\"},\"context_window\":{\"used_percentage\":$PCT},\"cost\":{\"total_cost_usd\":0.56,\"total_duration_ms\":435000},\"session_id\":\"test-$PCT\"}" | "$STATUSLINE_SCRIPT"
    echo
done

echo "=== Testing with git branch ==="
if git rev-parse --git-dir > /dev/null 2>&1; then
    echo "{\"model\":{\"display_name\":\"qwen3.5-32k:latest\"},\"workspace\":{\"current_dir\":\"$(pwd)\"},\"context_window\":{\"used_percentage\":75},\"cost\":{\"total_cost_usd\":0.56,\"total_duration_ms\":435000},\"session_id\":\"test-git\"}" | "$STATUSLINE_SCRIPT"
else
    echo "Not in a git repo, skipping git test"
fi

echo
echo "=== All tests completed ==="