# Agentic OS Frameworks Research — Session Findings

**Source Video:** "The 3-Step System to Build an Agentic OS in 2026" — Charlie Automates (@charlieautomates)
**Video ID:** 01mYICuCI_Q
**Duration:** 26:46
**Date Analyzed:** 2026-07-08

---

## Video Summary

The video walks through building a complete **Agentic OS dashboard** ("Charlie OS v2") that integrates:
- **Brain**: Obsidian + Graphify (codebase knowledge graph)
- **Build**: Seed (ideation) → Paul (Plan/Apply/Unify/Loop framework) → Next.js dashboard
- **Ship**: Localhost → Railway deploy → MCP bridge to Hermes Agent (VPS) → Graphify queryable via Hermes chat

---

## Transcript Extraction

**Tool Used:** `youtube-content` skill → `scripts/fetch_transcript.py`
**Command:** `uv run python3 fetch_transcript.py "https://youtu.be/01mYICuCI_Q?si=iKleiOoHIHdunYxU" --text-only --timestamps`

**Result:** Full 26-minute transcript extracted successfully with timestamps.

---

## GitHub Repository Discovery Results

### Proprietary Tools (Not on GitHub)

| Tool | Description | Availability |
|------|-------------|--------------|
| **Seed** | Ideation CLI — interviews user, packages spec, launches into Paul | **Gatekept** — only via `charlieautomates.com/free-resources/` (requires email/phone signup) |
| **Paul** | PAUL = Plan, Apply, Unify, Loop framework with phase management, state files, handoff docs | **Gatekept** — same as above |

### Open-Source Alternatives Found

| Pattern | Repo | Description |
|---------|------|-------------|
| **PAUL (Plan/Apply/Unify/Loop)** | `SanthoshVishnuRajamanickam/forge-framework` | 32 slash commands (`/forge:plan`, `/forge:apply`, `/forge:unify`, `/forge:pause`, `/forge:resume`, `/forge:dashboard`). CLAUDE.md documents full command set. |
| **Charlie OS + Graphify + Hermes + Paul Builder** | `mafzalkalwardev/tony-ai-agent` | **TONY AI Agent** — unified personal AI with: Paul builder API (`/api/agents/paul/build`), Charlie OS runtime shell, Graphify code-graph brain, Hermes Agent integration, 52+ tools, voice (Deepgram + ElevenLabs), JARVIS HUD, companion mode, MCP servers. |

### Search Commands That Worked

```bash
# PAUL pattern search
curl "https://api.github.com/search/repositories?q=plan+apply+unify+loop+framework"
# → Found: forge-framework (1 result)

# Charlie Automates search
curl "https://api.github.com/search/repositories?q=%22charlie+automates%22"
# → Found: 1 repo (personal workspace, not the tools)

# Creator search (Charles Dove / @doveccl)
curl "https://api.github.com/users/doveccl/repos"
# → AutoHam, click — unrelated

# Agentic OS + Claude search
curl "https://api.github.com/search/repositories?q=charlie+os+agent"
# → Found: tony-ai-agent (description mentions "Charlie OS")

# Graphify + Hermes
curl "https://api.github.com/search/repositories?q=graphify+hermes+agent"
# → 0 results (but tony-ai-agent has both integrated)
```

---

## Key Findings for Future Research

1. **Charlie Automates tools are proprietary** — Seed & Paul CLIs are distributed only through their "Founder's Toolkit" signup wall. They are NOT open source on GitHub.

2. **The "PAUL" pattern IS implemented openly** — FORGE Framework (`forge-framework`) implements the exact Plan→Apply→Verify→Unify loop with slash commands.

3. **TONY AI Agent is the closest full-stack alternative** — It integrates:
   - Paul builder (agent that builds integrations)
   - Charlie OS runtime shell
   - Graphify (code-graph brain)
   - Hermes Agent (your current environment)
   - MCP servers (Playwright, Perplexity, Firecrawl, etc.)
   - Voice + JARVIS HUD

4. **Research Pitfall to Document:** When a YouTube tutorial gates tools behind signup, search GitHub for the *pattern names* (PAUL, plan/apply/unify, Charlie OS) rather than the tool names. The pattern is often implemented openly under a different name.

5. **Video Transcript Extraction Works Reliably** — The `youtube-content` skill's `fetch_transcript.py` handles timestamps, language selection, and error cases cleanly.

---

## Recommended Next Actions

For building an Agentic OS with Hermes + Graphify:

1. **Option A (Fastest):** Clone `mafzalkalwardev/tony-ai-agent` → `npm run charlie` → wire to your Hermes session
2. **Option B (Learn the pattern):** Install FORGE Framework → run `/forge:init` → `/forge:plan` → `/forge:apply` loops
3. **Option C (Custom):** Scaffold Next.js dashboard → integrate your `graphify-out/` → add Hermes MCP tools → deploy to Railway

---

## Related Files

- `web-research-and-scraping/references/` — GitHub search patterns added to that skill
- `youtube-content/scripts/fetch_transcript.py` — transcript extraction tool
- Transcript output available in session history (2026-07-08)