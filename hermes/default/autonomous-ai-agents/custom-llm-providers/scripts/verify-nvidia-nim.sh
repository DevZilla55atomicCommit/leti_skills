#!/bin/bash
# Verify NVIDIA NIM endpoint connectivity and model availability
# Usage: ./verify-nvidia-nim.sh [endpoint] [api_key] [model_id]
# Example: ./verify-nvidia-nim.sh https://integrate.api.nvidia.com/v1 nvapi-xxx nvidia/nemotron-3-ultra-550b-a55b

set -euo pipefail

ENDPOINT="${1:-https://integrate.api.nvidia.com/v1}"
API_KEY="${2:-$NVIDIA_API_KEY}"
MODEL="${3:-nvidia/nemotron-3-ultra-550b-a55b}"

if [[ -z "$API_KEY" ]]; then
    echo "Error: API key required. Set NVIDIA_API_KEY env var or pass as second argument."
    exit 1
fi

echo "=== Verifying NVIDIA NIM Endpoint ==="
echo "Endpoint: $ENDPOINT"
echo "Model: $MODEL"
echo ""

# Test 1: List models
echo "1. Testing /v1/models..."
MODELS_RESPONSE=$(curl -s -w "\n%{http_code}" "$ENDPOINT/models" \
    -H "Authorization: Bearer $API_KEY" \
    -H "Content-Type: application/json")

HTTP_CODE=$(echo "$MODELS_RESPONSE" | tail -1)
MODELS_BODY=$(echo "$MODELS_RESPONSE" | head -n -1)

if [[ "$HTTP_CODE" != "200" ]]; then
    echo "❌ FAIL: /v1/models returned HTTP $HTTP_CODE"
    echo "$MODELS_BODY"
    exit 1
fi

echo "✅ PASS: /v1/models returned 200 OK"
AVAILABLE_MODELS=$(echo "$MODELS_BODY" | jq -r '.data[].id' 2>/dev/null || echo "$MODELS_BODY")
echo "Available models:"
echo "$AVAILABLE_MODELS" | sed 's/^/  - /'

# Check if our model is available
if echo "$AVAILABLE_MODELS" | grep -q "^${MODEL}$"; then
    echo "✅ Model '$MODEL' found in available models"
else
    echo "⚠️  WARNING: Model '$MODEL' NOT found in available models"
fi

echo ""

# Test 2: Chat completion (OpenAI format)
echo "2. Testing /v1/chat/completions (OpenAI format)..."
CHAT_RESPONSE=$(curl -s -w "\n%{http_code}" "$ENDPOINT/chat/completions" \
    -H "Authorization: Bearer $API_KEY" \
    -H "Content-Type: application/json" \
    -d "{\"model\":\"$MODEL\",\"messages\":[{\"role\":\"user\",\"content\":\"Hello, reply OK\"}],\"max_tokens\":20}")

HTTP_CODE=$(echo "$CHAT_RESPONSE" | tail -1)
CHAT_BODY=$(echo "$CHAT_RESPONSE" | head -n -1)

if [[ "$HTTP_CODE" != "200" ]]; then
    echo "❌ FAIL: /v1/chat/completions returned HTTP $HTTP_CODE"
    echo "$CHAT_BODY"
else
    echo "✅ PASS: /v1/chat/completions returned 200 OK"
    echo "Response:"
    echo "$CHAT_BODY" | jq -r '.choices[0].message.content' 2>/dev/null || echo "$CHAT_BODY"
fi

echo ""

# Test 3: Messages endpoint (Anthropic format)
echo "3. Testing /v1/messages (Anthropic format)..."
MESSAGES_RESPONSE=$(curl -s -w "\n%{http_code}" "$ENDPOINT/messages" \
    -H "Authorization: Bearer $API_KEY" \
    -H "Content-Type: application/json" \
    -H "anthropic-version: 2023-06-01" \
    -d "{\"model\":\"$MODEL\",\"messages\":[{\"role\":\"user\",\"content\":\"Hello, reply OK\"}],\"max_tokens\":20}")

HTTP_CODE=$(echo "$MESSAGES_RESPONSE" | tail -1)
MESSAGES_BODY=$(echo "$MESSAGES_RESPONSE" | head -n -1)

if [[ "$HTTP_CODE" != "200" ]]; then
    echo "❌ FAIL: /v1/messages returned HTTP $HTTP_CODE"
    echo "$MESSAGES_BODY"
else
    echo "✅ PASS: /v1/messages returned 200 OK"
    echo "Response:"
    echo "$MESSAGES_BODY" | jq -r '.content[1].text' 2>/dev/null || echo "$MESSAGES_BODY"
fi

echo ""
echo "=== Verification Complete ==="