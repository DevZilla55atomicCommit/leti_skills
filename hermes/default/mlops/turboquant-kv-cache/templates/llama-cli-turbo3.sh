#!/bin/bash
# TurboQuant llama-cli command template
# Usage: ./llama-cli-turbo3.sh [model.gguf] [context] "prompt"

set -euo pipefail

MODEL="${1:-~/models/gemma4-12b-q4.gguf}"
CTX="${2:-32768}"
PROMPT="${3:-Hello, how are you?}"

MODEL="${MODEL/#\~/$HOME}"

if [[ ! -f "$MODEL" ]]; then
    echo "Error: Model not found: $MODEL"
    exit 1
fi

~/llama-cpp-turboquant/build/bin/llama-cli \
  -m "$MODEL" \
  --cache-type-k q8_0 \
  --cache-type-v turbo3 \
  -c "$CTX" \
  -p "$PROMPT" \
  -n 512 \
  -ngl 99 \
  --flash-attn auto \
  --temp 0.7 \
  --top-p 0.95