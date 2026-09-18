---
name: ai-agent-dashboards
category: creative
description: Build professional control interfaces for AI agents and Agentic OS — dashboards with voice I/O, knowledge graph visualization, document vault browsers, workflow automation, MCP/integration status, and real-time system monitoring.
tags: [ai-agent, dashboard, voice-interface, knowledge-graph, obsidian, mcp, workflow-automation, realtime-monitoring, elevenlabs, deepgram, graphify]
---

# AI Agent Dashboards

## When to Use
- Building a control panel for an AI agent system (TONY, JARVIS, custom agents)
- Need a unified interface combining chat, voice, graph, vault, workflows, integrations
- Professional-grade UI required (not prototype) — production styling, animations, accessibility
- Multiple real-time data sources: LLM providers, MCP servers, graph databases, voice APIs

## Core Architecture Patterns

### 1. Application Shell (`dashboard.html` + `dashboard.css`)
- **Layer stack**: Background canvas (z:0) → Main app (z:10) → Modals/Toasts (z:100)
- **Sidebar navigation** with collapsible mobile support (≤900px breakpoint)
- **Top bar**: View title, system status pills, voice/theme/session controls
- **View system**: 9 views (command, workflows, goals, graph, brain, obsidian, integrations, mcp, settings)
- **Token auth**: URL param `?token=` → localStorage → token dialog fallback

### 2. API Client Pattern (`dashboard.js` → `APIClient` class)
```javascript
class APIClient {
  constructor(getToken) { this.getToken = getToken; this.base = '/api'; }
  headers() { return { 'Content-Type': 'application/json', ...(this.getToken() ? { Authorization: 'Bearer ' + this.getToken() } : {}) }; }
  async request(endpoint, options = {}) {
    const res = await fetch(this.base + endpoint, { headers: this.headers(), ...options, body: options.body ? JSON.stringify(options.body) : undefined });
    const data = await res.json().catch(() => ({}));
    if (!res.ok) throw new Error(data.error || `HTTP ${res.status}`);
    return data;
  }
  // Endpoint methods: health(), chat(), transcribe(), speak(), getGraph(), listVault(), etc.
}
```
**Key**: All endpoints prefixed with `/api/` — matches `src/gateway/server.js` routes.

### 3. View Lifecycle
```javascript
async function initView(view) {
  switch (view) {
    case 'command': await initCommandView(); break;   // Chat + Voice
    case 'graph': await initGraphView(); break;       // Canvas graph
    case 'obsidian': await loadObsidianVault(); break; // Tree + search
    // ...
  }
}
```
Each view initializes on first load, caches data in `state.*`, cleans up on unload.

### 4. Voice Interface (ElevenLabs + Deepgram with Fallbacks)
**STT Priority**: Deepgram (cloud) → Browser SpeechRecognition
```javascript
async function startListening() {
  if (!state.voice.deepgramOk) return startBrowserRecognition();
  const stream = await navigator.mediaDevices.getUserMedia({ audio: { noiseSuppression: true, echoCancellation: true } });
  const recorder = new MediaRecorder(stream, { mimeType: MediaRecorder.isTypeSupported('audio/webm') ? 'audio/webm' : 'audio/mp4' });
  recorder.ondataavailable = e => e.data.size && state.voice.audioChunks.push(e.data);
  recorder.onstop = async () => { await processAudioBlob(new Blob(state.voice.audioChunks, { type: mime }), mime); };
  recorder.start();
}
```
**TTS Priority**: ElevenLabs → Browser speechSynthesis
```javascript
async function speakText(text) {
  const result = await api.speak(cleanText, state.settings.elevenVoice || CONFIG.defaultVoice);
  if (result.ok && result.audio) await playBase64Audio(result.audio, result.mimeType);
  else await browserSpeak(cleanText);
}
```
**Push-to-talk**: Space keydown/keyup on Command view.

### 5. Knowledge Graph Canvas (Graphify)
- **Force-directed layout** with cached positions (`node._x`, `node._y`)
- **Node types**: file=cyan, function=green, class=red, import=yellow, concept=purple
- **Edges**: rgba(0,229,255,0.15) lines between `_x/_y` positions
- **Controls**: Layout selector (force/hierarchical/circular), Rebuild button → `/api/brain/graph/build`
- **Stats**: Nodes, Edges, Communities from `/api/brain/graph` response

### 6. Obsidian Vault Browser
- **Index**: `state.obsidian.searchIndex[path] = (title + path + content + tags).toLowerCase()`
- **Tree**: Grouped by folder, clickable note cards with preview + tags
- **Search**: Debounced (300ms) filter on index
- **Filters**: All / Projects / Tasks / Notes / Archive buttons
- **Modal**: Full note with markdown rendering (basic: headers, bold, code, links, lists)
- **Open in Obsidian**: `obsidian://open?vault=...&file=...`

### 7. System Status Panel
- **6 indicators**: Gateway, LLM, Graphify, Obsidian, ElevenLabs, Deepgram
- **States**: ok (green), warn (amber), error (red)
- **Provider pills**: NVIDIA, Groq, Gemini, Ollama, Jan.ai — active highlighted
- **Refresh button** → `loadSystemStatus()` → `/health` + `/api/local/status`

### 8. Workflows & Goals
- **Workflow form**: Task textarea, Mode select (auto/plan/execute), Success criteria, Speak toggle
- **Progress modal**: Streaming steps (WebSocket-ready), tool calls, status
- **History**: Cards with task, status badge, mode, relative time
- **Goals**: Title, description, success criteria array, max rounds

### 9. Integrations & MCP
- **Integration cards**: Deepgram, ElevenLabs, NVIDIA, Groq, Gemini, OpenAI, Firecrawl, Perplexity
- **Config fields**: apiKey, voiceId, modelId — masked inputs, save/test buttons
- **MCP grid**: Playwright (configured), others — tools list, URL, restart/logs actions

### 10. Settings Persistence
- **localStorage keys**: `tony_theme`, `tony_settings`, `tony_api_token`, `tony_session_id`
- **Settings object**: elevenVoice, ttsModel, autoListen, theme, accentColor, reducedMotion, API keys (masked)
- **Apply**: `document.documentElement.setAttribute('data-theme')`, `--cyan` CSS var, transition speed

## API Endpoint Map (Must Match Backend)

| Feature | Endpoint | Method |
|---------|----------|--------|
| Health | `/health` | GET |
| Chat | `/api/chat` | POST |
| Voice STT | `/api/voice/transcribe` | POST |
| Voice TTS | `/api/voice/speak` | POST |
| Voice Converse | `/api/voice/converse` | POST |
| Graph | `/api/brain/graph` | GET |
| Graph Build | `/api/brain/graph/build` | POST |
| Graph Query | `/api/brain/graph/query` | GET |
| Brain Status | `/api/brain/status` | GET |
| Architectures | `/api/brain/architectures` | GET |
| Vault List | `/api/brain/obsidian/list` | GET |
| Vault Search | `/api/brain/obsidian/search` | GET |
| Vault Read | `/api/brain/obsidian/read` | GET |
| Vault Create | `/api/brain/obsidian/create` | POST |
| Workflows | `/api/workflows` | GET |
| Workflow Run | `/api/workflows/run` | POST |
| Goals | `/api/goals` | GET |
| Goal Run | `/api/goals/run` | POST |
| MCP Status | `/api/mcp/status` | GET |
| MCP Call | `/api/mcp/call` | POST |
| Integrations | `/api/integrations/manifest` | GET |
| Free LLM | `/api/free-llm` | GET |
| Tasks | `/api/tasks` | GET |
| Profile | `/api/profile` | GET |
| Local Status | `/api/local/status` | GET |

## CSS Architecture (`dashboard.css`)
- **CSS Custom Properties**: `--bg`, `--panel`, `--border`, `--text`, `--text-dim`, `--cyan`, `--green`, `--red`, `--amber`, `--purple`, `--font-ui`, `--font-mono`, `--transition-base`
- **Dark/Light themes** via `[data-theme="dark/light"]` on `<html>`
- **Reduced motion**: `--transition-base: 0.01ms` when enabled
- **Components**: Buttons (primary/secondary/ghost), Cards, Forms, Modals, Toasts, Badges, Tables, Canvas containers
- **Animations**: `slideIn`, `fadeIn`, `pulse`, `spin`, `shimmer`

## Common Pitfalls & Fixes

| Problem | Solution |
|---------|----------|
| 404 on `/brain/graph` | Use `/api/brain/graph` — all endpoints need `/api/` prefix |
| Voice STT fails silently | Check `state.voice.deepgramOk` from `/health`; fallback to `SpeechRecognition` |
| Canvas graph blank | Call `resize()` on mount + window resize; `canvas.width = rect.width * devicePixelRatio` |
| Buttons unclickable | Ensure no overlapping transparent elements; check `z-index` stacking |
| Markdown not rendering | `renderMarkdown()` only handles basic syntax; use `marked` lib for production |
| Token not sent | `APIClient.headers()` reads `state.token` — ensure `loadToken()` ran before init |
| Obsidian vault empty | Backend `configured: false` — check vault path in settings |
| View not loading | `initView()` must be called after `switchView()` sets active class |

## Templates
- `templates/agent-dashboard-starter.html` — Minimal shell with auth, sidebar, view switching, toast system
- `templates/voice-interface-module.js` — Standalone voice class (STT/TTS with fallbacks)
- `templates/graph-canvas-renderer.js` — Force-directed graph renderer (nodes, edges, layouts)
- `templates/vault-browser-module.js` — Obsidian tree + search + markdown preview

## References
- `references/tony-backend-api.md` — Actual endpoint signatures from `src/gateway/server.js`
- `references/voice-api-patterns.md` — Deepgram/ElevenLabs request/response formats
- `references/graphify-data-format.md` — Nodes/edges/communities JSON schema
- `references/obsidian-api-patterns.md` — Vault list/search/read/create endpoints

## Related Skills
- `interactive-3d-dashboards` — For Three.js-based graph visualizations (alternative to canvas)
- `developer-workflows` — API design, state management, production standards
- `claude-design` — Rapid HTML prototyping for dashboard variants