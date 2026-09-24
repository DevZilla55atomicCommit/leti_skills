# Next.js Core — App Router Fundamentals

## Overview

The App Router is the foundation of every Next.js project. It uses file-system routing where folders define URL segments and special files handle specific behaviors. This skill covers the App Router's core concepts: layouts, pages, error boundaries, loading states, and the overall project structure.

**Key APIs covered:**
- `layout.tsx` — shared UI across routes
- `page.tsx` — route content
- `template.tsx` — re-renders on navigation
- `loading.tsx` — Suspense boundary skeleton
- `error.tsx` — React error boundary
- `global-error.tsx` — root-level error with own `<html>`
- `not-found.tsx` — 404 page

**Related skills:** routing, data-fetching, streaming, mutations, proxy

---

## Project Structure

A minimal Next.js App Router project:

```
my-app/
├── app/                        # App Router
│   ├── layout.tsx              # Root layout (required: <html>, <body>)
│   ├── page.tsx                # Home page (/)
│   ├── loading.tsx             # Global loading skeleton
│   ├── error.tsx               # Global error boundary
│   ├── not-found.tsx           # Global 404 page
│   ├── global-error.tsx        # Root-level error (own <html>)
│   ├── template.tsx            # Re-renders on navigation
│   ├── page.module.css         # CSS Module (optional)
│   ├── globals.css             # Global CSS
│   ├── favicon.ico             # Favicon
│   ├── sitemap.ts              # Dynamic sitemap
│   ├── robots.ts               # Dynamic robots.txt
│   ├── opengraph-image.tsx     # OG image
│   ├── icon.tsx                # Generated icon
│   ├── blog/
│   │   ├── layout.tsx          # Blog-specific layout
│   │   ├── page.tsx            # /blog
│   │   ├── loading.tsx         # Blog loading skeleton
│   │   ├── error.tsx           # Blog error boundary
│   │   ├── not-found.tsx       # Blog 404
│   │   └── [slug]/
│   │       ├── page.tsx        # /blog/[slug]
│   │       └── loading.tsx     # Post loading skeleton
│   └── api/
│       └── route.ts            # API route
├── public/                      # Static assets (/profile.png)
├── src/                         # Optional: src/ folder
│   └── app/
│       └── ...                  # Same structure as above
├── next.config.ts               # Next.js config
├── package.json
└── tsconfig.json
```

---

## Root Layout (Required)

The root `app/layout.tsx` is **required** and must contain `<html>` and `<body>`:

```tsx
// app/layout.tsx
import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'My App',
  description: 'Welcome to my Next.js app',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
```

**Key rules:**
- `layout.tsx` must export a default React component
- The root layout must include `<html>` and `<body>`
- Child layouts are optional but wrap their child segments
- Layouts receive `children` automatically

---

## Pages

A `page.tsx` is the content for a route. The route becomes publicly accessible when `page.tsx` exists:

```tsx
// app/page.tsx — renders at /
export default function Page() {
  return <h1>Hello, Next.js!</h1>
}

// app/blog/page.tsx — renders at /blog
export default function BlogPage() {
  return <h1>Blog</h1>
}
```

Pages can be Server Components (default) or Client Components (`'use client'`):

```tsx
// app/page.tsx — Server Component (default, preferred)
export default async function Page() {
  const data = await fetch('https://api.example.com/posts')
  return <h1>{data.title}</h1>
}
```

---

## Nested Layouts

Layouts nest to share UI across routes. Each layout wraps all routes beneath it:

| File | Wraps |
|------|-------|
| `app/layout.tsx` | All routes |
| `app/blog/layout.tsx` | `/blog/*` |
| `app/blog/[slug]/layout.tsx` | `/blog/[slug]/*` |

```tsx
// app/blog/layout.tsx
export default function BlogLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <section>
      <nav>
        <Link href="/blog">All Posts</Link>
        <Link href="/blog/about">About</Link>
      </nav>
      {children}
    </section>
  )
}
```

---

## Loading Skeletons (`loading.tsx`)

Create `loading.tsx` to show a skeleton while the route segment renders. It automatically wraps the page in `<Suspense>`:

```tsx
// app/blog/loading.tsx
export default function Loading() {
  return (
    <div>
      <div className="skeleton h-4 w-1/2" />
      <div className="skeleton h-4 w-3/4" />
      <div className="skeleton h-4 w-1/4" />
    </div>
  )
}
```

**Behavior:**
- Shows immediately on navigation
- Wraps `page.tsx` automatically in `<Suspense>`
- Works at any route segment level
- Combine with individual `<Suspense>` boundaries for granular streaming

**Tip:** Design loading states that are meaningful — skeletons with the right shape are better than spinners.

---

## Error Boundaries (`error.tsx` and `global-error.tsx`)

### `error.tsx` — Per-Segment Error Boundary

```tsx
// app/blog/error.tsx
'use client' // Error boundaries MUST be Client Components

import { useEffect } from 'react'

export default function ErrorPage({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  useEffect(() => {
    // Log to error reporting service
    console.error(error)
  }, [error])

  return (
    <div>
      <h2>Something went wrong!</h2>
      <p>{error.message}</p>
      <button onClick={() => reset()}>Try again</button>
    </div>
  )
}
```

**Rules:**
- Must be a Client Component (`'use client'`)
- Errors bubble up to the nearest parent `error.tsx`
- Use `reset()` (formerly `unstable_retry`) to attempt recovery

### Component-Level Error Boundary (`unstable_catchError`)

```tsx
// app/custom-error-boundary.tsx
'use client'
import { unstable_catchError as catchError } from 'next/error'

function ErrorFallback(
  props: { title: string },
  { error, reset }: { error: Error; reset: () => void }
) {
  return (
    <div>
      <h2>{props.title}</h2>
      <p>{error.message}</p>
      <button onClick={reset}>Try again</button>
    </div>
  )
}

export default catchError(ErrorFallback)
```

### `global-error.tsx` — Root Error Handler

For root-level errors. Must define its own `<html>` and `<body>` since it replaces the root layout:

```tsx
// app/global-error.tsx
'use client'

export default function GlobalError({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  return (
    <html>
      <body>
        <h2>Something went wrong!</h2>
        <button onClick={() => reset()}>Try again</button>
      </body>
    </html>
  )
}
```

---

## 404 Pages (`not-found.tsx`)

```tsx
// app/not-found.tsx
import Link from 'next/link'

export default function NotFound() {
  return (
    <div>
      <h1>404 — Page Not Found</h1>
      <Link href="/">Go home</Link>
    </div>
  )
}
```

Programmatically trigger a 404:

```tsx
// Inside any page or layout
import { notFound } from 'next/navigation'

export default async function Page({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params
  const post = await getPost(slug)

  if (!post) {
    notFound() // Triggers the nearest not-found.tsx
  }

  return <div>{post.title}</div>
}
```

---

## Template (`template.tsx`)

Unlike `layout.tsx`, `template.tsx` **re-renders on every navigation**. Use it when you need fresh state on navigation:

```tsx
// app/template.tsx
// Unlike layout (persists across navigations), template remounts on each visit
export default function Template({ children }: { children: React.ReactNode }) {
  return <div className="animate-fade-in">{children}</div>
}
```

**When to use template vs layout:**
- Use `layout` when state should persist across navigations (e.g., sidebar, navigation)
- Use `template` when you want state to reset on navigation (e.g., animated transitions, form reset)

---

## Component Rendering Order

The component hierarchy for any route:

```
layout.tsx
  template.tsx       ← re-renders on every navigation
    error.tsx        ← React error boundary
      loading.tsx    ← Suspense boundary
        page.tsx     ← or nested layout.tsx
```

---

## src/ Directory

You can optionally place all app files inside a `src/` folder:

```
my-app/
├── src/
│   └── app/
│       ├── layout.tsx
│       └── page.tsx
├── public/
└── package.json
```

This keeps application code separate from configuration files.

---

## Private Folders (`_folderName`)

Prefix any folder with `_` to exclude it from routing while keeping files colocated:

```
app/blog/
├── _components/     ← NOT routable (safe for UI utilities)
│   └── PostCard.tsx
├── _lib/            ← NOT routable (safe for utils)
│   └── data.ts
├── layout.tsx
└── page.tsx        ← Only page.tsx creates the /blog route
```

**Use cases:**
- Separate UI logic from routing logic
- Organize internal files consistently
- Avoid naming conflicts with future Next.js file conventions

---

## Next.js Config (`next.config.ts`)

```ts
// next.config.ts
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  // Enable React strict mode
  reactStrictMode: true,

  // Enable experimental features
  experimental: {
    // Enable Cache Components
    cacheComponents: true,
    // Enable taint APIs
    taint: true,
  },

  // Image optimization
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: '**.example.com',
      },
    ],
  },
}

export default nextConfig
```

---

## Gotchas

1. **Root layout is required** — must contain `<html>` and `<body>`. Next.js creates one automatically in dev mode, but always define it explicitly.
2. **Layouts persist, templates remount** — navigation doesn't re-render layouts but does remount templates. Use templates for animations.
3. **Error boundaries must be Client Components** — `'use client'` is required on `error.tsx`.
4. **`error.tsx` bubbles up** — place it at the appropriate segment level. A `blog/error.tsx` catches errors from all `/blog/*` routes.
5. **`global-error.tsx` needs its own `<html>`** — since it replaces the root layout when active.
6. **`notFound()` throws**, not returns — it's a special function that triggers the nearest `not-found.tsx`.
7. **`params` is now a Promise** in Next.js 15+ — always `await` it: `const { slug } = await params`.

---

## Prerequisites

- Node.js 20.9+ (minimum for Next.js 16)
- TypeScript 5.1+ recommended

## Next Steps

- **Routing:** See `skills/routing.md` for dynamic routes, route groups, parallel routes
- **Data fetching:** See `skills/data-fetching.md` for Server Components and fetch
- **Streaming:** See `skills/streaming.md` for Suspense and loading patterns
- **Styling:** See `skills/styling.md` for Tailwind CSS setup
