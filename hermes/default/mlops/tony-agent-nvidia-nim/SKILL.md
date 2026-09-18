---
name: tony-agent-nvidia-nim
description: "Deploy TONY Agent (Charlie OS) with NVIDIA NIM as primary LLM provider"
version: 1.0.0
author: Hermes Agent
license: MIT
tags: [tony-agent, charlie-os, nvidia-nim, nvidia-nim, llm-inference, ai-agent, openai-compatible]
platforms: [linux, macos]
dependencies: [node, npm, ollama-optional]
metadata:
  hermes:
    tags: [tony-agent, charlie-os, nvidia-nim, nvidia-nim, llm-inference, ai-agent, openai-compatible]
---

# TONY Agent (Charlie OS) with NVIDIA NIM

Deploy the TONY AI Agent (Charlie OS runtime) using NVIDIA NIM as the primary LLM provider via OpenAI-compatible API.

## What this skill covers

- Cloning and configuring TONY Agent (Charlie OS)
- Setting up NVIDIA NIM as primary LLM provider
- Fixing NVIDIA provider integration for tool-calling behavior
- Gateway configuration with NVIDIA as primary + Ollama fallback
- System prompt engineering for NVIDIA to prevent tool-calling on greetings

## Prerequisites

- Node.js 20+ (via Hermes node or system)
- NVIDIA NIM API key (from https://build.nvidia.com)
- Optional: Ollama for local fallback
- macOS/Linux environment

## Quick start

```bash
# 1. Clone TONY Agent
git clone https://github.com/mafzalkalwardev/tony-ai-agent.git ~/tony-ai-agent
cd ~/tony-ai-agent

# 2. Install dependencies (use Hermes Node for compatibility)
/Users/alfredkamisese/.hermes/node/bin/npm install

# 3. Fix better-sqlite3 for Node 22+
/Users/alfredkamisese/.hermes/node/bin/npm rebuild better-sqlite3

# 4. Configure environment
cp .env.example .env
# Edit .env with your NVIDIA NIM credentials
```

## Configuration

### Required .env variables

```env
# NVIDIA NIM (Primary)
NVIDIA_API_KEY=nvapi-xxxxxxxxxxxxxxxxxxxxxxxx
NVIDIA_BASE_URL=https://integrate.api.nvidia.com/v1
NVIDIA_MODEL=meta/llama-3.1-70b-instruct

# LLM Provider chain
TONY_LLM_PROVIDER=nvidia

# Optional: Ollama fallback
OLLAMA_ENABLED=true
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen3.5:4b-mlx

# Gateway
TONY_API_TOKEN=your-secure-token
PORT=8787

# Optional: Other providers (disabled by default)
OLLAMA_ENABLED=false
GROQ_API_KEY=
GOOGLE_AI_API_KEY=
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
```

### Provider chain order (src/llm/index.js)

The provider chain is built in this priority:
1. `nvidia` (if NVIDIA_API_KEY set)
2. `anthropic` (if ANTHROPIC_API_KEY set)
3. `openai` (if OPENAI_API_KEY set)
4. `ollama` (if OLLAMA_ENABLED=true)
5. `jan` (if JAN_ENABLED=true)
6. `mock` (always last)

## Key fixes applied

### 1. NVIDIA provider (src/llm/nvidia.js)

- Fixed Authorization header formatting: `Bearer ${apiKey}` (was template literal bug)
- Added `tool_choice: auto` for proper tool-calling
- Handles both tool calls and regular responses

### 2. Minimal system prompt for NVIDIA (src/core/agent.js)

NVIDIA models get confused by long system prompts with 61 tool definitions. The fix uses an ultra-minimal prompt for NVIDIA:

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

### 3. Gateway startup

```bash
# Start gateway (uses Hermes Node for compatibility)
/Users/alfredkamisese/.hermes/node/bin/node src/gateway/server.js

# Or via npm script
/Users/alfredkamisese/.hermes/node/bin/npm run charlie
```

## API Endpoints

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/health` | GET | None | System status |
| `/api/chat` | POST | Bearer token | Chat with TONY |
| `/api/brain/graph/query?q=term` | GET | Bearer token | Query Graphify brain |
| `/api/agents/paul/build` | POST | Bearer token | Paul builder agent |
| `/jarvis` | GET | Token query | JARVIS HUD UI |

## Testing

```bash
# Health check
curl http://localhost:8787/health

# Chat with TONY
curl -X POST http://localhost:8787/api/chat \
  -H "Authorization: Bearer tony-hermes-local-2026" \
  -H "Content-Type: application/json" \
  -d '{"message":"Hi TONY"}'

# Query Graphify brain
curl "http://localhost:8787/api/brain/graph/query?q=agent&token=tony-hermes-local-2026"
```

## Troubleshooting

### "invalid x-api-key" from NVIDIA

The NVIDIA provider was sending malformed Authorization header. Fixed in `src/llm/nvidia.js`:

```javascript
// Before (broken):
Authorization: `Bearer ${config.nvidia.apiKey}`

// After (fixed):
Authorization: `Bearer ${config.nvidia.apiKey}`
```

### NVIDIA calls tools on greetings

Fixed by ultra-minimal system prompt for NVIDIA provider that explicitly forbids tool use on greetings.

### Gateway fails to start - port 8787 in use

```bash
lsof -ti:8787 | xargs kill -9
```

### better-sqlite3 rebuild needed

```bash
cd ~/tony-ai-agent
/Users/alfredkamisese/.hermes/node/bin/npm rebuild better-sqlite3
```

### Ollama not available as fallback

Ensure `OLLAMA_ENABLED=true` and Ollama is running:
```bash
ollama serve
ollama pull qwen3.5:4b-mlx
```

## Architecture

```
┌─────────────────────────────────────────────┐
│           TONY Gateway (Express)            │
│              Port 8787                       │
└─────────────────┬───────────────────────────┘
                  │
        ┌─────────┴─────────┐
        ▼                   ▼
   ┌─────────┐         ┌─────────┐
   │  NVIDIA │         │  Ollama │
   │   NIM   │         │ (Local) │
   └────┬────┘         └────┬────┘
        │                   │
        └─────────┬─────────┘
                  ▼
         ┌─────────────────┐
         │  Provider Chain │
         │  (src/llm)      │
         └─────────────────┘
```

## References

- TONY Agent repo: https://github.com/mafzalkalwardev/tony-ai-agent
- NVIDIA NIM API: https://build.nvidia.com
- Charlie OS: https://charlieautomates.com

## Files modified from upstream

- `src/llm/nvidia.js` - Fixed auth header, tool choice
- `src/core/agent.js` - Minimal NVIDIA system prompt
- `src/config.js` - Added NVIDIA config section
- `src/llm/index.js` - Added NVIDIA to provider chain

---

*This skill captures the deployment pattern for TONY Agent with NVIDIA NIM as primary LLM provider. Use for rapid deployment of Charlie OS with cloud LLM backend.*