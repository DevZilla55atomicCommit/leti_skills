# Power Masking — Loris Marie (@loris_marie) Session Capture

**Date:** July 7, 2025
**Source:** Instagram post https://www.instagram.com/p/Daf3Pdain5r/
**Creator:** @loris_marie (Verified French colorist/photographer 🇫🇷)

---

## Original Caption (Full Text)

> Power of Masking 🥶
>
> (Edited with Ultimate Powergrade - link in bio )
>
> Mask Tip :
>
> Start with the radial mask: drop an ellipse around your subject to isolate that zone without touching the rest. This keeps the next mask from grabbing random stuff in the background.
>
> Then magic mask: it reads the edges and contrast to cut out the silhouette precisely. Way faster than manual brushing.
>
> Once the silhouette's clean, invert the selection and work only on the background: boost exposure, add warmth or a glow. End result: light hitting behind the subject, strong backlight effect, silhouette popping clean off the background.

---

## Technique Summary

**3-Node Serial Chain:** Radial Mask → Magic Mask → Inverted Background Grade
**Creative Intent:** Clean subject isolation + dramatic backlight separation ("silhouette popping clean off background")
**Time Savings:** Seconds vs. hours of manual rotoscoping

---

## Complete Node Settings (Reference)

### Node 01: Radial Mask
```yaml
Node Type: Serial (after primary grade)
Label: "Radial Mask"
Power Window:
  Shape: Ellipse
  Position: Subject center
  Size: Tight + 10-15% padding
  Softness: 0.3 (0.2-0.4 range)
  Symmetry: Adjust per subject proportions
Key Output: ENABLED
```

### Node 02: Magic Mask
```yaml
Node Type: Serial (after Node 01)
Label: "Magic Mask"
Panel: Magic Mask (Studio only)
Mode: Object → Person
Stroke: Single rough stroke across subject torso
Track Forward: ENABLED
Track Backward: ENABLED
Edge Softness: 4 px
Feather: 2 px
Clean Black: 0.02 (2%)
Clean White: 0.98 (98%)
Temporal Stabilization: ON (High)
Quality: High (or Auto)
Key Output: ENABLED
```

### Node 03: BG Grade (Inverted)
```yaml
Node Type: Serial (after Node 02)
Label: "BG Grade"
Key Input: ← Node 02 Alpha Output
Key Invert: ENABLED (checkbox ON)
Primary Wheels:
  Gain: +0.8 stops
  Temperature: +20
  Tint: +10
  Contrast: +10
  Pivot: 0.4
OpenFX (optional, on same node or new serial):
  - Glow: Threshold 0.75, Radius 30, Intensity 0.4
  - Bloom: Threshold 0.7, Radius 25, Intensity 0.3
Key Output: ENABLED
```

---

## Vault Integration

**Files Created:**
- `DaVinci_Knowledge_Base/Color Grading & Looks/Masking & Power Windows/00-MASTER-INDEX.md`
- `DaVinci_Knowledge_Base/Color Grading & Looks/Masking & Power Windows/01-Power-Masking_Loris-Marie_Radial-MagicMask-InvertedBG-Workflow.md`

**Master Map Updated:** `DaVinci_Knowledge_Base/Memory.md` — Added "Masking & Power Windows" category under YouTube Tutorials.

---

## Related Techniques in Vault

| Technique | Location | Relationship |
|-----------|----------|--------------|
| Layer Node Skin Protection | `Skin Tones/Skin-Tones_Layer-Node-Teal-Orange-Protection.md` | Combine with BG Grade to protect subject edges |
| Qualifier Skin Workflow | `Skin Tones/Skin-Tones_Qualifier-Vectorscope-Workflow.md` | Alternative isolation method |
| S-Log3 Portrait PowerGrade | `S-Log3/S-Log3_Mehran-Haddad_Resolve21-Portrait-PowerGrade.md` | Similar creative intent (subject pop) |

---

## Skill Integration

This technique is also saved as Hermes skill:
- **Skill:** `davinci-resolve-masking-power-masking` (creative category)
- **Use:** `skill_view(name='davinci-resolve-masking-power-masking')` for quick reference during grading