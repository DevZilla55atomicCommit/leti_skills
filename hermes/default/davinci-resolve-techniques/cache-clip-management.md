---
name: 'cache-clip-management'
description: 'Manage Render Cache, Optimized Media, and Proxy files — locate cache directories, clear caches, relink proxies, and monitor disk usage.'
category: 'davinci-resolve-techniques'
tags: ['workflow', 'project-settings', 'cache', 'optimized-media', 'proxy', 'disk-management', 'performance']
---

# Cache Clip Management

**Category:** davinci-resolve-techniques  
**Resolve Page:** Project Settings / Edit / Color  
**Node Graph:** N/A  
**Tags:** workflow, project-settings, cache, optimized-media, proxy, disk-management, performance

---

## Overview

Manage Render Cache, Optimized Media, and Proxy files — locate cache directories, clear caches, relink proxies, and monitor disk usage.

This skill covers 2 related techniques extracted from 2 Instagram Reel analyses.

### Techniques Covered
- Cache Clip Management
- Managing Cache Clips

---

## Key Nodes & Tools
- **Project Settings → Master → Cache Location**
- **Playback → Render Cache**
- **Clip → Generate Optimized Media**

---

## Parameters & Settings

### Cache Location
- Project Settings → Master Settings → Working Folders → Cache Files

### Cache Formats
- DNxHR HQ
- ProRes 422 HQ
- ProRes LT

### Auto Cache
- Playback → Render Cache → Smart

### Cleanup
- Delete render cache files via Playback menu or manually in cache folder

### Proxy Workflow
- Attach proxy → Playback → Proxy Mode → Prefer Proxy

---

## Typical Workflow
1. **Import & Organize** — Add clips to timeline, create Color page version
2. **Base Correction** — Serial Node 1: White Balance, Exposure, Contrast (Primary Wheels)
3. **Technical Transform** — CST/LUT node for log→Rec.709 if needed
4. **Creative Grade** — Additional serial nodes for look development
5. **Local Adjustments** — Power Windows, Qualifiers, Magic Mask for isolation
6. **Texture & Finish** — Film grain, halation, sharpening, noise reduction
7. **Review & Deliver** — Toggle grades, compare versions, render

---

## Related Skills
- `davinci-resolve-techniques/serial-node-grading-workflow`
- `davinci-resolve-techniques/custom-curves-contrast-adjustment`
- `davinci-resolve-techniques/hsl-curves-qualifier-techniques`
- `davinci-resolve-techniques/power-windows-zone-grading`
- `davinci-resolve-techniques/magic-mask-ai-tracking`
- `davinci-resolve-techniques/noise-reduction-spatial-temporal`
- `davinci-resolve-techniques/render-cache-proxy-workflow`

---

## Source
Generated from 453 completed vision analyses of Instagram Reels (DaVinci Resolve techniques) — `VISION_PROGRESS.json`
