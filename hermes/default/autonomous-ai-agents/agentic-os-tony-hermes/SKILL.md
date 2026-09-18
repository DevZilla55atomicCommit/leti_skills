---
name: agentic-os-tony-hermes
description: Build and deploy an Agentic OS using TONY (Charlie OS) with Hermes Agent integration. Covers TONY repo setup, Ollama/NVIDIA NIM LLM config, Charlie OS gateway, Graphify brain, Paul builder, JARVIS HUD, MCP stack, and Hermes ↔ TONY API wiring.
platforms: [linux, macos]
tags: [agentic-os, tony, charlie-os, hermes, ollama, nvidia-nim, graphify, paul, mcp, jarvis]
---

# Agentic OS with TONY + Hermes Agent

## When to Use
- Building a local-first Agentic OS dashboard that connects to Hermes Agent
- Integrating TONY (Charlie OS) with existing Graphify knowledge graph
- Setting up Paul builder agent for autonomous code generation
- Configuring Ollama or NVIDIA NIM as LLM backend
- Wiring Hermes Agent skills via MCP to TONY's gateway

## Prerequisites
- macOS/Linux with Node.js 20+ (Hermes Node 22.23.0 recommended for native addon compat)
- Ollama installed with models pulled (`ollama pull qwen3.5:4b-mlx`)
- Git, Python 3.9+ (for desktop automation bridge)
- Hermes Agent running (this session)

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     HERMES AGENT                            │
│  (Graphify, Skills, MCP Client, Claude Code Bridge)        │
└─────────────────────┬───────────────────────────────────────┘
                      │ HTTP + WS (Bearer token)
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                    TONY GATEWAY :8787                       │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐  │
│  │ Charlie  │ │  Graphify│ │   Paul   │ │   MCP Stack  │  │
│  │   OS     │ │  Brain   │ │ Builder  │ │ (Playwright, │  │
│  │ Runtime  │ │ 97 nodes │ │  Agent   │ │  Perplexity) │  │
│  └──────────┘ └──────────┘ └──────────┘ └──────────────┘  │
│         │           │            │              │          │
│         ▼           ▼            ▼              ▼          │
│  ┌──────────────────────────────────────────────────────┐ │
│  │              LLM Provider Chain                      │ │
│  │  NVIDIA NIM → Ollama (qwen3.5:4b-mlx) → Jan → Mock   │ │
│  └──────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                    JARVIS HUD                               │
│         http://localhost:8787/jarvis?token=...              │
└─────────────────────────────────────────────────────────────┘
```

## Quick Start (if TONY already cloned/installed)

```bash
# Check if already running
lsof -tiTCP:8787 -sTCP:LISTEN 2>/dev/null && echo "RUNNING" || echo "STOPPED"

# Use the workflow script (handles PID, NVIDIA env override, health-wait)
bash scripts/start-tony-workflow.sh start
# or: ./scripts/start-tony-workflow.sh start
# or: bash scripts/start-tony.sh start
```

The script:
1. Kills stale processes on port 8787
2. Reads `NVIDIA_API_KEY` from `.env` and overrides inherited env
3. Starts gateway with Hermes Node for native addon compat
4. Waits for `/health` (30s timeout)
5. Shows status: chain, model, skills, brain nodes
6. Opens JARVIS HUD in Chrome app mode (1400×900)

### Script Commands
```bash
./scripts/start-tony-workflow.sh start    # Start + open dashboard
./scripts/start-tony-workflow.sh stop     # Stop gateway
./scripts/start-tony-workflow.sh restart  # Restart + open dashboard
./scripts/start-tony-workflow.sh status   # Show health + chain
./scripts/start-tony-workflow.sh logs     # Tail gateway log
```

## Step-by-Step Deployment (Fresh Clone)

### 1. Clone TONY Repo
```bash
git clone https://github.com/mafzalkalwardev/tony-ai-agent.git ~/tony-ai-agent
cd ~/tony-ai-agent
```

### 2. Configure `.env` for Local-First (Ollama)
```bash
cp .env.example .env
# Edit .env:
TONY_LLM_PROVIDER=ollama
OLLAMA_MODEL=qwen3.5:4b-mlx
OLLAMA_BASE_URL=http://localhost:11434
TONY_API_TOKEN=tony-hermes-local-2026
TONY_USER_NAME=Alfred
TONY_COMPANION_MODE=true
TONY_LOCAL_FIRST=true
```

### 3. Fix Native Addon Compatibility (Critical)
```bash
# Hermes Node v22.23.0 (module v127) vs system Node v26 (v147)
# Use Hermes Node for rebuild:
cd ~/tony-ai-agent
/Users/alfredkamisese/.hermes/node/bin/node -e "require('better-sqlite3')" 2>&1 || \
  /Users/alfredkamisese/.hermes/node/bin/npm rebuild better-sqlite3 --force
```

### 4. Install & Boot
```bash
/Users/alfredkamisese/.hermes/node/bin/npm install
/Users/alfredkamisese/.hermes/node/bin/node src/gateway/server.js &
# Or: /Users/alfredkamisese/.hermes/node/bin/node src/charlie-os/index.js boot
```

### 5. Verify Health
```bash
curl http://localhost:8787/health
# Should show: ollama provider, 97 graph nodes, 21 skills, 61 tools
```

### 6. Test Chat API (Hermes → TONY)
```bash
curl -X POST http://localhost:8787/api/chat \
  -H "Authorization: Bearer tony-hermes-local-2026" \
  -H "Content-Type: application/json" \
  -d '{"message":"Hello TONY, this is Hermes Agent"}'
```

### 7. Query Graphify Brain
```bash
curl "http://localhost:8787/api/brain/graph/query?q=agent&token=tony-hermes-local-2026"
```

### 8. Test Paul Builder
```bash
curl -X POST http://localhost:8787/api/agents/paul/build \
  -H "Authorization: Bearer tony-hermes-local-2026" \
  -H "Content-Type: application/json" \
  -d '{"task":"Create a test integration module"}'
```

### 9. Launch JARVIS HUD
```bash
open -a "Google Chrome" --args --app="http://localhost:8787/jarvis?token=tony-hermes-local-2026" --window-size=1400,900
```

## NVIDIA NIM Integration (Faster Cloud LLM)

### Add to `.env`:
```bash
NVIDIA_API_KEY=your_nim_api_key
NVIDIA_BASE_URL=https://integrate.api.nvidia.com/v1
NVIDIA_MODEL=meta/llama-3.1-70b-instruct
TONY_LLM_PROVIDER=nvidia
```

### Provider Chain Priority:
1. **NVIDIA NIM** (primary, if API key set)
2. **Ollama** (local fallback)
3. **Jan.ai** (if running)
4. **Mock** (tests only)

### Provider Module Added:
- `src/llm/nvidia.js` — OpenAI-compatible client
- Registered in `src/llm/index.js` `createProvider()` and `buildChain()`
- Config in `src/config.js` under `nvidia: {}`

## Graphify Integration (Your Project)

Your existing Graphify output at `graphify-out/` can be connected:

```bash
# In .env:
OBSIDIAN_VAULT_PATH=/Users/alfredkamisese/TamaZila Obsidian Vault
OBSIDIAN_BRAIN_FOLDER=Agentic Brain
```

Then TONY's `architectures.assembleContext()` will include your Obsidian vault notes.

## MCP Stack (Playwright + More)

```bash
# Start Playwright MCP (free local browser automation)
npm run playwright:mcp

# Start full MCP stack
npm run mcp:stack
```

Available MCPs: Perplexity, Firecrawl, QuickBooks, Higgsfield, OpenWiki, Scraper Media, Motiongraph, Obsidian Skills.

## Hermes ↔ TONY Skill Bridge

TONY's MCP client can call Hermes skills if Hermes exposes MCP endpoints. Configure in `.env`:
```bash
# If Hermes runs MCP server on port XXXX
HERMES_MCP_URL=http://localhost:XXXX/mcp
```

Then TONY's `mcp_call` tool can invoke Hermes skills directly.

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `better-sqlite3` NODE_MODULE_VERSION mismatch | Rebuild with Hermes Node: `/Users/alfredkamisese/.hermes/node/bin/npm rebuild better-sqlite3 --force` |
| Port 8787 EADDRINUSE | `lsof -ti:8787 | xargs kill -9` |
| Ollama not responding | `ollama serve` in separate terminal; check `curl localhost:11434/api/tags` |
| Chat API hangs | Check Ollama model loaded: `ollama ps`; reduce context in `.env` `TONY_MAX_CONTEXT_TOKENS=50000` |
| Graphify 0 nodes | Run `npm run charlie:graph` to rebuild from workspace |
| "invalid x-api-key" error despite correct token | Trim whitespace in auth comparison: ensure both token and config.apiToken are trimmed before comparison |
| NVIDIA provider timeout with tool calls | Use minimal system prompt: "You are TONY, a helpful AI assistant. CRITICAL: For greetings like Hi/Hello, NEVER use tools. Just respond naturally." |
| NVIDIA provider not being used despite TONY_LLM_PROVIDER=nvidia | Check that anthropic API key is empty string (not undefined) - empty string in env causes config.anthropic.apiKey to be "" which is truthy in JS; explicitly check for non-empty strings |
| **NVIDIA 403 "Authorization failed" / Anthropic "invalid x-api-key" in gateway** | **CRITICAL: Gateway inherits shell env vars from parent (Hermes/Claude Code).** Override at startup: `NVIDIA_API_KEY=$(grep NVIDIA_API_KEY .env | cut -d= -f2) node src/gateway/server.js`. Also ensure `isValidApiKey()` in `src/llm/index.js` rejects fake keys like "ollama", "none", "dummy" |
| **Provider chain shows anthropic despite TONY_LLM_PROVIDER=nvidia** | Inherited `ANTHROPIC_API_KEY=ollama` (from Hermes Ollama integration) makes config truthy. Fix: `isValidApiKey()` filters out known-invalid values; or unset ANTHROPIC_API_KEY before starting gateway |
| **NVIDIA model returns 403 on free tier** | Free NIM tier doesn't support `meta/llama-3.1-70b-instruct`. Use `nvidia/nemotron-3-ultra-550b-a55b` (works on free tier) |

### Workflow Pitfalls

| Issue | Fix |
|-------|-----|
| **Agent re-clones or re-installs TONY when it's already running** | **Check port 8787 + PID file FIRST.** `lsof -tiTCP:8787` + `cat ~/tony-ai-agent/tony-gateway.pid`. If running, just health-check and report status. Use the Quick Start section, not the fresh-deploy steps. |
| **Agent doesn't know about `start-tony.sh` script** | Use `bash scripts/start-tony.sh start|stop|restart|status|logs` — it handles PID management, NVIDIA env override, and health-wait automatically. Don't manually `nohup node src/gateway/server.js` when the script exists. |

## References
- `references/tony-architecture.md` — Full component diagram
- `references/nvidia-nim-setup.md` — NIM API key, model selection, rate limits
- `references/env-var-inheritance-fix.md` — Shell env var inheritance root cause & fix
- `references/env-var-inheritance-debugging.md` — Step-by-step debugging reproduction
- `references/graphify-integration.md` — Connecting your Obsidian vault
- `templates/tony-env.template` — Complete .env with all options
- `scripts/verify-tony.sh` — Health check + API test script
- `scripts/start-tony.sh` — Original start/stop/restart/status manager (handles PID, NVIDIA env override, health-wait)
- `scripts/start-tony-workflow.sh` — Enhanced workflow script with Chrome dashboard open (preferred for "start-tony" command)

## Scripts
- `scripts/verify-tony.sh` — Health check + API test
- `scripts/start-tony.sh` — Start/stop/restart/status/logs manager
- `scripts/start-tony-workflow.sh` — Enhanced workflow with Chrome dashboard open (used by "start-tony" command)