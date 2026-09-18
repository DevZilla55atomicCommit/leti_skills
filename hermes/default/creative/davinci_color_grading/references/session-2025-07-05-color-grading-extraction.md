# Session 2025-07-07-05: Color Grading Tutorial Extraction & Flux Integration

## Summary
Extracted 7 cinematic color grading tutorials from YouTube (DaVinci Resolve 19-21), organized into vault, and built a hybrid Flux image generation wrapper for Hermes MCP integration.

## Tutorials Extracted & Saved

### S-Log3 (Sony) — 4 Tutorials
| File | Source | Key Focus |
|------|--------|-----------|
| `Color Grading & Looks/S-Log3/S-Log3_Kyle-White_FX3-Cinematic-Node-Tree.md` | Kyle White (239K views) | 7-node: EXP→WB→PW→SKIN→CST→LUT. CST at end (S-Gamut3/S-Log3→Rec.709/2.4). Power Window + Outside Node. Skin Midtone Detail ~10. Creative LUT via Key Output Gain. |
| `Color Grading & Looks/S-Log3/S-Log3_Danny-Gan_3-Node-CST-Workflow.md` | Danny Gan (287K views) | Minimal 3-node: PRIMARIES→LOOK→CST. All upstream in S-Gamut3.Cine. Upstream vs downstream demo. CST: S-Gamut3.Cine/S-Log3→Rec.709/2.4. Tone Mapping: DaVinci. |
| `Color Grading & Looks/S-Log3/S-Log3_Cullen-Kelly_Pro-Noise-Highlight-Management.md` | Cullen Kelly (25K views) | ETTR philosophy. Lum vs Sat highlight desaturation. Conservative NR (Better/Med/Threshold 20). Toe-down curves. Template node tree + Timeline Voyager LUTs. Camera-agnostic methodology. |
| `Color Grading & Looks/S-Log3/S-Log3_Mehran-Haddad_Resolve21-Portrait-PowerGrade.md` | Mehran Hadad (4.8K views) | 17-node DWG Intermediate pipeline. Dual CST (S-Log3→DWG→Rec.709). HDR wheels, HSV/HSL tandem, Color Slice, Power Window skin isolation, Retouch Me Heal/Dodge&Burn, Halation/Glow/Grain. Studio features. |

### Apple Log 2 (iPhone) — 3 Tutorials
| File | Source | Key Focus |
|------|--------|-----------|
| `Color Grading & Looks/Apple Log 2/Apple-Log2_Russell-Wofford_CST-DWG-Workflow.md` | Russell Wofford (63K views) | Group Pre/Post-Clip dual CST: Apple Log 2→DWG Intermediate (grade here)→Rec.709. Batch conversion for multi-clip timelines. |
| `Color Grading & Looks/Apple Log 2/Apple-Log2_CineMirage_LUT-And-Manual-Grade.md` | CineMirage (1.7K views) | Two methods: (1) One-click LUTs (free Basic + 5 paid) with CST baked in; (2) Manual 2-node: CST Apple Log 2→Rec.709 + Primaries (Sat~70, Gain/Lift/Gamma). 4:3 aspect for vertical/horizontal. |
| `Color Grading & Looks/Apple Log 2/Apple-Log_FujiCinema_Basics-Kodak-Film-Look.md` | FujiCinema (51K views) | 3-4 node: CST Rec.2020/Apple Log→Rec.709/2.4 → HDR Exposure fix → Contrast 1.3+Sat (Commercial) OR CST→ST2084+Kodak 2383 LUT (Film). Auto-WB assumed. |

## Vault Organization Applied
```
Color Grading & Looks/
├── Apple Log 2/          # iPhone Apple Log 2 tutorials
└── S-Log3/               # Sony S-Log2/3 tutorials
```

## Memory.md Cross-Reference Pattern
Added categorized YouTube Tutorials section with emoji headers:
```markdown
### 🎬 S-Log3 (Sony) Tutorials
*   **[Title]** :: `Color Grading & Looks/S-Log3/filename.md` — Summary...

### 🍎 Apple Log 2 (iPhone) Tutorials
*   **[Title]** :: `Color Grading & Looks/Apple Log 2/filename.md` — Summary...
```

## Flux Hybrid Wrapper Built
**File:** `/Users/alfredkamisese/TamaZila Obsidian Vault/Hermes Agent/Hermes Image Generates/flux_wrapper.py`

**Dual-purpose:**
1. **Python API:** `from flux_wrapper import generate_flux, batch_generate`
2. **MCP Server:** Run `python flux_wrapper.py` → Hermes calls `generate_image`, `list_recent`, `get_image_info`

**Tested & Working:**
- Model: `x/flux2-klein:4b` (5.7GB, Ollama)
- Python: Hermes venv 3.11 (system Python 3.9 has urllib3 version conflict)
- Output: `~/Pictures/Flux_Generations/{project}/` with PNG + JSON metadata sidecars
- MCP tools: `generate_image`, `list_recent`, `get_image_info`

**Use Cases for Color Grading:**
- Previsualization / mood boards for Kodak 2383 looks
- Storyboard frames matching tutorial looks
- Film emulation reference frames (Kodak 2383 D55, Fuji, etc.)
- Skin tone test frames with different film stocks

## Key Technical Notes for davinci_color_grading Skill

### CST Pipeline Consistency
All S-Log3 tutorials converge on **CST at end** (upstream grading):
- Input: S-Gamut3(.Cine) / S-Log3
- Output: Rec.709 / Gamma 2.4 (broadcast) or DWG Intermediate
- Tone Mapping: DaVinci (default) or Luminance Mapping

### Film Emulation (Kodak 2383) — Correct Pipeline
```bash
# WRONG: Direct LUT on Rec.709 → crushed/oversaturated
# RIGHT:
1. Grade fully in Rec.709 / DWG Intermediate
2. Disable creative nodes
3. CST: Rec.709/Gamma 2.4 → Cineon Film Log
4. Apply Kodak 2383 LUT (D55/D65)
5. CST + LUT → Compound Node → Key Output Gain = intensity slider
```

### Skin Tone Protection — Three Pro Methods
| Method | Key | Best For |
|--------|-----|----------|
| **Layer Node Composite** (Darren Mostyn) | Key Output Gain blend corrected skin OVER grade | Teal/Orange, heavy grades |
| **Qualifier + Vectorscope** (Darren Mostyn) | Gamma nudge to skin tone line + Sat pop | Precision correction |
| **Parallel Mixer** (Gabe Lomotey) | Blends (not stacks) skin branch with grade | Non-destructive, flexible |

### DWG Intermediate as Universal Working Space
- All S-Log3, Apple Log 2, RED, BMD footage → DWG Intermediate
- Wider gamut/DR than Rec.709 → better highlight retention
- Grade in DWG → CST to Cineon for Film Looks → CST to Rec.709 for delivery

## Integration with This Skill
The extracted tutorials directly reinforce the workflows documented in `davinci_color_grading`:
- Primary correction → CST at end → Creative grade → Film emulation
- Skin tone workflows (Qualifier + Vectorscope + Gamma)
- CST management (upstream vs downstream)
- Node tree organization principles

These extracted tutorials serve as **concrete, source-attributed examples** for each workflow pattern in this skill.