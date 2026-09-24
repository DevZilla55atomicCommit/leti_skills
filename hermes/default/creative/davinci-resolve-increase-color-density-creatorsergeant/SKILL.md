---
name: davinci-resolve-increase-color-density-creatorsergeant
description: "Increase Color Density — @creatorsergeant DaVinci Resolve technique (Density vs HSV Saturation vs Normal Saturation)"
version: 0.1.0
author: Hermes
metadata:
  hermes:
    tags: [DaVinci Resolve, Color Grading, Density, Saturation, HSV, Color Warper, Curves, Cinematic]
---

# Increase Color Density — @creatorsergeant

Technique for increasing color density (subtractive saturation) vs regular saturation in DaVinci Resolve.

## When to Use
- Richer, more cinematic colors without oversaturation
- Understanding density vs saturation vs HSV saturation
- Film-like color rendering

## Prerequisites
- DaVinci Resolve (Free or Studio)
- Color Warper (Studio) or Custom Curves (Free)

## Quick Reference

| Method | Mechanism | Effect | Best For |
|--------|-----------|--------|----------|
| **Normal Saturation** | Additive (pushes RGB equally) | Can clip, looks digital | Quick boost |
| **HSV Saturation** | Intensifies hue, maintains luma | Neutral saturation | Controlled saturation |
| **Density (Subtractive)** | Reduces luminance of saturated hues | Film-like, rich, no clipping | Cinematic look |

---

## Density Technique

### Studio: Color Warper
1. Open Color Warper
2. Switch to **Density** mode (not Saturation)
3. Increase density for target hues
4. Luminance drops as saturation increases → filmic

### Free: Hue vs Lum Curves
1. Custom Curves → Hue vs Lum
2. **Lower luminance** for saturated hue ranges
3. Creates "subtractive saturation" effect

---

## Community Insight (from comments)

> "Density reduces the luminosity of the respective hue to intensify the color. HSV saturation attempts to maintain the luminosity as much as possible. Every method of adding saturation has its use case. Generally, however, you'll probably mainly need HSV and density." — @_daniel.pk

---

## Verification Checklist

- [ ] Compare Normal Sat vs HSV Sat vs Density
- [ ] Test on skin tones (protect via qualifier)
- [ ] Verify no highlight clipping
- [ ] Check Vectorscope for natural spread

---

## References

- Source: Instagram @creatorsergeant — "How to increase the density of your colors" (51 weeks ago)
- Type: Video Reel (technique demo)
- Community: High engagement, technical discussion in comments

---

## Tags

```markdown
#davinci-resolve #density #saturation #hsv #color-warper #hue-vs-lum #cinematic #creatorsergeant #subtractive-saturation
```