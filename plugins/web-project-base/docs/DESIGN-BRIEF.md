# Design Brief — warm Hawaiian restaurant one-pager
*(vendored guidance; mirrors the `frontend-design` + `ui-ux-pro-max` plugin skills so the build never depends on resolving a skill name)*

## Palette (deliberate, not defaults)
- Base: charcoal-kiawe near-black `#1c1008` / `#2a1709` for hero + footer grounds
- Surface: warm sand `#faf3e7` / `#f3e7d0` for section backgrounds (NOT cream #F4F1EA)
- Primary accent: mango-gold `#d98a1f` / hover `#b56f14` — CTAs, active nav, price highlights
- Quiet secondary: deep palm green `#2f4a2c` — badges, dividers, footer notes
- Never: terracotta #D97757, acid-green, SaaS-card-kit grey shadows

## Type
- Display: Fraunces (serif, 600–700) for H1/H2 — warm, editorial, island-menu feel
- Body: Inter (400–500), line length < 80ch
- No single-word accent coloring in headlines; no ALL-CAPS eyebrow on every heading

## Layout
- Hero: full-bleed grill photo, dark overlay, left-aligned headline + 2 CTAs (Menu / Visit)
- Sections alternate sand tints; MenuCards in a 3-col grid (1-col mobile), generous whitespace
- Sticky navbar with smooth-scroll anchors (`scroll-behavior: smooth`, `scroll-margin-top: 5rem`)

## Motion (restraint)
- ONE orchestrated hero entrance + fade-up on section scroll (framer-motion, `whileInView`)
- Motion that answers actions only (filter, hover, expand); everything gated behind `prefers-reduced-motion`
