---
name: open-design-integration
description: Use Open Design with Hermes for prototypes, decks, video.
category: creative
tags: [open-design, design-systems, mcp, hermes-agent, prototyping, hyperframes, design-templates, plugins]
license: MIT
---

# Open Design Integration Skill

## Overview

**Open Design (OD)** is an open-source, agent-native design workspace — the "Claude Design alternative" — that runs locally on macOS/Windows/Linux and plugs directly into **Hermes Agent** (and 24 other CLIs). It provides:

- **151 brand-grade design systems** (Linear, Vercel, Stripe, Apple, Figma, Notion, Tesla, Nvidia, etc.) centered on `DESIGN.md` + `tokens.css`
- **100+ functional skills** (briefs, audits, asset packagers, Figma→React migration, code migration)
- **277 plugins** (scenarios, image/video templates, design-system wrappers, UI atoms)
- **Design templates** for prototypes (web/mobile/desktop), decks (15×36 themes), live dashboards, images, video (HyperFrames), audio
- **Artifact types**: HTML prototypes, live dashboards, decks (HTML/PDF/PPTX/MP4), images, video (HyperFrames + Seedance/Veo/Kling/Sora), audio

## When to Use

- Generating production-grade prototypes that read your `DESIGN.md` tokens
- Creating pitch decks, marketing pages, dashboards, mobile onboarding flows
- Producing motion graphics (HyperFrames: HTML+CSS+GSAP → deterministic MP4)
- Migrating Figma/Pencil workflows to React/Next.js/Vue
- Refreshing an existing codebase to a brand spec via `DESIGN.md`
- Generating brand-grade images/video for creative direction

## Installation

### 1. Install the `od` CLI

```bash
# macOS (Apple Silicon + Intel)
brew install nexu-io/tap/open-design
# Or download DMG from https://open-design.ai

# Verify
od --version
```

> **macOS PATH conflict**: `/usr/bin/od` (octal dump) shadows the OD CLI. Ensure `/opt/homebrew/bin` precedes `/usr/bin` in PATH, or use the absolute path from the desktop app's Settings → MCP Server snippet.

### 2. Wire into Hermes Agent (MCP server)

```bash
# One-liner — registers the OD MCP server in Hermes config
od mcp install hermes

# Or copy the snippet from the desktop app: Settings → MCP Server
```

After restarting Hermes, the agent can call OD tools via MCP.

### 3. (Optional) Run the desktop app

```bash
# Zero-config — auto-detects Hermes, Ollama, Claude Code, Codex, Cursor, etc.
open-design
```

## Core Workflows

### A. Generate a prototype from a brief

```text
> Use open-design to generate a SaaS landing page with the Linear design system
```

The agent composes: selected design template (`saas-landing`) + design system (`linear-app`) → writes canonical project files → previews in sandboxed iframe.

### B. Create a pitch deck from your brand

```text
> Use open-design to create a pitch deck from our brand DESIGN.md
```

Uses deck templates (`guizang-ppt` or `html-ppt-*`) + your `DESIGN.md` → exports HTML/PDF/PPTX/MP4.

### C. Migrate Figma to React with a design system

```text
> Use open-design to migrate our Figma file to React components with the Vercel design system
```

Runs `od-figma-migration` plugin + `od-react-export` scenario + `vercel` design system.

### D. Produce motion graphics (HyperFrames)

```text
> Use open-design to generate a 30s SaaS product promo video with our brand
```

Agent writes HTML+CSS+GSAP → HyperFrames renders MP4 (1920×1080 @ 30fps). Pair with Seedance 2.0 / Veo 3 / Kling 2 for cinematic t2v, Suno v5 / Lyria 2 for audio.

### E. Generate brand images

```text
> Use open-design to generate editorial travel poster images with our brand
```

Uses `image-templates` plugins (45 editorial/cinematic/product/portrait prompts).

## Design Systems

### Built-in (151 packages)

Located in `design-systems/<slug>/` with:
```
design-systems/<slug>/
├── manifest.json      # metadata, provenance, declared paths
├── DESIGN.md          # canonical design prose for agents
└── tokens.css         # compiled semantic-token stylesheet
```

Key systems for your workflow:
- `linear-app` — ultra-minimal dark-mode, purple accent, Inter Variable
- `vercel` — clean, geometric, teal accent
- `stripe` — refined, trustworthy, indigo
- `apple` — system-native, SF Pro, precise
- `figma` — collaborative, purple, multi-brand
- `nvidia` — technical, green, data-dense
- `tesla` — minimal, red accent, automotive

### Add your own brand

Drop a package into the OD repo or your vault:

```bash
# Option 1: In OD repo (bundled)
mkdir -p /path/to/open-design/design-systems/my-brand/
# Add DESIGN.md, tokens.css, manifest.json

# Option 2: In your vault (symlinked)
mkdir -p ~/TamaZila_Obsidian_Vault/design-systems/my-brand/
# Add DESIGN.md, tokens.css, manifest.json
```

Switch design systems on the fly — next render uses new tokens instantly.

## Plugins

### Key plugin categories

| Category | Count | Examples |
|----------|-------|----------|
| `scenarios/` | 13 | `od-default`, `od-figma-migration`, `od-code-migration`, `od-react-export`, `od-nextjs-export`, `od-vue-export`, `od-media-generation`, `od-new-generation`, `od-tune-collab`, `od-plugin-authoring`, `od-share-to-community`, `od-web-effect-extractor` |
| `image-templates/` | 45 | Editorial, cinematic, product, portrait prompts |
| `video-templates/` | 63 | HyperFrames / Seedance / Veo motion templates |
| `design-systems/` | 143 | Brand `DESIGN.md` wrapped as plugins |
| `atoms/` | 13 | Buttons, heroes, KPI cards |
| `examples/` | 183 | Remixable reference outputs |

### CLI usage

```bash
od plugin list                       # list installed (--task-kind / --mode / --tag filters)
od plugin search "landing page"      # search by keyword
od plugin info od-default            # inspect metadata, inputs, capabilities
od plugin install od-figma-migration # install from registry or local folder
od plugin apply od-default --input brief="a one-page pitch for our seed round"
od plugin upgrade od-default
od plugin uninstall od-default
```

All commands support `--json` for piping.

## Design Templates (Renderable Shapes)

| Template | Mode | Scenario | Output |
|----------|------|----------|--------|
| `web-prototype` | prototype | design | Default landing page / hero |
| `saas-landing` | prototype | marketing | Hero / features / pricing / CTA |
| `dashboard` | prototype | operation | Admin / analytics (with sidebar) |
| `mobile-app` | prototype | design | iPhone 15 Pro / Pixel framed app |
| `mobile-onboarding` | prototype | design | Splash · value-prop · sign-in flow |
| `social-carousel` | prototype | marketing | 3-card 1080×1080 carousel |
| `email-marketing` | prototype | marketing | Table-fallback-safe brand email |
| `magazine-poster` | prototype | marketing | Single-page magazine layout |
| `motion-frames` | prototype | marketing | Looping CSS motion hero |
| `sprite-animation` | prototype | marketing | 8-bit pixel animated explainer |
| `pm-spec` | prototype | product | PM spec doc (TOC + decision log) |
| `team-okrs` | prototype | product | OKR scorecard |
| `eng-runbook` | prototype | engineering | Incident runbook |
| `finance-report` | prototype | finance | Exec finance summary |
| `hr-onboarding` | prototype | hr | Role onboarding plan |
| `guizang-ppt` | deck | marketing | Magazine-style web PPT (deck default) |
| `html-ppt-*` | deck | marketing | 15 deck templates × 36 themes |
| `hyperframes` | video | marketing | HTML → MP4 motion graphics |
| `critique` | utility | design | Five-dimensional self-critique scoresheet |
| `tweaks` | utility | design | AI-emitted tweaks-panel manifest |

## BYOK / Offline Operation

OD's daemon includes a **BYOK proxy** at `/api/proxy/{anthropic,openai,azure,google,ollama,senseaudio}/stream`:

- Paste your `baseUrl` + `apiKey` + model
- Works with local **Ollama** (your `gemma4:12b`, etc.), **LM Studio**, **vLLM**, any OpenAI-compatible endpoint
- **Atlas Cloud**: `https://api.atlascloud.ai/v1` with your key and OpenAI-compatible model IDs (e.g., `qwen/qwen3.5-flash`)
- SSRF-guarded at the edge (private IPs blocked; opt-in via `OD_ALLOWED_INTERNAL_HOSTS`)

No cloud dependency unless you want it.

## Integration with Your Dual-Mac Setup

### Hermes Agent (this session)

```bash
od mcp install hermes   # already done or run once
```

Then in Hermes chat:
```
> Use open-design to generate a mobile onboarding flow with the Linear design system
```

### Claude Code (on either Mac)

```bash
od mcp install claude
# Then in Claude Code:
> Use open-design to create a dashboard with the Vercel design system
```

### Codex / Cursor / Copilot / OpenCode / etc.

```bash
od mcp install codex
od mcp install cursor
od mcp install copilot
od mcp install opencode
# ... 25 CLIs supported
```

### Docker / Self-hosted

```bash
git clone https://github.com/nexu-io/open-design.git
cd open-design/deploy
cp .env.example .env
echo "OD_API_TOKEN=$(openssl rand -hex 32)" >> .env
docker compose up -d
# open http://localhost:7456
```

## Pitfalls & Fixes

| Symptom | Cause | Fix |
|---------|-------|-----|
| `od` command not found / runs octal dump | macOS `/usr/bin/od` shadows CLI | Use `brew install nexu-io/tap/open-design` + ensure `/opt/homebrew/bin` first in PATH; or use absolute path from desktop app Settings → MCP Server |
| MCP tools not appearing in Hermes | Hermes not restarted after `od mcp install hermes` | Restart Hermes desktop app (Cmd+R) or `hermes stop && hermes start` |
| Design system not picked up | `manifest.json` missing or malformed | Ensure `design-systems/<slug>/manifest.json` exists with correct `id`, `files.design`, `files.tokens` |
| HyperFrames render fails | Missing Chrome/FFmpeg in Docker | Install `google-chrome-stable` + `ffmpeg` in container; or run on host with desktop app |
| BYOK proxy returns "Internal IPs blocked" | Local Ollama/LM Studio on private IP | Set `OD_ALLOWED_INTERNAL_HOSTS=host.docker.internal,10.0.0.5,litellm.internal.corp` |
| Plugin apply fails with "capability denied" | Plugin declares `od.capabilities` requiring elevated permission | Run with elevated capabilities or adjust plugin manifest |

## Support Files

- `references/design-systems-catalog.md` — full 151-system list with categories
- `references/plugin-scenarios.md` — detailed scenario plugin capabilities
- `references/hyperframes-templates.md` — 11 HyperFrames + 39 Seedance prompts
- `scripts/od-quickstart.sh` — one-shot install + MCP wiring for Hermes
- `templates/brand-design-system.md` — starter `DESIGN.md` + `manifest.json` + `tokens.css` for new brands

## Related Skills

- `github-codebase-research` — used to explore the OD repo initially
- `mcp-configuration` — MCP server wiring details for Hermes
- `hermes-agent` — Hermes-specific configuration and orchestration
- `design-md` — authoring/validating `DESIGN.md` token spec files
- `architecture-diagram` — visualizing OD architecture
- `videography` — motion graphics workflows (HyperFrames)
- `photography` — image generation workflows