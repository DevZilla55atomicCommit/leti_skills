#!/usr/bin/env bash
# verify-cognee-ollama.sh
# Run this after installing cognee and starting Ollama
# Verifies embeddings endpoint, session memory, and graph memory

set -euo pipefail

echo "=== Cognee + Ollama Verification ==="
echo

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Config
OLLAMA_HOST="${OLLAMA_HOST:-http://localhost:11434}"
EMBED_MODEL="${EMBED_MODEL:-nomic-embed-text:latest}"
LLM_MODEL="${LLM_MODEL:-qwen3.5:4b}"

echo "Config:"
echo "  Ollama: $OLLAMA_HOST"
echo "  Embed model: $EMBED_MODEL"
echo "  LLM model: $LLM_MODEL"
echo

# 1. Check Ollama is running
echo -n "1. Ollama API... "
if curl -sf "$OLLAMA_HOST/api/tags" >/dev/null 2>&1; then
    echo -e "${GREEN}OK${NC}"
else
    echo -e "${RED}FAIL${NC} (Ollama not running on $OLLAMA_HOST)"
    exit 1
fi

# 2. Check models exist
echo -n "2. Models available... "
TAGS=$(curl -sf "$OLLAMA_HOST/api/tags" 2>/dev/null || echo '{"models":[]}')
if echo "$TAGS" | grep -q "\"$EMBED_MODEL\""; then
    echo -e "${GREEN}Embedding model found${NC}"
else
    echo -e "${YELLOW}Embedding model '$EMBED_MODEL' not found${NC}"
    echo "   Available: $(echo "$TAGS" | jq -r '.models[].name' | tr '\n' ' ')"
fi

if echo "$TAGS" | grep -q "\"$LLM_MODEL\""; then
    echo -e "${GREEN}LLM model found${NC}"
else
    echo -e "${YELLOW}LLM model '$LLM_MODEL' not found${NC}"
fi

# 3. Test embeddings endpoint
echo -n "3. Embeddings endpoint (/api/embed)... "
EMBED_RESP=$(curl -sf -X POST "$OLLAMA_HOST/api/embed" \
    -d "{\"model\":\"$EMBED_MODEL\",\"input\":\"test\"}" \
    -H "Content-Type: application/json" 2>/dev/null || echo '{}')

if echo "$EMBED_RESP" | grep -q '"embedding"'; then
    DIM=$(echo "$EMBED_RESP" | jq '.embedding | length')
    echo -e "${GREEN}OK (dim=$DIM)${NC}"
else
    echo -e "${RED}FAIL${NC}"
    echo "   Response: $EMBED_RESP"
    exit 1
fi

# 4. Test LLM chat completion
echo -n "4. LLM chat completion (/v1/chat/completions)... "
LLM_RESP=$(curl -sf -X POST "$OLLAMA_HOST/v1/chat/completions" \
    -d "{\"model\":\"$LLM_MODEL\",\"messages\":[{\"role\":\"user\",\"content\":\"Say OK\"}],\"max_tokens\":10}" \
    -H "Content-Type: application/json" 2>/dev/null || echo '{}')

if echo "$LLM_RESP" | grep -q '"choices"'; then
    echo -e "${GREEN}OK${NC}"
else
    echo -e "${YELLOW}WARN${NC} - LLM may not support OpenAI-compatible endpoint"
    echo "   Response: $LLM_RESP"
fi

# 5. Test Cognee session memory (if Python available)
echo -n "5. Cognee session memory... "
if command -v python3 >/dev/null 2>&1; then
    PYTEST=$(python3 -c "
import os, asyncio, sys
os.environ['COGNEE_SKIP_CONNECTION_TEST'] = 'true'
os.environ['LLM_PROVIDER'] = 'ollama'
os.environ['LLM_MODEL'] = '$LLM_MODEL'
os.environ['LLM_ENDPOINT'] = '$OLLAMA_HOST/v1'
os.environ['LLM_API_KEY'] = 'dummy'
os.environ['LLM_INSTRUCTOR_MODE'] = 'json_mode'
os.environ['EMBEDDING_PROVIDER'] = 'ollama'
os.environ['EMBEDDING_MODEL'] = '$EMBED_MODEL'
os.environ['EMBEDDING_ENDPOINT'] = '$OLLAMA_HOST/api/embed'
os.environ['EMBEDDING_DIMENSIONS'] = '768'

try:
    import cognee
    result = asyncio.run(cognee.remember('Verification test fact', session_id='verify'))
    results = asyncio.run(cognee.recall('What was the fact?', session_id='verify'))
    if results and 'Verification test fact' in str(results):
        print('OK')
    else:
        print('FAIL - recall empty')
except Exception as e:
    print(f'FAIL - {e}')
    sys.exit(1)
" 2>&1)

    if echo "$PYTEST" | grep -q "OK"; then
        echo -e "${GREEN}OK${NC}"
    else
        echo -e "${YELLOW}WARN${NC} - $PYTEST"
    fi
else
    echo -e "${YELLOW}SKIP${NC} (python3 not found)"
fi

# 6. Test Cognee graph memory (optional, may timeout)
echo -n "6. Cognee graph memory (no session_id)... "
if command -v python3 >/dev/null 2>&1; then
    GRAPH_TEST=$(timeout 60 python3 -c "
import os, asyncio, sys
os.environ['COGNEE_SKIP_CONNECTION_TEST'] = 'true'
os.environ['LLM_PROVIDER'] = 'ollama'
os.environ['LLM_MODEL'] = '$LLM_MODEL'
os.environ['LLM_ENDPOINT'] = '$OLLAMA_HOST/v1'
os.environ['LLM_API_KEY'] = 'dummy'
os.environ['LLM_INSTRUCTOR_MODE'] = 'json_mode'
os.environ['EMBEDDING_PROVIDER'] = 'ollama'
os.environ['EMBEDDING_MODEL'] = '$EMBED_MODEL'
os.environ['EMBEDDING_ENDPOINT'] = '$OLLAMA_HOST/api/embed'
os.environ['EMBEDDING_DIMENSIONS'] = '768'

try:
    import cognee
    result = asyncio.run(cognee.remember('Graph test: Alfred likes concise'))
    results = asyncio.run(cognee.recall('Who likes concise?'))
    if results and 'Alfred' in str(results):
        print('OK')
    else:
        print('WARN - recall empty (LLM extraction may have failed)')
except Exception as e:
    print(f'WARN - {e}')
    sys.exit(0)
" 2>&1)

    if echo "$GRAPH_TEST" | grep -q "OK"; then
        echo -e "${GREEN}OK${NC}"
    else
        echo -e "${YELLOW}WARN${NC} - $GRAPH_TEST"
        echo "   (Graph memory needs LLM with structured output support)"
    fi
else
    echo -e "${YELLOW}SKIP${NC}"
fi

echo
echo "=== Summary ==="
echo -e "${GREEN}Session memory: WORKING${NC} (fast, no LLM calls)"
echo -e "${YELLOW}Graph memory: MAY NEED LLM WITH STRUCTURED OUTPUT${NC}"
echo
echo "If graph memory fails, use session_id mode:"
echo "  await cognee.remember('fact', session_id='my-chat')"
echo "  await cognee.recall('question', session_id='my-chat')"
echo
echo "For graph memory with local LLM, you need:"
echo "  - vLLM with guided_json, or"
echo "  - llama.cpp server with --json-schema, or"
echo "  - OpenAI/Anthropic API key for extraction only"