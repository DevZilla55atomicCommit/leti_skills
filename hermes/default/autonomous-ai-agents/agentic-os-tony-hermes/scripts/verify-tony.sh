#!/usr/bin/env bash
# TONY Gateway Health & Provider Chain Verification
# Usage: ./scripts/verify-tony.sh

set -euo pipefail

GATEWAY_URL="${GATEWAY_URL:-http://localhost:8787}"
AUTH_TOKEN="${TONY_API_TOKEN:-tony-hermes-local-2026}"

echo "=== TONY Gateway Verification ==="
echo "URL: $GATEWAY_URL"
echo ""

# 1. Health check
echo "1. Health endpoint..."
HEALTH=$(curl -s -m 10 -H "Authorization: Bearer $AUTH_TOKEN" "$GATEWAY_URL/health" || echo '{"ok":false}')
if echo "$HEALTH" | grep -q '"ok":true'; then
  echo "   ✅ Health OK"
else
  echo "   ❌ Health FAILED"
  echo "$HEALTH" | python3 -m json.tool
  exit 1
fi

# 2. Provider chain
CHAIN=$(echo "$HEALTH" | python3 -c "import sys,json; print(json.load(sys.stdin)['llmChain']['chain'])")
echo "   Provider chain: $CHAIN"

if echo "$CHAIN" | grep -q '"anthropic"'; then
  echo "   ❌ FAIL: anthropic in chain (should be filtered)"
  exit 1
else
  echo "   ✅ No anthropic in chain"
fi

if echo "$CHAIN" | grep -q '"nvidia"'; then
  echo "   ✅ nvidia in chain"
else
  echo "   ❌ FAIL: nvidia NOT in chain"
  exit 1
fi

# 3. Chat test
echo ""
echo "2. Chat endpoint..."
CHAT=$(curl -s -m 30 -X POST "$GATEWAY_URL/api/chat" \
  -H "Authorization: Bearer $AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message":"Say hello in one sentence.","sessionId":"verify-'$(date +%s)'"}')

PROVIDER=$(echo "$CHAT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('provider',''))")
RESPONSE=$(echo "$CHAT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('response','')[:80])")
ERROR=$(echo "$CHAT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('error',''))")

if [ -n "$ERROR" ]; then
  echo "   ❌ Chat FAILED: $ERROR"
  exit 1
fi

if [ "$PROVIDER" = "nvidia" ]; then
  echo "   ✅ Provider: nvidia"
else
  echo "   ❌ FAIL: provider='$PROVIDER' (expected nvidia)"
  exit 1
fi

echo "   Response: $RESPONSE..."

echo ""
echo "=== ALL CHECKS PASSED ==="