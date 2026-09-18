---
name: multi-model-agent-routing
description: Route tasks to best model in multi-model AI by intent.
category: automation
tags: [routing, model-selection, ollama, mlx, cloud, agent-squad]
---

# Multi-Model Agent Routing Skill

## Purpose

Design and implement routing logic that directs each task to the optimal model in a heterogeneous local AI environment. Covers model capability assessment, task-to-model matching, agent squad design, and routing implementation patterns.

## When to Use

- Setting up a new multi-model environment (Ollama + cloud + MLX)
- Designing specialized agent squads where each agent uses a different model
- Creating routing rules for kanban/orchestration systems
- Documenting model capability matrices for a specific hardware setup
- Troubleshooting why a task went to the wrong model

## Core Concepts

### Model Capability Dimensions

| Dimension | What It Affects | Assessment Method |
|-----------|-----------------|-------------------|
| **Tool Calling** | Can the model use functions/tools natively? | Test with Hermes tool calls |
| **Reasoning Depth** | Complex multi-step analysis, architecture | Benchmark on coding/reasoning tasks |
| **Context Window** | Max tokens for input+output | Provider docs + empirical test |
| **Speed (tok/s)** | Iteration velocity for coding/creative tasks | `ollama run` timing or MLX benchmarks |
| **Memory Footprint** | RAM/VRAM required, affects concurrent runs | `ollama list` + `htop`/`nvidia-smi` |
| **Specialization** | Code, vision, creative, analysis, chat | Task-specific evals |

### Routing Principles

1. **Tool-dependent tasks → Tool-capable models** (Ollama with native tool calling, cloud APIs)
2. **Speed-critical iteration → Fast local models** (quantized MLX, small Ollama models)
3. **Deep reasoning/architecture → High-capability models** (large cloud, 70B+ local)
4. **Vision/multimodal → Vision models** (llava, qwen-vl, gpt-4v)
5. **Cost-sensitive high-volume → Local models** (avoid cloud token costs)

## Task-to-Model Mapping Template

```markdown
## Model Capability Matrix (Session-Specific)

| Model | Provider | Tool Calling | Context | Speed | Best For |
|-------|----------|--------------|---------|-------|----------|
| nemotron-3-ultra:cloud | NVIDIA Cloud | ✅ | Large | Med | Architecture, creative, analysis |
| gpt-oss:120b-cloud | Cloud | ✅ | Very Large | Med | Code gen, long-context, reasoning |
| qwen3.5:4b | Ollama Local | ✅ | 32K | **Fast** | Quick edits, grading, local-first |
| llava:7b | Ollama Local | ❌ | 4K | Med | Vision: frame analysis, storyboards |
| qwen3.5-32k:latest | Ollama Local | ✅ | 32K | Med | Long-context code/docs review |
| gemma4:12b | Ollama Local | ✅ | 8K | Med | Balanced general purpose |
```

## Agent Squad Design Pattern

### Specialization Axes

1. **Domain Specialization** - Each agent owns a knowledge domain (video, code, creative, forex)
2. **Model Specialization** - Each agent uses the model optimal for its domain's workload
3. **Tool Specialization** - Each agent gets only the tools its domain needs
4. **Skill Inheritance** - Agents inherit relevant skill subsets from the parent profile

### Squad Template

```yaml
agents:
  - name: video-grader
    domain: "DaVinci Resolve grading, video effects, reel analysis"
    model: "qwen3.5:4b (local) / nemotron-3-ultra:cloud (complex)"
    tools: [computer_use, terminal, read_file, write_file, patch, search_files, vision_analyze]
    skills: [davinci-resolve/*, creative/davinci-resolve-techniques/*, video-effects/*, instagram-reels-davinci-pipeline, local-vision-pipeline-vault-integration]
    prompt_focus: "Hybrid workflow: CDL API for primary grade, computer_use for UI (tabs, buttons, viewer, nodes)"

  - name: code-architect
    domain: "Next.js, React, TypeScript, APIs, architecture"
    model: "nemotron-3-ultra:cloud / gpt-oss:120b-cloud"
    tools: [terminal, read_file, write_file, patch, search_files, git, github, browser_exec]
    skills: [software-development/*, webdev-instructor, coding-workflow, project-conventions, tdd-workflow, nextjs-build-workflow]
    prompt_focus: "TDD, clean architecture, Alfred's project conventions, terminal-first"

  - name: creative-director
    domain: "Photography, videography, UI/UX, storyboards, brand"
    model: "nemotron-3-ultra:cloud"
    tools: [terminal, read_file, write_file, patch, search_files, browser_exec, flux-image-generation]
    skills: [creative/*, design/*, ui-ux-pro-max, videography/*, portrait-creative-direction]
    prompt_focus: "Actionable creative briefs, not vague suggestions. Bridge technical + artistic."

  - name: forex-analyst
    domain: "FX technical + macro analysis, automated alerting"
    model: "nemotron-3-ultra:cloud"
    tools: [terminal, read_file, write_file, search_files, browser_exec, jupyter-live-kernel]
    skills: [forex-technical-analysis, forex-macro-fundamentals, terminal-alerting, trading-journal]
    prompt_focus: "Structured trade setups: entry, stop, targets, risk%, timeframe, conviction"
```

## Hybrid Workflow Patterns

### DaVinci Resolve: API + computer_use

| Operation | Method | Why |
|-----------|--------|-----|
| Primary grade (CDL: slope/offset/power/sat) | API / DCTL / script | Precise, repeatable, scriptable |
| Node creation/connection | computer_use | UI-only operations |
| Tab switching (Color/Edit/Fairlight) | computer_use | AX-exposed controls |
| Viewer clicks (qualifier pick, power window) | computer_use | Custom Metal controls not scriptable |
| Version navigation | computer_use | UI state management |
| Render queue | API | Scriptable, batchable |
| Gallery stills | API | Scriptable |

**Rule**: Never claim computer_use can drive color wheels, curves, or qualifier HSL on macOS — they are custom Metal controls with no AX exposure.

## Implementation in Hermes

### Agent Creator Form Fields

| Form Field | Content Source |
|------------|----------------|
| Name | `agents[].name` |
| Description | `agents[].domain` |
| Model | `agents[].model` |
| Tools | `agents[].tools` (multi-select) |
| Skills | `agents[].skills` (multi-select, supports wildcards) |
| Prompt/Instructions | `agents[].prompt_focus` + domain-specific instructions |

### Delegation Patterns

```python
# Parallel delegation for independent domains
delegate_task(tasks=[
    {"goal": "Grade clip C001 with teal-orange look", "context": "...", "role": "leaf"},  # → video-grader
    {"goal": "Build Next.js component for video gallery", "context": "...", "role": "leaf"},  # → code-architect
    {"goal": "Create storyboard for product launch video", "context": "...", "role": "leaf"},  # → creative-director
])

# Sequential for dependent work
# 1. creative-director outputs creative brief
# 2. code-architect builds delivery tool
# 3. video-grader grades assets
# 4. code-architect integrates graded assets
```

## Reference Files

- `references/model-capability-matrix.md` — Current session's model matrix with empirical notes
- `references/agent-squad-template.yaml` — Reusable squad definition template
- `references/hermes-agent-creator-fields.md` — Field-by-field guide for the Agent Creator UI
- `references/hybrid-davinci-workflow.md` — Detailed API vs computer_use boundary decisions

## Updating This Skill

When the model lineup changes:
1. Update the Model Capability Matrix in `references/model-capability-matrix.md`
2. Adjust agent squad model assignments in `references/agent-squad-template.yaml`
3. Add new models to the routing principles table if they introduce new capability classes

When a new agent specialization is added:
1. Add to the Squad Template section
2. Document its tool/skill/prompt profile
3. Note any delegation patterns it participates in