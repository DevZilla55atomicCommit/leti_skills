#!/bin/bash
# Quick Ollama endpoint check

echo "=== Ollama Endpoint Check ==="
echo

echo "1. Chat endpoint (/v1/models):"
curl -s http://localhost:11434/v1/models | head -20

echo
echo "2. Native embeddings endpoint (/api/embed):"
curl -s http://localhost:11434/api/embed \
  -d '{"model":"nomic-embed-text:latest","input":"test"}' \
  -H "Content-Type: application/json" | head -c 200

echo
echo "3. OpenAI-compatible embeddings (/v1/embeddings):"
curl -s http://localhost:11434/v1/embeddings \
  -d '{"model":"nomic-embed-text:latest","input":"test"}' \
  -H "Content-Type: application/json" | head -c 200

echo
echo "=== Expected: #2 works, #3 may return different format ==="