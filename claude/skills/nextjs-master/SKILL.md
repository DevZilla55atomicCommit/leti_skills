---
name: nextjs-master
description: Next.js 16 App Router reference router — routing, data fetching, caching, Server Actions, forms, auth, security, styling, SEO, testing, deployment. Use for any Next.js work; consults the matching topic file.
---

# nextjs-master — index router (adapted from CodeForFee/skills-nextjs, MIT)

Complete Next.js 16 (App Router) reference set. Topic files live beside this
file (`core.md`, `routing.md`, ...). Consult the matching file — do not rely
on memory for version-sensitive APIs.

Topic map:
- App Router/layouts/pages/boundaries → `core.md`
- Dynamic routes, groups, parallel/intercepted → `routing.md`
- Server Components, fetch, ORMs, React.cache → `data-fetching.md`
- Suspense, loading.js, use() API, skeletons → `streaming.md`
- Server Actions, revalidatePath/Tag, redirect → `mutations.md`
- Action forms, Zod, useActionState → `forms.md`
- use cache, cacheLife/cacheTag, PPR → `caching.md`
- route.ts handlers, webhooks → `route-handlers.md`
- proxy.ts, CSP nonce, headers, auth guards → `proxy.md`
- Sessions, DAL/DTOs, JOSE → `auth.md`
- CSP, taint APIs, server-only, XSS/CSRF/IDOR → `security.md`
- Tailwind v4, CSS Modules → `styling.md`
- next/image, next/font, placeholders → `images-fonts.md`
- Metadata, OG, sitemap, JSON-LD → `metadata.md`
- next/dynamic, Turbopack, bundles → `performance.md`
- Playwright/Vitest/Jest/Cypress → `testing.md`
- ISR → `isr.md`, MDX → `mdx.md`, i18n → `i18n.md`
- Vercel/adapters/CI → `deployment.md`, advanced → `advanced.md`

Source: https://github.com/CodeForFee/nextjs-master-skills (see _upstream-CLAUDE.md).
Prefer laguagu-next-best-practices when the two disagree (newer revision).
