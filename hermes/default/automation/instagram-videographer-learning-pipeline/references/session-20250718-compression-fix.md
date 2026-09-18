# Session 2025-07-18 — Auto-Compression Fix & Carousel Processing

> **Date:** 2025-07-18  
> **Sessions Involved:** `20260717_181054_79863a` (parent), `20260717_222510_ab6181` (branched), `20260718_...` (current)

---

## Summary

Fixed a critical auto-compression misconfiguration that caused sessions to hang at 1M+ tokens. Processed 4 carousel posts via browser vision, bringing total carousels processed to 27/29.

---

## Root Cause: Wrong Context Length Override

### The Bug
Profile config (`~/.hermes/profiles/default/config.yaml`) had:
```yaml
model:
  context_length: 65536  # WRONG — forces ALL models to 64K context
```

This overrode `nvidia/nemotron-3-ultra-550b-a55b`'s true **1,000,000 token** context window.

### The Cascade Failure
1. Compression threshold = 75% of *configured* context → 75% × 64K = **48K tokens**
2. Actual session tokens: ~217K (well above 48K)
3. Compression triggered prematurely, sent 1M+ tokens to NVIDIA API
4. NVIDIA API rejected: `"maximum context length is 4096 tokens... requested 197629 tokens"`
5. Compression failure → cooldown set on session (12h)
6. Branched sessions inherited broken config

### The Fix
**Removed** `model.context_length` from profile config entirely. Let Hermes resolve actual model context via provider API metadata.

```yaml
# ~/.hermes/profiles/default/config.yaml — AFTER
model:
  default: nvidia/nemotron-3-ultra-550b-a55b
  provider: nvidia
  # context_length: REMOVED
```

Also fixed global config: removed `base_url` from `auxiliary.compression` to use NVIDIA API directly.

---

## Carousel Posts Processed (4 new)

| URL | Creator | Slides | Discipline | Output |
|-----|---------|--------|------------|--------|
| `DPgOCdMDLoC` | @awid.safaei | 8 | Composition / Camera Theory | Aspect Ratio Cheat Sheet |
| `DMzzBUlorMk` | @kierzacporter | 7 | Production | Frame-by-Frame Shot List |
| `DE7bo_xCzZc` | @kierzacporter | 9 | Production | 9 Essential Shot Types |
| `DRwi6KPjMqo` | @deith__ | 1 (post) | Camera Theory | Sony Picture Profile S-Log3 |

**Total:** 27/29 carousels complete (2 remaining: `C-tul9VgTZp` — Reel not carousel, `DPgOCdMDLoC` already done)

---

## Vault Notes Created

| Path | Discipline |
|------|------------|
| `Camera Theory/04-Sony-Picture-Profile-Settings_deith_Camera-Theory.md` | Camera Theory |
| `Production/01-Frame-by-Frame-Breakdown_gazdavies_Production.md` | Production |
| `Production/01-Shot-List-Essential-Shot-Types_kierzacporter.md` | Production |

---

## Hermes Skills Created

| Skill | Category |
|-------|----------|
| `videographer-camera-theory-sony-picture-profile-slog3-deith` | Camera Theory |
| `videographer-production-frame-by-frame-shotlist-kierzacporter` | Production |
| `videographer-production-shot-list-essential-types-kierzacporter` | Production |

---

## Pipeline Validation Results

| Content Type | Status | Method |
|--------------|--------|--------|
| **Carousels (/p/)** | ✅ Full pipeline | Browser vision + ffmpeg GIFs |
| **Reels (/reel/)** | ❌ Blocked | yt-dlp auth failure (needs cookies.txt) |
| **TV (/tv/)** | ❌ Blocked | Same as Reels |

**Key insight:** Carousel posts work end-to-end via browser vision (no download needed). Reels require authenticated yt-dlp session with fresh Chrome cookies.

---

## Config Changes Made

| File | Change |
|------|--------|
| `~/.hermes/profiles/default/config.yaml` | Removed `model.context_length: 65536` |
| `~/.hermes/config.yaml` | Removed `base_url` from `auxiliary.compression` |

---

## Troubleshooting Reference

See `references/auto-compression-troubleshooting.md` for:
- Session recovery steps
- Config file locations
- Cooldown expiration (~12h)
- Related session IDs

---

## Next Actions

1. **Reels:** Export cookies.txt from Chrome ("Get cookies.txt" extension) → enable yt-dlp download
2. **Remaining carousels:** Process last 2 (if any true carousels remain)
3. **Batch script:** Complete `scripts/run_pipeline.py` for automated runs
4. **Exports:** Run `regenerate_exports_and_diagram` skill

---

## Session Lineage

```
20260715_203740_bc494a (1014 msgs, original compression failure)
    └── 20260717_181054_79863a (931 msgs, hit cooldown)
          └── 20260717_222510_ab6181 (branched, inherited broken config)
                └── 20260718_... (current, config fixed, 27 carousels done)
```

*All sessions now use corrected 1M context → compression at 750K tokens.*