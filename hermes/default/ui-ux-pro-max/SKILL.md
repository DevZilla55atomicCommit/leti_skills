---
name: ui-ux-pro-max
description: A comprehensive UI/UX design system for professional-grade interfaces across web, mobile, and desktop platforms.
category: ui-ux
---

# UI/UX Pro Max Skill

A comprehensive UI/UX design system and decision framework for professional-grade interfaces across web, mobile, and desktop platforms. Provides design system generation, domain-specific search, stack-specific implementation guidance, and a 98-rule UX checklist.

## Skill Structure

This skill provides a comprehensive UI/UX design system with:
- **Design System Generation**: `--design-system` flag generates complete design systems with reasoning
- **Domain-Specific Search**: 13 domains (product, style, color, typography, google-fonts, chart, ux, landing, icons, gsap, react, web, stack-specific)
- **Design Dials**: Three dials (variance, motion, density) to tune design system output
- **Stack-Specific Guidelines**: 22 supported stacks (React, Next.js, Vue, Svelte, Flutter, SwiftUI, etc.)
- **UX Rule Engine**: 98 rules across 10 categories with rationale
- **Pro Rules & Checklist**: App-specific polish rules and pre-delivery checklist

## Installation

This skill is installed at `~/.claude/skills/ui-ux-pro-max.md` and references scripts at:
```
${CLAUDE_PLUGIN_ROOT}/.claude/skills/ui-ux-pro-max/scripts/search.py
```

The search script requires Python 3.x (no external dependencies).

## Usage

### Step 1: Analyze User Requirements

Extract from user request:
- **Product type**: SaaS, e-commerce, portfolio, dashboard, entertainment, tool, productivity, or hybrid
- **Target audience & context**: age group, usage context (commute, leisure, work)
- **Style keywords**: playful, vibrant, minimal, dark mode, content-first, immersive, etc.
- **Stack**: Detect from project files (package.json, pubspec.yaml, *.xcodeproj, Package.swift, composer.json, app.json + react-native). Default to `html-tailwind` if undetectable.

### Step 2: Generate Design System (Required for New Pages/Projects)

```bash
python "${CLAUDE_PLUGIN_ROOT}/.claude/skills/ui-ux-pro-max/scripts/search.py" "<product_type> <industry> <keywords>" --design-system [-p "Project Name"]
```

Example:
```bash
python "${CLAUDE_PLUGIN_ROOT}/.claude/skills/ui-ux-pro-max/scripts/search.py" "beauty spa wellness service" --design-system -p "Serenity Spa"
```

### Step 2b: Persist Design System (Master + Overrides Pattern)

```bash
python "${CLAUDE_PLUGIN_ROOT}/.claude/skills/ui-ux-pro-max/scripts/search.py" "<query>" --design-system --persist -p "Project Name" --output-dir "<project-root>"
```

This creates:
- `design-system/<project-slug>/MASTER.md` — Global Source of Truth
- `design-system/<project-slug>/pages/` — Folder for page-specific overrides

With a page-specific override, add `--page "dashboard"` to also create `design-system/<project-slug>/pages/dashboard.md`.

### Step 2c: Design Dials (Optional)

Three optional 1-10 sliders:
```bash
python "${CLAUDE_PLUGIN_ROOT}/.claude/skills/ui-ux-pro-max/scripts/search.py" "<query>" --design-system --variance <1-10> --motion <1-10> --density <1-10>
```

| Dial | Low (1-3) | Mid (4-7) | High (8-10) |
|------|-----------|-----------|-------------|
| `--variance` | Centered/minimal | Balanced/modern | Bold/asymmetric |
| `--motion` | Subtle micro-interactions | Standard scroll/stagger | Complex choreography |
| `--density` | Spacious (24-96px) | Standard (16-64px) | Dense/dashboard (8-32px) |

### Step 3: Supplement with Detailed Searches

```bash
python "${CLAUDE_PLUGIN_ROOT}/.claude/skills/ui-ux-pro-max/scripts/search.py" "<keyword>" --domain <domain> [-n <max_results>]
```

| Need | Domain | Example |
|------|--------|---------|
| Product type patterns | `product` | `--domain product "entertainment social"` |
| More style options | `style` | `--domain style "glassmorphism dark"` |
| Color palettes | `color` | `--domain color "entertainment vibrant"` |
| Font pairings | `typography` | `--domain typography "playful modern"` |
| Individual Google Fonts | `google-fonts` | `--domain google-fonts "sans serif popular variable"` |
| Chart recommendations | `chart` | `--domain chart "real-time dashboard"` |
| UX best practices | `ux` | `--domain ux "animation accessibility"` |
| Landing page structure | `landing` | `--domain landing "hero social-proof"` |
| Icon recommendations | `icons` | `--domain icons "navigation outline"` |
| GSAP animation presets | `gsap` | `--domain gsap "scroll reveal stagger"` |
| React/Next.js performance | `react` | `--domain react "rerender memo list"` |
| App/native interface guidelines | `web` | `--domain web "accessibilityLabel touch safe-areas"` |

### Step 4: Stack Guidelines

```bash
python "${CLAUDE_PLUGIN_ROOT}/.claude/skills/ui-ux-pro-max/scripts/search.py" "<keyword>" --stack <stack>
```

Available stacks: `react`, `nextjs`, `vue`, `svelte`, `astro`, `nuxtjs`, `nuxt-ui`, `angular`, `laravel`, `swiftui`, `react-native`, `flutter`, `jetpack-compose`, `html-tailwind`, `shadcn`, `threejs`, `javafx`, `wpf`, `winui`, `avalonia`, `uno`, `uwp`.

### If Search Returns 0 Results

1. Retry once with broader/differently-worded keywords
2. If still empty, fall back to the priority table (built-in defaults) and explicitly state: "no database match for X, using general SaaS defaults"
3. Never present 0-result search as if it returned data

## UX Rule Priority Table (98 Rules, 10 Categories)

| # | Category | Priority | Tags | Key Do | Key Don't |
|---|----------|----------|------|--------|-----------|
| 1 | Accessibility | CRITICAL | `ux` | WCAG AA, semantic HTML, focus visible, alt text, ARIA | Missing focus styles, color-only meaning, no alt/ARIA |
| 2 | Touch & Input | CRITICAL | `ux` | 44×44px targets, 8px+ spacing, loading feedback | Hover-only, instant state changes (0ms) |
| 3 | Performance | HIGH | `ux` | WebP/AVIF, lazy load, CLS < 0.1 | Layout thrashing, CLS |
| 4 | Style Selection | HIGH | `style`, `product` | Match product type, consistency, SVG icons | Mixing flat/skeuomorphic, emoji as icons |
| 5 | Layout & Responsive | HIGH | `ux` | Mobile-first, viewport meta, no horizontal scroll | Horizontal scroll, fixed px containers, disable zoom |
| 6 | Typography & Color | MEDIUM | `typography`, `color` | Base 16px, line-height 1.5, semantic color tokens | Body < 12px, gray-on-gray, raw hex in components |
| 7 | Animation | MEDIUM | `ux`, `gsap` | 150-300ms, motion conveys meaning, spatial continuity | Decorative-only, animating width/height, no reduced-motion |
| 8 | Forms & Feedback | MEDIUM | `ux` | Visible labels, error near field, helper text, progressive disclosure | Placeholder-only labels, errors only at top, overwhelm upfront |
| 9 | Navigation Patterns | HIGH | `ux` | Predictable back, bottom nav ≤5, deep linking | Overloaded nav, broken back, no deep links |
| 10 | Charts & Data | LOW | `chart` | Legends, tooltips, accessible colors | Color-only meaning |

Full rule list: `references/quick-reference.md` (all ~98 guidelines with rationale)
Pro rules & pre-delivery checklist: `references/pro-rules.md`

## Before Delivering App UI

Read `references/pro-rules.md` and run through its canonical Pre-Delivery Checklist covering:
- Icon/visual-element discipline
- Interaction feedback
- Light/dark contrast
- Safe-area layout
- Accessibility (iOS/Android/React Native/Flutter scoped)

## Search Script Usage Notes

The search script lives inside the skill directory. Always invoke by full path:
```bash
python "${CLAUDE_PLUGIN_ROOT}/.claude/skills/ui-ux-pro-max/scripts/search.py" "<query>" [flags]
```

If `python` not found, try `python3`, then `py -3`. Requires Python 3.x, no external dependencies.

## Output Formats

`--design-system` supports `-f ascii` (default, terminal), `-f markdown` (documentation), and `--json` (machine-readable with raw design system dict + persistence status).

## Tips for Better Results

- Use **multi-dimensional keywords**: combine product + industry + tone + density
- Try different phrasings: "playful neon" → "vibrant dark" → "content-first minimal"
- Use `--design-system` first for full recommendations, then `--domain` to deep-dive
- Pass detected stack explicitly for implementation-specific guidance

| Problem | What to Do |
|---------|------------|
| Can't decide on style/color | Re-run `--design-system` with different keywords |
| Dark mode contrast issues | `references/quick-reference.md` §6: `color-dark-mode` + `color-accessible-pairs` |
| Animations feel unnatural | `references/quick-reference.md` §7: `spring-physics` + `easing` + `exit-faster-than-enter` |
| Form UX is poor | `references/quick-reference.md` §8: `inline-validation` + `error-clarity` + `focus-management` |
| Navigation feels confusing | `references/quick-reference.md` §9: `nav-hierarchy` + `bottom-nav-limit` + `back-behavior` |
| Layout breaks on small screens | `references/quick-reference.md` §5: `mobile-first` + `breakpoint-consistency` |
| Performance/jank | `references/quick-reference.md` §3: `virtualize-lists` + `main-thread-budget` + `debounce-throttle` |

## Example Workflow

**User request:** "Make an AI search homepage." (Stack detected as Next.js from package.json)

```bash
# Step 2: design system
python "${CLAUDE_PLUGIN_ROOT}/.claude/skills/ui-ux-pro-max/scripts/search.py" "AI search tool modern minimal" --design-system -p "AI Search"

# Step 3: supplement
python "${CLAUDE_PLUGIN_ROOT}/.claude/skills/ui-ux-pro-max/scripts/search.py" "search loading animation" --domain ux

# Step 4: stack guidelines
python "${CLAUDE_PLUGIN_ROOT}/.claude/skills/ui-ux-pro-max/scripts/search.py" "suspense streaming bundle" --stack nextjs
```

Then synthesize the design system + detailed searches and implement.