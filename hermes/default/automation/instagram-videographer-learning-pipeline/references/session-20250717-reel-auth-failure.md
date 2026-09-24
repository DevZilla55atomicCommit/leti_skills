# Reel Authentication Pitfall & Carousel Processing Workflow

> **Session**: 2025-07-17 | **Pipeline**: instagram-videographer-learning-pipeline | **Key Learning**: Reel authentication failure pattern + Carousel vision-only workflow

---

## 🔴 Reel Authentication Failure Pattern

### The Problem
**All 200+ Reels fail with `yt-dlp`** even with `--cookies-from-browser chrome`:

```
ERROR: [Instagram] DaeM5UmIofZ: Instagram sent an empty media response.
Check if this post is accessible in your browser without being logged-in.
```

### Root Cause
Instagram serves **empty media responses** to automated requests even with valid Chrome cookies. The cookies extracted from Chrome may be:
- Stale/expired
- Missing required session tokens
- Blocked by Instagram's bot detection
- Missing required headers (User-Agent, Referer, etc.)

### Failed Attempts
| Method | Result |
|--------|--------|
| `yt-dlp --cookies-from-browser chrome` | ❌ Empty media response |
| `yt-dlp --cookies cookies.txt` (exported from Cookie Editor) | ❌ Empty media response |
| Browser vision on Reel page | ⚠️ Video player loads but can't extract MP4 |

### Current Status
**All 200+ Reels fail** — pipeline processes carousels but fails on all Reels.

### Workarounds (To Implement)
| Approach | Effort | Success Probability |
|----------|--------|---------------------|
| **Authenticated Playwright/Selenium** with cookie injection + video element extraction | High | High |
| **Browser vision analysis** on Reel page (if video renders in DOM) | Low | Medium |
| **Manual MP4 download** → pipeline processes local file | Manual | High |
| **Instagram Graph API** (requires Business account + app review) | Very High | High |
| **Burner account + isolated Chrome profile** + fresh cookie export | Medium | Medium |

### Immediate Workflow
**Current pipeline behavior**: 
1. Carousels → Browser vision → ✅ Processed
2. Reels → yt-dlp → ❌ Failed → Marked "Download failed" in queue
3. Pipeline continues to next URL

---

## 🟢 Carousel Post Processing Workflow (Working!)

### Discovery
**Carousel posts (`/p/`) work perfectly** via browser vision — no yt-dlp needed!

### Per-Carousel Workflow

#### 1. Navigate to Carousel URL
```bash
browser_navigate("https://www.instagram.com/p/DaBejwDkznl/")
browser_click(close_login_modal)
```

#### 2. Extract Per-Slide Content
```python
for slide_num in range(1, total_slides + 1):
    browser_vision("Analyze slide {slide_num} for educational content")
    browser_click(next_arrow)  # @e153 / @e181 / @e184
```

#### 3. Classify Each Slide Independently
| Slide | Technique | Discipline | Vault Folder |
|-------|-----------|------------|--------------|
| 1 | The Art of Static Shots | Cinematography | Videographer/Cinematography/ |
| 2 | Silhouetting + Atmospheric Depth | Camera Theory | Camera Theory/ |
| 3 | Dutch Angle (Canted) | Composition | Videographer/Composition/ |
| 4 | Layering + Silhouetting | Composition | Videographer/Composition/ |
| 5 | Shallow DOF + Low Angle | Lenses & Optics | Videographer/Lenses & Optics/ |
| 6 | Natural Framing + Negative Space | Composition | Videographer/Composition/ |

#### 4. Generate Assets
| Asset | Tool | Storage |
|-------|------|---------|
| Per-slide screenshots | Browser screenshots | `assets/{post_code}/slide_01.png`... |
| Carousel combined GIF | `ffmpeg -framerate 1 -i slide_%02d.png` | `assets/{post_code}/carousel_combined.gif` |
| Technique comparison grid | `ffmpeg tile=3x2` | `assets/{post_code}/technique_comparison_grid.png` |
| Per-technique assets | Copied from slides | `assets/{discipline}/{category}/{technique}/` |

#### 5. Queue Tracking
| Post Code | Slide | Technique | Discipline | Status |
|-----------|-------|-----------|------------|--------|
| DaBejwDkznl | 1 | Static Shots | Cinematography | ✅ |
| DaBejwDkznl | 2 | Silhouetting | Camera Theory | ✅ |
| DaBejwDkznl | 3 | Dutch Angle | Composition | ✅ |
| ... | ... | ... | ... | ... |

---

## 📊 Session 2025-07-17 Processing Log

### Completed Carousels
| Post Code | Creator | Slides | Techniques | Disciplines |
|-----------|---------|--------|------------|-------------|
| DaBejwDkznl | @anshuluniyyal | 6 | 6 | Cinematography, Camera Theory, Composition, Lenses & Optics |
| Dax2p1aEaB4 | @jb.brandon4 | 9 | 9 | Camera Movement, Lenses & Optics |
| DasrHyOCEWZ | @shadi.3001 | 12+ | 12+ | Camera Theory, Composition, Lighting |
| DaSu0r0mMZM | (unknown) | ? | ? | ? |
| DaVGidIEih_ | (unknown) | ? | ? | ? |
| Dae7IeFCGPu | (unknown) | ? | ? | ? |
| DZhmFCnE5Ks | @openailearning | 12 | 12 | Camera Movement |
| DaLdhlNDZuw | (unknown) | ? | ? | ? |

### Pending Carousels (21 remaining)
```
DaSu0r0mMZM, DaVGidIEih_, Dae7IeFCGPu, DZhmFCnE5Ks, DaLdhlNDZuw,
DaM8mLZo3af (reel?), DaSu0r0mMZM, DaVGidIEih_, Dae7IeFCGPu,
DZhmFCnE5Ks, DaLdhlNDZuw, DaM8mLZo3af, ...
```

### Failed Reels (185+)
```
DaeM5UmIofZ, DavSPEWJtMZ, Dah5kECAgEh, DaWoOJtqIP1, DaM8mLZo3af,
DZpILj3JcgB, DaLR3LKiuT8, DZobVihCQGd, DZRgDZwCvI4, DZUrB0kzybS,
DZAcKFuMe3q, DY9ckzJPsS0, DY1aoKIJnDo, DYE7JNyAR07, DYBbiPUx_Eb,
DW6W6h5k7yr, DXpfJCJiGVc, DR1mNyxjmWg, DU8KlrtE0dT, DXd3tmuDeKv,
... and 165+ more
```

---

## 🎯 Next Session Priorities

1. **Kill failing batch processor** — It's just burning cycles on Reels
2. **Process remaining 21 carousels** via browser vision (one by one)
3. **Decide Reel strategy**:
   - Option A: Implement Playwright-based authenticated downloader
   - Option B: Switch to manual download + pipeline processing
   - Option C: Accept Reel failure, focus on Carousels + YouTube (video-tutorial-extraction)
4. **Document carousel pipeline** in `references/carousel-processing-workflow.md`

---

## 📝 Files Updated This Session

| File | Change |
|------|--------|
| `instagram-videographer-learning-pipeline/SKILL.md` | Added carousel handling, Reel auth pitfall, auto-cleanup details |
| `references/auto-cleanup-workflow.md` | Created — documents MP4/temp cleanup workflow |
| `references/carousel-processing-workflow.md` | Created — carousel vision workflow |
| `references/session-20250717-pipeline-creation.md` | Created — session log |
| `references/session-20250717-carousel-processing.md` | Created — carousel processing log |
| `references/session-20250717-reel-auth-failure.md` | Created — this file |
| `Videographer/VIDEOGRAPHER_QUEUE.md` | Updated with processing log |
| `Videographer/00-MASTER-INDEX.md` | Updated with technique index |
| `Videographer/Cinematography/01-Art-of-Static-Shots_anshuluniyyal_Cinematography.md` | Created |
| `Camera Theory/02-Silhouetting-Atmospheric-Depth_anshuluniyyal.md` | Created |
| `Videographer/Composition/01-Dutch-Angle_anshuluniyyal.md` | Created |
| `Videographer/Composition/02-Layering-Silhouette_anshuluniyyal.md` | Created |
| `Videographer/Lenses & Optics/01-Shallow-DOF-Low-Angle_anshuluniyyal.md` | Created |
| `Videographer/Composition/03-Natural-Framing_anshuluniyyal.md` | Created |
| 6 Hermes skills created | `videographer-{discipline}-{technique}-anshuluniyyal` |

---

*Generated from session 2025-07-17 | Pipeline v1.1.0*