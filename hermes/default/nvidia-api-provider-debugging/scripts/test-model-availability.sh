#!/bin/bash
# NVIDIA NIM Model Availability Test Script
# Tests which models are accessible for the current API key/account
# Usage: ./scripts/test-model-availability.sh

set -euo pipefail

API_KEY="${NVIDIA_API_KEY:-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}"
ENDPOINT="https://integrate.api.nvidia.com/v1/chat/completions"
EMBEDDING_ENDPOINT="https://integrate.api.nvidia.com/v1/embeddings"
TIMEOUT=60

# Working NVIDIA models (✅ confirmed)
NVIDIA_WORKING=(
    "nvidia/nemotron-3-ultra-550b-a55b"
    "nvidia/nemotron-3-super-120b-a12b"
    "nvidia/nemotron-3-nano-30b-a3b"
    "nvidia/nemotron-mini-4b-instruct"
    "nvidia/llama-3.3-nemotron-super-49b-v1"
    "nvidia/nemotron-nano-12b-v2-vl"
    "nvidia/nvidia-nemotron-nano-9b-v2"
    "nvidia/nemotron-3-content-safety"
    "nvidia/nemotron-3.5-content-safety"
    "nvidia/nemotron-content-safety-reasoning-4b"
)

# Working partner models (✅ confirmed)
PARTNER_WORKING=(
    "meta/llama-3.1-70b-instruct"
    "meta/llama-3.1-8b-instruct"
    "meta/llama-3.2-11b-vision-instruct"
    "meta/llama-3.2-90b-vision-instruct"
    "google/gemma-2-2b-it"
    "qwen/qwen3.5-122b-a10b"
)

# Known timeout models (⏱️)
TIMEOUT_MODELS=(
    "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning"
    "nvidia/llama-3.1-nemotron-nano-8b-v1"
    "meta/llama-3.3-70b-instruct"
    "meta/llama-3.2-1b-instruct"
    "meta/llama-3.2-3b-instruct"
    "microsoft/phi-4-mini-instruct"
)

# Known 404 models (❌ not available for this account tier)
NOT_FOUND_MODELS=(
    "nvidia/llama-3.1-nemotron-70b-instruct"
    "nvidia/nemotron-4-340b-instruct"
    "nvidia/nemotron-4-340b-reward"
    "nvidia/llama-3.1-nemotron-ultra-253b-v1"
    "nvidia/mistral-nemo-minitron-8b-8k-instruct"
    "nvidia/nemotron-nano-3-30b-a3b"
    "mistralai/mistral-7b-instruct-v0.3"
    "mistralai/mixtral-8x7b-instruct-v0.1"
    "mistralai/mistral-large-2-instruct"
    "ibm/granite-3.0-8b-instruct"
    "google/gemma-3-12b-it"
    "deepseek-ai/deepseek-v4-flash"
    "microsoft/phi-3.5-moe-instruct"
)

ALL_MODELS=(
    "${NVIDIA_WORKING[@]}"
    "${PARTNER_WORKING[@]}"
    "${TIMEOUT_MODELS[@]}"
    "${NOT_FOUND_MODELS[@]}"
)

echo "🔍 Testing NVIDIA NIM model availability..."
echo "Account: S78BOeXjisIHupYw0xGlAMHQef1sugZJyno_XivDIzw"
echo "Endpoint: $ENDPOINT"
echo ""

WORKING=0
TIMEOUT_COUNT=0
NOT_FOUND_COUNT=0

for MODEL in "${ALL_MODELS[@]}"; do
    echo -n "Testing $MODEL ... "

    START=$(date +%s%3N)
    RESPONSE=$(curl -s -w "\n%{http_code}" --max-time "$TIMEOUT" \
        -H "Authorization: Bearer $API_KEY" \
        -H "Content-Type: application/json" \
        -d "{\"model\":\"$MODEL\",\"messages\":[{\"role\":\"user\",\"content\":\"Hi\"}],\"max_tokens\":10}" \
        "$ENDPOINT" 2>/dev/null || echo -e "\nCURL_FAILED")
    END=$(date +%s%3N)
    LATENCY=$((END - START))

    HTTP_CODE=$(echo "$RESPONSE" | tail -1)
    BODY=$(echo "$RESPONSE" | head -n -1)

    if [[ "$HTTP_CODE" == "200" ]]; then
        if echo "$BODY" | grep -q "choices"; then
            echo "✅ OK (${LATENCY}ms)"
            ((WORKING++))
        else
            echo "⚠️  HTTP 200 but unexpected response"
        fi
    elif [[ "$HTTP_CODE" == "404" ]]; then
        echo "❌ 404 NOT FOUND (not available for this account)"
        ((NOT_FOUND_COUNT++))
    elif [[ "$RESPONSE" == *"CURL_FAILED"* ]] || [[ $LATENCY -ge $((TIMEOUT * 1000)) ]]; then
        echo "⏱️  TIMEOUT (${LATENCY}ms)"
        ((TIMEOUT_COUNT++))
    else
        echo "❓ HTTP $HTTP_CODE"
    fi
done

echo ""
echo "=========================================="
echo "📋 SUMMARY"
echo "=========================================="
echo "✅ Working:     $WORKING"
echo "⏱️  Timeout:     $TIMEOUT_COUNT"
echo "❌ 404 Not Found: $NOT_FOUND_COUNT"
echo "Total tested:  ${#ALL_MODELS[@]}"
echo ""
echo "💡 Add only ✅ models to your Hermes config.yaml"
echo "   Timeout/404 models will fail at runtime"
echo ""
echo "📄 See references/nvidia-nim-model-availability.md for full details"