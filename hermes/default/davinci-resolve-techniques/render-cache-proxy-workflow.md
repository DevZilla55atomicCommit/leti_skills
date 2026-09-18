---
name: 'render-cache-proxy-workflow'
description: 'Optimize playback performance with Render Cache (Smart/User/None), Optimized Media, and Proxy generation — background caching for Fusion transitions and heavy grades.'
category: 'davinci-resolve-techniques'
tags: ['edit-page', 'color-page', 'render-cache', 'optimized-media', 'proxy', 'performance', 'playback', 'fusion']
---

# Render Cache Proxy Workflow

**Category:** davinci-resolve-techniques  
**Resolve Page:** Edit / Color / Deliver  
**Node Graph:** N/A  
**Tags:** edit-page, color-page, render-cache, optimized-media, proxy, performance, playback, fusion

---

## Overview

Optimize playback performance with Render Cache (Smart/User/None), Optimized Media, and Proxy generation — background caching for Fusion transitions and heavy grades.

This skill covers 4 related techniques extracted from 4 Instagram Reel analyses.

### Techniques Covered
- Fix Laggy Fusion Transitions (Render Cache / Proxy)
- Render in Place (Workflow Optimization)
- Cache Clip Management
- Managing Cache Clips

---

## Key Nodes & Tools
- **Playback → Render Cache**
- **Project Settings → Master Settings → Optimized Media**
- **Clip → Render in Place**
- **Project Settings → Cache Location**

---

## Parameters & Settings

### Render Cache Modes
- None
- User
- Smart (auto)

### Cache Formats
- DNxHR HQ
- ProRes 422 HQ
- ProRes LT

### Optimized Media
- Lower-res proxy for editing

### Proxy Media
- Custom proxy files (external)

### Render In Place
- Bakes grade+effects to new clip (Ctrl+R)

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
