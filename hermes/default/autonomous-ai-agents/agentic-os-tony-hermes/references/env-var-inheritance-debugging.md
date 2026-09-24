# Env Var Inheritance Debugging — Session 20260709_101631_28266c

## Problem
TONY gateway running under Hermes Agent inherits shell environment variables from the parent process (Hermes/Claude Code integration). These override `.env` file values, causing:
- Anthropic key = `"ollama"` (from Hermes Ollama integration) → `invalid x-api-key` error
- NVIDIA key = placeholder → `403 Authorization failed`
- Provider chain polluted with providers that have fake keys

## Root Cause
`dotenv` loads `.env` but **does not override** existing process.env values by default. Hermes Agent sets:
- `ANTHROPIC_API_KEY=ollama` (for its Ollama/Claude Code proxy)
- `ANTHROPIC_BASE_URL=http://localhost:11434`
- `NVIDIA_API_KEY=...` (placeholder)

TONY's `config.js` reads these via `env()` → process.env → inherits fake values.

## Reproduction
```bash
# In Hermes shell (has ANTHROPIC_API_KEY=ollama, NVIDIA_API_KEY=placeholder)
cd ~/tony-ai-agent
node -e "console.log(process.env.ANTHROPIC_API_KEY)"  # "ollama"
node -e "const c=require('./src/config'); console.log(c.anthropic.apiKey)"  # "ollama"
```

## Fixes Applied

### 1. Permanent: `isValidApiKey()` in `src/llm/index.js`
```javascript
function isValidApiKey(key) {
  const trimmed = key?.trim();
  if (!trimmed) return false;
  const invalid = ['ollama', 'none', 'dummy', 'test', 'sk-', 'placeholder'];
  return !invalid.some((v) => trimmed.toLowerCase() === v);
}
```
Used in `buildChain()` and `providerStatus()` — filters out fake keys from inherited env.

### 2. Operational: Start gateway with explicit key override
```bash
cd ~/tony-ai-agent
NVIDIA_API_KEY=$(grep NVIDIA_API_KEY .env | cut -d= -f2) node src/gateway/server.js
```

### 3. Model selection
Free NIM tier: `nvidia/nemotron-3-ultra-550b-a55b` ✅
`meta/llama-3.1-70b-instruct` ❌ 403 Forbidden

## Verification Checklist
- [ ] `curl /health` → `llmChain.chain` shows `['nvidia', 'jan']` (no anthropic)
- [ ] `curl /api/chat` → `provider: "nvidia"` in response
- [ ] No 403/401 errors in gateway logs
- [ ] `[NVIDIA ERROR]` debug log shows actual error if any

## Related Files
- `src/llm/index.js` — `isValidApiKey()`, `buildChain()`, `providerStatus()`
- `src/llm/nvidia.js` — NVIDIA provider with error logging
- `src/config.js` — `env()` function reads process.env
- `.env` — Source of truth for TONY config