---
name: claude-app-build-routing
description: "Route Claude-app builds between coder and reviewer models."
version: 1.0.0
author: Apollo (Hermes Agent)
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [Claude-Desktop, Code-Sessions, Ollama, Model-Routing]
    related_skills: []
---

# Claude App (Desktop) Code Build Routing

## When to use

Use when architecting any coding project Alfred will build inside the Claude Desktop app's Code feature. "Claude app (Claude Code)" ALWAYS means the Desktop app — never the CLI.

## The split

- **Writer:** `qwen2.5-coder:7b` (7.6B, 4.7GB Q4_K_M, 32K ctx, text-only, FIM-capable). Strong single-function generation (88.4% HumanEval, 83.5% MBPP), 92 languages. Give it tight tickets, never whole-repo architecture.
- **Reviewer:** `qwen3.5-96k:latest` (9.7B, 6.6GB Q4_K_M, 96K ctx, thinking + tools). Read-heavy audits, full file + diff + spec in context at once.
- Never substitute `:14b`/`:32b` coder tags — they exceed 16GB with the reviewer workflow.

## Phase plan (write into every project spec)

1. **BUILD** — Code session on `qwen2.5-coder:7b`. Small milestones, one file or function per task.
2. **GATE** — human runs `ollama stop qwen2.5-coder:7b` before review. Non-negotiable: Ollama's ~5min keepalive otherwise stacks both models (~13GB) and swap-thrashes the 16GB host.
3. **REVIEW** — new/fresh session on `qwen3.5-96k:latest`. Audit, multi-file check, conventions, tests.

## Hard constraints

- Sequential only: one local model loaded at a time (writer 5.5GB loaded, reviewer 7.5GB loaded; macOS reserve ~3.5GB of 16GB).
- Desktop model selection is manual per session — project text cannot switch backends. The human owns the GATE step.
- No subagents exist in the Desktop app yet; do not reference CLI agents (@Avengers, @Cap, etc.) in Desktop project docs.
- CLI pairing (`claude-qwen coder7b` / `claude-qwen 96k` + OOM guard) is parked for terminal use only.
- Verify load with `ollama ps` when unsure which model is resident.
