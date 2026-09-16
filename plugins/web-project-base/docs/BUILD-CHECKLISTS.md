# Build Checklists (vendored; mirrors `testing` + `accesslint` plugin skills)

## After every task
```bash
npm run typecheck && npm run lint && npm run test && npm run verify:assets
```
Fix failures now. Never "pre-existing", never "later".

## Images (asset gate)
- Every `/images/*` ref exists in `public/images/` AND is listed in `assets/manifest.json`
- `npm run verify:assets` PASSES (checks missing / stub / corrupt via magic bytes)
- Local files only in production — hotlinks banned

## Accessibility floor
- [ ] Semantic landmarks: header / main / section (aria-label) / footer
- [ ] One H1; heading order never skipped
- [ ] Visible keyboard focus on all links/buttons/inputs
- [ ] `prefers-reduced-motion` disables smooth scroll + reveals
- [ ] Contrast: body text ≥ 4.5:1, gold-on-dark combos checked
- [ ] Images have alt text; decorative images `alt=""`
- [ ] Form inputs labeled; errors announced

## Pre-handoff (M5)
- [ ] `npm run gates` fully green (typecheck · lint · test · verify:assets · build)
- [ ] Anchor nav works desktop + mobile widths
- [ ] No lorem ipsum; copy matches content source
- [ ] `PROJECT-STATUS.md` updated
