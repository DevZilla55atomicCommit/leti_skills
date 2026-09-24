# Next.js Routing — Dynamic Routes, Route Groups, Parallel & Intercepted Routes

## Overview

Next.js App Router uses file-system routing where the folder hierarchy maps directly to URL segments. Beyond basic static routes, Next.js supports dynamic segments, route groups, parallel routes, and intercepted routes for complex UI patterns.

**Related skills:** core, data-fetching, mutations, proxy

---

## Static Routes

Basic routes from folder structure:

| File | URL |
|------|-----|
| `app/page.tsx` | `/` |
| `app/blog/page.tsx` | `/blog` |
| `app/blog/about/page.tsx` | `/blog/about` |
| `app/dashboard/settings/page.tsx` | `/dashboard/settings` |

---

## Dynamic Routes

Wrap a folder name in `[brackets]` to create a dynamic segment that captures URL values.

### Single Segment — `[param]`

```tsx
// app/blog/[slug]/page.tsx
export default async function Page({
  params,
}: {
  params: Promise<{ slug: string }>
}) {
  const { slug } = await params
  const post = await getPost(slug)
  return <h1>{post.title}</h1>
}
```

URLs: `/blog/my-first-post`, `/blog/hello-world`

### Multiple Segments — `[city]/[locale]/page.tsx`

```tsx
// app/[city]/[locale]/page.tsx
export default async function Page({
  params,
}: {
  params: Promise<{ city: string; locale: string }>
}) {
  const { city, locale } = await params
  return <div>Events in {city}, locale: {locale}</div>
}
```

URLs: `/tokyo/en`, `/paris/fr`

### Catch-All — `[...param]`

Captures **one or more** URL segments into an array. Use for unbounded paths:

```tsx
// app/shop/[...slug]/page.tsx
export default async function Page({
  params,
}: {
  params: Promise<{ slug: string[] }>
}) {
  const { slug } = await params
  // slug = ['clothing', 'shirts', 'blue'] → /shop/clothing/shirts/blue
  return <div>Path: {slug.join(' / ')}</div>
}
```

URLs: `/shop/clothing`, `/shop/clothing/shirts`, `/shop/clothing/shirts/blue`

### Optional Catch-All — `[[...param]]`

Captures **zero or more** segments. The route matches with or without the segment:

```tsx
// app/docs/[[...slug]]/page.tsx
export default async function Page({
  params,
}: {
  params: Promise<{ slug?: string[] }>
}) {
  const { slug } = await params
  if (!slug) {
    return <div>Docs Home</div>
  }
  return <div>Docs: {slug.join(' / ')}</div>
}
```

URLs: `/docs`, `/docs/layouts`, `/docs/api-reference/use-router`

### Dynamic Routes Summary

| Pattern | File | Matches | `params.slug` example |
|---------|------|---------|----------------------|
| Single | `[slug]` | `/blog/one` | `"one"` |
| Multiple | `[city]/[locale]` | `/tokyo/en` | `{ city: "tokyo", locale: "en" }` |
| Catch-all | `[...slug]` | `/a/b/c` | `["a", "b", "c"]` |
| Optional | `[[...slug]]` | `/` or `/a/b` | `undefined` or `["a", "b"]` |

---

## Route Groups `(group)`

Wrap a folder name in `(parentheses)` to **organize routes without affecting the URL**. Route groups are useful for:

1. Grouping related routes with shared layouts
2. Separating marketing routes from app routes
3. Avoiding URL clutter from organizational folders

```text
app/
├── (marketing)/           ← Route group — URL unchanged
│   ├── layout.tsx         ← Marketing layout
│   ├── page.tsx           ← / (home)
│   ├── about/page.tsx     ← /about
│   └── pricing/page.tsx   ← /pricing
│
├── (shop)/                ← Route group — URL unchanged
│   ├── layout.tsx         ← Shop layout
│   ├── cart/page.tsx      ← /cart
│   ├── products/page.tsx   ← /products
│   └── checkout/page.tsx  ← /checkout
│
└── (auth)/                ← Route group — URL unchanged
    ├── login/page.tsx     ← /login
    └── signup/page.tsx    ← /signup
```

**Key rules:**
- `(marketing)/page.tsx` maps to `/`, NOT `/marketing`
- Route groups can share layouts (each has its own layout)
- Route groups can be nested inside other route groups
- Route groups cannot conflict with other route groups

---

## Parallel Routes `@slot`

Parallel routes allow **multiple independent views** to be rendered simultaneously in the same layout. They use named slots (`@folder` convention).

### Use Case: Dashboard with Sidebar + Main Content

```text
app/
├── @sidebar/               ← Named slot
│   └── page.tsx           ← Renders in the sidebar slot
├── @main/                 ← Named slot
│   └── page.tsx           ← Renders in the main slot
├── layout.tsx             ← Receives both slots as children
└── page.tsx               ← (optional) default page
```

```tsx
// app/layout.tsx
export default function DashboardLayout({
  children,
  sidebar,
  main,
}: {
  children: React.ReactNode
  sidebar: React.ReactNode
  main: React.ReactNode
}) {
  return (
    <div className="flex">
      <aside className="w-64">{sidebar}</aside>
      <main className="flex-1">{main}</main>
    </div>
  )
}
```

### Default Fallback (`default.tsx`)

When a slot has no matching route, `default.tsx` renders:

```tsx
// app/@modal/default.tsx
export default function Default() {
  return null // Don't render anything if no modal
}
```

---

## Intercepted Routes `(.)folder`

Intercepted routes let you render a **different route inside the current layout** without changing the URL. This is the pattern for modals, photo galleries, and "peek" views.

### Use Case: Photo Modal Over Gallery

```text
app/
├── layout.tsx              ← Main layout (persistent)
├── page.tsx                ← Photo gallery (/)
├── photo/[id]/page.tsx     ← Full page view: /photo/1
└── (.)photo/[id]/page.tsx ← Intercepted modal: renders over / when navigating
```

```tsx
// app/(.)photo/[id]/page.tsx — Intercepted route
// When user navigates from / to /photo/1,
// this renders IN PLACE of the gallery instead of replacing it
export default function PhotoModal({
  params,
}: {
  params: Promise<{ id: string }>
}) {
  return (
    <div className="modal-overlay">
      <div className="modal">
        <img src={`/photos/${params.id}.jpg`} alt="Photo" />
      </div>
    </div>
  )
}
```

### Intercept Levels

| Pattern | Meaning | Use Case |
|---------|---------|---------|
| `(.)folder` | Intercept same level | Modal over list item |
| `(..)folder` | Intercept parent level | Open child as overlay |
| `(..)(..)folder` | Intercept two levels | Deeply nested overlay |
| `(...)folder` | Intercept from root | Show any route as overlay |

```text
Intercept Levels:
(.) → same folder level
(..) → one level up (parent)
(..)(..) → two levels up
(...) → root level
```

### Combining Parallel + Intercepted Routes

```text
app/
├── @modal/
│   ├── default.tsx         ← Empty when no modal
│   └── [...catchAll]/page.tsx ← Intercepted route
├── layout.tsx             ← Receives @modal slot
└── page.tsx               ← Gallery (/)

// User clicks photo → URL changes to /photo/1
// @modal renders the intercepted modal over the gallery
// URL is /photo/1 but the gallery stays visible underneath
```

---

## `generateStaticParams`

For dynamic routes that should be statically generated at build time, export `generateStaticParams`:

```tsx
// app/blog/[slug]/page.tsx
export async function generateStaticParams() {
  const posts = await getAllPosts()
  return posts.map((post) => ({ slug: post.slug }))
}

export default async function Page({
  params,
}: {
  params: Promise<{ slug: string }>
}) {
  const { slug } = await params
  const post = await getPost(slug)
  return <article>{post.content}</article>
}
```

**Tip:** For routes with `generateStaticParams`, set `dynamicParams = false` to return 404 for non-prerendered paths:

```tsx
export const dynamicParams = false
```

---

## Gotchas

1. **`params` is always a Promise** in Next.js 15+ — always `await` before destructuring
2. **Catch-all `[...slug]` gives an array** — `slug.join('/')` to reconstruct the path
3. **Route groups don't appear in URLs** — `(marketing)/about/page.tsx` is just `/about`
4. **Parallel slots must be explicitly received** — `layout.tsx` must list each named slot as a prop
5. **Intercepted routes need a fallback URL** — the full page route (`app/photo/[id]/page.tsx`) must also exist so direct navigation works
6. **Intercepted routes break on hard navigation** — use `router.push()` from `next/navigation` for soft navigation; direct URL access renders the full page instead
7. **`generateStaticParams` + `dynamicParams: false`** — only pre-generated pages are accessible; others return 404

---

## Prerequisites

- Next.js Core — see `skills/core.md`

## Next Steps

- **Data fetching in dynamic routes:** See `skills/data-fetching.md` — use `React.cache` to deduplicate metadata + page fetches
- **Form actions in dynamic routes:** See `skills/forms.md` — server actions receive params as arguments
- **Metadata per dynamic route:** See `skills/metadata.md` — `generateMetadata` for per-page OG tags
- **ISR for dynamic content:** See `skills/isr.md` — `revalidate` on dynamic routes
