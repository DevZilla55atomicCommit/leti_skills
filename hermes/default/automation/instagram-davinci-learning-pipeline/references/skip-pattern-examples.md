# Skip Pattern Examples — Instagram Learning Pipeline

Real-world examples of content that should be auto-skipped or reclassified by the pipeline's classification logic.

---

## 📱 Mobile App Editing (Not DaVinci Resolve)

### **@magimirrai — Magimir App** ⭐ *Confirmed 2025-07-14*
- **URL Pattern**: `instagram.com/reel/...` from @magimirrai
- **Content**: Mobile photo editing tutorials using the **Magimir app**
- **Visual Signals** (from browser vision): Before/after portrait splits, "Skin Removal", "Neutral Gray", "high-quality portrait is finished", mobile UI overlays, app-specific feature callouts
- **Skip Reason**: Not DaVinci Resolve — mobile app editing
- **Auto-Detection Keywords**: `magimir`, `mobile`, `app`, `smartphone`, `iphone editing`, `lightroom mobile`, `snapseed`, `vsco`, `picsart`, `facetune`, `airbrush`, `meitu`, `beautyplus`

### **@moizxmhd — Lightroom Mobile**
- **Content**: Lightroom mobile vintage pastel tutorial
- **Skip Reason**: Lightroom, not DaVinci Resolve
- **Auto-Detection**: `lightroom`, `lr mobile`, `mobile preset`

### **@mahi_photography_editing — VN/Other Mobile Apps**
- **Content**: Best color grading settings for urban footage
- **Visual Signals**: Mobile UI overlays, app-specific feature callouts
- **Skip Reason**: Not DaVinci Resolve — mobile app editing

---

## 📸 Lightroom & Mobile Editing (New Category — Route to Photography/Lightroom/)

### **@magimirrai — Color Curves Tutorial (Magimir App)** ⭐ *Confirmed 2025-07-14*
- **Content**: "Color Grading Feels Easy Once You Truly Understand Curves" — but demonstrated in Magimir mobile app
- **Action**: **Route to Photography/Lightroom/** — technique is valid (curves for color grading), tool is mobile
- **Auto-Detection**: `tone curve`, `point curve`, `rgb curve`, `curves tutorial`, `color curves`, `mobile curves`, `photo editing curves`, `mobile curves`, `photo editing curves`
- **Vault Path**: `Photography/Lightroom/NN-Tone-Curve-Mastery_Magimir_Point-Curve-RGB.md`

### **@hue_black — Lightroom Mobile Tips**
- **Content**: "Secret Tool for Dramatic Photos" — Radial Mask + Feathering
- **Category**: Lightroom Mobile / Masking
- **Vault Path**: `Photography/Lightroom/NN-Dramatic-Photos-Radial-Mask_HueBlack_Lightroom-Masking.md`

### **@hue_black — Skin Tone Fixes (Lightroom Mobile)**
- **Content**: "Fix you skin tones in 3 simple steps"
- **Category**: Lightroom Mobile / Skin Tones
- **Vault Path**: `Photography/Lightroom/NN-Skin-Tones-3-Steps_HueBlack_Lightroom-Mobile.md`

### **General Lightroom Mobile Creators**
- **Keywords**: `lightroom mobile`, `lr mobile`, `mobile editing`, `iphone editing`, `mobile photography`, `photo editing`, `tone curve`, `point curve`, `rgb curve`, `color grading panel`, `calibration panel`, `hsl panel`, `masking`, `adaptive preset`, `creative profile`, `mobile curves`, `photo editing curves`, `mobile photo editing`
- **Route**: `Photography/Lightroom/` (not skipped, just re-routed)

---

## 📢 Promo/Marketing Content

### **@c.vladmanea — Color Grading Guide Promo**
- **Content**: "50+ page professional color grading guide" promo video (comment "Tutorial" for DM link)
- **Skip Reason**: Marketing for lead magnet, not the technique itself
- **Auto-Detection**: `promo`, `lead magnet`, `dm for link`, `comment.*tutorial`, `guide.*promo`, `masterclass promo`

### **@jacob.wagler — Cinematic Preset Pack Promo**
- **Content**: Preset pack marketing reel
- **Skip Reason**: Selling product, not teaching technique
- **Auto-Detection**: `preset pack`, `lut pack`, `buy now`, `link in bio`, `discount`, `sale`

### **@filmsbychristian — Meme/Joke Content**
- **Content**: Humor/meme reel, not educational
- **Skip Reason**: Entertainment, not color grading education
- **Auto-Detection**: `meme`, `joke`, `funny`, `humor`, `parody`, `satire`

---

## 🎥 Camera Theory (Reclassified — Not Skipped)

### **@lowlight.co — RAW vs LOG Fundamentals**
- **Content**: General camera theory (RAW vs Log, dynamic range, sensor science)
- **Action**: **Reclassified to Camera Theory** → vault note created
- **Auto-Detection**: `raw vs log`, `dynamic range`, `sensor`, `bit depth`, `camera theory`, `log curve`, `gamma curve`, `exposure latitude`, `highlight rolloff`, `noise floor`

---

## 🔍 Detection Heuristics for Pipeline

### **Hard Skip Keywords** (in caption, hashtags, or visual text)
```yaml
promo, marketing, preset pack, lut pack, buy, sale, discount,
lightroom, lr mobile, photoshop mobile, snapseed, vsco, picsart,
magimir, facetune, airbrush, meitu, beautyplus,
meme, joke, funny, humor, parody, satire,
comment.*tutorial, dm.*link, link in bio, check bio
```

### **Camera Theory Keywords** (reclassify, don't skip)
```yaml
raw vs log, dynamic range, sensor, bit depth, log curve,
gamma curve, camera theory, raw workflow, log workflow,
exposure latitude, highlight rolloff, noise floor
```

### **Lightroom/Mobile Editing Keywords** (route to Photography/Lightroom/)
```yaml
lightroom mobile, lr mobile, mobile editing, iphone editing,
mobile photography, photo editing, tone curve, point curve,
rgb curve, color grading panel, calibration panel, hsl panel,
masking, adaptive preset, preset, creative profile,
magimir, snapseed, vsco, picsart, facetune, airbrush, meitu,
beautyplus, mobile curves, photo editing curves, mobile photo editing
```

### **DaVinci Positive Signals** (boost confidence)
```yaml
davinci resolve, davinci, resolve, node, cst, color space transform,
power window, qualifier, magic mask, color wheels, log wheels,
hdr wheels, curves, hue vs sat, hue vs hue, hue vs lum,
color warper, color slice, texture pop, film grain, halation,
lut, kodak 2383, fuji, kodak film, film emulation,
apple log, s-log3, slog3, braw, prores raw, dwg
```

---

## 📊 Classification Decision Tree

```
URL → Extract Content (caption + vision)
       │
       ├─ Contains HARD_SKIP keywords? → ⏭️ SKIP (Not DaVinci / Promo / Meme)
       │
       ├─ Contains LIGHTROOM_MOBILE keywords? → 📸 ROUTE → Photography/Lightroom/
       │
       ├─ Contains CAMERA_THEORY keywords? → 📚 RECLASSIFY → Camera Theory/
       │
       ├─ Contains DAVINCI_POSITIVE signals? → ✅ PROCESS → Categorize by technique
       │
       └─ Ambiguous? → 🤔 Flag for manual review
```

---

## 🛠️ Pipeline Integration Notes

### **Vision Analysis Signals** (from browser_vision)
When `browser_vision` analyzes a reel page, look for:
- **Mobile app UI**: App-specific tool names, mobile gestures, phone mockups
- **DaVinci UI**: Node graph, color wheels, scopes (parade/vectorscope), timeline, CST nodes
- **Promo text**: "Link in bio", "Comment X for link", "DM me", "Preset pack", "Masterclass"
- **Meme indicators**: Exaggerated reactions, text overlays like "POV:", "When you...", humor formatting
- **Lightroom UI**: Tone curve panel, color grading panel, HSL panel, masking tools, mobile app chrome

### **Profile-Level Signals**
- Handle patterns: `*.app`, `*mobile*`, `*preset*`, `*pack*`
- Bio keywords: "Presets available", "Link in bio", "Course", "Masterclass"

---

## 📁 Vault Routing Rules (Updated 2025-07-14)

| Category | Vault Path | Skill Prefix |
|----------|------------|--------------|
| DaVinci Color Grading | `DaVinci_Knowledge_Base/Color Correction Fundamentals/` | `davinci-resolve-` |
| DaVinci Creative Looks | `DaVinci_Knowledge_Base/Creative Grading & Looks/` | `davinci-resolve-` |
| Camera Theory | `DaVinci_Knowledge_Base/Camera Theory/` | `davinci-resolve-` |
| **Lightroom Mobile** | **`Photography/Lightroom/`** | **`lightroom-` (new)** |
| Photo Editing Theory | `Photography/Color Theory & Techniques/` (planned) | `photo-` (new) |

---

## 🔍 Cross-References

| Skill | Topic |
|-------|-------|
| `davinci-resolve-qualifier-focus-color-page` | Qualifier precision masking |
| `davinci-resolve-hue-vs-hue-skin-protection` | Skin tone locking on Hue vs Hue |
| `davinci-resolve-power-masking` | Power Window + Qualifier combo |
| `davinci-resolve-skin-separation-layermixer-qualifier` | Skin isolation with Layer Mixer |
| `davinci-resolve-color-warper-saturation-balance` | Sat vs Sat density control |

---

*Updated: 2025-07-14 — Based on session analysis of @magimirrai reel (Magimir mobile app editing) with browser vision confirmation. Added Lightroom/Mobile Editing routing to Photography vault.*

---

## 🎬 Video Effects Skip/Route Patterns (New — 2025-07-15)

### **Video Effects Positive Signals** (boost confidence for Video Effects pipeline)
```yaml
davinci resolve transition, davinci resolve composite, davinci resolve vfx,
fusion composite, fusion vfx, fusion motion graphics,
power window transition, mask transition, alpha transition,
chroma key, luma key, rotoscope, rotoscoping,
lower third, kinetic type, title animation,
particle effect, explosion, fire, smoke, energy,
glitch, vhs, film damage, film burn, light leaks,
speed ramp, time remap, freeze frame, optical flow
```

### **Video Effects Routing Rules**

| Category | Vault Path | Skill Prefix |
|----------|------------|--------------|
| Transitions | `Video_Effects/transitions/` | `davinci-resolve-` |
| Compositing | `Video_Effects/compositing/` | `davinci-resolve-` |
| Motion Graphics | `Video_Effects/motion-graphics/` | `davinci-resolve-` |
| VFX | `Video_Effects/vfx/` | `davinci-resolve-` |
| Text Effects | `Video_Effects/text-effects/` | `davinci-resolve-` |
| Stylization | `Video_Effects/stylization/` | `davinci-resolve-` |
| Time Effects | `Video_Effects/time-effects/` | `davinci-resolve-` |

### **Detection Heuristics for Video Effects**

**Vision Analysis Signals:**
- **Transition demos**: Before/after split screen, A/B comparison, side-by-side
- **Compositing**: Green screen visible, matte/alpha channel shown, keying parameters
- **Motion Graphics**: Lower thirds, animated text, callout boxes, title sequences
- **VFX**: Particle systems, 3D elements, simulation controls, emitter settings
- **Stylization**: Glitch artifacts, film grain, color channel separation, scanlines
- **Time Effects**: Speed graph, retime curve, frame interpolation settings

**Profile-Level Signals:**
- Handles: `*effects*`, `*transition*`, `*vfx*`, `*motion*`, `*composite*`
- Bio: "VFX artist", "Motion designer", "Transition tutorials", "DaVinci Resolve effects"