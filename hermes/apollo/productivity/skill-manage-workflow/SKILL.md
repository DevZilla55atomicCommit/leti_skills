---
name: skill-manage-workflow
description: "Create and update Hermes skills via skill_manage correctly."
version: 1.0.0
author: Apollo (Hermes Agent)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Skills, Curation, Workflow]
    related_skills: []
---

# skill_manage Workflow

## When to Use

Use whenever creating or patching skills through `skill_manage` — single creates, bulk creates, or skill updates.

## Procedure

1. Draft every `description` FIRST, at or under 60 chars, one sentence ending with a period, trigger-first (e.g. `Process DaVinci Resolve version videos into vault notes.`). Count characters before sending.
2. Batch independent creates into ONE `operations` array — one entry per skill. The batch applies atomically.
3. For bulk support-file creation (10+ files: tags, collections, notes), use ONE `execute_code` python loop writing files directly instead of N `write_file`/`skill_manage` calls — one round-trip instead of dozens.
4. Before patching an existing skill's SKILL.md, call `skill_view(name)` fresh in the same review; before overwriting an existing support file, `skill_view(name, file_path=...)` for that exact file.
5. After any batch, verify with one read-back (list dir or read index) before claiming success.

## Pitfalls

- Keep `description` under the 60-char budget or the ENTIRE batch rolls back — one long description destroys every sibling op, so a 61-char string costs the whole batch, not just itself.
- Shorten the description, never the skill name, when hitting the budget — the name is the routing key and must stay descriptive.
- Prefer extending one class-level umbrella skill over spawning a narrow skill per item in a batch ingest — 25 tools become 25 unmaintainable one-session skills that violate the class-level library shape.
- Never retry a refused write with identical arguments more than once — change the description length, the target, or the strategy instead of looping.
- Do not patch user-owned skills (refusal names `created_by=None`); recommend `hermes curator adopt <name>` in the reply and stop.
