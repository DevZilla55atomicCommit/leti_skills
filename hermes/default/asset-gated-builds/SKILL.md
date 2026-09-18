---
name: asset-gated-builds
description: "Use when a build must ship with zero broken local assets."
---

# Asset-Gated Builds

Makes broken images, videos, and download links structurally impossible: a
green build means every referenced asset resolves, or the build is red. Never
rely on opening the site and eyeballing the gallery — placeholder text files
posing as `.jpg` pass `existsSync` and render as 404s.

## Procedure (SETUP-phase, before UI work)

1. **Inventory first.** List every asset the build will reference. Record each
   in `assets/manifest.json`: path, section, purpose, source
   (`unsplash | pre-existing | generated`), sourceId, attribution, and
   `placeholder: true` on anything not final. Mark unverified files
   `Source unverified — replace or confirm` so a later pass must resolve them.
2. **Local-first.** Download themed files into `public/`; production hotlinks
   are banned. Label every placeholder as a placeholder (slates, stubs,
   `ATTRIBUTION.md` entries) — never pass one off as final.
3. **Write the verifier** (`scripts/verify-assets.mjs`, no deps). Starter:
   `templates/verify-assets.mjs` — copy it in, adjust `REF_PREFIX` /
   `PUBLIC_DIR` / `MANIFEST` if your layout differs. It scans
   code for `/assets/*` refs and FAILS on: MISSING (no such file), STUB
   (image under a byte floor — catches text files with image extensions),
   CORRUPT (wrong magic bytes: JPEG `FF D8 FF`, PNG `89 50 4E 47`, WebP
   `RIFF....WEBP`, MP4 `ftyp` at offset 4, PDF `%PDF`). Skip directory
   mentions in prose (trailing slash). WARN — don't fail — on
   referenced-but-unlisted manifest drift. Derive the project root with
   `fileURLToPath(new URL('..', import.meta.url))` — plain `.pathname`
   percent-encodes the path, so any space in a parent directory becomes
   `%20` and every check fails with ENOENT.
4. **Wire the gate.** `verify:assets` script in `package.json` + an acceptance
   criterion (`PASSED, zero broken refs`). A missing file means download it
   or remove the ref — never commit the ref and hope.
5. **Cross-check the fetch script.** Confirm it writes the SAME paths the code
   references (`gallery/landscape/` vs `galleries/mountain-lake.jpg` drift
   ships broken while reporting 'download complete'). Grep refs vs script
   targets before trusting it.

## Pitfalls

- With `"type": "module"` in `package.json`, keep CJS tooling configs
  (`next.config`, `postcss.config`, `.eslintrc` using `module.exports`) as
  `.cjs` — the build fails on `.js` with `module is not defined`, and the
  failure surfaces as a webpack/css-loader error, not a config error.
- A passing `tsc`/`lint` says nothing about assets; run the asset gate in the
  same command chain as the other gates or it will be skipped exactly when
  it matters.
- Never attribute from memory — record an author only from a publisher
  credit line or the source page itself; CDN photo IDs cannot be mapped back
  to authors without an API key, so mark the rest `author unconfirmed` with
  the license basis and keep building. Stalling on unresolvable credits
  wastes the session; inventing names ships a lie.
