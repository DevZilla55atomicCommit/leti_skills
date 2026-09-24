---
name: start-tony-workflow
description: Start TONY Agentic OS gateway and open JARVIS dashboard in Chrome app mode
platforms: [macos]
tags: [tony, charlie-os, agentic-os, hermes, dashboard]
---

# Start TONY Workflow

When user says "start-tony", execute this complete workflow:

## Steps

1. **Check if TONY is already running**
   ```bash
   lsof -tiTCP:8787 -sTCP:LISTEN 2>/dev/null
   ```
   If running, show status and open dashboard. If not, proceed to step 2.

2. **Kill any stale processes**
   ```bash
   kill -9 $(cat ~/tony-ai-agent/tony-gateway.pid 2>/dev/null) 2>/dev/null
   lsof -tiTCP:8787 -sTCP:LISTEN 2>/dev/null | xargs -r kill -9 2>/dev/null
   sleep 2
   ```

3. **Start TONY gateway with NVIDIA API key from .env**
   ```bash
   cd ~/tony-ai-agent
   NVIDIA_API_KEY=$(grep '^NVIDIA_API_KEY=' .env | cut -d= -f2) \
     /Users/alfredkamisese/.hermes/node/bin/node src/gateway/server.js \
     >> tony-gateway.log 2>&1 &
   echo $! > tony-gateway.pid
   ```

4. **Wait for health endpoint**
   ```bash
   for i in {1..30}; do
     if curl -s -f "http://localhost:8787/health" -H "Authorization: Bearer tony-hermes-local-2026" >/dev/null 2>&1; then
       echo "Health check passed"
       break
     fi
     sleep 1
   done
   ```

5. **Verify status**
   ```bash
   curl -s "http://localhost:8787/health" -H "Authorization: Bearer tony-hermes-local-2026" | python3 -c "
   import sys, json
   d = json.load(sys.stdin)
   print(f'TONY: {d[\"name\"]} v{d[\"version\"]} | Online: {d[\"online\"]} | LLM: {d[\"llm\"]} | Chain: {\" -> \".join(d[\"llmChain\"][\"chain\"])} | Skills: {d.get(\"skills\",0)} | Brain nodes: {d.get(\"mind\",{}).get(\"graphify\",{}).get(\"nodes\",0)}')
   "
   ```

6. **Open JARVIS Dashboard in Chrome app mode**
   ```bash
   open -a "Google Chrome" --args \
     --app="http://localhost:8787/jarvis?token=tony-hermes-local-2026" \
     --window-size=1400,900
   ```

## Key Configuration

- **Project dir**: `~/tony-ai-agent`
- **Port**: 8787
- **API Token**: `tony-hermes-local-2026`
- **NVIDIA API Key**: Read from `~/tony-ai-agent/.env`
- **Node**: Hermes Node (`/Users/alfredkamisese/.hermes/node/bin/node`) for native addon compatibility
- **Dashboard**: `dashboard.html` (rich 686-line version, served at `/jarvis`)

## Endpoints

| Endpoint | Description |
|---|---|
| `GET /health` | System status + LLM chain |
| `GET /jarvis` | JARVIS HUD dashboard |
| `POST /api/chat` | Chat with TONY |
| `GET /api/skills` | List 21 skills |
| `GET /api/brain/graph/query?q=<term>` | Query Graphify brain |
| `GET /api/hermes/status` | Hermes Agent bridge status |
| `GET /api/hermes/bridge` | TONY status for Hermes |

## Troubleshooting

| Issue | Fix |
|---|---|
| `better-sqlite3` NODE_MODULE_VERSION mismatch | `cd ~/tony-ai-agent && /Users/alfredkamisese/.hermes/node/bin/npm rebuild better-sqlite3 --force` |
| Port 8787 EADDRINUSE | `lsof -ti:8787 \| xargs kill -9` |
| Ollama not responding | `ollama serve` in separate terminal; check `curl localhost:11434/api/tags` |
| Health check fails | Check `~/tony-ai-agent/tony-gateway.log` |
| NVIDIA 403 / invalid x-api-key | Ensure `.env` has `NVIDIA_API_KEY` and no inherited `ANTHROPIC_API_KEY=ollama` |
| Provider chain shows anthropic despite TONY_LLM_PROVIDER=nvidia | Unset `ANTHROPIC_API_KEY` before starting: `unset ANTHROPIC_API_KEY` |

## Hermes Bridge Panel

The JARVIS dashboard includes a **Hermes Agent Bridge** panel (INTELLIGENCE section, diamond icon) with:
- Connection status (online/offline badge)
- Hermes profile, model, skills count
- Bridge commands: Delegate Task, Search Sessions, Sync Memory
- Activity log
- Task delegation textarea + execute button