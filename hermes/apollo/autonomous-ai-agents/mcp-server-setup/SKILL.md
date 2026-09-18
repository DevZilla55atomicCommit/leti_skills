---
name: mcp-server-setup
description: "Configure MCP servers — correct packages, auth, verify."
version: 1.0.0
author: Apollo
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [mcp, claude-code, configuration, setup, debugging]
    related_skills: [claude-code, hermes-agent]
---

# MCP Server Setup for AI Coding Agents

Configure Model Context Protocol (MCP) servers for Claude Code and similar agents. This skill covers the end-to-end workflow: discovering correct package names, installing with proper scope, wiring API keys, and verifying connectivity.

## Prerequisites

- **Node.js + npx** — required for all stdio MCP servers
- **Claude Code installed** (`npm install -g @anthropic-ai/claude-code`) and **authenticated to Anthropic** (not a local proxy)
- **API keys** for services that require them (Firecrawl, Perplexity, Higgsfield, etc.)

## Procedure

### 1. Verify Claude Code Authentication First

```bash
claude auth status --text
```

**Expected output:**
```
Auth token: sk-ant-... (or OAuth token)
Anthropic base URL: https://api.anthropic.com
```

**Pitfall:** If `Anthropic base URL` shows `http://localhost:11434` or any Ollama endpoint, **Claude Code is misconfigured** — it will fail with "unrecognized_model" because local models don't speak the Anthropic API format. Fix before proceeding:
```bash
claude auth login --console   # API key billing
# OR
claude auth login             # Pro/Max OAuth
```

### 2. Discover Correct MCP Package Names

**Do not guess.** The `@modelcontextprotocol/server-*` namespace is largely deprecated. Use these verified packages:

| Capability | Correct Package | Notes |
|------------|----------------|-------|
| Browser automation | `@playwright/mcp@latest` | Installs Chromium on first run (~60s) |
| Chrome DevTools debugging | `chrome-devtools-mcp@latest` | Requires Chrome with `--remote-debugging-port=9222` |
| Web scraping | `firecrawl-mcp@latest` | Requires `FIRECRAWL_API_KEY` |
| Web search | `@modelcontextprotocol/server-perplexity` | Requires `PERPLEXITY_API_KEY` |
| Image/video gen | `@modelcontextprotocol/server-higgsfield` | Requires `HIGGSFIELD_API_KEY` |

**Pitfall:** Search npm or the provider's docs for the current package name — the ecosystem moves fast and `@modelcontextprotocol/server-*` packages are mostly unmaintained.

### 2b. Install Python-based servers on macOS

Some MCP servers ship as Python packages instead of npm. On macOS system Python
there is no venv and /Library/Python is SIP-protected, so `uv pip install` fails
(no environment) and `uv pip install --system` fails (permission denied) — install
to user site-packages and invoke with system python: `pip3 install --user <pkg>`,
then run via `python3 -m <pkg>`. Prefer `uvx`/`pipx` isolation when the server
supports it; fall back to `--user` only when they don't.

### 3. Add MCP Server with User Scope (Global)

```bash
claude mcp add -s user <name> -- npx <package>@latest
```

**Scope flags:**
- `-s user` — Global (all projects), stored in `~/.claude.json` ✅ **Default choice**
- `-s local` — This project only (personal), `.claude/settings.local.json`
- `-s project` — This project (team-shared), `.claude/settings.json`

### 4. Wire API Keys via Environment Variables

For servers requiring API keys, edit `~/.claude.json` directly after adding the server:

```json
"mcpServers": {
  "firecrawl": {
    "type": "stdio",
    "command": "npx",
    "args": ["firecrawl-mcp@latest"],
    "env": {
      "FIRECRAWL_API_KEY": "fc-xxxxxxxxxxxxxxxx"
    }
  }
}
```

**Pitfall:** Do not put secrets in `.claude/settings.json` (git-tracked). Use `~/.claude.json` (global, gitignored) or `.claude/settings.local.json` (local, gitignored). The `claude mcp add` command creates empty `env: {}` — you must populate it manually.

### 5. Verify Connectivity

```bash
claude mcp list
```

**Expected:** All servers show `✔ Connected`. `✘ Failed to connect — -32000: Connection closed` means the package name is wrong or the binary failed to start.

### 6. Test Each Server

```bash
# Playwright
claude -p "Go to https://example.com and tell me the page title" --allowedTools "mcp__playwright__*" --max-turns 3

# Chrome DevTools (start Chrome first: Chrome --remote-debugging-port=9222)
claude -p "List open Chrome tabs" --allowedTools "mcp__chrome-devtools__*" --max-turns 3

# Firecrawl (needs FIRECRAWL_API_KEY in env)
claude -p "Scrape https://example.com and give me the main content" --allowedTools "mcp__firecrawl__*" --max-turns 3
```

Use `--max-turns 3` and `--model haiku` for fast, cheap verification.

## Common Pitfalls

| Symptom | Cause | Fix |
|---------|-------|-----|
| `unrecognized_model` + Ollama URL in auth status | Claude Code pointing to local Ollama | Run `claude auth login --console` or `claude auth login` |
| `✘ Failed to connect — -32000` | Wrong package name or missing binary | Verify package on npm; for Playwright, wait for Chromium install |
| `MCP error -32000: Connection closed` immediately | Server process crashed on startup | Check npx output; some servers need `--headless` or other flags |
| API key not recognized | Key in wrong file or wrong env var name | Edit `~/.claude.json` directly; verify exact env var name in server docs |
| Timeout on first Playwright run | Chromium downloading | Wait 60s; subsequent runs are instant |
| `uv pip install` fails (no venv) / `--system` permission denied on macOS | No venv; SIP-protected /Library/Python | `pip3 install --user <pkg>`; prefer `uvx`/`pipx` when supported |

## References

- `references/package-names.md` — Verified MCP package names by capability
- `references/auth-troubleshooting.md` — Claude Code auth misconfiguration patterns

## Quick Reference Card

```bash
# 1. Check auth
claude auth status --text

# 2. Add servers (global scope)
claude mcp add -s user playwright -- npx @playwright/mcp@latest
claude mcp add -s user chrome-devtools -- npx chrome-devtools-mcp@latest
claude mcp add -s user firecrawl -- npx firecrawl-mcp@latest

# 3. Add API keys to ~/.claude.json (env block per server)

# 4. Verify
claude mcp list

# 5. Test
claude -p "test" --allowedTools "mcp__<server>__*" --max-turns 3
```

## Cross-Provider Model Switching & Auto-Compact Pitfall

**Critical:** Claude Code's `/model` picker ONLY changes the `model` field in settings. It does NOT update:
- `ANTHROPIC_BASE_URL` (endpoint)
- `CLAUDE_CODE_MAX_CONTEXT_TOKENS` (what CC thinks the window is)
- `CLAUDE_CODE_AUTO_COMPACT_WINDOW` (when compaction triggers)
- `OLLAMA_CONTEXT_LENGTH` (Ollama-specific)

**Consequences of cross-provider `/model` switches:**
| Switch Direction | Auto-Compact Threshold | Result |
|------------------|------------------------|--------|
| 48k → 96k (larger) | Stays at 36864 (75% of 48k) | Early compaction — wastes tokens |
| 128k → 48k (smaller) | Stays at 98304 (75% of 128k) | **Exceeds new model's hard limit** → OOM before compaction fires |
| Ollama → Zen (or reverse) | Unchanged | Wrong endpoint + wrong window = 429 / 400 errors |

**Correct pattern:** Always use a switcher script that rewrites the full trio + endpoint + picker atomically:

```bash
# Example switcher (claude-qwen.sh pattern)
MODEL="qwen3.5-48k:latest" CTX=49152 COMPACT=36864 OUT=4096 python3 -c '
import json, os
p = os.path.expanduser("~/.claude/settings.json")
s = json.load(open(p))
s["model"] = os.environ["MODEL"]
s.setdefault("env", {})
s["env"]["ANTHROPIC_BASE_URL"] = "http://localhost:11434"
s["env"]["CLAUDE_CODE_MAX_CONTEXT_TOKENS"] = os.environ["CTX"]
s["env"]["CLAUDE_CODE_AUTO_COMPACT_WINDOW"] = os.environ["COMPACT"]
s["env"]["CLAUDE_CODE_MAX_OUTPUT_TOKENS"] = os.environ["OUT"]
with open(p, "w") as f: json.dump(s, f, indent=2)
'
```

**Auto-compact payload size:** Each compaction re-injects system prompt + CLAUDE.md + auto-memory + skills (capped 5k/skill, 25k total). Keep agents/skills lean (<500 tokens each) or compaction itself becomes a latency spike.

> **Rule:** Never use `/model` to cross provider boundaries. Use a switcher that atomically updates model + endpoint + trio + picker. Within a single provider, `/model` is safe.
