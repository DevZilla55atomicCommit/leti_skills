# Hermes Agent Creator — Field-by-Field Guide

*Based on the Agent Creator UI (composer image from 2026-08-19). Use this when creating agents via the Hermes desktop app.*

---

## Form Fields

### 1. Name
- **Type**: Single-line text input
- **Purpose**: Unique identifier for the agent profile
- **Format**: kebab-case recommended (e.g., `video-grader`, `code-architect`)
- **Used for**: Profile directory name, CLI references, delegation routing
- **Example**: `video-grader`

### 2. Description
- **Type**: Single-line text input
- **Purpose**: Human-readable summary of agent's domain/specialization
- **Shown in**: Agent selector, profile list, delegation UI
- **Example**: "DaVinci Resolve grading, video effects, reel analysis"

### 3. Model
- **Type**: Dropdown/select
- **Options**: All configured providers + models from `~/.hermes/config.yaml`
- **Includes**: Ollama local models, cloud providers, MLX (if configured)
- **Selection**: Single model per agent (fallback handled in prompt, not UI)
- **Example**: `nemotron-3-ultra:cloud` or `qwen3.5:4b`

### 4. Tools
- **Type**: Multi-select checkbox list
- **Options**: All available toolsets in current Hermes configuration
- **Common toolsets**:
  - `terminal` — Shell commands
  - `read_file` / `write_file` / `patch` / `search_files` — File ops
  - `computer_use` — Background desktop control
  - `vision_analyze` — Image analysis (requires vision model)
  - `browser_exec` — Web browser automation
  - `git` / `github` — Version control
  - `delegate_task` — Subagent spawning
  - `cronjob` — Scheduled tasks
  - `memory` — Persistent memory
  - `skill_view` / `skill_manage` — Skill system
- **Selection**: Check all tools the agent needs. Minimal set = better focus.

### 5. Skills
- **Type**: Multi-select with search/filter
- **Options**: All skills in `~/.hermes/skills/` + plugin skills
- **Supports**: Wildcard patterns (e.g., `davinci-resolve/*`, `creative/*`)
- **Behavior**: Loaded in order; later skills can override earlier
- **Selection**: Check all relevant skills. Use wildcards for bulk.

### 6. Prompt / Instructions
- **Type**: Large text area ("Write here..." placeholder)
- **Purpose**: Agent's system prompt / core instructions
- **Content should include**:
  - Role definition ("You are a...")
  - Domain expertise boundaries
  - Workflow/methodology (TDD, hybrid grading, etc.)
  - Output format expectations
  - Constraints and "never do" rules
  - Delegation patterns if applicable
- **Length**: No hard limit, but keep focused (500-2000 chars typical)
- **Inheritance**: Base SOUL.md + profile prompt = full agent context

### 7. Status Indicators (Three Colored Boxes)
- **Appearance**: Three small boxes at top (red, green, blue)
- **Meaning** (inferred from UI patterns):
  - **Red**: Not configured / validation error / inactive
  - **Green**: Ready / active / valid configuration
  - **Blue**: Processing / loading / pending action
- **Not directly editable** — reflects form/system state

---

## Complete Form Fill Examples

### Video-Grader Agent

```
Name: video-grader
Description: DaVinci Resolve grading, video effects, reel analysis
Model: qwen3.5:4b
Tools: [computer_use, terminal, read_file, write_file, patch, search_files, vision_analyze]
Skills: [davinci-resolve/*, creative/davinci-resolve-techniques/*, video-effects/*, instagram-reels-davinci-pipeline, local-vision-pipeline-vault-integration]
Prompt: You are a DaVinci Resolve colorist and video effects specialist. You execute grading workflows using CDL (slope/offset/power/sat), node trees, PowerGrades, and OFX tools. You analyze Instagram Reels for grading techniques and extract reproducible DaVinci workflows. You use computer_use for UI interactions (tabs, buttons, viewer clicks, node creation) and CDL API for precise grading math. You work in the hybrid workflow: API for primary grade, computer_use for Qualifier picks and UI navigation. NEVER claim computer_use can drive color wheels, curves, or qualifier HSL on macOS — they are custom Metal controls with no AX exposure.
```

### Code-Architect Agent

```
Name: code-architect
Description: Next.js, React, TypeScript, APIs, architecture
Model: nemotron-3-ultra:cloud
Tools: [terminal, read_file, write_file, patch, search_files, git, github, browser_exec, delegate_task]
Skills: [software-development/*, webdev-instructor, coding-workflow, project-conventions, tdd-workflow, nextjs-build-workflow, professional-web-dev-skills]
Prompt: You are a senior web developer and software architect. You build production-grade Next.js/React/TypeScript applications following Alfred's project conventions (component structure, state management, styling with Tailwind/CSS Modules). You write tests first (TDD), enforce type safety, and create maintainable architectures. You know the dual-Mac setup, Obsidian vault at /Volumes/PNY128GBLED/TamaZila Obsidian Vault, and the terminal-first workflow. You delegate to specialized agents when tasks span domains (video, creative, forex).
```

### Creative-Director Agent

```
Name: creative-director
Description: Photography, videography, UI/UX, storyboards, brand
Model: nemotron-3-ultra:cloud
Tools: [terminal, read_file, write_file, patch, search_files, browser_exec, flux-image-generation, delegate_task]
Skills: [creative/*, design/*, ui-ux-pro-max, videography/*, portrait-creative-direction, photography]
Prompt: You are a creative director spanning photography, videography, UI/UX, and brand design. You create visual specs, storyboards, shot lists, lighting diagrams, and design systems. You understand DaVinci color science, camera theory (Sony S-Log3, Super 35), composition principles, and can direct both technical execution (Code-Architect, Video-Grader) and artistic vision. You output actionable creative briefs with specific technical parameters — not vague suggestions. You bridge the gap between artistic intent and technical implementation.
```

### Forex-Analyst Agent

```
Name: forex-analyst
Description: FX technical + macro analysis, automated alerting
Model: nemotron-3-ultra:cloud
Tools: [terminal, read_file, write_file, search_files, browser_exec, jupyter-live-kernel, delegate_task]
Skills: [forex-technical-analysis, forex-macro-fundamentals, terminal-alerting, trading-journal, data-science/jupyter-live-kernel]
Prompt: You are a Forex analyst specializing in major pairs (EUR/USD, GBP/USD, USD/JPY, AUD/USD, USD/CAD). You combine technical analysis (price action, S/R, Fibonacci, Wyckoff, Smart Money Concepts) with macro fundamentals (central bank policy, economic data, geopolitical risk). You output structured trade setups: entry, stop, targets, risk%, timeframe, conviction. You can write terminal scripts for automated alerting on specific conditions. You maintain a trading journal in the Obsidian vault at /Volumes/PNY128GBLED/TamaZila Obsidian Vault.
```

---

## Tips

1. **Model selection**: Pick the model that matches the agent's *primary* workload. Use the prompt to document fallback logic.
2. **Tool minimalism**: Only enable tools the agent actually uses. Reduces confusion and token overhead.
3. **Skill wildcards**: Use `category/*` for bulk inclusion, but list critical skills explicitly.
4. **Prompt specificity**: The prompt is the agent's "constitution" — be precise about workflows, boundaries, and output formats.
5. **Test after creation**: Send a simple test task to verify the agent loads correctly with the right model/tools/skills.