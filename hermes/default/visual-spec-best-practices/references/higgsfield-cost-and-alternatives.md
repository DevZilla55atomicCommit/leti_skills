# Higgsfield Cost and Local Alternatives

## Pricing (as of 2026-08-08)
- **Free Tier**: Limited use, likely a few generations only.
- **Starter**: $19/month (billed annually) → 270 credits/month (~15 Seedance 2.0 Fast videos or 135 Nano Banana Pro images).
- **Plus**: $47/month (billed annually) → 1,200 credits/month (~53 Seedance 2.0 videos or 600 Nano Banana Pro images).
- **Ultra**: $99/month (billed annually) → 3,000 credits/month (~133 Seedance 2.0 videos or 1,500 Nano Banana Pro images).

## Access Model
- **Paid tiers only**: All "Unlimited & Free Gens" models (Nano Banana Pro, Nano Banana 2, Kling 3.0) are **exclusively accessible via the web UI**, not via MCP/CLI/Canvas/Supercomputer.

## Local Free Alternatives
| Goal | Tool | Approx. Cost | Notes |
|------|------|--------------|-------|
| Short video clips (2‑4 s) | **SD 1.5 + AnimateDiff** | Free (disk ≈ 15 GB) | Organic motion, low control. |
| Procedural 3D motion graphics | **Blender + Geometry Nodes** | Free (disk ≈ 10 GB) | Industry‑standard, full control. |
| Web‑ready 3D animations | **Spline (free tier)** | Free (disk ≈ 2 GB) | Exports to React/Three.js, real‑time. |
| Interactive UI motion | **Rive (free tier)** | Free (disk ≈ 1 GB) | Runtime for apps, state‑driven. |
| Data‑driven 2D motion | **Cavalry (free)** | Free (disk ≈ 1 GB) | Procedural charts & illustrations. |

## Cost‑Effective Workflow
1. **Start with SD 1.5 + AnimateDiff** for quick video prototypes (~15 GB disk).  
2. **If longer or higher‑quality video needed**, switch to **Blender + Geometry Nodes** for procedural 3D motion.  
3. **For web integration**, export from Blender/Spline and embed via `<spline-asset>` or similar.

## Verification Checklist
- [ ] Confirm credit balance before running generation.  
- [ ] Verify output file size ≤ expected (e.g., ≤ 50 MB for short clips).  
- [ ] Check `exit_code == 0` and file exists before reporting success.