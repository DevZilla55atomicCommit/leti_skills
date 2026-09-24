#!/bin/bash
# TurboQuant llama-server startup script
# Usage: ./llama-server-turbo3.sh [model.gguf] [port] [context]

set -euo pipefail

MODEL="${1:-~/models/gemma4-12b-q4.gguf}"
PORT="${2:-8081}"
CTX="${3:-32768}"

# Expand tilde
MODEL="${MODEL/#\~/$HOME}"

if [[ ! -f "$MODEL" ]]; then
    echo "Error: Model not found: $MODEL"
    exit 1
fi

# Kill existing server on port
lsof -ti:"$PORT" | xargs -r kill -9 2>/dev/null
sleep 1

# TurboQuant environment
export TURBO_LAYER_ADAPTIVE=7
export TURBO_AUTO_ASYMMETRIC=1
export TURBO_SPARSE_V=1
export GGML_METAL_LOG_LEVEL=0
export GGML_METAL_NDEBUG=1

echo "Starting TurboQuant server..."
echo "  Model: $MODEL"
echo "  Port: $PORT"
echo "  Context: $CTX"
echo "  KV Cache: Q8_0 K + Turbo3 V (asymmetric)"

~/llama-cpp-turboquant/build/bin/llama-server \
  -m "$MODEL" \
  --cache-type-k q8_0 \
  --cache-type-v turbo3 \
  -c "$CTX" \
  --port "$PORT" \
  --host 0.0.0.0 \
  -ngl 99 \
  --flash-attn auto \
  --no-warmup