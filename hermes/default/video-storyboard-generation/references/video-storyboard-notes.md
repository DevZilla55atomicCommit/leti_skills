# Video Storyboard Generation – Session Notes

## Pitfalls Encountered
- **Token limits**: Prompts exceeding model token limits should be truncated to essential cinematographic descriptors.
- **Missing reference links**: Ensure photography reference frames are correctly linked in `references/` to avoid broken cross‑links.
- **Aspect ratio mismatch**: Maintain consistent aspect ratio (1920×1080) across all generated frames.
- **Generation timeout**: Large batches may exceed execution time; break into smaller batches if needed.

## Recommended Workflow
1. Draft concise cinematographic prompt (≤ 800 tokens).
2. Validate prompt length and clarity.
3. Call `generate_flux` for each shot, specifying width, height, steps.
4. Verify output path exists before proceeding to next shot.
5. Assemble HTML documentation with per‑frame metadata.
6. Validate generated frames exist before proceeding.

## Reference Links (example)
- `../GG_Bridge_Storyboard_A6700/145639_Cinematic_wide_establishing_shot__Sony_A6700__Sigm.png`
- `../GG_Bridge_Storyboard_A6700/145720_Medium_close-up_portrait__Sony_A6700__75mm_f_1_2__.png`
- `../GG_Bridge_Storyboard_A6700/150419_Cinematic_environmental_portrait__Sony_A6700__Sigm.png`

## Script location
- `scripts/generate_frames.sh` – Bash wrapper for bulk frame generation.

## Key Commands (example)
```bash
# Generate a single frame
generate_flux \
  --prompt "Drone pullback sunset, Sony A6700 Sigma 16mm f/2.8, rising from Crissy Field revealing full Golden Gate Bridge illuminated, model small on beach, San Francisco skyline, Kodak 2383, S-Log3" \
  --project "GG_Bridge_Video_Storyboard" \
  --width 1920 --height 1080 --steps 4
```