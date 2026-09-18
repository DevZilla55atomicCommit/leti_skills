# TONY Architecture Reference

## Component Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              HERMES AGENT                                    │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐    │
│  │  Graphify   │  │   Skills    │  │  MCP Client │  │  Claude Code    │    │
│  │  Knowledge  │  │  Loader     │  │  (native)   │  │  Bridge         │    │
│  │  Graph      │  │  (45+ skills)│  │             │  │                 │    │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └────────┬────────┘    │
└─────────┼────────────────┼────────────────┼─────────────────┼─────────────┘
          │                │                │                 │
          ▼                ▼                ▼                 ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           TONY GATEWAY (Express + WS)                       │
│  Port 8787                                                                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐    │
│  │  Charlie OS │  │  Graphify   │  │    Paul     │  │    MCP Stack    │    │
│  │  Runtime    │  │   Brain     │  │  Builder    │  │                 │    │
│  │             │  │             │  │  Agent      │  │  • Playwright   │    │
│  │  • boot()   │  │  • nodes    │  │             │  │  • Perplexity   │    │
│  │  • status() │  │  • edges    │  │  • build()  │  │  • Firecrawl    │    │
│  │  • graph()  │  │  • communities│  │  • tools    │  │  • OpenWiki     │    │
│  │  • build()  │  │  • god nodes│  │             │  │  • ScraperMedia │    │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └────────┬────────┘    │
└─────────┼────────────────┼────────────────┼─────────────────┼─────────────┘
          │                │                │                 │
          ▼                ▼                ▼                 ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         LLM PROVIDER CHAIN                                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │  NVIDIA NIM │  │   Ollama    │  │   Jan.ai    │  │    Mock     │        │
│  │  (Cloud)    │  │  (Local)    │  │  (Local)    │  │  (Tests)    │        │
│  │  llama-3.1  │  │  qwen3.5:   │  │  OpenAI-    │  │             │        │
│  │  70b-inst   │  │  4b-mlx     │  │  compat     │  │             │        │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │
└─────────────────────────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           JARVIS HUD                                        │
│  http://localhost:8787/jarvis?token=...                                     │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ Arc Reactor UI • Voice STT/TTS • Command Panel • Neural Graph View │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Data Flow: Hermes → TONY Chat

```
Hermes Agent                    TONY Gateway
    │                              │
    │ POST /api/chat               │
    │ {message, sessionId}         │
    │ Authorization: Bearer ****   │
    │─────────────────────────────▶│
    │                              │ 1. Auth middleware
    │                              │ 2. runAgent({sessionId, message})
    │                              │    ├── loadIdentity()
    │                              │    ├── assembleContext() ← Graphify
    │                              │    ├── loadSkillsContext()
    │                              │    ├── plan() → tool definitions
    │                              │    ├── complete() → LLM chain
    │                              │    │    ├── NVIDIA NIM?
    │                              │    │    ├── Ollama?
    │                              │    │    ├── Jan?
    │                              │    │    └── Mock
    │                              │    ├── executeTool() for each call
    │                              │    ├── synthesize() final response
    │                              │    └── appendEpisode() memory
    │                              │
    │ ◀────────────────────────────│ 200 OK {response, toolResults, iterations}
    │                              │
```

## Core Modules

| Module | Path | Responsibility |
|--------|------|----------------|
| Gateway Server | `src/gateway/server.js` | Express + WS, auth, routes |
| Agent Loop | `src/core/agent.js` | ReAct loop, tool calling, memory |
| Planner | `src/core/planner.js` | Intent → tool plan |
| LLM Chain | `src/llm/index.js` | Provider fallback, completion |
| Providers | `src/llm/*.js` | OpenAI, Anthropic, Groq, Gemini, Ollama, NVIDIA, Jan, Mock |
| Charlie OS | `src/charlie-os/index.js` | Boot, status, graph, build |
| Graphify | `src/brain/graphify.js` | Workspace AST analysis |
| Architectures | `src/brain/architectures.js` | 7-layer cognitive stack context |
| Paul Builder | `src/agents/paul.js` | Autonomous code generation |
| Memory | `src/memory/` | Episodic, semantic, procedural, profile, errors |
| Companion | `src/companion/` | Wake phrases, habits, mood, persona |
| Voice | `src/channels/voice.js` | Deepgram STT, ElevenLabs/edge-tts TTS |
| MCP | `src/mcp/` | Client + server implementations |
| Tools | `src/tools/registry.js` | 61 registered tools |

## LLM Provider Config

```javascript
// src/config.js exports:
{
  llmProvider: 'ollama',           // TONY_LLM_PROVIDER
  nvidia: {                        // NEW
    apiKey: '',                    // NVIDIA_API_KEY
    model: 'meta/llama-3.1-70b-instruct',  // NVIDIA_MODEL
    baseUrl: 'https://integrate.api.nvidia.com/v1'  // NVIDIA_BASE_URL
  },
  ollama: {
    baseUrl: 'http://localhost:11434',  // OLLAMA_BASE_URL
    model: 'qwen3.5:4b-mlx',            // OLLAMA_MODEL
    enabled: true                       // OLLAMA_ENABLED
  },
  // ... groq, gemini, openai, anthropic, jan
}
```

## Graphify Brain Output

`data/graphify.json`:
```json
{
  "nodes": 97,
  "edges": 236,
  "godNodes": ["src/core/agent.js", "src/llm/index.js"],
  "communities": 8,
  "builtAt": "2026-07-08T23:42:36.852Z"
}
```

Query API:
```
GET /api/brain/graph/query?q=<term>&token=<token>
```

## Paul Builder API

```
POST /api/agents/paul/build
Authorization: Bearer <token>
Content-Type: application/json
{"task": "Build a REST API with auth"}

Response:
{
  "agent": "paul",
  "role": "builder",
  "task": "...",
  "response": "Created files...",
  "toolResults": [{"tool": "write_file", "result": {...}}],
  "iterations": 3
}
```

## JARVIS HUD Endpoints

| Route | Description |
|-------|-------------|
| `/jarvis` | Main HUD (HTML + canvas arc reactor) |
| `/css/jarvis.css` | Styles |
| `/js/jarvis.js` | Canvas animation + WS client |
| `/api/voice/converse` | Voice → STT → Agent → TTS |
| `/api/voice/transcribe` | Audio base64 → text |
| `/api/voice/speak` | Text → audio base64 |

## Environment Variables (Complete)

See `templates/tony-env.template` for full list with descriptions.