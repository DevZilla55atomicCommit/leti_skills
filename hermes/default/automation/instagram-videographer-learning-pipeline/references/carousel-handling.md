# Carousel Post Handling Pattern

> **New capability** — processing Instagram carousel posts (`/p/`) as multi-technique educational content.

---

## 🎯 Problem

Instagram carousel posts (`/p/`) are **static image collections**, not videos:
- No MP4 to download via yt-dlp
- Each slide = potential separate technique
- Browser automation required to view all slides
- Vision analysis must run per slide

---

## 🔄 Workflow

### 1. Detect Carousel Post
```python
# URL pattern detection
if "/p/" in url:
    content_type = "carousel"
elif "/reel/" in url:
    content_type = "reel"
elif "/tv/" in url:
    content_type = "igtv"
```

### 2. Browser Automation to Extract All Slides
```python
# Navigate to post
browser_navigate(url)

# Close login modal if present
browser_click(ref="@e181")  # Close button

# Detect carousel: look for navigation arrows or slide indicators
# Click through each slide
slides = []
for i in range(max_slides):  # e.g., 10 max
    # Vision analyze current slide
    result = browser_vision(question="Describe this slide: visual content, any text overlays, compositional techniques visible")
    slides.append(result)
    
    # Try to click next arrow
    try:
        browser_click(ref="NEXT_ARROW_REF")
        time.sleep(0.5)
    except:
        break  # No more slides
```

### 3. Per-Slide Vision Analysis Prompt
```
Analyze this carousel slide from an educational videography post.
Identify:
1. Visual content (what's in the frame)
2. Any text overlays or captions
3. Cinematography/composition/lighting techniques demonstrated
4. Camera settings implied (lens, angle, exposure)
5. Post-production techniques visible (grading, effects)
Return structured data for vault note creation.
```

### 4. Classification Per Slide
Each slide classified independently:
- Slide 1: "Silhouetting + Atmospheric Depth" → Camera Theory / Exposure
- Slide 2: "Dutch Angle (Canted)" → Composition / Camera Angle
- Slide 3: "Layering + Silhouetting" → Composition / Depth Layers
- Slide 4: "Shallow DOF + Low Angle" → Lenses & Optics / DOF Technique
- Slide 5: "Natural Framing + Negative Space" → Composition / Framing

### 5. Queue Tracking (Multi-Row)
```markdown
| # | Post Code | URL | Creator | Slide | Technique | Discipline | Category | Status | Vault File |
|---|-----------|-----|---------|-------|-----------|------------|----------|--------|------------|
| 2 | DaBejwDkznl | instagram.com/p/DaBejwDkznl/ | @anshuluniyyal | 1 | Silhouetting + Atmos. Depth | Camera Theory | Exposure | ⏳ Pending | Camera Theory/02-Silhouetting-Atmospheric-Depth.md |
| 3 | DaBejwDkznl | instagram.com/p/DaBejwDkznl/ | @anshuluniyyal | 2 | Dutch Angle (Canted) | Composition | Camera Angle | ⏳ Pending | Videographer/Composition/02-Dutch-Angle.md |
| 4 | DaBejwDkznl | instagram.com/p/DaBejwDkznl/ | @anshuluniyyal | 3 | Layering + Silhouetting | Composition | Depth Layers | ⏳ Pending | Videographer/Composition/03-Layering-Silhouette.md |
| 5 | DaBejwDkznl | instagram.com/p/DaBejwDkznl/ | @anshuluniyyal | 4 | Shallow DOF + Low Angle | Lenses & Optics | DOF Technique | ⏳ Pending | Videographer/Lenses & Optics/01-Shallow-DOF-Low-Angle.md |
| 6 | DaBejwDkznl | instagram.com/p/DaBejwDkznl/ | @anshuluniyyal | 5 | Natural Framing + Neg Space | Composition | Framing | ⏳ Pending | Videographer/Composition/04-Natural-Framing.md |
```

### 6. Visual Assets for Carousels
```
assets/{post-code}/
├── slide_01.png ... slide_N.png          # Original slides
├── carousel_combined.gif                 # ffmpeg -framerate 1
├── technique_comparison_grid.png         # ffmpeg tile=5x1
assets/{discipline}/{category}/{technique-slug}/
├── slide_{N}.png                         # Copy of relevant slide
├── technique_demo.gif                    # Same as slide (static)
└── before_after_comparison.png           # If grade comparison shown
```

---

## 🔧 Implementation Notes

### Browser Automation Challenges
- **Login modal** — must close first (`@e181` close button)
- **Carousel navigation** — right arrow `@e184` or swipe gesture
- **Slide indicators** — dots at bottom show total count
- **Rate limiting** — 1-2s between slide clicks
- **Dynamic refs** — ref IDs change per page load; use relative selectors

### Vision Prompt Tuning
For carousels, vision prompt must be **per-slide specific**:
```
"This is slide {N} of a carousel post about {topic}. 
Describe the visual content and identify the specific 
cinematography/composition/lighting technique being taught."
```

### Classification Keywords (Extended)
Add carousel-specific keywords to config:
```yaml
# Carousel indicators
carousel_keywords:
  - "carousel"
  - "swipe"
  - "slide"
  - "part 1"
  - "part 2"
  - "series"
  - "thread"
```

---

## 📋 Session 2025-07-17 Example

**Post:** @anshuluniyyal "The Art of Static Shots" (`DaBejwDkznl`)
**Total slides visible:** 6 (title + 5 technique slides)
**Slides analyzed:** 1 (title + main image)
**Slides pending:** 5

**Extracted from Slide 1 (Title + Main):**
- Technique: Static Shot Composition
- Discipline: Cinematography
- Principles: Scale juxtaposition, negative space, atmospheric diffusion, golden hour, patience

**Pending from Slides 2-6:**
| Slide | Likely Technique | Discipline |
|-------|-----------------|------------|
| 2 | Silhouetting + Atmospheric Perspective | Camera Theory |
| 3 | Dutch Angle (Canted) | Composition |
| 4 | Layering + Silhouetting | Composition |
| 5 | Shallow DOF + Low Angle | Lenses & Optics |
| 6 | Natural Framing + Negative Space | Composition |

---

## 🔗 Related Files
- `scripts/run_pipeline.py` — needs carousel handler added
- `references/config_videographer.yaml` — needs carousel keywords
- `templates/vault_note_template_cinematography.md` — carousel-aware template
- `visual-asset-pipeline.md` — carousel asset specs