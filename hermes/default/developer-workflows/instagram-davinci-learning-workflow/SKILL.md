---
name: instagram-davinci-learning-workflow
description: "Automate Instagram→DaVinci vault pipeline: extract techniques, create skills, update indices."
version: 0.1.0
author: Hermes
metadata:
  hermes:
    tags: [Instagram, DaVinci Resolve, Color Grading, Automation, Vault, Skills]
---

# Instagram → DaVinci Knowledge Base Learning Workflow

Automates the end-to-end pipeline: **Instagram URLs → Technique Extraction → Hermes Skill → Vault File → Index Updates**.

## When to Use
- Batch-processing Instagram Reels/posts from colorists/educators
- Building a curated DaVinci Resolve technique library in Obsidian
- Creating reusable Hermes skills from social media content
- Maintaining cross-referenced vault indices (category, master map, queue)

## Prerequisites
- Hermes Agent with browser tools (`browser_navigate`, `browser_vision`, `browser_snapshot`)
- `skill_manage` tool for skill creation
- `write_file` / `patch` / `read_file` for vault operations
- DaVinci Knowledge Base vault structure at `/Users/alfredkamisese/TamaZila Obsidian Vault/Hermes Agent/DaVinci_Knowledge_Base/`
- Instagram Learning Queue file at `DaVinci_Knowledge_Base/Instagram_Learning_Queue.md`

## How to Run
1. Add URLs to `Instagram_Learning_Queue.md` (Queue table)
2. Invoke this workflow via Hermes (or run steps manually)
3. Each URL gets: skill + vault file + index updates + queue status flip

## Quick Reference

| Step | Tool | Purpose |
|------|------|---------|
| 1 | `read_file` | Load queue file |
| 2 | `browser_navigate` | Open Instagram URL |
| 3 | `browser_vision` | Analyze thumbnail/video frames |
| 4 | `browser_snapshot` | Extract caption + comments |
| 5 | `skill_manage create` | Create Hermes skill |
| 6 | `write_file` | Save vault technique file |
| 7 | `patch` | Update category `00-MASTER-INDEX.md` |
| 8 | `patch` | Update `Memory.md` master map |
| 9 | `patch` | Move queue row: Pending → Completed |

## Procedure

### 1. Load Queue & Pick Next URL
```python
# Read queue file
queue_content = read_file("DaVinci_Knowledge_Base/Instagram_Learning_Queue.md")
# Parse markdown table, find first row with Status = "⏳ Pending"
# Extract: URL, Context/Focus, Priority
```

### 2. Extract Instagram Content
```bash
# Navigate to URL
browser_navigate(url="https://www.instagram.com/p/XXXX/")

# Dismiss login modal if present
browser_click(ref="close_button_ref")

# Get full page snapshot for caption + comments
snap = browser_snapshot(full=true)

# Analyze video frames / carousel images
images = browser_get_images()
for img in images:
    if "carousel" in img.alt or "video" in img.alt:
        vision = browser_vision(image_url=img.src, question="Extract all text, UI elements, node graphs, settings, before/after comparisons, color wheels, scopes, text overlays from this color grading educational content")
```

### 3. Classify Technique & Determine Category
Map extracted content to vault category:

| Keywords | Category Folder |
|----------|-----------------|
| mask, magic mask, power window, qualifier, rotoscope | `Masking & Power Windows` |
| white balance, luma mix, printer lights, primary, exposure, scopes | `Color Correction Fundamentals` |
| node structure, cst, dwg, gain pivot, color management | `Cinematic Grading Workflows` |
| teal orange, complementary, creative look, film emulation, halation, diffusion | `Creative Grading & Looks` |
| automotive, car, vehicle, tracking | `Automotive & Specialty` |
| skin tone, qualifier, layer node, hue vs hue | `Skin Tones` |
| s-log3, sony, cst pipeline | `S-Log3 / Sony Workflows` |
| apple log, iphone, rec2020 | `Apple Log 2 / iPhone` |
| kodak 2383, film emulation, lut, dctl | `Kodak 2383 / Film Emulation` |

### 4. Create Hermes Skill
```yaml
# skill_manage create
name: "davinci-resolve-<technique-slug>"
category: "creative"
content: |
  ---
  name: davinci-resolve-<technique-slug>
  description: "<=60 chars: DaVinci Resolve <technique>: <key tools> for <outcome>."
  version: 0.1.0
  author: Hermes
  metadata:
    hermes:
      tags: [DaVinci Resolve, Color Grading, <Key Tools>, <Creative/Technical>]
  ---

  # DaVinci Resolve <Technique Name>

  Learn the **<Technique>** from @<source> — <one-sentence summary>.

  ## When to Use
  - <use case 1>
  - <use case 2>

  ## Prerequisites
  - DaVinci Resolve <Free/Studio> <version>
  - <specific requirements>

  ## Quick Reference
  | Step | Node | Tool | Key Action |
  |------|------|------|------------|

  ## Procedure
  ### 1. Node 01 — <Name>
  ...
  ### 2. Node 02 — <Name>
  ...

  ## Pitfalls
  | Issue | Cause | Fix |

  ## Verification
  1. <check 1>
  2. <check 2>

  ## References
  - Source: Instagram @<handle> — "<caption excerpt>"
  - Hashtags: #davinciresolve #colorgrading ...
```

### 5. Write Vault Technique File
```markdown
# <Technique Name> — <Source Handle>

**Vault Path:** `Color Grading & Looks/<Category>/`
**File:** `<NN>-<Technique>_<Source>_<Key-Tools>.md`
**Source:** Instagram @<handle> — "<caption>" (date)
**Technique:** <one-line summary>

---

## 🎬 Technique Overview
...

## 🏗️ Complete Node Graph
(ASCII diagram)

## ⚙️ Step-by-Step Procedure
### NODE 01 — <Name>
| Setting | Value | Why |
|---------|-------|-----|

...

## 🎯 Key Principles
| Principle | Application |

## ⚠️ Common Pitfalls
| Symptom | Cause | Fix |

## ✅ Verification Checklist
- [ ] ...

## 🔗 Cross-References
| Topic | File |

## 🏷️ Obsidian Tags
```markdown
#davinci-resolve #<tags>
```

## 📅 Revision Log
| Date | Version | Notes |
```

**Naming Convention:** `NN-Technique_Source_KeyTools.md` (NN = 2-digit sequence per category)

### 6. Update Category Master Index (`00-MASTER-INDEX.md`)
```markdown
# Patch the File Index table:
| **NN** | [Technique Name](filename.md) | @source | Technique summary | Key focus |
```

### 7. Update DaVinci Master Map (`Memory.md`)
```markdown
# Patch the appropriate category section:
### 🎨 Creative Grading & Looks (NEW)
*   **[Technique — @source]** :: `path/to/file.md` — One-line summary.
```

### 8. Update Learning Queue (`Instagram_Learning_Queue.md`)
```markdown
# Move row from Queue → Completed:
| # | URL | Source | Technique | Skill | Vault File | Date |
|---|-----|--------|-----------|-------|------------|------|
| N | [link](url) | @handle | Summary | `skill-name` | `Category/file.md` | YYYY-MM-DD |
```

## Pitfalls
| Issue | Cause | Fix |
|-------|-------|-----|
| Instagram login modal blocks content | Bot detection | Click close button (ref from snapshot) before snapshot |
| Carousel/video frames not captured | Dynamic loading | Use `browser_vision` on each image URL from `browser_get_images()` |
| Skill description >60 chars | Verbose summary | Trim to capability only, no marketing words |
| Duplicate category file number | Manual count off | Read category folder, count existing `NN-` files, increment |
| Broken relative links in vault | Wrong depth | Use `../../Memory.md` from category folder, `../../../../index.md` from root |

## Verification
After processing a URL:
1. ✅ Skill loads: `skill_view(name='davinci-resolve-<slug>')`
2. ✅ Vault file exists and renders in Obsidian
3. ✅ Category `00-MASTER-INDEX.md` shows new row
4. ✅ `Memory.md` has new entry in correct section
5. ✅ Queue file shows "✅ Done" with links
6. ✅ All relative links resolve (test in Obsidian)

## Related Skills
- `hermes-agent-skill-authoring` — SKILL.md format standards
- `web-research-and-scraping` — General web→vault patterns
- `developer-workflows` — Professional automation patterns