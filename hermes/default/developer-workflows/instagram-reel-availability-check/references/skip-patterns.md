# Skip Pattern Documentation — Instagram Reel Availability Check

Enhanced classification rules for Instagram reel availability checking and content categorization.

---

## Enhanced Classification Logic (v1.1+)

### Content Categories & Routing

| Category | Keywords | Route |
|----------|----------|-------|
| **DaVinci Tutorials** | davinci resolve, davinci, resolve, node, cst, power window, qualifier, magic mask, color wheels, log wheels, hdr wheels, curves, hue vs sat, color warper, lut, kodak 2383, apple log, s-log3, braw, prores raw | ✅ **Process** → DaVinci Knowledge Base |
| **Mobile App Editing** | magimir, snapseed, vsco, picsart, facetune, airbrush, meitu, beautyplus, mobile editing, iphone editing, mobile photo editing, photo editing curves, mobile curves, photo editing mobile | 📸 **Route** → Photography/Lightroom/ |
| **Lightroom (Mobile/Desktop)** | lightroom mobile, lr mobile, lightroom tutorial, point curve, tone curve, rgb curve, color grading panel, hsl panel, calibration panel, masking, adaptive preset, creative profile | 📸 **Route** → Photography/Lightroom/ |
| **Camera Theory** | raw vs log, dynamic range, sensor, bit depth, log curve, gamma curve, camera theory, raw workflow, log workflow, exposure latitude, highlight rolloff, noise floor, transfer function, bit depth, exposure latitude, highlight rolloff, noise floor | 📚 **Reclassify** → Camera Theory/ |
| **Promo/Marketing** | promo, preset pack, lut pack, buy now, link in bio, discount, sale, masterclass promo, lead magnet, dm for link, comment tutorial, guide promo | ⏭️ **Skip** |
| **Meme/Humor** | meme, joke, funny, humor, parody, satire | ⏭️ **Skip** |

---

## Detection Heuristics

### **Vision Analysis Signals** (from browser_vision)

**Mobile App UI Indicators:**
- App-specific tool names (Magimir, Snapseed, VSCO, etc.)
- Mobile gestures (pinch, swipe, tap)
- Phone mockups / app chrome
- Portrait orientation with app UI

**DaVinci Resolve UI Indicators:**
- Node graph visible
- Color wheels (Primary/Log/HDR)
- Scopes (Parade/Vectorscope/Waveform)
- Timeline with clips
- CST nodes visible

**Promo Text Indicators:**
- "Link in bio"
- "Comment X for link"
- "DM me for access"
- "Preset pack"
- "Masterclass"
- "50+ page guide"
- "Link in bio"

**Meme Indicators:**
- Exaggerated reactions
- "POV:" text overlays
- "When you..." format
- Humor formatting

**Lightroom UI Indicators:**
- Tone curve panel
- Color grading panel
- HSL panel
- Masking tools
- Mobile app chrome

**Age-Restricted Indicators:**
- "Age-restricted content"
- "Log in to continue"
- "This content is age-restricted"

**Removed/Unavailable Indicators:**
- "Content unavailable"
- "Page not found"
- "This reel isn't available"

---

### **Profile-Level Signals**
- Handle patterns: `*.app`, `*mobile*`, `*preset*`, `*pack*`
- Bio keywords: "Presets available", "Link in bio", "Course", "Masterclass"

---

## Skip Pattern Configuration

```yaml
# Hard skip (don't process)
skip_patterns:
  - "promo"
  - "preset pack"
  - "lut pack"
  - "buy now"
  - "link in bio"
  - "discount"
  - "sale"
  - "meme"
  - "joke"
  - "funny"
  - "parody"
  - "satire"
  - "comment.*tutorial"
  - "dm.*link"
  - "link in bio"
  - "lead magnet"
  - "guide.*promo"
  - "masterclass promo"

# Route to Photography/Lightroom (don't skip, just re-route)
route_to_photography_patterns:
  - "magimir"
  - "snapseed"
  - "vsco"
  - "picsart"
  - "facetune"
  - "airbrush"
  - "meitu"
  - "beautyplus"
  - "lightroom mobile"
  - "lr mobile"
  - "mobile editing"
  - "iphone editing"
  - "mobile photo editing"
  - "photo editing curves"
  - "mobile curves"
  - "point curve"
  - "tone curve"
  - "rgb curve"
  - "hsl panel"
  - "calibration panel"
  - "masking"
  - "adaptive preset"
  - "creative profile"

# Reclassify to Camera Theory (don't skip)
camera_theory_patterns:
  - "raw vs log"
  - "dynamic range"
  - "sensor"
  - "bit depth"
  - "log curve"
  - "gamma curve"
  - "camera theory"
  - "raw workflow"
  - "log workflow"
  - "exposure latitude"
  - "highlight rolloff"
  - "noise floor"
  - "transfer function"
  - "bit depth"
  - "exposure latitude"
  - "highlight rolloff"
  - "noise floor"
```

---

## Classification Decision Tree

```
URL → Extract Content (caption + vision)
       │
       ├─ Age-restricted? → 🔒 AGE-RESTRICTED
       ├─ Removed/Unavailable? → ❌ REMOVED
       ├─ Contains HARD_SKIP keywords? → ⏭️ SKIP
       ├─ Contains ROUTE_TO_PHOTOGRAPHY? → 📸 PHOTOGRAPHY/LIGHTROOM
       ├─ Contains CAMERA_THEORY keywords? → 📚 CAMERA THEORY
       ├─ Contains DAVINCI_POSITIVE signals? → ✅ PROCESS (DaVinci KB)
       └─ Ambiguous? → 🤔 FLAG FOR REVIEW
```

---

## Real-World Examples from Session

| Reel | Creator | Classification | Action |
|------|---------|----------------|--------|
| DFagthrsgkF | creatorsergeant | Qualifier Focus | ✅ Process |
| DFX8xhsuBwC | brattphotoandfilm | Promo (LUT pack) | ⏭️ Skip |
| DFHPXTyMGA_ | caleboshi | Promo (Course + Free LUT) | ⏭️ Skip |
| DFQOtTcMeD9 | creatorsergeant | Photography/Lightroom (Carousel - Halation) | 📸 Photography |
| DDzf-sTNsVk | shotbysammy_ | Custom Kodak 2383 LUT Design | ✅ Process |
| DD7eTVHxCWl | anybodyshoots | ChatGPT LUT Experiment | ⏭️ Skip (Not Educational) |
| DEks7VbRH97 | caleboshi | Moody Cinematic Greens | ✅ Process |
| DElH7btvMia | aparicio.co | Noise Reduction Part 1 (Temporal) | ✅ Process |
| DEfoV8CyH98 | davinciresolved | Before/After Effect | ✅ Process |
| DENpNOGNE0R | meliorstudios | Sky Color Isolation (HDR Wheels) | ✅ Process |
| DFgheS3ylWy | lowlight.co | Camera Theory (RAW vs LOG) | 📚 Camera Theory |
| DFQOtTcMeD9 | creatorsergeant | Photography/Lightroom (Halation carousel) | 📸 Photography |
| C_rm3h-zMM2 | colorgradeshala | Age-Restricted | 🔒 Age-Restricted |
| C9m9A2SpR-_ | davinciresolved | Super 8 Film Look (Dehancer) | ✅ Process |
| C--Rx3TpMJQ | theqazman | Photographer's Split Toning | 📸 Photography |

---

*Updated: 2025-07-14 — Based on comprehensive session analysis of 161 unique Instagram URLs with browser vision confirmation.*