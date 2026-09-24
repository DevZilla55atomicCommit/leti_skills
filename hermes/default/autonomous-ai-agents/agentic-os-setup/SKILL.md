---
name: agentic-os-setup
description: "Complete setup and deployment of local-first Agentic OS (TONY/Charlie OS) with Hermes Agent integration, local LLM (Ollama), Graphify brain, and Paul builder"
platforms: [linux, macos]
tags: [agentic-os, tony, charlie-os, ollama, graphify, paul, hermes, local-llm]
---

# Agentic OS Setup & Deployment

## When to Use

Use when the user wants to deploy a complete **Agentic OS** — a local-first autonomous AI operating system that integrates:
- **TONY/Charlie OS** runtime (Charlie Automates framework)
- **Local LLM** via Ollama (fully offline capable)
- **Graphify** code-graph brain for codebase intelligence
- **Paul builder** (Plan/Apply/Unify/Loop) for agent-driven development
- **Hermes Agent** bridge for skill/MCP sharing
- **JARVIS HUD** voice/visual dashboard
- **MCP stack** (Playwright, Perplexity, Firecrawl, etc.)

## Prerequisites

| Tool | Version | Install |
|------|---------|---------|
| Node.js | 22.x (Hermes bundled) | Use `/Users/alfredkamisese/.hermes/node/bin/node` |
| Ollama | Latest | `brew install ollama` |
| Git | Latest | `brew install git` |
| Python | 3.9+ | For desktop automation bridge |

## Setup Procedure

### 1. Clone Repository

```bash
git clone https://github.com/mafzalkalwardev/tony-ai-agent.git ~/tony-ai-agent
cd ~/tony-ai-agent
```

### 2. Configure Environment (`.env`)

```bash
cp .env.example .env
```

**Critical edits for local-first operation:**
```env
# Use Ollama local LLM (not Groq/cloud)
TONY_LLM_PROVIDER=ollama
OLLAMA_ENABLED=true
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen3.5:4b-mlx   # or your preferred model

# Secure API token for Hermes integration
TONY_API_TOKEN=tony-hermes-local-2026

# User identity for companion mode
TONY_USER_NAME=Alfred

# Local-first: fallback to graphify/repos when paid APIs missing
TONY_LOCAL_FIRST=true
TONY_OFFLINE_AUTO=true
```

**Pull required Ollama model:**
```bash
ollama pull qwen3.5:4b-mlx
```

### 3. Install Dependencies (CRITICAL: Use Hermes Node)

**The system Node (v26+) has module version 147. Hermes bundles Node v22.23.0 (module version 127). Native modules like `better-sqlite3` MUST be compiled against v22.**

```bash
# Use Hermes' Node and npm
/Users/alfredkamisese/.hermes/node/bin/npm install

# If better-sqlite3 fails (prebuild mismatch), rebuild from source:
cd ~/tony-ai-agent
rm -rf node_modules/better-sqlite3
/Users/alfredkamisese/.hermes/node/bin/npm install better-sqlite3@12.11.1 --ignore-scripts
cd node_modules/better-sqlite3
/Users/alfredkamisese/.hermes/node/bin/node /Users/alfredkamisese/.hermes/node/lib/node_modules/npm/node_modules/node-gyp/bin/node-gyp.js rebuild
```

### 4. Boot Charlie OS Gateway

```bash
# Terminal 1: Start gateway (runs on localhost:8787)
/Users/alfredkamisese/.hermes/node/bin/node src/gateway/server.js

# Verify health
curl http://localhost:8787/health
```

### 5. Launch JARVIS HUD

```bash
# Terminal 2: Open JARVIS UI in Chrome app mode
open -a "Google Chrome" --args --app="http://localhost:8787/jarvis?token=tony-hermes-local-2026" --window-size=1400,900
```

### 6. Verify Core Components

| Component | Verification Command | Expected |
|-----------|---------------------|----------|
| Health | `curl localhost:8787/health` | `ok: true`, 97 nodes, 236 edges |
| Chat | `POST /api/chat` with Bearer token | Response from Ollama |
| Graphify | `GET /api/brain/graph/query?q=term` | Nodes/edges for term |
| Paul Builder | `POST /api/agents/paul/build` | Creates files, runs tests |

## Hermes ↔ TONY Integration

**Hermes can call TONY:**
```bash
curl -X POST http://localhost:8787/api/chat \
  -H "Authorization: Bearer tony-hermes-local-2026" \
  -H "Content-Type: application/json" \
  -d '{"message": "Build a dashboard for my metrics"}'
```

**TONY can call Hermes via MCP** (configure in `.env`):
```env
# Add Hermes MCP endpoint when available
HERMES_MCP_URL=http://localhost:XXXX/mcp
```

## Common Pitfalls & Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `NODE_MODULE_VERSION 147 ... requires 127` | Native module compiled with wrong Node | Rebuild with Hermes Node (see Step 3) |
| `EADDRINUSE :::8787` | Port already in use | `lsof -ti:8787 \| xargs kill -9` |
| `better-sqlite3.node` missing | Prebuild not available for Node 26 | Build from source with node-gyp (Step 3) |
| Ollama timeout on `/api/chat` | Model loading / cold start | Pre-warm: `curl -X POST localhost:11434/api/generate -d '{"model":"qwen3.5:4b-mlx","prompt":"hi"}'` |
| Graphify shows 0 nodes | Workspace not indexed | Run `npm run charlie:graph` or check `src/brain/graphify.js` |

## Verification Checklist

- [ ] Gateway responds at `localhost:8787/health`
- [ ] JARVIS HUD loads in browser
- [ ] Chat API returns Ollama response (iterations: 1)
- [ ] Graphify query returns nodes/edges
- [ ] Paul builder creates and verifies test file
- [ ] Ollama model responds directly (`/api/generate`)
- [ ] MCP stack shows Playwright as "local-free"

## Support Files

- `references/tony-env-template.md` — Complete `.env` with all options documented
- `references/node-version-fix.md` — Detailed better-sqlite3 rebuild recipe
- `scripts/verify-tony.sh` — Automated health check script
- `scripts/rebuild-native-modules.sh` — One-command native module rebuild

## Related Skills

- `hermes-agent` — Hermes configuration and native MCP client
- `environment-setup` — General environment auditing and dependency management
- `developer-workflows` — Professional software engineering workflows
- `native-mcp` — MCP server configuration for Hermes
- `llama-cpp` / `serving-llms-vllm` — Alternative local LLM serving