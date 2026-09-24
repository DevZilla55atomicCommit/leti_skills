# Draft Preview Rendering (ffmpeg + PIL)

Render a short look-preview MP4 (fade + push-in + title + music swell) when the
Resolve scripting API cannot build the effect itself. The preview sells the look;
the timeline build still happens by hand afterwards.

## When to use

- Keyframed intro/outro drafts (fade from black, slow push-in/pull-out, title bloom).
- Any preview where `drawtext` or animated filters are unavailable in the local ffmpeg build.

## Recipe (5s, 1080p24, verified)

1. **Extract base frames**: `ffmpeg -t <dur> -i <clip> -vf "scale=1920:1080" -r 24 base_%03d.png`
   — do motion and fades in PIL, not in-filter.
2. **Render the title card once with PIL**: transparent RGBA PNG at output resolution,
   white text + dark stroke for legibility over dance footage.
3. **Per-frame composite in PIL** (N = dur × fps):
   - Push-in: factor `1 + 0.08*i/(N-1)`, center-crop `W/f × H/f`, BICUBIC resize back.
   - Fade from black: `Image.blend(black, frame, i/fade_frames)` over the fade window.
   - Title bloom: scale the title alpha channel `0 → 1` across its window, paste with mask.
   - Preview-only grade lift (Contrast ~1.12, Color ~1.35) — label it preview-only; the real grade lives in Resolve.
4. **Assemble**: `ffmpeg -framerate 24 -i f_%03d.png -t <dur> -i <music>` with
   `afade=t=in:st=0:d=1,apad=whole_dur=<dur>` on audio, libx264 CRF 20 + AAC 160k.
5. **Verify before delivering**: extract one frame at title-hold time and vision-check
   that the text reads exactly and the scene is visible.

## Pitfalls

- Check `ffmpeg -filters` for `drawtext` first — Homebrew builds often lack libfreetype, which is why this recipe renders text in PIL instead.
- Never put time-variable expressions (`t`, `n`) in `crop`/`scale` — they evaluate to NAN at filter init and abort the job; per-frame PIL is the reliable path.
- Keep preview grade lifts clearly labeled preview-only so a future session never mistakes the MP4 look for the Resolve grade target.
