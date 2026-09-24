# Next.js Streaming — Suspense, loading.js, and the use() API

## Overview

Streaming allows you to progressively send UI from the server to the client. Instead of waiting for all data to be ready before showing anything, you can stream the page shell immediately and fill in content as data resolves. This dramatically improves perceived performance.

**Key concepts:**
- `<Suspense>` — wraps async work and shows fallback until it resolves
- `loading.tsx` — file-based Suspense boundary for entire route segments
- React's `use()` hook — reads promises in Client Components for streaming
- Skeleton UI — meaningful loading states

**Related skills:** core, data-fetching, caching

---

## Why Streaming?

Without streaming, a page with multiple slow data requests renders nothing until the slowest request completes. With streaming, you show the page shell immediately and stream each data-dependent section as it resolves.

**Before streaming:**
```
Request → [Wait 2s for all data] → Full page rendered
```

**After streaming:**
```
Request → [Page shell renders immediately]
           → [Fast data streams in at 0.5s]
           → [Slow data streams in at 2s]
```

---

## `loading.tsx` — File-Based Streaming

Create `loading.tsx` in any route segment to automatically wrap that segment's page in `<Suspense>` with a loading fallback:

```tsx
// app/blog/loading.tsx
export default function Loading() {
  return (
    <div className="space-y-4">
      <div className="skeleton h-8 w-1/2" />
      <div className="skeleton h-4 w-3/4" />
      <div className="skeleton h-4 w-2/3" />
      <div className="skeleton h-4 w-1/2" />
    </div>
  )
}
```

**What happens:**
1. User navigates to `/blog`
2. Layout renders immediately (it's synchronous)
3. `loading.tsx` skeleton renders immediately
4. Data fetches in `page.tsx` run in parallel
5. When `page.tsx` resolves, it replaces the skeleton

**Automatic wrapping:** `loading.tsx` automatically nests inside `layout.tsx` and wraps `page.tsx` in `<Suspense>`.

---

## `<Suspense>` — Granular Streaming

For more control, use `<Suspense>` directly to stream specific components independently:

```tsx
// app/blog/page.tsx
import { Suspense } from 'react'
import BlogList from '@/components/BlogList'
import BlogListSkeleton from '@/components/BlogListSkeleton'

export default function BlogPage() {
  return (
    <div>
      {/* Header renders immediately */}
      <header>
        <h1>My Blog</h1>
        <p>Read the latest posts below.</p>
      </header>

      <main>
        {/* Content outside Suspense renders immediately */}
        <p>Latest posts:</p>

        {/* Suspense boundary — shows skeleton until BlogList resolves */}
        <Suspense fallback={<BlogListSkeleton />}>
          <BlogList />
        </Suspense>
      </main>
    </div>
  )
}
```

**Best practice:** Place `<Suspense>` as close to the data-dependent component as possible. This minimizes the streaming "hole" while keeping the page shell visible.

---

## Streaming with `use()` in Client Components

Pass a promise from a Server Component to a Client Component, then resolve it with React's `use()` hook:

```tsx
// app/blog/page.tsx — Server Component (source of data)
import Posts from '@/app/ui/posts'
import { Suspense } from 'react'

export default function Page() {
  // Don't await — pass the unresolved promise
  const posts = getPosts()

  return (
    <Suspense fallback={<div>Loading posts...</div>}>
      <Posts posts={posts} />
    </Suspense>
  )
}
```

```tsx
// app/ui/posts.tsx — Client Component (consumer)
'use client'
import { use } from 'react'

export default function Posts({
  posts,
}: {
  posts: Promise<{ id: string; title: string }[]>
}) {
  // use() resolves the promise — Suspense catches the pending state
  const allPosts = use(posts)

  return (
    <ul>
      {allPosts.map((post) => (
        <li key={post.id}>{post.title}</li>
      ))}
    </ul>
  )
}
```

**How it works:**
1. Server renders the page shell immediately
2. `<Posts>` suspends because `posts` isn't resolved yet
3. Suspense boundary shows the fallback
4. React streams the resolved `<Posts>` content to the client
5. Page appears complete

---

## Meaningful Loading States

Design loading states that help users understand what's coming. Good loading states:

```tsx
// BAD: Generic spinner
export default function Loading() {
  return <Spinner />
}

// GOOD: Skeleton that matches the page structure
export default function Loading() {
  return (
    <div className="max-w-2xl mx-auto p-6 space-y-6">
      {/* Hero skeleton */}
      <div className="space-y-3">
        <div className="skeleton h-10 w-2/3" />
        <div className="skeleton h-4 w-full" />
        <div className="skeleton h-4 w-4/5" />
      </div>

      {/* Article skeleton */}
      <div className="space-y-4 border-t pt-6">
        <div className="skeleton h-6 w-1/2" />
        <div className="space-y-2">
          <div className="skeleton h-4 w-full" />
          <div className="skeleton h-4 w-full" />
          <div className="skeleton h-4 w-3/4" />
        </div>
      </div>
    </div>
  )
}
```

---

## Streaming + Route Segment Config

### Force Dynamic (Always Stream)

```tsx
// app/stats/page.tsx
export const dynamic = 'force-dynamic'

export default async function StatsPage() {
  // This always runs at request time — no caching
  const stats = await fetchLiveStats()
  return <Dashboard stats={stats} />
}
```

### Streaming vs. Parallel Data Fetching

Use streaming when different parts of the page have different data with different speeds. Use parallel fetching when all data is needed together:

```tsx
// STREAMING — different data, different speeds
export default async function Page() {
  return (
    <div>
      <Suspense fallback={<HeaderSkeleton />}><Header /></Suspense>
      <Suspense fallback={<FeedSkeleton />}><Feed /></Suspense>
      <Suspense fallback={<SidebarSkeleton />}><Sidebar /></Suspense>
    </div>
  )
}

// PARALLEL — same data needed together
export default async function Page() {
  const [artist, albums] = await Promise.all([
    getArtist(id),
    getAlbums(id),
  ])
  return <ArtistPage artist={artist} albums={albums} />
}
```

---

## Gotchas

1. **`loading.tsx` auto-wraps in Suspense** — you don't need to add `<Suspense>` yourself
2. **Suspense boundaries don't catch all async** — only async components/promises. Synchronous work outside Suspense blocks the boundary
3. **`use()` requires `<Suspense>` in the parent** — always wrap components using `use()` with a Suspense boundary
4. **`loading.tsx` is route-segment specific** — `app/blog/loading.tsx` only covers `/blog`. `app/loading.tsx` covers the whole subtree
5. **Layouts with runtime data don't fall back to loading.js** — if a layout accesses `cookies()`, `headers()`, or uncached fetches, navigation doesn't fall back to that segment's `loading.tsx`. Wrap the dynamic access in its own `<Suspense>`
6. **Always design meaningful skeletons** — a blank loading state is worse than a spinner; match the page structure

---

## Prerequisites

- Next.js Core — see `skills/core.md`
- Data fetching basics — see `skills/data-fetching.md`

## Next Steps

- **Cache Components with streaming:** See `skills/caching.md` — `use cache` + uncached data in `<Suspense>`
- **Forms with loading states:** See `skills/forms.md` — `useActionState` + `useOptimistic`
- **Route handlers with streaming:** See `skills/route-handlers.md` — `Response` streaming
