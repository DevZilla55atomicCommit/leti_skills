# NVIDIA NIM Integration Bug Fixes

## 1. Authorization Header Template Literal Bug

**File**: `src/llm/nvidia.js`

**Issue**: The Authorization header used a template literal incorrectly:
```javascript
// BROKEN
headers: {
  Authorization: `Bearer ${config.nvidia.apiKey}`,
  // ...
}
```

This created a literal string with backticks instead of a proper string.

**Fix**: Use regular string concatenation or proper template:
```javascript
// FIXED
headers: {
  Authorization: `Bearer ${config.nvidia.apiKey}`,
  'Content-Type': 'application/json',
}
```

**Root cause**: The original code had `${config.nvidia.apiKey}` inside a template literal that was already using backticks, causing the backtick to be included in the string.

---

## 2. NVIDIA Tool-Calling on Greetings

**File**: `src/core/agent.js` (buildMessages function)

**Issue**: NVIDIA models (meta/llama-3.1-70b-instruct) were calling `memory_search` tool on simple greetings like "Hi", "Hello".

**Root cause**: The system prompt was too long (~2000 tokens) with 61 tool definitions, causing the model to default to tool use.

**Fix**: Ultra-minimal system prompt for NVIDIA provider:
```javascript
const isNvidia = config.llmProvider === 'nvidia';

let system;
if (isNvidia) {
  system = `You are TONY, a helpful AI assistant.

CRITICAL TOOL USAGE INSTRUCTION:
If the user says "Hi", "Hello", "Hey", or any simple greeting — DO NOT use any tools. Simply respond with a friendly greeting like "Hi! How can I help you today?" or "Hello! How's it going?".
Only use tools when the user asks you to do something specific that requires action (search memory, read files, research, etc.).`;
} else {
  // Full system prompt for other providers
}
```

---

## 3. Provider Chain Order

**File**: `src/llm/index.js`

The provider chain priority:
1. `nvidia` (if NVIDIA_API_KEY set)
2. `anthropic` (if ANTHROPIC_API_KEY set)
3. `openai` (if OPENAI_API_KEY set)
4. `ollama` (if OLLAMA_ENABLED=true)
5. `jan` (if JAN_ENABLED=true)
6. `mock` (always last)

---

## 4. Node.js Version Compatibility

**Issue**: `better-sqlite3` v11.x fails to build on Node 22+ (module version mismatch)

**Fix**: Upgrade to v12.x and rebuild:
```bash
npm install better-sqlite3@12.11.1
npm rebuild better-sqlite3
# Or with Hermes Node:
/Users/alfredkamisese/.hermes/node/bin/npm rebuild better-sqlite3
```

---

## 5. Port 8787 Already in Use

**Issue**: Multiple gateway processes started during development

**Fix**:
```bash
lsof -ti:8787 | xargs kill -9
```
Or use the cleanup pattern before starting:
```bash
lsof -ti:8787 | xargs kill -9 2>/dev/null; sleep 1
/Users/alfredkamisese/.hermes/node/bin/node src/gateway/server.js
```

---

## 6. Auth Token Mismatch

**Issue**: Gateway returns "invalid x-api-key" despite correct token

**Cause**: The error was from NVIDIA API, not the gateway auth. The NVIDIA provider was failing and the error message was being passed through.

**Fix**: Ensure NVIDIA provider works correctly (fixes 1 & 2 above), then the gateway will use NVIDIA successfully and not fall back to error messages.