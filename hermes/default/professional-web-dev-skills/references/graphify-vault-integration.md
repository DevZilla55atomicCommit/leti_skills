# Graphify Vault Integration Guide

## Overview
Integrates Obsidian vault's `graph.canvas` data into a 3D visualization using Next.js + React Three Fiber. Provides a class-level skill for professional web development with Hermes Agent and Claude Code.

## Key Components
- **GraphCanvas**: Main canvas component with loading/error states.
- **NodeField**: Renders ~200+ spheres colored by file extension.
- **LightningLinks**: Animated connections between nodes.
- **Legend**: Node type count display.
- **API Route**: `/api/vault/canvas` serves vault data.

## Workflow Steps
1. Parse `graph.canvas` JSON from vault.
2. Create API route to expose data.
3. Build React components for 3D visualization.
4. Implement camera controls (orbit/zoom/pan).
5. Add UI legend for node type distribution.
6. Toggle glow effect via UI.

## Pitfalls & Fixes
- **Duplicate variable declarations**: Renamed `geometry` → `particleGeometry` to avoid TypeScript redeclare errors.
- **Unused variables/imports**: Cleaned up `useFrame` duplicates and removed dead code.
- **Large JSON handling**: 900KB response caused browser fetch hangs; consider static import or chunking.
- **Build failures**: Cleaned unused imports; ensured TypeScript types correct.
- **Stale dependencies**: Ensured all linked skills are installed via `~/.claude/skills/`.

## User Preferences
- Nodes must be **colorful** by file type.
- **Disable glow** effect for now.
- Use **vault information** for node/sphere data.
- Build via **Claude Code** sub-agents, one at a time, with manual review after each step.

## Verification
- Run `npm run build` – should succeed with only ESLint warnings.
- Start dev server: `npm run dev` → http://localhost:3000.
- Verify `GraphCanvas` state: `{ isLoading: false, error: null, hasGraphData: true, hasLayoutData: true }`.

## References
- `references/frontend-ui-engineering.md`
- `references/test-driven-development.md`
- `references/modern-web-design.md`