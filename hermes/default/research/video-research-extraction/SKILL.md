---
name: video-research-extraction
description: "Research, discover, and extract structured knowledge from YouTube tutorial videos. Covers search strategies, transcript fetching via youtube-transcript-api, content analysis, and vault-ready markdown generation with cross-references."
platforms: [linux, macos, windows]
---

# Video Research & Extraction Skill

## Overview
This skill covers the end-to-end workflow for finding, analyzing, and extracting actionable knowledge from YouTube tutorial videos — specifically designed for technical domains like color grading, software development, and creative workflows where visual demonstration is key but transcript content holds the procedural details.

## Prerequisites
- `uv` package manager (for installing youtube-transcript-api)
- Python 3.10+
- Hermes Agent with `youtube-content` skill available
- Browser tools for initial discovery (YouTube search, channel pages)

---

## Phase 1: Discovery & Search Strategy

### Search Patterns by Domain

**Color Grading / DaVinci Resolve:**
```
"S-Log3 color grading DaVinci Resolve 19 tutorial"
"Apple Log 2 color grading DaVinci Resolve tutorial"
"Cullen Kelly DaVinci Resolve S-Log3"
"Mixing Light DaVinci Resolve color grading"
"Dehancer Pro DaVinci Resolve film emulation"
"Mehran Hadad S-Log3 Resolve 21"
```

**Software Development:**
```
"Next.js 14 app router tutorial"
"TanStack Query v5 tutorial"
"GSAP scroll animations tutorial"
```

**Search Filters to Apply:**
- Upload date: Past year (for version-specific content)
- Duration: 5-30 minutes (tutorials), 30-60+ minutes (courses)
- Features: CC (closed captions) — required for transcript extraction

### Channel Authority Signals
| Channel | Subscribers | Specialty | Trust Level |
|---------|-------------|-----------|-------------|
| Cullen Kelly | 129K | Pro colorist, image scientist | ⭐⭐⭐⭐⭐ (Gold standard) |
| Mixing Light | — | Pro colorist training | ⭐⭐⭐⭐⭐ |
| Waqas Qazi | 496K | Color grading education | ⭐⭐⭐⭐ |
| Kyle White | — | Sony FX3/S-Log3 workflows | ⭐⭐⭐⭐ |
| Danny Gan | — | Color Space Transform workflows | ⭐⭐⭐⭐ |
| Mehran Hadad | — | Complete courses, Resolve 21 | ⭐⭐⭐⭐ |
| Victor Melchor | — | Dehancer Pro workflows | ⭐⭐⭐ |

---

## Phase 2: Transcript Extraction

### Install Dependency
```bash
uv pip install youtube-transcript-api
```

### Fetch Transcript (via youtube-content skill script)
```bash
# Get video ID from URL: https://youtube.com/watch?v=VIDEO_ID
uv run python3 /path/to/youtube-content/scripts/fetch_transcript.py "VIDEO_ID" --timestamps --language en
```

### Output Formats
- **JSON** (default): Structured with segments, timestamps, full_text
- **Text-only** (`--text-only`): Plain transcript
- **Timestamped** (`--timestamps`): `MM:SS text` format

### Error Handling
| Error | Cause | Resolution |
|-------|-------|------------|
| "Transcripts are disabled" | Creator disabled captions | Skip video, find alternative |
| "No transcript found" | No captions in requested language | Try without `--language` for auto |
| "Video unavailable" | Private/deleted/region-locked | Verify URL, try different region |

---

## Phase 3: Content Analysis & Structuring

### Extract These Elements from Transcript
1. **Node Tree / Workflow Steps** — Sequential operations (e.g., "Node 1: CST, Node 2: Exposure, Node 3: LUT")
2. **Parameter Values** — Specific numbers (e.g., "Gamma 0.45", "Gain 1.2", "Temperature 5600")
3. **Tool/LUT/Plugin Names** — Dehancer Pro, Voyager LUT, Mononodes DCTLs, PowerGrades
4. **Camera/Log Profile** — S-Log3, Apple Log 2, S-Log2, Arri LogC
5. **Color Space Transforms** — Input/Output color spaces, CST settings
6. **Creative Decisions** — "Teal/Orange push", "Skin tone protection", "Highlight roll-off"
7. **Version-Specific Features** — Resolve 19 vs 20 vs 21 differences

### Structured Output Template
```markdown
# [Video Title]
**Source:** [Channel Name] — [URL]
**Duration:** [MM:SS] | **Views:** [X] | **Date:** [YYYY-MM-DD]
**DaVinci Resolve Version:** [19/20/21] | **Camera/Log:** [S-Log3 / Apple Log 2]

## Chapter Breakdown
| Time | Chapter | Key Actions |
|------|---------|-------------|
| 00:00 | Introduction | ... |
| 02:15 | Project Setup / Color Management | ... |
| 05:30 | Node 1: Color Space Transform | CST: S-Log3/S-Gamut3 → Rec.709 |
| 08:45 | Node 2: Primary Balance | Lift/Gamma/Gain values... |
| 12:00 | Node 3: Creative LUT | Voyager LUT at 65% strength |

## Key Parameter Reference
- **CST Settings:** Input: S-Log3/S-Gamut3.Cine, Output: Rec.709/Gamma 2.4
- **Exposure Correction:** Gain +0.15, Gamma -0.05
- **White Balance:** Temp 5600, Tint +2
- **Creative LUT:** Voyager "Kodak 2383" at 65% key output gain

## Node Tree Diagram
```
Node 1: CST (S-Log3 → Rec.709)
  └─ Node 2: Primary (Balance)
      └─ Node 3: Creative LUT (Voyager)
          └─ Node 4: Skin Tone Protection (Qualifier)
              └─ Node 5: Output (Gain 0.98)
```

## Cross-References
- Related: [Other tutorial filename.md]
- LUT Pack: [Voyager / Dehancer / Custom]
- Plugin: [Dehancer Pro / Mononodes DCTLs]
```

---

## Phase 4: Vault Integration

### File Naming Convention
```
{LogProfile}_{Creator}_{KeyTechnique}.md
Examples:
  S-Log3_Kyle-White_FX3-Cinematic-Node-Tree.md
  S-Log3_Danny-Gan_3-Node-CST-Workflow.md
  Apple-Log2_Russell-Wofford_CST-Rec2020-Rec709.md
  Film-Emulation_Mediabee_Dehancer-Pro-Voyager-DCTLs.md
```

### Target Directory
```
/Users/alfredkamisese/TamaZila Obsidian Vault/Hermes Agent/DaVinci_Knowledge_Base/Color Grading & Looks/
```

### Update Domain Memory Map
After creating files, append to `/Users/alfredkamisese/TamaZila Obsidian Vault/Hermes Agent/DaVinci_Knowledge_Base/Memory.md`:

```markdown
## YouTube Tutorial References (v19-21)
- **S-Log3 Workflows:**
  - `S-Log3_Kyle-White_FX3-Cinematic-Node-Tree.md` — 8-node tree, power windows, skin tones
  - `S-Log3_Danny-Gan_3-Node-CST-Workflow.md` — Minimal CST approach
  - `S-Log3_Cullen-Kelly_Pro-Noise-Highlight-Management.md` — Noise/highlight strategies
  - `S-Log3_Mehran-Haddad_Resolve21-Portrait-PowerGrade.md` — v21 PowerGrade workflow
- **Apple Log 2 Workflows:**
  - `Apple-Log2_Russell-Wofford_CST-Rec2020-Rec709.md` — iPhone CST workflow
  - `Apple-Log2_CineMirage_iPhone15ProMax-Presets.md` — Preset-based approach
  - `Apple-Log2_FujiCinema_Basics-Kodak-Look.md` — Kodak film emulation
- **Film Emulation / Plugins:**
  - `Film-Emulation_Mediabee_Dehancer-Pro-Voyager-DCTLs.md` — Dehancer + Mononodes + Voyager
  - `Film-Emulation_Victor-Melchor_Dehancer-Pro-Quick.md` — 5-min Dehancer workflow
```

---

## Quick Reference: Video IDs from Recent Research

| # | Title | Channel | Video ID | Duration | Priority |
|---|-------|---------|----------|----------|----------|
| 1 | How to Grade S-Log3 in DaVinci Resolve \| Sony FX3 | Kyle White | udVtG5jD2H0 | 8:34 | ⭐⭐⭐⭐⭐ |
| 2 | FASTEST Way To Color Grade Sony S-Log3 \| CST | Danny Gan | hFZDiXbFeJQ | 11:20 | ⭐⭐⭐⭐⭐ |
| 3 | How to Grade SLog Footage | Cullen Kelly | YT3Mn3mk9Rg | 14:04 | ⭐⭐⭐⭐⭐ |
| 4 | Cinematic Portrait Workflow in Resolve 21 | Mehran Hadad | AR9K-GqY4Eg | 13:23 | ⭐⭐⭐⭐ |
| 5 | How to color grade iPhone Apple Log 2 the RIGHT way | Russell Wofford | JMIfDOfo_nE | 3:53 | ⭐⭐⭐⭐⭐ |
| 6 | Cinematic Color Grading \| Resolve 19 \| BMPCC 6K Pro | Mediabee Color Lab | [extract from URL] | 12:30 | ⭐⭐⭐⭐ |
| 7 | Get the Film Look FAST \| Dehancer Pro Workflow | Victor Melchor | [extract from URL] | 5:19 | ⭐⭐⭐ |
| 8 | Struggling with Apple Log? Watch This! | FujiCinema | IzV3t7RxPi4 | 4:10 | ⭐⭐⭐ |
| 9 | Kodak 2383 Film Look - Resolve Tutorial | Gabe Lomotey | Ug-ygRJqSzM | 13:53 | ⭐⭐⭐⭐ |
| 10 | Why Do My Film LUTs Look Bad? - KODAK 2383 | Darren Mostyn | A2OLQNSIJgU | 5:16 | ⭐⭐⭐⭐⭐ |
| 11 | How to Get Perfect Skin Tones in DaVinci Resolve 17 | Tutorial Channel | Bw14wqVbpOo | 8:11 | ⭐⭐⭐⭐⭐ |
| 12 | The Qualifier in DaVinci Resolve (Sony S-Log3) | Pro Colorist | azM7dQSR8To | 8:36 | ⭐⭐⭐⭐⭐ |
| 13 | How to Color Grade - Apple LOG 2 - iPhone 17 Pro Max | CineMirage | a1ZVeTKDNLY | 9:39 | ⭐⭐⭐⭐ |

> **Note:** Video IDs extracted from YouTube URLs (the `v=` parameter or `youtu.be/` suffix). Use browser search snapshots to capture full URLs.

---

## Automation Opportunities

### Batch Processing Script
Create a script that:
1. Reads a list of video IDs from a text file
2. Fetches transcripts for all
3. Outputs JSONL for downstream processing
4. Flags failed extractions for manual review

### Content Classification
Use LLM to auto-classify extracted transcripts into:
- `workflow` (step-by-step node tree)
- `technique` (specific skill: skin tones, highlights, noise)
- `tool_review` (plugin/LUT evaluation)
- `course` (multi-video series)

---

## Maintenance Notes

- Re-run discovery quarterly for new Resolve versions
- Archive deprecated version tutorials (mark with `DEPRECATED:` prefix)
- Update Memory.md cross-references after each batch
- Verify transcript availability before committing to extraction (some channels disable captions)

---

## 📋 GitHub Repository Discovery for AI Agent Frameworks

When researching AI agent tools from YouTube tutorials (Seed, Paul, Charlie OS, etc.), use these search patterns:

```bash
# Search for repos implementing "PAUL" (Plan/Apply/Unify/Loop) patterns
curl "https://api.github.com/search/repositories?q=plan+apply+unify+loop+framework"

# Search for "Charlie OS" or "Charlie Automates" related repos  
curl "https://api.github.com/search/repositories?q=%22charlie+automates%22"

# Search for Graphify + Hermes integrations
curl "https://api.github.com/search/repositories?q=graphify+hermes+agent"

# Search by known creator (Charles Dove / @charlieautomates / @doveccl)
curl "https://api.github.com/users/doveccl/repos"

# Search for open-source alternatives to proprietary agent frameworks
curl "https://api.github.com/search/repositories?q=agentic+os+dashboard+claude"
```

**Known Open-Source Alternatives to Charlie Automates Tools:**
| Proprietary Tool | Open-Source Alternative | Repo |
|-----------------|------------------------|------|
| Seed (ideation) | — | Not yet found |
| Paul (Plan/Apply/Unify/Loop) | **FORGE Framework** | `SanthoshVishnuRajamanickam/forge-framework` |
| Charlie OS runtime | **TONY AI Agent** (includes Charlie OS shell) | `mafzalkalwardev/tony-ai-agent` |
| Graphify + Hermes bridge | **TONY AI Agent** (built-in) | `mafzalkalwardev/tony-ai-agent` |

**Research Pitfall:** Many "Agentic OS" tutorials (like Charlie Automates) gatekeep their core CLIs behind email signup walls. Always search GitHub for the *pattern names* (PAUL, plan/apply/unify, Charlie OS) before assuming the tool is the only option.