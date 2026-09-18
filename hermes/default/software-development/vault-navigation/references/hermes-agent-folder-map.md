# Hermes Agent Folder Structure Map

**Root Path:** `/Users/alfredkamisese/TamaZila Obsidian Vault/Hermes Agent`

This document maps the complete structure of the Hermes Agent folder with its Memory.md navigation files for each subdirectory.

---

## Top-Level Structure

```
/Users/alfredkamisese/TamaZila Obsidian Vault/Hermes Agent/
├── .hermes/                          # Hermes config (empty subfolder)
├── Claude Code/                      # (empty)
├── DaVinci_Knowledge_Base/           # Color grading & DaVinci Resolve knowledge
├── Developer Workflows/              # Web dev, Python automation, motion design
├── Forex Center/                     # Forex trading strategies & automation
├── Hermes Course/                    # (empty)
├── Hermes Image Generates/           # Flux/Storyboard image generation scripts
├── Hermes Memory/                    # Core Hermes Agent instructions & user profile
├── Hermes Sessions/                  # (empty)
├── MaddieMyAPI/                      # MyApi architecture study & build plan
├── Photography/                      # Portrait photography reference library
├── Projects/                         # Active projects (model assignments, video assets)
├── Security Audit Master Index.md    # Security audit index
├── Technical_Navigation_Master.md    # DaVinci SOP navigation
├── standing_orders.md                # Daily ritual protocols (Morning/Evening)
└── mnemo-cortex/                     # Mnemo Cortex protocol files
```

---

## Subfolder Memory Maps

### 1. `DaVinci_Knowledge_Base/Memories.md`
**Core Workflows:**
- Proper Balancing → `/DaVinci Resolve 20/Proper Balancing.md`
- Editing Architecture → `/DaVinci Resolve 20/Reviewing vs Grading.md`
- LUT & Technique → `/DaVinci Resolve 20/LUT_and_Technical_Accuracy.md`

**Categories:**
- Color Grading: `/DaVinci Resolve 20/` (manuals & guides)
- Advanced Technicals: `/DaVinci Resolve 20/` (exposure, lenses, pro workflows)
- Archives: `/DaVinci Resolve 20/davinci_guide_part_*` (129 raw manual segments)

**Versioning:**
- Resolve 20 Series: `/DaVinci Resolve 20/`
- Latest Features (v21): `/DaVinci Resolve 21/`

### 2. `Developer Workflows/Memory.md`
**Directory Overview:**
- NextJS/: `Best_Practices.md`
- Styling_Tailwind/: `Best_Practices.md`, `Advanced_Design.md`
- Interactive_Motion/: 6 scroll/GSAP guides (01-06)
- Python_Automation/: `Foundations.md`, `Scripts/media_processor.py`, `Scripts/market_tracker.py`
- State_Management/: `Architecture_Best_Practices.md`
- API_Design/: `Standards.md`
- HTML5_Basics/: `Foundations.md`

### 3. `Forex Center/Memory.md`
**Directory Overview:**
- Market_Dynamics/: Macro-economic correlations
- Technical_Indicators/: RSI, MACD, EMA math & signal timing
- Automated_Strategy/: Scripts, alerts, Python signal tracking
- Trading_Logics/: Execution protocols, risk management, win conditions

**Active Research:** Macro/Technical correlation, indicator maps, alert logic
**Core Compliance:** Risk limits (max drawdown, fixed % sizing), watchlist with triggers

### 4. `Hermes Memory/MEMORY.md` — **CORE AGENT INSTRUCTIONS**
Contains the memorized cross-session instructions:
- Response guidelines for complex research
- Time-sensitive data handling protocol
- Error handling approach (pause on binary/complex format failures)
- Active task persistence protocol (write to `active-task.md`)
- Deliverable quality standards (high technical depth, cinematic workflows)
- Process automation priority (formalize into Skills immediately)
- User identity: Alfred, Agent Persona: **Maddie**, ZIP: 94303

### 5. `MaddieMyAPI/index.md` + `IMPLEMENTATION_PLAN.md`
**MyApi Architecture Study** — Unified OAuth data gateway for AI agents
- Core concept: Service Proxy Pattern + Zero-Trust Auth (Ed25519 ASC tokens) + 30-day approval queue + append-only audit log
- Services: 18+ (GitHub, Google, Slack, Discord, LinkedIn, Stripe, fal.io, Home Assistant, etc.)
- Build plan: 8 phases over ~8 weeks (Foundations → Core Gateway → OAuth Services → Approval System → Deployment)
- Project structure template provided (FastAPI/Express, MongoDB/PostgreSQL, Redis, Ed25519)

### 6. `Photography/Memory.md`
**Resources:**
- Portrait Analysis: `Creative_Director_Communication_Mastery.md`, `Lens_Dynamics_Comparison.md`, `Sony_Eye_AF_Mastery.md`, `Depth_of_Field_Mastery.md`, `Mood_and_Styling_Techniques.md`, `Body_Dynamics.md`
- Historical Foundations: `Best_Sony_Portrait_Settings.md`, `Portrait_Scene_Guide.md`
- Light Management: `Natural_Light_Manipulation.md`

**Learning Pillars:** Fundamentals → Technical Mastery → Post-Processing → Creative Style

### 7. `Hermes Image Generates/`
- `Using-Flux-models-with-Hermes-Agent.py` — MCP server for Ollama Flux2-Klein (512x512, 4 steps)
- `storyboard_agent.py` — OpenAI-compatible client for Draw Things API (storyboard frames via tool calling)

### 8. `Projects/`
- `Hermes_Model_Assignments.md` — Model-to-profile mapping across 4 workflows (Deep Research, Storyboard, Web Dev, Colorist) for 4 profiles (Default, Builder, Reviewer, Auditor)
- `input_reel.MP4` — 13.9MB video asset

### 9. `mnemo-cortex/`
- `01-Core_Protocol_Overrides.md`
- `Architecture_Summary.md`
- `Mnemo_Usage_BestPractices.md`
- `mnemo-cortex_skill_guide.md`

### 10. Root-Level Navigation Files
- `Technical_Navigation_Master.md` — DaVinci SOP (3-layer architecture: Conforming → Creative → Collaboration)
- `standing_orders.md` — **MANDATORY** Daily Briefing (Morning) + Evening Check-Out protocols
- `Security Audit Master Index.md` — Security audit index

---

## Key Navigation Patterns

| Task | Entry Point |
|------|-------------|
| DaVinci color grading workflow | `DaVinci_Knowledge_Base/Memories.md` → Core Workflows |
| Web dev best practices | `Developer Workflows/Memory.md` → Directory Overview |
| Forex strategy/automation | `Forex Center/Memory.md` → Directory Overview |
| Hermes agent config/rules | `Hermes Memory/MEMORY.md` |
| MyApi build plan | `MaddieMyAPI/IMPLEMENTATION_PLAN.md` |
| Portrait photography refs | `Photography/Memory.md` → Resources |
| Storyboard/image gen | `Hermes Image Generates/storyboard_agent.py` |
| Model selection for workflow | `Projects/Hermes_Model_Assignments.md` |
| Daily ritual protocol | `standing_orders.md` |

---

## Maintenance Notes

- Each subfolder has its own `Memory.md` acting as a local map
- Root-level `Technical_Navigation_Master.md` and `standing_orders.md` are cross-cutting
- `Hermes Memory/MEMORY.md` contains the agent's standing instructions (memorized)
- Empty folders: `Claude Code/`, `Hermes Course/`, `Hermes Sessions/`, `.hermes/TamaZila Obsidian Vault/`

*Generated from vault scan on 2025-07-05*