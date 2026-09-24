# Pipeline Comparison & Evolution

> **Reference for:** `instagram-videographer-learning-pipeline`
> **Context:** How this pipeline extends/evolves from previous pipelines

---

## Pipeline Lineage

| Pipeline | Focus | Disciplines | Output Vaults |
|----------|-------|-------------|---------------|
| `instagram-davinci-learning-pipeline` | Color grading | 10 color grading categories | `DaVinci_Knowledge_Base/Color Grading & Looks/`, `Camera Theory/`, `Photography/Lightroom/` |
| `instagram-davinci-video-effects-pipeline` | DaVinci effects/transitions | 7 effect types | `DaVinci_Knowledge_Base/Video_Effects/` |
| **`instagram-videographer-learning-pipeline`** | **Full videography education** | **11 disciplines + 3 legacy** | **All of above + `Videographer/`** |

---

## What's New in Videographer Pipeline

### 1. Broader Scope (Not Just DaVinci)
| Old Pipelines | New Pipeline |
|---------------|--------------|
| DaVinci Resolve specific | Camera-agnostic techniques |
| Post-production only | Pre-production → Production → Post |
| Effect tutorials | **Shoot-ready workflows** |
| Color grading focus | **Full videography stack** |

### 2. 11 Disciplines (vs 7-10 categories)
```
DaVinci-Specific (inherited):
├── Video Effects & Transitions (7 sub-types)
├── Color Grading & Color Science
└── Camera Theory & Color Science

NEW — Videographer Education:
├── Cinematography & Camera Technique
├── Camera Movement
├── Lenses & Optics
├── Lighting & Exposure
├── Composition & Visual Storytelling
├── Production Workflow & Directing
├── Post-Production Workflow
├── VFX & Compositing
├── Audio & Sound
└── Business & Career
```

### 3. Carousel Post Support (NEW)
| Content Type | Old Pipelines | New Pipeline |
|--------------|---------------|--------------|
| Reels (`/reel/`) | ✅ Full video download + frames | ✅ Same |
| Carousels (`/p/`) | ❌ Skipped / not handled | ✅ **Per-slide vision analysis** |
| IGTV (`/tv/`) | ⚠️ Limited | ✅ Video download |

### 4. Multi-Technique Per URL Queue Tracking
```
Old: One row per URL
New: One row per technique (carousel = N rows per URL)
```

### 5. Enhanced Visual Assets
| Asset | Reel | Carousel |
|-------|------|----------|
| Demo GIF | ✅ From MP4 | ✅ Slide as static GIF |
| Technique Loop | ✅ 3s MP4 segment | ❌ N/A (static) |
| Key Frames | ✅ Before/During/After | ✅ Per slide |
| Comparison Grid | ❌ | ✅ **Tile all techniques** |
| Carousel Combined GIF | ❌ | ✅ **All slides animated** |

---

## Auto-Compression Fix (Critical for Long Sessions)

**Problem (Session 20260715_203740_bc494a):** 1,014 messages without compression — session hung 10-30 min each trigger.

**Root Cause:**
```yaml
# ~/.hermes/config.yaml (and profile config)
auxiliary:
  compression:
    provider: nvidia
    model: nvidia/nemotron-mini-4b-instruct
    base_url: http://127.0.0.1:11434/v1    # ← LOCAL OLLAMA
    enabled: true
    threshold: 0.7
```
Model `nvidia/nemotron-mini-4b-instruct` **does not exist locally** (only `qwen3.5-4b-compress` is pulled).

**Fix Applied:**
```yaml
auxiliary:
  compression:
    provider: nvidia
    model: nvidia/nemotron-mini-4b-instruct
    base_url: https://integrate.api.nvidia.com/v1    # ← NVIDIA API DIRECT
    enabled: true
    threshold: 0.7
```

**Verified:** Model exists on NVIDIA API (`/v1/models` returns it).

**Lesson:** Always verify compression model exists at configured endpoint. Local Ollama ≠ NVIDIA API models.

---

## Session 2025-07-17 Accomplishments

| Item | Status |
|------|--------|
| Create `instagram-videographer-learning-pipeline` skill | ✅ |
| 11-discipline config with keyword routing | ✅ |
| Carousel multi-technique extraction design | ✅ |
| Vault structure (11 folders + templates + index + queue) | ✅ |
| Master template (`TEMPLATE-Videographer-Technique.md`) | ✅ |
| Discipline templates (cinematography, lighting, composition, production) | ✅ |
| Skill template with carousel awareness | ✅ |
| First URL processed: @anshuluniyyal "The Art of Static Shots" | ✅ Slide 1/6 |
| Queue tracker with carousel multi-row format | ✅ |
| Hermes skill for first technique | ✅ |
| References: session log, visual asset pipeline, carousel handling, carousel workflow | ✅ |

---

## Next Session Checklist

- [ ] **Browser-click through carousel slides 2-6** for @anshuluniyyal post
- [ ] **Vision analyze each slide** → extract 5 pending techniques
- [ ] **Create 5 vault notes** in Camera Theory, Composition, Lenses & Optics
- [ ] **Generate 5 Hermes skills** for each technique
- [ ] **Build `scripts/run_pipeline.py`** with carousel handler
- [ ] **Add `yt-dlp` + `ffmpeg` automation** for reel processing
- [ ] **Process batch of 10-20 URLs** from queue

---

*Reference created: 2025-07-17 | Pipeline v1.0.0*