---
name: local-model-orchestration
description: "Use when Claude Code runs on local Ollama models."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [Ollama, Claude-Code, Local-Models, Orchestration, tmux]
    related_skills: [claude-code]
---

# Local-Model Orchestration

Procedures that differ when Claude Code's backend is a local Ollama model
(`ANTHROPIC_BASE_URL=http://localhost:11434`) rather than api.anthropic.com.
Base tmux orchestration, dialogs (except where noted below), and print-vs-interactive
mode selection live in the `claude-code` skill — this skill carries only the local delta.

## 1. Cold-start discipline (always)

A cold local session shows minutes of spinner with zero tool calls and 0% context
while it loads multi-GB weights to GPU and prefills the first turn over the full
skill stack. This is indistinguishable from a dead loop — so never diagnose a stall
until warmup is excluded: wait out the first turn (5+ minutes on 9B-class models),
then judge by tool calls issued, not by spinner time.

## 2. Settings trio parity check (when context dies early)

Symptom: Claude reports a context limit at a fraction of the loaded model's real
window. Cause: the settings accounting trio drifts from the model (e.g. after a
partial model switch that flips the `model` field but not the numbers).

```
python3 -c "import json;e=json.load(open('$HOME/.claude/settings.json'))['env'];print({k:e.get(k) for k in ['OLLAMA_CONTEXT_LENGTH','CLAUDE_CODE_MAX_CONTEXT_TOKENS','CLAUDE_CODE_AUTO_COMPACT_WINDOW']})"
ollama ps   # CONTEXT column is the live loaded value — the trio must equal it
ollama show <model>  # num_ctx is the source of truth when ps is ambiguous
```

Fix with the model switcher (it rewrites the trio atomically and backs up
settings), never by hand-editing one key: `bash ~/.claude/claude-qwen.sh <profile> --no-launch`.
New sessions pick settings up; running sessions keep the old values — always start
a fresh session after a settings change.

## 3. Direction-file protection (when a small model builds from docs)

Small local models 'helpfully' rewrite spec/design direction files with generic
defaults (observed: design tokens replaced with stock indigo/violet, status tables
rebuilt looser, architecture doc deleted). Defend before handing over the project:

1. Declare direction files READ-ONLY in project `CLAUDE.md` and in every step
   prompt/command (only status/changelog files may be updated).
2. Commit the direction baseline first, so any overwrite shows as a revertible diff.
3. Verify with `grep` for unique markers (exact hex tokens, font names) after the
   first agent turn — restores are byte-identical rewrites, not merges.

## 4. v2.1.x dialog correction

The workspace-trust dialog starts its cursor on "No, exit" — pressing Enter quits.
Send Down, verify the cursor moved via `capture-pane`, then Enter. (The bundled
`claude-code` skill text still describes the old default-Yes layout.)
