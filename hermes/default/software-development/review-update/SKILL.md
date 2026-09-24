---
name: review-update
title: Review and Update Memory & Skills
description: Process for auditing Hermes conversations, extracting durable user preferences, and maintaining the class-level skill library. Captures how to identify persistent user traits, save them via the memory tool, detect skill gaps (style corrections, missing steps, outdated patterns), and apply updates via skill_manage (patch, create, or reference files). Emphasizes preferring patches to existing umbrella skills, adding reference files for session‑specific detail, and only creating new umbrella skills when no existing skill covers the learning.
tags: [metadata, skill-management, memory, review]
owner: alfredkamisese
version: 1.0
status: active
---

# Review & Update Process

## 1. Memory Update
- **Detect signals**: user reveals persona, preferences, frustrations, explicit “I want X” statements, repeated corrections, or style complaints.
- **Consolidate**: If a memory entry already exists, use `memory(action='replace', ...)` to merge the new fact, keeping it concise (≤ ~300 chars). If no entry exists, `memory(action='add', ...)` is fine.
- **Prioritize**: Preference > correction > permanent fact. Discard transient errors or session‑specific details (they belong in references, not core memory).

## 2. Skill Gap Detection
- **Style/format corrections** → update the skill that governs that output (e.g., “don’t use bullet points, use plain paragraphs”).
- **Missing verification steps** → patch the skill with a “Verification” section.
- **Outdated commands** → patch the skill with the new command path.
- **New class of work** → if no loaded skill covers it, locate the appropriate umbrella skill (via `skills_list`) or create a new class‑level skill.

## 3. Skill Update Workflow
1. **Load the target skill**: `skill_view(name='<skill>')`.
2. **Identify the gap**: note what’s missing or wrong.
3. **Patch**: use `skill_manage(action='patch', ...)` for small fixes; supply `old_string`/`new_string` or a `patch` block.
4. **Create/Replace**: for major overhauls, `skill_manage(action='edit')` with full new `SKILL.md`.
5. **Add reference files**: for session‑specific details, add files under `references/` and link them from the skill’s `SKILL.md` (e.g., `[[references/faq.md]]`).
6. **Verify**: re‑load the skill (`skill_view`) to confirm the changes load correctly.

## 4. Reference Files
- Store per‑session details (e.g., “user prefers concise responses”, “current project is X”) in `references/<topic>.md`.
- Link them from the skill’s frontmatter or body so future runs can rediscover the nuance without bloating memory.

## 5. Umbrella Skill Creation (last resort)
- When the learning spans multiple existing umbrellas, create a new class‑level skill in a suitable category (e.g., `software-development`, `configuration`).
- Follow the naming convention: lowercase, hyphens, max 64 chars.
- Include frontmatter with `name`, `title`, `description`, `tags`, `owner`, `version`, `status`.
- Add a `references/` folder for any session‑specific notes.

## 6. Checklist Before Saving
- [ ] Memory entry is concise and durable.
- [ ] Skill patch preserves existing structure and adds only the needed change.
- [ ] New skill’s frontmatter follows the required schema (name, title, description, tags, owner, version, status).
- [ ] Reference files are placed under `references/` and linked correctly.
- [ ] All changes are tested by re‑loading the skill (`skill_view`) to ensure no syntax errors.

---  
*When in doubt, prefer patching an existing umbrella skill over creating a new one. This keeps the library cohesive and avoids proliferation of redundant abstractions.*