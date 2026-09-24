---
name: user-profile-management
title: User Profile Management
description: How to capture and store user preferences, persona, and durable facts for persistent memory in Hermes Agent.
authors: [maddie]
created: 2026-07-12
---

# User Profile Management

## Purpose
Persist user-specific preferences, professional details, communication style, and workflow expectations so future sessions automatically apply the right tone, depth, and format.

## Scope
- User identity (name, role, location, contact)
- Preferences (tone, verbosity, format, focus areas)
- Technical context (tools, environment, constraints)
- Recurring tasks (e.g., 'always provide folder structure')
- Cultural or language rules (e.g., 'English only core')

## Workflow
1. **Gather** user statements about who they are and what they want.
2. **Condense** into short, declarative facts.
3. **Add** to memory target `user` using `memory(action='add', content='…', target='user')`.
4. **Verify** by retrieving memory and confirming key facts.
5. **Document** the process in this skill for reuse.

## Example Entry
> Alfred: web developer, photographer/videographer, creative director, FX analyst, AI learner. Dual Macs: mini "Leti" and M2 Pro 16 GB; BenQ P3 calibrated (Display P3). Prefers concise technical answers, visual artifacts over prose, verification before deletions, no filler. Persona: Maddie. Values: precision, correctness, root‑cause analysis, visual verification, clarity.

## Best Practices
- Keep entries under 200 characters to stay within memory limits.
- Use present tense, declarative sentences.
- Prioritize preferences that affect output style or task approach.
- Update when the user revises preferences or corrects you.
- Never store temporary task state or iterative workflow steps.

## Linked Files
- `references/user-profile-template.md` – template for new entries
- `scripts/verify-user-profile.js` – CLI check for profile completeness