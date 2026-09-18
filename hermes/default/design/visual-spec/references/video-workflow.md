# Video Workflow for AI‑Generated Design Systems

## Overview
The workflow demonstrated in the YouTube video (https://youtu.be/wJWO91mi5o0) outlines how to use Claude + Higgsfield to generate brand identities, design system tokens, and motion‑graphics asset packs in five systematic steps.

## 5‑Step Methodology

1. **Stop AI Slop Forever** – Define a strict quality gate (e.g., “no auto‑generated filler”).
2. **The Five‑Step System** – Map out each stage: concept, token generation, token validation, asset export, integration.
3. **Level 1 – Design System Created** – Produce the foundational design tokens (color palette, typography scale, spacing system) using AI.
4. **Design System Created** – Expand tokens into a full component inventory (buttons, cards, icons) and generate animation specifications.
5. **Higgsfield Skill Unlocked / Claude Builds Your Brand** – Apply motion‑graphics/AI‑animation tools (Higgsfield, ElevenLabs audio) to produce final brand assets and full asset packs.

## Integration with `visual-spec`

- **Trigger**: Use this workflow when you need to **auto‑generate** a design system for a new project (e.g., Kasini Tree) rather than manually author tokens.
- **Pitfall**: The video only claims “animation specifications” – you must explicitly define the animation tokens (easing curves, keyframe timing) in the generated output.
- **Verification**: After generation, run the `visual-spec` skill’s **component inventory** checklist to confirm all required tokens are present.

## Support Files
- `visual-spec-overview.md` – High‑level feature list.
- `video-workflow.md` – This document.

### Using the workflow
1. Pause the video at each chapter marker.
2. Extract the step’s action items.
3. Translate each item into a concrete task in your project (e.g., “Generate color palette with AI”).
4. Execute the task using Claude/Higgsfield APIs.
5. Validate output against the `visual-spec` inventory before promoting to production.