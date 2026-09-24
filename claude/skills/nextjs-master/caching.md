# Next.js Caching — Cache Components, use cache, cacheLife, and Partial Prerendering

## Overview

Caching in Next.js App Router lets you control when and how data is stored and refreshed. With **Cache Components** (`cacheComponents: true`), the `use cache` directive provides fine-grained control over data-level and UI-level caching. Combined with `cacheLife`, `cacheTag`, and Partial Prerendering, you can build applications that serve cached content instantly while keeping data fresh.

**Key APIs:**
- `use cache` — caches the result of async functions or components
- `cacheLife()` — configures how long data is considered fresh
- `cacheTag()` — tags cached data for targeted invalidation
- `updateTag()` — immediately expires cache (Server Actions only)
- `revalidateTag()` — invalidates tagged cache (stale-while-revalidate)
- `revalidatePath()` — invalidates all cache for a route path

**Related skills:** core, data-fetching, mutations, streaming, isr

---

## Enabling Cache Components

Add to `next.config.ts`:

```ts
// next.config.ts
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  cacheComponents: true,
}

export default nextConfig
```

---

## `use cache` — Data-Level Caching

Wrap an async function to cache its result:

```ts
// app/lib/data.ts
import { cacheLife } from 'next/cache'

// Cache this function's result
export async function getProducts() {
  'use cache'
  cacheLife('hours') // Fresh for 1 hour, stale for 5 hours
  return db.query('SELECT * FROM products')
}

// Cache with arguments
export async function getProduct(id: string) {
  'use cache'
  cacheLife('days')
  return db.query('SELECT * FROM products WHERE id = $1', [id])
}
```

Arguments and closed-over values become the cache key — different inputs produce different cache entries:

```ts
// Same function, different arguments → different cache entries
const product1 = getProduct('123') // cache key includes '123'
const product2 = getProduct('456') // cache key includes '456'
```

---

## `use cache` — UI-Level Caching

Cache an entire component or page:

```tsx
// app/page.tsx
import { cacheLife } from 'next/cache'

export default async function Page() {
  'use cache'
  cacheLife('hours')

  const posts = await db.query('SELECT * FROM posts ORDER BY created_at DESC')

  return (
    <ul>
      {posts.map((post) => (
        <li key={post.id}>{post.title}</li>
      ))}
    </ul>
  )
}
```

---

## `cacheLife` — Cache Profiles

Control how long data stays fresh:

```ts
import { cacheLife } from 'next/cache'

// Profile-based configuration
export async function getProducts() {
  'use cache'
  cacheLife('hours') // See profile table below
  return db.query('SELECT * FROM products')
}
```

| Profile | stale | revalidate | expire | Use Case |
|---------|-------|-----------|--------|---------|
| `seconds` | 0s | 1s | 60s | Real-time data |
| `minutes` | 0 | 1m | 5m | Frequently changing |
| `hours` | 0 | 1h | 5h | Standard content |
| `days` | 0 | 1d | 1w | Slowly changing |
| `weeks` | 0 | 1w | 30d | Archives |
| `max` | 0 | 30d | ~indefinite | Nearly static |

### Custom Configuration

```ts
'use cache'
cacheLife({
  stale: 3600,    // 1 hour until "stale"
  revalidate: 7200, // 2 hours until auto-refresh
  expire: 86400,  // 1 day hard expiry
})
```

**Short-lived caches** (`expire < 5min`, `revalidate: 0`, or `seconds` profile) are excluded from prerenders and become dynamic holes instead.

---

## `cacheTag` — Tag-Based Invalidation

Tag cached data for precise invalidation:

```ts
// app/lib/data.ts
import { cacheTag } from 'next/cache'

export async function getProducts() {
  'use cache'
  cacheTag('products') // Tag this cache entry
  return db.query('SELECT * FROM products')
}

export async function getUsers() {
  'use cache'
  cacheTag('users') // Separate cache entry
  return db.query('SELECT * FROM users')
}
```

```ts
// app/actions.ts
'use server'
import { revalidateTag } from 'next/cache'

export async function createProduct(formData: FormData) {
  const product = await db.product.create({ data: { title: formData.get('title') as string } })
  // Immediately expire users cache (read-your-own-writes)
  updateTag('products')
  return product
}

export async function deleteUser(userId: string) {
  await db.user.delete({ where: { id: userId } })
  // Background refresh — user sees stale data briefly
  revalidateTag('users', 'max') // max = longest stale window
}
```

---

## On-Demand Revalidation Summary

| Function | Where to Call | Behavior | Use Case |
|---------|--------------|---------|---------|
| `updateTag(tag)` | Server Actions only | Immediate expiry | Read-your-own-writes |
| `revalidateTag(tag, stale?)` | Server Actions + Route Handlers | Stale-while-revalidate | Background refresh |
| `revalidatePath(path)` | Server Actions + Route Handlers | Expire all for path | When tag unknown |

---

## Partial Prerendering (PPR)

With Cache Components enabled, Next.js uses Partial Prerendering by default:

1. **Static shell** — rendered at build time (includes cached components + Suspense fallbacks)
2. **Dynamic holes** — rendered at request time (runtime data, short-lived cache)
3. **Streaming** — dynamic content streams into the shell

### Static Content — Automatically Prerendered

```tsx
// app/blog/page.tsx
export default function BlogPage() {
  return (
    <>
      <header>Static header</header>     {/* Prerendered */}
      <BlogPosts />                     {/* Cached → prerendered */}
      <Suspense fallback={<Skeleton />}>
        <UserPreferences />            {/* Runtime → streamed */}
      </Suspense>
    </>
  )
}
```

### Handling Runtime APIs (cookies, headers, searchParams)

Components accessing runtime APIs must be wrapped in `<Suspense>`:

```tsx
import { Suspense } from 'react'
import { cookies } from 'next/headers'

// NOT cached — reads user-specific cookie
async function Greeting() {
  const cookieStore = await cookies()
  const name = cookieStore.get('name')?.value || 'Guest'
  return <p>Hello, {name}!</p>
}

export default function Page() {
  return (
    <>
      <h1>Welcome</h1>
      {/* Wrap runtime data in Suspense */}
      <Suspense fallback={<p>Loading...</p>}>
        <Greeting />
      </Suspense>
    </>
  )
}
```

### Handling Non-Deterministic Operations

Operations like `Math.random()` or `crypto.randomUUID()` produce different values each time. Wrap in `<Suspense>`:

```tsx
import { connection } from 'next/server'
import { Suspense } from 'react'

async function UniqueID() {
  await connection() // Defer to request time
  const id = crypto.randomUUID()
  return <p>Request ID: {id}</p>
}

export default function Page() {
  return (
    <Suspense fallback={<p>Loading...</p>}>
      <UniqueID />
    </Suspense>
  )
}
```

---

## Complete Example — Blog with Static, Cached, and Dynamic Content

```tsx
// app/blog/page.tsx
import { Suspense } from 'react'
import { cookies } from 'next/headers'
import { cacheLife, cacheTag } from 'next/cache'
import Link from 'next/link'

export default function BlogPage() {
  return (
    <>
      {/* Static — prerendered */}
      <header>
        <h1>Our Blog</h1>
        <nav>
          <Link href="/">Home</Link> | <Link href="/about">About</Link>
        </nav>
      </header>

      {/* Cached dynamic content — prerendered in shell */}
      <BlogPosts />

      {/* Runtime dynamic — streams at request time */}
      <Suspense fallback={<p>Loading preferences...</p>}>
        <UserPreferences />
      </Suspense>
    </>
  )
}

// All users see the same posts (revalidated every hour)
async function BlogPosts() {
  'use cache'
  cacheLife('hours')
  cacheTag('posts')

  const res = await fetch('https://api.example.com/posts')
  const posts = await res.json()

  return (
    <section>
      <h2>Latest Posts</h2>
      <ul>
        {posts.slice(0, 5).map((post: any) => (
          <li key={post.id}>
            <h3>{post.title}</h3>
          </li>
        ))}
      </ul>
    </section>
  )
}

// Personalized per user (reads cookie → runtime)
async function UserPreferences() {
  const theme = (await cookies()).get('theme')?.value || 'light'
  return <p>Theme: {theme}</p>
}
```

---

## Gotchas

1. **`'use cache'` cannot be used directly inside Route Handlers** — extract to a helper function instead
2. **`cacheLife` profiles apply to time-based revalidation** — `updateTag`/`revalidateTag` overrides time-based expiration
3. **Short-lived caches become dynamic holes** — `expire < 5min`, `revalidate: 0`, or `seconds` profile excludes from prerenders
4. **Runtime APIs (cookies, headers) require `<Suspense>`** — without it, the whole route becomes dynamic
5. **`connection()` defers to request time** — call it before non-deterministic operations in cached components
6. **Cache keys include arguments AND closed-over values** — avoid capturing large objects or unstable values in cached functions
7. **`revalidateTag(tag, 'max')` gives the longest stale window** — use for background refresh where slight delay is acceptable

---

## Prerequisites

- Next.js Core — see `skills/core.md`
- Data fetching — see `skills/data-fetching.md`

## Next Steps

- **ISR with revalidate:** See `skills/isr.md` — time-based revalidation for pages
- **Server Actions + revalidation:** See `skills/mutations.md` — `updateTag` after mutations
- **Route Handlers + caching:** See `skills/route-handlers.md` — caching API responses
- **Proxy + CSP:** See `skills/proxy.md` — proxy + caching interaction
