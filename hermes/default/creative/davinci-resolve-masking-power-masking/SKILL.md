---
name: davinci-resolve-masking-power-masking
description: "DaVinci Resolve Power Masking: Radial + Magic Mask + inverted background grade for clean silhouette separation."
version: 0.1.0
author: Hermes
metadata:
  hermes:
    tags: [DaVinci Resolve, Color Grading, Magic Mask, Power Windows, Cinematic]
---

# DaVinci Resolve Power Masking Technique

Learn the **Power Masking** technique from colorist Loris Marie (@loris_marie) — a fast, node-based masking workflow in DaVinci Resolve that combines **Radial Mask** + **Magic Mask** + **Inverted Background Grading** to create clean silhouette separation with dramatic backlight effects.

## When to Use
- Creating clean subject separation from busy backgrounds
- Building strong backlight / silhouette pop effects
- Fast subject isolation without manual rotoscoping
- Creative grading workflows needing clean subject/background separation
- DaVinci Resolve color grading workflows using Magic Mask + Power Windows

## Prerequisites
- DaVinci Resolve Studio (Studio required for Magic Mask / Neural Engine)
- DaVinci Neural Engine enabled (Preferences → Memory & GPU → Enable Neural Engine)
- DaVinci Resolve 18.5+ (Magic Mask improved significantly in 18.5+)
- GPU with adequate VRAM (8GB+ recommended for Magic Mask)

## How to Run
Execute the step-by-step procedure in DaVinci Resolve's Color page using the node graph workflow described in **Procedure**. No external tools required beyond DaVinci Resolve Studio.

## Quick Reference
| Step | Node | Tool | Key Action |
|------|------|------|------------|
| 1 | Node 1 | Power Window → Radial | Draw ellipse around subject |
| 2 | Node 2 | Magic Mask | Draw rough stroke, let Neural Engine refine |
| 3 | Node 3 | Invert Mask (Node 2) | Invert to select background only |
| 4 | Node 3 | Grade | Boost exposure, add warmth/glow to background |
| — | All Nodes | Key Output | Toggle **Key Output** to verify mattes |

## Procedure

### 1. Node 1 — Radial Mask (Subject Isolation)
1. Add a **Serial Node** after your primary grade (label: `Radial Mask`).
2. Open **Power Window** palette → select **Circle / Ellipse** tool.
3. Draw an ellipse around your subject — tight enough to isolate, loose enough to not clip edges.
4. Soften the edge: increase **Softness** (~0.2–0.4) for natural falloff.
5. **Key Output** → enable to verify the radial mask isolates the subject cleanly.

> **Why radial first?** It constrains Magic Mask's search area, preventing it from "grabbing random stuff in the background" — Loris's tip.

### 2. Node 2 — Magic Mask (Precise Silhouette)
1. Add another **Serial Node** after Node 1 (label: `Magic Mask`).
2. Open **Magic Mask** panel (DaVinci Resolve Studio only).
3. Select **Object** mode (person/silhouette).
4. Draw a **rough stroke** across the subject — don't be precise; let Neural Engine do the edge detection.
4. Click **Track Forward / Track Backward** to propagate across the clip.
5. Refine: adjust **Edge Softness**, **Feather**, **Clean Black/White** sliders for a clean matte.
6. **Key Output** → verify: clean silhouette, no background leakage.

> **Magic Mask tip**: It "reads edges and contrast to cut out the silhouette precisely. Way faster than manual brushing." — Loris Marie

### 3. Node 3 — Inverted Background Grade (The "Power" Look)
1. Add a **Serial Node** after Node 2 (label: `BG Grade`).
2. In Node 3's **Key** palette: connect Node 2's **Alpha Output** → Node 3 **Key Input**.
3. **Invert** the key (Key palette → **Invert** checkbox ON).
   - Now Node 3 affects **only the background**.
3. Grade the background:
   - **Exposure** / **Gain**: boost +0.5 to +1.5 stops
   - **Temperature**: push warm (+10 to +30) for golden-hour glow
   - **Tint**: slight magenta/orange for sunset feel
   - **Glow / Bloom** (OpenFX): subtle bloom on highlights for "light hitting behind subject"
4. Optional: add **Vignette** (Power Window → Circle, inverted, soft) to further direct focus.

> **The look**: "Light hitting behind the subject, strong backlight effect, silhouette popping clean off the background."

### 4. Refine & Polish
1. Toggle **Key Output** on each node to verify mattes at each stage.
2. If Magic Mask drifts: add **Keyframe** corrections on problematic frames.
3. For tough edges: add a **Serial Node** before Node 3 with **Matte Finesse** (Matte Finesse OFX) to clean edge halos.
4. Group Nodes 1–3 into a **Compound Node** (right-click → Create Compound Node) for reusability across clips.

## Pitfalls
| Issue | Cause | Fix |
|-------|-------|-----|
| Magic Mask "grabs background" | Radial mask too loose / missing | Tighten radial mask in Node 1; add more strokes in Magic Mask |
| Edge flicker / jitter | Neural Engine temporal inconsistency | Increase **Temporal Stabilization** in Magic Mask; add keyframes |
| Halo / fringing on subject edge | Hard mask edge / no feather | Increase **Softness** on radial; **Feather** + **Clean Black/White** in Magic Mask |
| Background grade affects subject | Key not inverted / alpha not connected | Verify Node 3 Key Input ← Node 2 Alpha; **Invert** ON |
| Magic Mask not available | Not on Resolve Studio / Neural Engine off | Requires Studio + Neural Engine enabled (Preferences → Memory & GPU) |
| Slow Magic Mask tracking | Insufficient GPU VRAM | Lower **Quality** in Magic Mask panel; reduce timeline resolution proxy |

## Verification
1. Scrub timeline: subject silhouette remains clean, background grade holds.
2. Toggle **Key Output** on Node 3 — background should glow/glow, subject untouched.
3. Play back at full resolution: no edge flicker, no halo on subject.
4. Export a still: subject pops cleanly off background with strong backlight look.

## Related Skills & Cross-References
- **davinci_color_grading** — Complete grading workflows including Linear+Gain primary, MCP integration, VLM grading loop, skin tone preservation, film emulation
- **davinci_workflows** — General Resolve editing, Fusion, delivery workflows; see `references/davinci-resolve-mcp.md` for MCP setup
- **davinci-resolve-white-balance-luma-mix** — Clean neutral balance technique (Luma Mix = 0 + RGB Gain)
- **davinci-resolve-mcp-color-grading** — AI-assisted grading with NVIDIA VLM integration

## References
- Source: Instagram post by **@loris_marie** — "Power of Masking 🥶" (July 7, 2026)
- Caption: "Edited with Ultimate Powergrade — link in bio"
- Technique: Radial Mask → Magic Mask → Inverted Background Grade
- DaVinci Resolve Magic Mask docs: https://www.blackmagicdesign.com/products/davinciresolve/features#magicMask