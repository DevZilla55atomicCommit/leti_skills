# Real-World Profile Examples — Greek God Personas

Reference for `hermes-multi-agent-orchestration` skill. These are actual profiles created by the user (Alfred) demonstrating custom persona-driven specialization.

---

## Profile Roster

| Profile | Archetype | Domain | Model | Alias |
|---------|-----------|--------|-------|-------|
| `default` | Maddie | Orchestrator / Systems Engineer | NVIDIA Nemotron-3-Ultra | — |
| `apollo` | Apollo | Creative Director (Photo/Video/UI/Brand) | NVIDIA Nemotron-3-Ultra | `apollo` |
| `helios` | Helios | DaVinci Resolve Colorist | NVIDIA Nemotron-3-Ultra | `helios` |
| `hephaestus` | Hephaestus | Code Architect / Web Dev (ECC) | NVIDIA Nemotron-3-Ultra | `hephaestus` |
| `hestia` | Hestia | Personal Assistant / Ops / Life Admin | NVIDIA Nemotron-3-Ultra | `hestia` |
| `kairos` | Kairos | Forex Analyst / Trader | NVIDIA Nemotron-3-Ultra | `kairos` |

> **Note:** All 6 profiles now use NVIDIA Nemotron-3-Ultra (including `default` and `hestia` — updated from local Ollama to cloud NVIDIA for consistency). All share the same provider config with API key in `.env`.

---

## Key Patterns Demonstrated

### 1. Persona-Driven SOUL.md
Each profile has a custom `SOUL.md` that defines its **identity, mission, tone, and scope** — not just tool config. This makes the agent's behavior consistent and predictable across sessions.

**Example (apollo):**
```
You are Apollo, Olympian god of light, arts, prophecy, and the Muses — leader of the nine Muses on Mount Helicon, oracle at Delphi, archer who sees the target before the arrow flies. You are a creative director spanning photography, videography, UI/UX, and brand design. You create visual specs, storyboards, shot lists, lighting diagrams, and design systems. You understand DaVinci color science, camera theory (Sony S-Log3, Super 35), composition principles, and can direct both technical execution (Hephaestus, Helios) and artistic vision. You output actionable creative briefs, not vague suggestions. Your vision is prophetic; your direction is precise.
```

### 2. Cross-Profile Delegation
Profiles explicitly reference each other in their SOUL.md:
- Apollo directs Helios (color) and Hephaestus (code)
- Hestia helps Default when needed
- This creates a **hierarchy of delegation** the orchestrator can leverage

### 3. Model Specialization
- **NVIDIA API models** for reasoning-heavy roles (Creative Director, Colorist, Code Architect, Forex, Orchestrator)
- **Local Ollama** for privacy/ops-heavy role (Personal Assistant — hestia uses qwen3.5:4b)
- All profiles share the same 2281 skills but different models suit different workloads

### 4. Alias System
Each profile has a shell alias (`apollo`, `helios`, `hephaestus`, `hestia`, `kairos`) pointing to `hermes -p <profile>`, enabling direct invocation from terminal:
```bash
apollo "Create a storyboard for the product launch"
helios "Extract grading technique from this Reel URL"
hephaestus "Refactor the auth module to use JWT"
kairos "Analyze EUR/USD for tomorrow's NY session"
hestia "Schedule follow-up with client and draft email"
```

### 5. Isolated State Per Profile
Each profile maintains:
- Own `config.yaml` (model, providers, toolsets)
- Own `.env` (API keys, secrets)
- Own `skills/` (2281 skills each — full copy)
- Own `memories/` (MEMORY.md, USER.md, SOUL.md)
- Own `sessions/` (conversation history)
- Own `cron/` (scheduled jobs)
- Own `logs/`

---

## SOUL.md Excerpts for Reference

### apollo (Creative Director)
> Olympian god of light, arts, prophecy, and the Muses... creative director spanning photography, videography, UI/UX, and brand design. Creates visual specs, storyboards, shot lists, lighting diagrams, design systems. Understands DaVinci color science, camera theory (Sony S-Log3, Super 35), composition principles. Directs technical execution (Hephaestus, Helios) and artistic vision. Outputs actionable creative briefs.

### helios (DaVinci Colorist)
> Titan of the Sun — master of light, color, and the visible spectrum. Executes DaVinci Resolve grading workflows using CDL (slope/offset/power/sat), node trees, PowerGrades, OFX tools. Analyzes Instagram Reels for grading techniques and extracts reproducible DaVinci workflows. Hybrid workflow: API for primary grade, computer_use for Qualifier picks and UI navigation.

### hephaestus (Code Architect)
> Code Architect, Senior web developer and software architect. Builds Next.js apps, React components, TypeScript systems, APIs. Enforces project conventions, TDD, clean architecture. Named for the divine forge-god — builder of systems, craftsman of code. Has full ECC suite (67 subagents, 281 skills, 94 commands).

### hestia (Personal Assistant)
> Goddess of the hearth — the house runs smoothly. Email (apple-mail, himalaya), Calendar & Reminders, Apple Notes, Documents (PowerPoint, Word, Excel, PDF, OCR), Come Follow Me (LDS), Weekly planning, X/Twitter, Session management. Native macOS automation first (osascript, remindctl, memo). Helps Default when needed.

### kairos (Forex Analyst)
> Personification of the opportune moment — the critical, fleeting instant when action must be taken. Forex analyst specializing in major pairs (EUR/USD, GBP/USD, USD/JPY, AUD/USD, USD/CAD). Combines technical analysis (price action, S/R, Fibonacci, Wyckoff, Smart Money Concepts) with macro fundamentals (central bank policy, economic data, geopolitical risk). Outputs structured trade setups: entry, stop, targets, risk%, timeframe, conviction. Writes terminal scripts for automated alerting. Maintains trading journal in Obsidian vault.

---

## Orchestration Implications

1. **Orchestrator (default/Maddie) knows each agent's specialty** — can route tasks by domain
2. **Personas are stable across sessions** — SOUL.md persists, no re-prompting needed
3. **Aliases enable quick terminal delegation** — no menu navigation
4. **Model choice matches workload** — local for privacy/ops, cloud for reasoning
5. **Cross-references in SOUL.md create implicit delegation graph** — Apollo → Helios/Hephaestus, Hestia → Default

---

## Creating Similar Profiles

```bash
# Clone default to get skills, config, memories
hermes profile create apollo --clone --description "Creative Director — photography, videography, UI/UX, brand design"

# Set model
hermes -p apollo config set model.default "nvidia/nemotron-3-ultra-550b-a55b"
hermes -p apollo config set model.provider "nvidia"

# Write custom SOUL.md
cat > ~/.hermes/profiles/apollo/SOUL.md << 'EOF'
You are Apollo... [persona definition]
EOF

# Create alias (auto-generated by hermes profile create)
# alias apollo="hermes -p apollo"
```