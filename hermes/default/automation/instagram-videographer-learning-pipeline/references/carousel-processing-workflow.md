# Carousel Post Processing Workflow

> **Reference for:** `instagram-videographer-learning-pipeline`
> **Added:** Session 2025-07-17
> **Updated:** Session 2025-07-17 (expanded with automation details)

## Problem

Instagram carousel posts (`/p/`) are **multi-image static posts**, not videos. They cannot be downloaded via `yt-dlp` as MP4. Each slide must be analyzed individually via browser vision.

## Solution: Browser Automation + Vision Analysis

### Step 1: Navigate to Post
```python
browser_navigate(url="https://www.instagram.com/p/DaBejwDkznl/")
```

### Step 2: Close Login Modal (if present)
```python
# Click "Close" button on login prompt
browser_click(ref="@e181")  # Close button ref from snapshot
```

### Step 3: Analyze Slide 1 (Default View)
```python
browser_vision(question="Analyze this carousel slide. Describe the visual content, any text overlays, and identify cinematography/composition techniques demonstrated.")
```

### Step 4: Click Through Remaining Slides
```python
# Instagram carousel uses right arrow navigation
for slide_num in range(2, total_slides + 1):
    browser_click(ref="@e184")  # "Next" arrow button
    time.sleep(1)  # Wait for slide transition
    browser_vision(question=f"Analyze slide {slide_num}. Describe visual content, text overlays, and techniques.")
```

### Step 5: Extract Slide Images (if accessible)
```python
# Get all images from page
browser_console(expression="""
    const images = document.querySelectorAll('img[src*="instagram"]');
    return Array.from(images).map(img => img.src);
""")
```

## Carousel-Specific Asset Generation

### Per-Slide Assets
| Asset | Source | Tool |
|-------|--------|------|
| `slide_01.png` ... `slide_N.png` | Browser screenshot per slide | `browser_vision` screenshot |
| `carousel_combined.gif` | Concatenated slides | `ffmpeg -framerate 1 -i slide_%02d.png` |
| `technique_comparison_grid.png` | Side-by-side all techniques | `ffmpeg -i slide_01.png -i slide_02.png ... -filter_complex "tile=5x1"` |

### Per-Technique Assets (from each slide)
```
assets/{discipline}/{category}/{technique-slug}/
├── demo.gif                    # The slide image itself (static)
├── technique_demo.gif          # Same (or zoomed detail)
├── frame_before.png            # Slide image
├── frame_during.png            # N/A for static
├── frame_after.png             # Graded version (if grade shown)
├── before_after_comparison.png # Slide vs graded (if applicable)
└── node_graph_screenshot.png   # If DaVinci UI shown in slide
```

## Queue Tracking for Carousels

### Reel/Video Queue (Single Technique)
| # | Code | URL | Creator | Discipline | Category | Status |
|---|------|-----|---------|------------|----------|--------|
| 1 | DaxUaKYuhb0 | /reel/... | @art3.studi0 | Video Effects | Transitions | ✅ Done |

### Carousel Queue (Multi-Technique)
| # | Post Code | Slide | Technique | Discipline | Category | Status |
|---|-----------|-------|-----------|------------|----------|--------|
| 1 | DaBejwDkznl | 1 | Static Shot Composition | Cinematography | Camera Technique | ✅ Done |
| 2 | DaBejwDkznl | 2 | Silhouetting + Atmospheric Depth | Camera Theory | Exposure | ⏳ Pending |
| 3 | DaBejwDkznl | 3 | Dutch Angle (Canted) | Composition | Camera Angle | ⏳ Pending |
| 4 | DaBejwDkznl | 4 | Layering + Silhouetting | Composition | Depth Layers | ⏳ Pending |
| 5 | DaBejwDkznl | 5 | Shallow DOF + Low Angle | Lenses & Optics | DOF Technique | ⏳ Pending |
| 6 | DaBejwDkznl | 6 | Natural Framing + Neg Space | Composition | Framing | ⏳ Pending |

## Implementation Notes for `run_pipeline.py`

### Content Type Detection
```python
def detect_content_type(url: str) -> str:
    if "/reel/" in url:
        return "reel"
    elif "/p/" in url:
        return "carousel"
    elif "/tv/" in url:
        return "tv"
    return "unknown"
```

### Carousel Processing Function
```python
def process_carousel_post(url: str, post_code: str, creator: str) -> List[Technique]:
    """Extract multiple techniques from carousel slides."""
    browser_navigate(url)
    close_login_modal_if_present()
    
    # Get total slide count from carousel indicators
    total_slides = get_carousel_slide_count()
    
    techniques = []
    for slide_num in range(1, total_slides + 1):
        if slide_num > 1:
            click_next_slide()
            time.sleep(1)
        
        analysis = browser_vision(f"Analyze slide {slide_num}...")
        technique = classify_technique(analysis, slide_num)
        techniques.append(technique)
    
    # Generate carousel shared assets
    generate_carousel_assets(post_code)
    
    return techniques
```

### Slide Count Detection
```python
def get_carousel_slide_count() -> int:
    """Get number of slides from carousel indicators (dots)."""
    try:
        # Try to find carousel dots/indicators
        snapshot = browser_snapshot()
        # Count indicators or fallback to max 10
        return min(count_carousel_dots(snapshot), 10)
    except:
        return 6  # Safe default
```

### Next Slide Click (robust)
```python
def click_next_slide():
    """Click carousel next arrow, handling dynamic refs."""
    # Re-snapshot to get fresh refs
    snapshot = browser_snapshot()
    # Find next arrow by accessibility label or position
    next_ref = find_next_arrow_ref(snapshot)
    if next_ref:
        browser_click(ref=next_ref)
    else:
        # Fallback: keyboard right arrow
        browser_press(key="ArrowRight")
```

## Vision Prompt Template for Carousel Slides

```
This is slide {slide_num} of a carousel post by @{creator} about "{post_topic}".

Describe:
1. Visual content (what's in the frame, lighting, atmosphere)
2. Any text overlays, captions, or annotations visible
3. Cinematography/composition/lighting techniques being demonstrated
4. Camera settings implied (lens type, angle, exposure, depth of field)
5. Post-production techniques visible (grading style, effects, transitions)

Return structured data for technique classification.
```

## Example: @anshuluniyyal DaBejwDkznl Processing

```bash
# Manual steps for this session:
1. browser_navigate("https://www.instagram.com/p/DaBejwDkznl/")
2. browser_click("@e181")  # Close login modal
3. browser_vision("Analyze slide 1...")  # Static shot composition
4. browser_click("@e184")  # Next slide
5. browser_vision("Analyze slide 2...")  # Silhouetting
6. browser_click("@e184")
7. browser_vision("Analyze slide 3...")  # Dutch angle
... etc for all 6 slides
```

## Next Steps for Automation

1. **Add `detect_content_type()`** to `run_pipeline.py`
2. **Implement `process_carousel_post()`** function with robust slide navigation
3. **Add carousel asset generation** (combined GIF, comparison grid)
4. **Update queue schema** with slide/technique columns
5. **Test with 3+ carousel posts** to validate automation

---

## Pitfalls & Fixes

| Pitfall | Fix |
|---------|-----|
| Login modal blocks carousel | Click close button `@e181` before analysis |
| Slide count unknown | Count dot indicators or fallback to max 10 |
| Vision analysis misses text | Explicitly ask "read all text overlays" in question |
| Slide images not downloadable | Use browser screenshot per slide; no direct image URL access |
| Rate limiting on rapid clicks | Add `time.sleep(1-2)` between slide clicks |
| Carousel auto-advances | Some carousels auto-play; add pause detection |
| Ref IDs change after click | Re-snapshot & re-find elements after each navigation |
| Carousel is actually a Reel (video) | Check for video player controls before carousel logic |

## Vision Prompt Template for Carousel Slides

```
This is slide {slide_num} of a carousel post by @{creator} about "{post_topic}".

Describe:
1. Visual content (what's in the frame, lighting, atmosphere)
2. Any text overlays, captions, or annotations visible
3. Cinematography/composition/lighting techniques being demonstrated
4. Camera settings implied (lens type, angle, exposure, depth of field)
5. Post-production techniques visible (grading style, effects, transitions)

Return structured data for technique classification.
```

## Example: @anshuluniyyal DaBejwDkznl Processing

```bash
# Manual steps for this session:
1. browser_navigate("https://www.instagram.com/p/DaBejwDkznl/")
2. browser_click("@e181")  # Close login modal
3. browser_vision("Analyze slide 1...")  # Static shot composition
4. browser_click("@e184")  # Next slide
5. browser_vision("Analyze slide 2...")  # Silhouetting
6. browser_click("@e184")
7. browser_vision("Analyze slide 3...")  # Dutch angle
... etc for all 6 slides
```

## Next Steps for Automation

1. **Add `detect_content_type()`** to `run_pipeline.py`
2. **Implement `process_carousel_post()`** function with robust slide navigation
3. **Add carousel asset generation** (combined GIF, comparison grid)
4. **Update queue schema** with slide/technique columns
5. **Test with 3+ carousel posts** to validate automation

---

## Carousel Posts Processed (This Session Batch)

| # | URL | Creator | Slides | Techniques | Disciplines Covered |
|---|-----|---------|--------|------------|---------------------|
| 1 | `p/DaBejwDkznl` | @anshuluniyyal | 6 | 6 | Camera Theory, Cinematography, Composition×3, Lenses & Optics |
| 2 | `p/Dax2p1aEa...` | @jb.brandon4 | 9 | 9 | Camera Movement, Cinematography |
| 3 | `p/...` | @openailearning | 5 | 5 | Camera Movement |
| 4 | `p/...` | @shadi.3001 | 5 | 5 | Production, Lighting |
| 5 | `p/...` | @shadi.3001 | 5 | 5 | Production, Lighting |
| 6 | `p/...` | @shadi.3001 | 5 | 5 | Production (iPhone) |
| 7 | `p/...` | @lukas.messing_ | 5 | 5 | Cinematography, Camera Movement |
| 8 | `p/...` | @mistertwister.me | 5 | 5 | Camera Movement, Cinematography |
| 9 | `p/...` | @openailearning | 5 | 5 | Camera Movement |

**Total: 9 carousels, ~50 slides, 50 techniques, 7 disciplines**

---

## Related Files

- `scripts/run_pipeline.py` — Batch processor with carousel support
- `templates/vault_note_template_cinematography.md`
- `templates/vault_note_template_composition.md`
- `templates/vault_note_template_camera_theory.md`
- `templates/skill_template_cinematography.md`
- `references/visual-asset-pipeline.md` — FFmpeg recipes
- `references/auto-cleanup-workflow.md` — (Reels only; carousels don't need)

---

*Workflow documented: 2025-07-17 | For `instagram-videographer-learning-pipeline` v1.0.0*