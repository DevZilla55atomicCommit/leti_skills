# Cross-Domain Knowledge Graph Discovery

## Overview

When Graphify processes multi-discipline corpora (code + documentation + notes across different domains), it discovers connections that aren't obvious through manual browsing. This reference documents patterns observed in the TamaZila vault and provides templates for finding similar cross-domain insights.

## Discovered Connection Types

### 1. Color Science Bridge (DaVinci ↔ Photography)
```
DaVinci: "Luma Mix Zero White Balance" (Color Grading & Looks)
Photography: "Sony Portrait Settings" / "Natural Light Manipulation"
Edge: semantically_similar_to [INFERRED, 0.85]
Reason: Both deal with color space transforms, white balance, exposure
```

### 2. Proxy/Render Pipeline (Flux Code ↔ DaVinci Workflows)
```
Flux: flux_wrapper.py (Ollama-based generation, local proxy)
DaVinci: "DaVinci Resolve Proxy Workflows" / "Offline and Online Workflows"
Edge: conceptually_related_to [INFERRED, 0.75]
Reason: Both implement proxy generation → high-res render workflows
```

### 3. Rate Fetching Implementation (Forex Code ↔ API Standards)
```
Forex: get_exchange_rate() in market_tracker.py
API: "API Design & Connectivity Standards"
Edge: references [EXTRACTED]
Reason: Direct code reference to API patterns
```

### 4. Communication Protocols (Creative Direction ↔ Technical Config)
```
Creative: "Creative Director Communication Mastery"
Technical: "API Design & Connectivity Standards" / "Smooth Scroll Foundations"
Edge: conceptually_related_to [INFERRED, 0.75]
Reason: Both define communication/interface contracts
```

### 5. Batch Processing Patterns (Media Processor ↔ Flux Batch)
```
Media: media_processor.py (batch image resize)
Flux: batch_generate() in flux_wrapper.py
Edge: conceptually_related_to [INFERRED, 0.70]
Reason: Both implement batch processing with parameterized configs
```

### 6. Storyboard ↔ Grading Workflow (Storyboard Agent ↔ Conform Tools)
```
Storyboard: generate_storyboard_frame() (Draw Things/SDXL)
Grading: "XML Timeline Import" / "ColorTrace" (DaVinci conform)
Edge: conceptually_related_to [INFERRED, 0.70]
Reason: Both deal with shot-level planning → execution pipelines
```

## Query Templates for Cross-Domain Discovery

### Find All Cross-Domain Bridges
```bash
graphify query "what connects different domains in this codebase?" --budget 2000
```

### Find Specific Domain Pairs
```bash
# DaVinci ↔ Photography
graphify query "how does color grading connect to photography?"

# Code ↔ Documentation
graphify query "what code implements the documented workflows?"

# Image Generation ↔ Video
graphify query "what connects Flux image generation to video workflows?"
```

### Trace Bridge Nodes
```bash
# God nodes that bridge communities
graphify query "which nodes connect the most communities?"

# Specific bridge
graphify path "Luma Mix Zero White Balance" "Sony Portrait Settings"
```

## Community Cohesion as Domain Indicator

| Cohesion Range | Interpretation | Action |
|----------------|----------------|--------|
| ≥ 0.7 | Single domain/module | Good encapsulation |
| 0.4–0.7 | Mixed domain | Review boundaries |
| < 0.4 | Cross-domain mashup | Likely bridge opportunity |

## Practical Workflow for New Vaults

1. **Initial scan**: `graphify /path/to/vault --no-cluster` (fast, free)
2. **Check domains**: Look at community labels in GRAPH_REPORT.md
3. **Full extraction**: `graphify /path/to/vault --backend gemini` (needs API)
4. **Cross-domain query**: `graphify query "what unexpected connections exist?"`
5. **Export subgraphs**: Per-domain Obsidian vaults for focused work

## TamaZila Vault Specific Commands

```bash
# Export API key from Hermes config
export GEMINI_API_KEY="$(grep -A2 'google-gemini:' ~/.hermes/config.yaml | grep 'api_key:' | cut -d'\"' -f2)"

# DaVinci Knowledge Base
graphify "/Users/alfredkamisese/TamaZila Obsidian Vault/Hermes Agent/DaVinci_Knowledge_Base" \
  --obsidian --obsidian-dir "/Users/alfredkamisese/TamaZila Obsidian Vault/Graphify-DaVinci"

# Forex Analysis
graphify "/Users/alfredkamisese/TamaZila Obsidian Vault/Hermes Agent/Forex Center" \
  --obsidian --obsidian-dir "/Users/alfredkamisese/TamaZila Obsidian Vault/Graphify-Forex"

# Photography
graphify "/Users/alfredkamisese/TamaZila Obsidian Vault/Hermes Agent/Photography" \
  --obsidian --obsidian-dir "/Users/alfredkamisese/TamaZila Obsidian Vault/Graphify-Photography"

# Full cross-domain
graphify "/Users/alfredkamisese/TamaZila Obsidian Vault" \
  --obsidian --obsidian-dir "/Users/alfredkamisese/TamaZila Obsidian Vault/Graphify-FullVault"
```

## Community Hubs as Navigation Anchors

The **Community Hubs** section of GRAPH_REPORT.md lists top nodes acting as cross-community bridges:

```
Community Hubs (Navigation)
- Cinematic Color Grading Tutorials
- Flux Image Generation API
- Sky Replacement and Masking
- Film Emulation Workflows
- Timeline and Conform Tools
- AI Photo Management
- Scroll and Parallax Animation
- Market and Exchange Rates
- Developer Infrastructure Standards
```

Click any hub in the HTML graph (`graph.html`) to see its cross-community edges.

## Suggested Questions (Graphify-Generated)

Graphify generates questions it's uniquely positioned to answer:

```
- What connects Fetches the real-time conversion rate between two currencies,
  Processes images in a folder and creates multiple resized versions,
  Generate image with Ollama x/flux2-klein on M4 to the rest of the system?
  (75 weakly-connected nodes found)

- Why does _generate() connect Batch Image Generation to Image Metadata,
  generate_flux, and generate_image?
  (High betweenness centrality - cross-community bridge)
```

## Practical Use Cases for Your Workflow

### As a Creative Director
- Trace how color grading decisions in DaVinci connect to photography lighting notes
- Find which grading workflows reference which photography techniques

### As a Web Dev
- See which API standards your forex scripts actually use
- Discover where frontend animation patterns (GSAP, Framer Motion) connect to creative briefs

### As a Forex Analyst
- Map technical indicators to their implementation in code
- Find which research notes inform which trading scripts

### As an AI Learner
- Track which Hermes Agent configs connect to which project domains
- See how MCP tool patterns propagate across scripts