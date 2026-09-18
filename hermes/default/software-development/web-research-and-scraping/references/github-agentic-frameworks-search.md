# GitHub Search Patterns for Agentic OS / AI Agent Frameworks

**Session:** 2026-07-08 — Researching "Charlie Automates" Agentic OS video tools
**Trigger:** Video gates Seed/Paul CLIs behind email signup; needed open-source alternatives

---

## Search Commands That Worked

### PAUL Pattern (Plan/Apply/Unify/Loop)
```bash
curl "https://api.github.com/search/repositories?q=plan+apply+unify+loop+framework"
```
**Result:** `SanthoshVishnuRajamanickam/forge-framework` — 32 slash commands implementing PAUL loop

### Charlie Automates / Charlie OS
```bash
curl "https://api.github.com/search/repositories?q=%22charlie+automates%22"
```
**Result:** 1 repo (personal workspace, not the tools)

```bash
curl "https://api.github.com/search/repositories?q=charlie+os+agent"
```
**Result:** `mafzalkalwardev/tony-ai-agent` — description explicitly mentions "Charlie OS"

### Creator Search (Charles Dove / @charlieautomates)
```bash
curl "https://api.github.com/users/doveccl/repos"
```
**Result:** AutoHam, click — unrelated

### Graphify + Hermes Integration
```bash
curl "https://api.github.com/search/repositories?q=graphify+hermes+agent"
```
**Result:** 0 direct results, but TONY agent has both integrated

### General Agentic OS Dashboard
```bash
curl "https://api.github.com/search/repositories?q=agentic+os+dashboard+claude"
```

---

## Known Open-Source Alternatives Table

| Proprietary Tool | Pattern Name | Open-Source Alternative | Repo | Notes |
|-----------------|--------------|------------------------|------|-------|
| Seed | Ideation interview → spec packaging | — | Not found | Still gatekept |
| Paul | Plan → Apply → Unify → Loop | **FORGE Framework** | `SanthoshVishnuRajamanickam/forge-framework` | 32 `/forge:*` commands, CLAUDE.md docs |
| Charlie OS | Runtime shell + dashboard | **TONY AI Agent** | `mafzalkalwardev/tony-ai-agent` | Full stack: Paul builder API, Graphify, Hermes, MCP, voice, JARVIS |
| Graphify + Hermes bridge | Code-graph + agent bridge | **TONY AI Agent** | `mafzalkalwardev/tony-ai-agent` | Built-in integration |

---

## Research Pitfall to Avoid

> **When a YouTube tutorial gates tools behind signup, search GitHub for the *pattern names* (PAUL, plan/apply/unify, Charlie OS) rather than the tool names.** The pattern is often implemented openly under a different name.

---

## Transcript Extraction (Reliable)

The `youtube-content` skill's `fetch_transcript.py` works well:
```bash
uv run python3 fetch_transcript.py "https://youtu.be/VIDEO_ID" --text-only --timestamps
```
Handles: timestamps, language selection, error cases (disabled transcripts, no transcript found).