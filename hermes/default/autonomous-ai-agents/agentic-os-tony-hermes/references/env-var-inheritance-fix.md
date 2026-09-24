# Shell Environment Variable Inheritance — Root Cause & Fix

## Problem
The TONY gateway process inherits shell environment variables from its parent process (Hermes Agent / Claude Code). These inherited vars override the `.env` file values loaded by `dotenv`:

| Inherited Var | Source | Value | Effect |
|---------------|--------|-------|--------|
| `ANTHROPIC_API_KEY` | Hermes Ollama/Claude Code integration | `"ollama"` (string) | Makes `config.anthropic.apiKey` truthy → anthropic added to provider chain |
| `ANTHROPIC_BASE_URL` | Hermes Ollama/Claude Code integration | `"http://localhost:11434"` | Points anthropic provider to local Ollama |
| `NVIDIA_API_KEY` | Hermes/Claude Code config | `"nvapi-YOUR_KEY_HERE"` (placeholder) | NVIDIA 403 "Authorization failed" |

## Root Cause
1. **dotenv doesn't override existing process.env** — `dotenv.config()` only sets undefined vars
2. **Hermes injects Ollama/Anthropic vars** for its own Claude Code/Ollama integration
3. **TONY config reads `process.env.ANTHROPIC_API_KEY`** → gets `"ollama"` instead of empty string from `.env`
4. **`config.anthropic.apiKey?.trim()` returns `"ollama"`** → truthy → added to provider chain
5. **TONY tries to call Anthropic with key `"ollama"`** → 401 "invalid x-api-key"
6. **NVIDIA_API_KEY is also overridden** with placeholder → 403 "Authorization failed"

## Fix: Explicit Override at Startup

```bash
# In start script:
NVIDIA_API_KEY=$(grep '^NVIDIA_API_KEY=' .env | cut -d= -f2)
export NVIDIA_API_KEY
node src/gateway/server.js
```

Or inline:
```bash
NVIDIA_API_KEY=$(grep NVIDIA_API_KEY .env | cut -d= -f2) node src/gateway/server.js
```

## Fix: Provider Key Validation in Code

Add `isValidApiKey()` to `src/llm/index.js`:

```javascript
function isValidApiKey(key) {
  const trimmed = key?.trim();
  if (!trimmed) return false;
  // Filter out known-invalid values from other tools
  const invalid = ['ollama', 'none', 'dummy', 'test', 'sk-', 'placeholder', 'your_key_here'];
  return !invalid.some(v => trimmed.toLowerCase() === v);
}

// Use in buildChain() and providerStatus()
```

## Fix: NVIDIA Model for Free Tier

Free NVIDIA NIM tier doesn't support `meta/llama-3.1-70b-instruct` (403).
Use: `nvidia/nemotron-3-ultra-550b-a55b` (works on free tier).

```env
NVIDIA_MODEL=nvidia/nemotron-3-ultra-550b-a55b
```

## Debugging Steps (Reproduction)

```bash
# 1. Check what env vars the running process has
ps eww -p <PID> | tr ' ' '\n' | grep -i ANTHROPIC

# 2. Verify .env values
grep NVIDIA_API_KEY .env
grep ANTHROPIC_API_KEY .env

# 3. Test config loading
node -e "
require('dotenv').config({path: '.env'});
console.log('ANTHROPIC_API_KEY:', JSON.stringify(process.env.ANTHROPIC_API_KEY));
const config = require('./src/config');
console.log('config.anthropic.apiKey:', JSON.stringify(config.anthropic.apiKey));
"

# 4. Test provider chain
node -e "
require('dotenv').config({path: '.env'});
const {buildChain} = require('./src/llm');
console.log('chain:', buildChain());
"

# 5. Test with clean env
ANTHROPIC_API_KEY= ANTHROPIC_BASE_URL= node -e "
require('dotenv').config({path: '.env'});
const {buildChain} = require('./src/llm');
console.log('chain:', buildChain());
"
```

## Files Modified This Session

| File | Change |
|------|--------|
| `src/llm/index.js` | Added `isValidApiKey()`; updated `buildChain()` and `providerStatus()` |
| `.env` | `NVIDIA_MODEL=nvidia/nemotron-3-ultra-550b-a55b` |
| `scripts/start-tony.sh` | Exports `NVIDIA_API_KEY` from `.env` before starting gateway |
| `src/llm/nvidia.js` | Added debug logging for 403 errors |

## References

- [dotenv behavior](https://github.com/motdotla/dotenv#how-do-i-use-dotenv-with-import) — doesn't override existing env vars
- [Node.js process.env](https://nodejs.org/api/process.html#process_process_env) — inherited from parent
- NVIDIA NIM Free Tier models: https://build.nvidia.com/explore/discover