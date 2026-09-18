# Next.js Master Skills — Claude Code Agent

This is the master skill for Next.js development. When Claude Code detects a Next.js project (presence of `package.json` with `next`), load this skill to understand the full context of the project and provide expert Next.js guidance.

This skill package covers **Next.js 16 (March 2026)** with the App Router — including Server Components, Server Actions, Cache Components, ISR, Auth, Security, Forms, and Deployment.

## Quick Decision Tree

Use this to pick the right sub-skill for the developer's task:

```
TASK: What is the developer asking about?

──────────────────────────────────────────────────────────────
LAYERS & PAGES
├─ Creating a new page or layout
│  → See skills/core.md — layout.tsx, page.tsx, template
├─ Dynamic URLs (/blog/[slug])
│  → See skills/routing.md — [slug], [...catch-all], groups
├─ Conditional layout / modal over list
│  → See skills/routing.md — parallel routes, intercepted routes
└─ Private/shared route sections
   → See skills/routing.md — route groups (marketing), (shop)

──────────────────────────────────────────────────────────────
DATA & FETCHING
├─ Fetching in Server Components
│  → See skills/data-fetching.md — fetch, ORMs, React.cache
├─ Slow data / progressive loading
│  → See skills/streaming.md — Suspense, loading.js, use() API
├─ Caching data (static/personalized)
│  → See skills/caching.md — use cache, cacheLife, revalidateTag
└─ Fetching on the client (Web APIs, polling)
   → See skills/data-fetching.md — SWR, React Query, use()

──────────────────────────────────────────────────────────────
MUTATIONS & FORMS
├─ Simple data mutation (createPost, deleteItem)
│  → See skills/mutations.md — Server Actions, revalidatePath
├─ Form with validation
│  → See skills/forms.md — Zod, useActionState, useFormStatus
├─ Optimistic UI update
│  → See skills/forms.md — useOptimistic
└─ Redirect after mutation
   → See skills/mutations.md — redirect(), cookies in actions

──────────────────────────────────────────────────────────────
API ROUTES & MIDDLEWARE
├─ Building an API endpoint
│  → See skills/route-handlers.md — route.ts, HTTP verbs
├─ Reading cookies / headers in API
│  → See skills/route-handlers.md — NextRequest, NextResponse
├─ Webhook receiver
│  → See skills/route-handlers.md — verification, revalidateTag
├─ Modifying request/response globally (auth, CSP)
│  → See skills/proxy.md — proxy.ts, matcher, security headers
└─ A/B testing, feature flags
   → See skills/proxy.md — proxy redirects, header matching

──────────────────────────────────────────────────────────────
AUTH & SECURITY
├─ Signup/login forms with sessions
│  → See skills/auth.md — Zod, JOSE, cookie config
├─ Protecting routes (dashboard → redirect to login)
│  → See skills/proxy.md — Proxy optimistic guard
├─ Fine-grained data authorization (DAL, DTOs)
│  → See skills/auth.md — Data Access Layer, role checks
├─ Content Security Policy (CSP)
│  → See skills/security.md — nonce generation, SRI
├─ Preventing XSS / exposure of secrets
│  → See skills/security.md — taint APIs, server-only
└─ Auditing an existing Next.js project
   → See skills/security.md — auditing checklist

──────────────────────────────────────────────────────────────
STYLING & ASSETS
├─ Tailwind CSS setup
│  → See skills/styling.md — Tailwind v4, postcss.config
├─ Component-scoped CSS
│  → See skills/styling.md — CSS Modules, .module.css
├─ CSS-in-JS (styled-components, styled-jsx)
│  → See skills/styling.md — registry pattern, useServerInsertedHTML
├─ Optimizing images
│  → See skills/images-fonts.md — next/image, fill, blur
└─ Loading fonts (Google Fonts)
   → See skills/images-fonts.md — next/font/google, variable fonts

──────────────────────────────────────────────────────────────
SEO & META
├─ Page title, description, favicon
│  → See skills/metadata.md — metadata object, generateMetadata
├─ Open Graph / Twitter cards
│  → See skills/metadata.md — OG images, ImageResponse
├─ Dynamic metadata (per blog post)
│  → See skills/metadata.md — generateMetadata + React.cache
├─ sitemap.xml / robots.txt
│  → See skills/metadata.md — sitemap.ts, robots.ts
└─ Structured data (JSON-LD)
   → See skills/metadata.md — JSON.stringify + sanitize

──────────────────────────────────────────────────────────────
PERFORMANCE
├─ Static generation / Incremental Static Regeneration
│  → See skills/isr.md — revalidate, generateStaticParams
├─ Making pages dynamic
│  → See skills/caching.md — Suspense, uncached data
├─ Lazy loading components
│  → See skills/performance.md — next/dynamic, ssr:false
├─ Reducing bundle size (icon libs, barrel files)
│  → See skills/performance.md — optimizePackageImports
└─ Turbopack vs webpack
   → See skills/performance.md — next dev --webpack

──────────────────────────────────────────────────────────────
I18N & CONTENT
├─ Multi-language routing (/fr/products)
│  → See skills/i18n.md — Accept-Language, generateStaticParams
├─ Translated UI strings
│  → See skills/i18n.md — dictionaries, getDictionary
└─ Markdown content / blog
   → See skills/mdx.md — @next/mdx, mdx-components.tsx

──────────────────────────────────────────────────────────────
TESTING
├─ End-to-end tests (clicking, navigation)
│  → See skills/testing.md — Playwright setup
├─ Unit/component tests
│  → See skills/testing.md — Vitest, Jest
└─ Optimizing 3rd-party scripts (analytics)
   → See skills/testing.md — @next/third-parties

──────────────────────────────────────────────────────────────
DEPLOYMENT
├─ Docker container
│  → See skills/deployment.md — Dockerfile, standalone output
├─ Vercel / Fly.io / Render / Netlify
│  → See skills/deployment.md — adapter guides
├─ Self-hosted Node.js
│  → See skills/deployment.md — next start, standalone output
├─ CI/CD build caching
│  → See skills/deployment.md — GitHub Actions, CircleCI
└─ Updating Next.js version
   → See skills/deployment.md — pnpm next upgrade

──────────────────────────────────────────────────────────────
ADVANCED
├─ Custom server (Express, custom routing)
│  → See skills/advanced.md — server.ts, next({})
├─ OpenTelemetry / instrumentation
│  → See skills/advanced.md — instrumentation.ts, register()
├─ Preview mode (draft CMS content)
│  → See skills/advanced.md — draftMode(), draft enable
├─ Progressive Web App (offline, service worker)
│  → See skills/advanced.md — next-pwa, service-worker.ts
├─ Multi-tenant (multiple customers, one app)
│  → See skills/advanced.md — subdomain routing, DAL
├─ Multi-zones (micro-frontends)
│  → See skills/advanced.md — rewrites, multi Next.js apps
└─ Debugging (VS Code, Chrome DevTools)
   → See skills/advanced.md — --inspect, launch.json
```

## Skill Index

| Sub-Skill File | Slash Command | Covers |
|---------------|-------------|---------|
| skills/core.md | /nextjs-core | App Router, layout, page, template, error, loading |
| skills/routing.md | /nextjs-routing | Dynamic routes, route groups, parallel/intercepted |
| skills/data-fetching.md | /nextjs-data-fetching | Server Components, fetch, ORMs, context sharing |
| skills/streaming.md | /nextjs-streaming | Suspense, loading.js, use() API |
| skills/mutations.md | /nextjs-mutations | Server Actions, revalidatePath, redirect |
| skills/forms.md | /nextjs-forms | Server Action forms, Zod, useActionState |
| skills/caching.md | /nextjs-caching | Cache Components, use cache, cacheLife |
| skills/route-handlers.md | /nextjs-route-handlers | route.ts, NextRequest, NextResponse |
| skills/proxy.md | /nextjs-proxy | proxy.ts, CSP, matcher, redirects |
| skills/auth.md | /nextjs-auth | Sessions, DAL, DTOs, JOSE, Proxy guard |
| skills/security.md | /nextjs-security | CSP, taint, server-only, XSS, IDOR |
| skills/styling.md | /nextjs-styling | Tailwind v4, CSS Modules, CSS-in-JS |
| skills/images-fonts.md | /nextjs-images-fonts | next/image, next/font |
| skills/metadata.md | /nextjs-metadata | Metadata API, OG images, sitemap |
| skills/isr.md | /nextjs-isr | Incremental Static Regeneration |
| skills/i18n.md | /nextjs-i18n | Accept-Language, dictionaries, routing |
| skills/mdx.md | /nextjs-mdx | @next/mdx, MDX pages |
| skills/deployment.md | /nextjs-deployment | Docker, Vercel, CI caching |
| skills/performance.md | /nextjs-performance | next/dynamic, Turbopack, bundle size |
| skills/testing.md | /nextjs-testing | Playwright, Vitest, Jest, Cypress |
| skills/advanced.md | /nextjs-advanced | Custom server, instrumentation, Draft Mode, PWA |

## Next.js Version

Based on **Next.js 16 (March 2026)**. Key features:
- App Router (default, recommended)
- React 19 with Server Components
- Cache Components (`use cache` directive, `cacheComponents: true`)
- Server Actions (`'use server'`)
- proxy.ts (formerly middleware)
- Turbopack (default dev bundler)
- Partial Prerendering (default with Cache Components)

## File Naming Conventions (Quick Reference)

| File | Purpose |
|------|---------|
| `app/layout.tsx` | Root layout (required: `<html>`, `<body>`) |
| `app/page.tsx` | Page component |
| `app/loading.tsx` | Loading skeleton for a route segment |
| `app/error.tsx` | Error boundary (client component) |
| `app/global-error.tsx` | Root-level error (has own `<html>`) |
| `app/not-found.tsx` | 404 page |
| `app/template.tsx` | Re-rendered on every navigation |
| `app/route.ts` | API route handler |
| `app/[param]/page.tsx` | Dynamic route |
| `app/[...catchAll]/page.tsx` | Catch-all route |
| `app/[[...optional]]/page.tsx` | Optional catch-all |
| `app/(group)/page.tsx` | Route group (no URL change) |
| `app/@slot/page.tsx` | Named slot (parallel route) |
| `app/(.)photo/[id]/page.tsx` | Intercepted route |
| `proxy.ts` | proxy/middleware (global request interception) |
| `instrumentation.ts` | Server startup code |
| `next.config.ts` | Next.js configuration |
| `app/sitemap.ts` | Dynamic sitemap |
| `app/robots.ts` | Dynamic robots.txt |
| `app/opengraph-image.tsx` | Dynamic OG image |
| `app/icon.tsx` | Generated app icon |

## Best Practices Checklist

When working on any Next.js task, ensure:
- [ ] Server Components for data fetching; Client Components (`'use client'`) only when needed
- [ ] `'use server'` on all Server Actions; verify auth inside every action
- [ ] `server-only` on all server-side utility modules
- [ ] Zod validation on all form inputs (server-side)
- [ ] DAL (Data Access Layer) for all database queries
- [ ] DTOs returned from DAL — never expose raw DB records
- [ ] `revalidatePath` or `revalidateTag` after mutations
- [ ] `generateStaticParams` for all static pages
- [ ] `next/image` for all images (never raw `<img>`)
- [ ] `next/font` for all Google/local fonts
- [ ] `metadata` or `generateMetadata` on all pages
- [ ] `Suspense` boundaries around uncached/runtime data
- [ ] `cacheLife` profile on all cached data functions
- [ ] Environment secrets never prefixed with `NEXT_PUBLIC_`
- [ ] Proxy guard for protected routes
- [ ] Cookie config: `httpOnly`, `secure`, `sameSite: 'lax'`
