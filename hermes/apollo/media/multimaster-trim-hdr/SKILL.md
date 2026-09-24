---
name: multimaster-trim-hdr
description: "Per-format HDR trim passes with Multimaster Trim."
version: 1.0.0
author: Apollo (Hermes Agent)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [DaVinci Resolve, Color, HDR, Trim, Dolby Vision, v21.1]
    related_skills: [davinci-resolve-version-tracker]
---

# Multimaster Trim HDR Workflows

## When to Use

Use when grading Dolby Vision, HDR10+, and HDR Vivid with independent trim passes. New in DaVinci Resolve 21.1.

## Video Reference
- **Video ID:** Wi44XLKQ3YA
- **Timestamp:** 6:24-7:13
- **Resolve Page:** Color

## Feature Overview
- Each HDR format gets dedicated trim pass
- Panel menu: "Add Trim Pass" → Select HDR format
- Grades independent, no shared HDR trim
- Override output sizing per trim
- Per-trim color output & timeline caching
- No recaching when switching trims
- Playhead retained on stacked clip navigation

## Trim Pass Types
| HDR Format | Trim Pass | Metadata |
|------------|-----------|----------|
| Dolby Vision | DV_Trim1, DV_Trim2... | Dynamic, per-shot |
| HDR10+ | HDR10+_Trim1... | Dynamic, per-shot |
| HDR Vivid | HDRVivid_Trim1... | Dynamic, per-shot |
| SDR | SDR_Trim1... | Static |

## Workflow
1. Open Color page
2. Enable Multimaster Trim (Color menu)
3. Panel menu → Add Trim Pass
4. Select HDR format (Dolby Vision/HDR10+/HDR Vivid)
5. Grade independently per trim
6. Override sizing per trim (Sizing palette)
7. Switch trims instantly (no recache)

## Sizing Palette Overwrites
- Output Sizing: Overwrite checkbox per trim
- Blanking: Overwrite checkbox per trim
- Independent framing per deliverable

## Caching Benefits
- Each trim retains own color output cache
- Each trim retains own timeline cache
- Switch trims = instant (no recalculation)
- Stacked clip navigation retains playhead

## Use Cases
- Multi-format delivery (DV + HDR10+ + SDR)
- Format-specific creative grades
- Client review per HDR format
- QC per deliverable spec

## Tips
- Name trims: "DV_Main", "HDR10+_Main", "HDRVivid_Main"
- Use Split Screen (vertical) for A/B comparison
- Gallery stills per trim for reference
- Export LUTs per trim for downstream

## Cross-References
- **Related Skills:** `dolby-vision-grading`, `hdr10plus-grading`, `sizing-palette-overwrite`
- **Tags:** `multimaster-trim`, `dolby-vision`, `hdr10plus`, `hdr-vivid`, `color`, `v21.1`
- **Collection:** `hdr-workflows`