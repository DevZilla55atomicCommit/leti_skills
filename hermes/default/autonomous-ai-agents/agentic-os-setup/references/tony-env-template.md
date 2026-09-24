# Complete TONY .env Template

Copy to `.env` and modify as needed.

```env
# ============================================================================
# TONY AI Agent Configuration — Local-First Agentic OS
# ============================================================================

# --- Server ---
PORT=8787
TONY_DATA_DIR=./data

# --- LLM Provider (choose one primary, chain falls back) ---
# Options: groq | gemini | openai | anthropic | ollama | jan | mock
TONY_LLM_PROVIDER=ollama

# Groq (fast cloud)
GROQ_API_KEY=
GROQ_MODEL=llama-3.3-70b-versatile
GROQ_BASE_URL=https://api.groq.com/openai/v1

# Google AI Studio (Gemini)
GOOGLE_AI_API_KEY=
GEMINI_MODEL=gemini-2.0-flash
GEMINI_BASE_URL=https://generativelanguage.googleapis.com/v1beta

# OpenAI
OPENAI_API_KEY=
OPENAI_MODEL=gpt-4o-mini

# Anthropic (Claude)
ANTHROPIC_API_KEY=
ANTHROPIC_MODEL=claude-sonnet-4-20250514

# Ollama — Fully Local Offline (RECOMMENDED FOR LOCAL-FIRST)
OLLAMA_ENABLED=true
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen3.5:4b-mlx

# Jan.ai — Local OpenAI-compatible
JAN_ENABLED=true
JAN_API_URL=http://localhost:1337/v1
# JAN_MODEL=

# --- Voice (STT + TTS) ---
DEEPGRAM_API_KEY=
DEEPGRAM_MODEL=nova-2
ELEVENLABS_API_KEY=
ELEVENLABS_VOICE_ID=21m00Tcm4TlvDq8ikWAM
ELEVENLABS_MODEL_ID=eleven_multilingual_v2
# Free local TTS fallback (edge-tts)
TONY_TTS_LOCAL_VOICE=en-US-GuyNeural

# --- Obsidian Vault (Agentic Brain) ---
OBSIDIAN_VAULT_PATH=./vault
OBSIDIAN_BRAIN_FOLDER=Agentic Brain

# --- MCP Integrations ---
PERPLEXITY_API_KEY=
PERPLEXITY_MODEL=sonar
FIRECRAWL_API_KEY=
QUICKBOOKS_CLIENT_ID=
QUICKBOOKS_CLIENT_SECRET=
QUICKBOOKS_REFRESH_TOKEN=
QUICKBOOKS_REALM_ID=
QUICKBOOKS_SANDBOX=true
HIGGSFIELD_API_KEY=
HIGGSFIELD_BASE_URL=https://platform.higgsfield.ai
# Playwright MCP (free, local browser automation)
PLAYWRIGHT_MCP_URL=http://localhost:8931/mcp
PLAYWRIGHT_MCP_PORT=8931
PLAYWRIGHT_MCP_HEADLESS=true

# Local-first fallbacks
TONY_LOCAL_FIRST=true

# --- Offline Mode ---
TONY_OFFLINE_AUTO=true
TONY_OFFLINE_FORCE=false

# --- Task Recorder ---
TONY_AUTO_RECORD_TASKS=true
TONY_TASK_MIN_STEPS=2

# --- Goal-Driven Execution ---
TONY_GOAL_MAX_ROUNDS=10
TONY_GOAL_AUTO_RUN=true

# --- Agent Behavior ---
TONY_MAX_ITERATIONS=12
TONY_AUTO_REFLECT=true
TONY_WORKSPACE_ROOT=.

# --- Integrations ---
SIGNALMINT_API_URL=http://localhost:5000
SIGNALMINT_EMAIL=super_admin@signalmint.local
SIGNALMINT_PASSWORD=password123
GITHUB_TOKEN=

# --- Security ---
TONY_API_TOKEN=change_me_tony_gateway_token

# --- Desktop Assistant (Python tony-ai) ---
TONY_DESKTOP_ENABLED=true
# TONY_DESKTOP_PATH=./integrations/repos/tony-ai

# Shell safety (dev only)
TONY_SHELL_UNSAFE=false

# --- Extended MCP Servers ---
OPENWIKI_MCP_URL=
OPENWIKI_DOCS_URL=http://localhost:8090
SCRAPER_MEDIA_MCP_URL=
MOTIONGRAPH_MCP_URL=

# --- 24/7 Daemon ---
TONY_DAEMON_ENABLED=false
TONY_DAEMON_AUTO_GOALS=true
TONY_DAEMON_INTERVAL_MS=300000
TONY_DAEMON_GRAPH_MS=3600000

# --- Self-Healing ---
TONY_SELF_HEAL=true
TONY_SELF_HEAL_RETRIES=1

# --- Companion Mode ---
TONY_COMPANION_MODE=true
TONY_USER_NAME=Alfred
# TONY_WAKE_PHRASES=wake up tony,wake up Tony Daddy's Home
TONY_COMPANION_LLM_GREETING=true
TONY_COMPANION_EMPATHY=true

# --- Always-On Voice ---
TONY_ALWAYS_LISTEN=true

# --- Desktop Automation ---
TONY_AUTOMATION_ENABLED=true

# --- Voice Noise Cancellation ---
TONY_VOICE_NOISE_CANCEL=true
TONY_VOICE_MIN_CONFIDENCE=0.55
TONY_VOICE_HIGHPASS_HZ=180
TONY_VOICE_VAD_MULT=3.2

# --- Context Window Limits ---
TONY_MAX_CONTEXT_TOKENS=100000
TONY_TOOL_RESULT_MAX_CHARS=4000
TONY_EPISODE_MAX_CHARS=6000
TONY_HISTORY_TURNS=12
```