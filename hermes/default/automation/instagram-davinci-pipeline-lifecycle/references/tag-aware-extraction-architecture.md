# Tag-Aware Extraction Architecture (2026-07-26)

## Overview
Replaced generic vision analysis with **category-specific extraction schemas**. Each subcategory gets a dedicated vision prompt returning structured JSON matching its output fields.

## Video Effects Subcategories (10)

| Subcategory | Keywords | Output Fields |
|-------------|----------|---------------|
| `transitions` | transition, cut, wipe, dissolve, morph, match cut, whip pan, speed ramp | `transition_type`, `duration_frames`, `duration_seconds`, `easing_curve`, `fusion_setup`, `keyframe_structure`, `color_handling`, `audio_crossfade`, `is_builtin_or_custom` |
| `color_grading` | lut, cst, color space, power grade, node tree, power window, qualifier, hue vs hue | `node_tree`, `nodes`, `cst_lut_chain`, `power_windows`, `curves`, `wheel_settings`, `effects`, `output_transform` |
| `fusion_compositing` | fusion, composite, keying, rotoscope, mask, tracker, planar tracker, 3d, particle | `node_graph`, `keying_workflow`, `tracking_setup`, `masking`, `setup_3d`, `particles`, `paint_tools`, `output_settings` |
| `motion_graphics` | motion graphics, mograph, text animation, kinetic type, lower third, title, template | `template_structure`, `keyframes`, `expressions`, `modifiers`, `publish_controls`, `data_driven`, `macro_setup` |
| `vfx` | vfx, explosion, fire, smoke, magic, energy, particle, simulation, fluid, cloth | `effect_type`, `fusion_setup`, `simulation_settings`, `shaders`, `compositing`, `practical_integration`, `render_settings` |
| `camera_techniques` | dolly, slider, gimbal, drone, handheld, steadicam, orbital, push in, tracking shot | `movement_type`, `equipment`, `movement_params`, `stabilization`, `lens_info`, `resolve_post` |
| `lighting` | key light, fill light, rim light, backlight, softbox, fresnel, led panel, golden hour | `setup_type`, `lights`, `ratios`, `color_temps`, `modifiers`, `golden_hour`, `resolve_relighting` |
| `composition` | rule of thirds, leading lines, framing, foreground, depth, layers, negative space | `composition_rule`, `lens`, `subject_placement`, `depth`, `aspect_ratio`, `camera_angle`, `resolve_reframe` |
| `audio_sound` | noise reduction, eq, compression, reverb, sync, foley, voiceover, dialogue, mastering | `technique`, `fairlight_tools`, `plugin_settings`, `music_layering`, `dialogue_processing`, `sound_design`, `delivery_specs` |
| `editing_workflow` | j cut, l cut, match cut, smash cut, jump cut, montage, b-roll, multicam, timeline | `edit_technique`, `pacing`, `timeline_org`, `multicam`, `trim_tools`, `speed_changes`, `automation` |

## Photography/Videography Subcategories (7)

| Subcategory | Output Fields |
|-------------|---------------|
| `portrait` | `lighting`, `lens`, `posing`, `camera_settings`, `retouching`, `color_grading`, `composition` |
| `landscape` | `composition`, `light`, `lens`, `exposure`, `focus`, `post_processing`, `gear` |
| `commercial_product` | `product_staging`, `lighting`, `camera_lens`, `background`, `special_techniques`, `post_processing`, `deliverables` |
| `street_documentary` | `focus_approach`, `lens_choice`, `composition`, `ethics`, `bw_vs_color`, `post_processing`, `storytelling` |
| `lighting_technique` | `light_source`, `modifier`, `position`, `power`, `ratios`, `gels`, `sync`, `resolve_relighting` |

## Vision Prompt Architecture
Each subcategory has a dedicated extraction prompt returning structured JSON matching its output fields. Prompts are stored in `scripts/full_tag_aware_pipeline.py` in the `VIDEO_EFFECT_CATEGORIES` and `PHOTOGRAPHY_CATEGORIES` dictionaries.

## Pipeline Flow
```
RTF files → Parse reel IDs + URLs → Categorize by source + subcategory
         → Download (downreels.com) → Extract frames/GIFs
         → Vision analysis (3 frames, subcategory-specific prompt)
         → Generate vault note + Hermes skill
         → Copy assets to vault
         → Cleanup temp
```

## Subcategory Detection
Currently based on source RTF file (Video Effects vs Photography). Future enhancement: auto-detect from vision analysis keywords.

## Usage
```bash
# Run full tag-aware pipeline
python3 scripts/full_tag_aware_pipeline.py
```