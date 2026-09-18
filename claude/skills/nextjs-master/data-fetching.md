# Next.js Data Fetching — Server Components, Fetch API, ORMs, and Caching

## Overview

In the App Router, data fetching happens primarily in **Server Components** — components that run exclusively on the server. This enables direct database access, secure credential handling, and automatic deduplication of fetch requests within a render tree.

**Key APIs:**
- `fetch()` in Server Components (with `cache`, `next.tags`)
- React's `cache()` for deduplication
- ORMs and database clients (直接查询，不需要 API 路由)
- Context + `cache()` for cross-component data sharing
- SWR / React Query for Client Components

**Related skills:** core, streaming, caching, mutations, auth, forms

---

## Data Fetching in Server Components

Server Components can be `async` and `await` data directly. No client-side loading state needed for the initial render:

```tsx
// app/blog/page.tsx
export default async function BlogPage() {
  const posts = await fetch('https://api.vercel.app/blog').then(r => r.json())

  return (
    <ul>
      {posts.map((post) => (
        <li key={post.id}>{post.title}</li>
      ))}
    </ul>
  )
}
```

**Key rules:**
- Server Components are `async` functions
- `fetch()` requests are automatically deduplicated within the same render tree
- Fetch requests are NOT cached by default — use `cache: 'force-cache'` or `use cache`
- Data is fetched at render time (dynamic) unless cached

---

## Fetch API Options

```tsx
// Default: not cached (dynamic)
const data = await fetch('https://api.vercel.app/posts')

// Cache the result (static until revalidate)
const data = await fetch('https://api.vercel.app/posts', {
  cache: 'force-cache', // or: 'no-store', 'no-cache'
})

// Cache with revalidation (ISR-style)
const data = await fetch('https://api.vercel.app/posts', {
  next: { revalidate: 3600 } // Revalidate every hour
})

// Tag-based invalidation
const data = await fetch('https://api.vercel.app/posts', {
  next: { tags: ['posts'] } // Can invalidate by tag
})
```

### Cache Options

| Option | Behavior |
|--------|---------|
| `cache: 'force-cache'` | Cache indefinitely (default for fetch) |
| `cache: 'no-store'` | Never cache (always dynamic) |
| `cache: 'no-cache'` | Bypass cache but still cache the response |
| `next: { revalidate: N }` | Cache with time-based revalidation |
| `next: { tags: ['name'] }` | Cache with tag for on-demand invalidation |

---

## Fetching with ORMs / Databases

Since Server Components run on the server, you can query your database **directly** without going through API routes:

```tsx
// app/blog/page.tsx
import { db, posts } from '@/lib/db'

export default async function BlogPage() {
  const allPosts = await db.select().from(posts)

  return (
    <ul>
      {allPosts.map((post) => (
        <li key={post.id}>{post.title}</li>
      ))}
    </ul>
  )
}
```

**Security note:** Server Components can safely access environment variables and database credentials — they never ship to the client.

---

## Deduplication with React's `cache()`

When the same data is needed in multiple places within a render tree, wrap the fetch in `React.cache()` to deduplicate:

```tsx
// app/lib/data.ts
import { cache } from 'react'
import { db } from '@/lib/db'

// This runs once per render pass, even if called multiple times
export const getPost = cache(async (slug: string) => {
  return db.query.posts.findFirst({ where: eq(posts.slug, slug) })
})
```

```tsx
// app/blog/[slug]/page.tsx
// getPost is called twice but executes only once
import { getPost } from '@/lib/data'

export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params
  const post = await getPost(slug) // First call
  return { title: post.title, description: post.description }
}

export default async function Page({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params
  const post = await getPost(slug) // Second call — deduplicated!
  return <div>{post.content}</div>
}
```

---

## Parallel Data Fetching

Initiate all requests simultaneously, then `await` them with `Promise.all()`:

```tsx
// app/artist/[username]/page.tsx
import { getArtist, getAlbums } from '@/lib/data'

export default async function Page({
  params,
}: {
  params: Promise<{ username: string }>
}) {
  const { username } = await params

  // Initiate both requests at the same time
  const artistData = getArtist(username)
  const albumsData = getAlbums(username)

  // Await both in parallel
  const [artist, albums] = await Promise.all([artistData, albumsData])

  return (
    <>
      <h1>{artist.name}</h1>
      <Albums list={albums} />
    </>
  )
}

// Separate functions that initiate fetches
async function getArtist(username: string) {
  const res = await fetch(`https://api.example.com/artist/${username}`)
  return res.json()
}

async function getAlbums(username: string) {
  const res = await fetch(`https://api.example.com/artist/${username}/albums`)
  return res.json()
}
```

**Tip:** Use `Promise.allSettled()` instead of `Promise.all()` if one failure shouldn't block the others:

```tsx
const [artistResult, albumsResult] = await Promise.allSettled([
  getArtist(username),
  getAlbums(username),
])
```

---

## Sequential Data Fetching

When one request depends on another, `await` them in order:

```tsx
export default async function Page({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params

  // First: get the artist
  const artist = await getArtist(id)

  // Second: get playlists (requires artist ID)
  return (
    <>
      <h1>{artist.name}</h1>
      <Suspense fallback={<div>Loading playlists...</div>}>
        <Playlists artistId={artist.id} />
      </Suspense>
    </>
  )
}

async function Playlists({ artistId }: { artistId: string }) {
  const playlists = await getArtistPlaylists(artistId)
  return (
    <ul>
      {playlists.map((p) => (
        <li key={p.id}>{p.name}</li>
      ))}
    </ul>
  )
}
```

**Tip:** Ensure the first request resolves quickly — it blocks everything downstream.

---

## Sharing Data Across Server + Client Components

Combine `React.cache()` with Context to share fetched data between Server and Client Components:

```tsx
// app/lib/user.ts
import { cache } from 'react'

export const getUser = cache(async () => {
  const res = await fetch('https://api.example.com/user')
  return res.json()
})
```

```tsx
// app/user-provider.tsx
'use client'
import { createContext } from 'react'

type User = { id: string; name: string }

export const UserContext = createContext<Promise<User> | null>(null)

export default function UserProvider({
  children,
  userPromise,
}: {
  children: React.ReactNode
  userPromise: Promise<User>
}) {
  return (
    <UserContext.Provider value={userPromise}>
      {children}
    </UserContext.Provider>
  )
}
```

```tsx
// app/layout.tsx
import UserProvider from './user-provider'
import { getUser } from './lib/user'

export default function RootLayout({ children }: { children: React.ReactNode }) {
  const userPromise = getUser() // Don't await — pass the promise
  return (
    <html>
      <body>
        <UserProvider userPromise={userPromise}>{children}</UserProvider>
      </body>
    </html>
  )
}
```

```tsx
// app/ui/profile.tsx — Client Component
'use client'
import { use, useContext } from 'react'
import { UserContext } from '../user-provider'

export function Profile() {
  const userPromise = useContext(UserContext)
  if (!userPromise) throw new Error('Missing UserProvider')
  const user = use(userPromise)
  return <p>Hello, {user.name}!</p>
}
```

**Important:** `React.cache` is scoped to the current request only — no sharing between different requests.

---

## Data Fetching in Client Components

For Client Components (interactive UI, real-time data, Web APIs):

### Using React's `use()` Hook for Streaming

Pass a promise from a Server Component to a Client Component:

```tsx
// app/blog/page.tsx — Server Component
import Posts from '@/app/ui/posts'
import { Suspense } from 'react'

export default function Page() {
  const posts = getPosts() // Don't await — pass the promise
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <Posts posts={posts} />
    </Suspense>
  )
}
```

```tsx
// app/ui/posts.tsx — Client Component
'use client'
import { use } from 'react'

export default function Posts({
  posts,
}: {
  posts: Promise<{ id: string; title: string }[]>
}) {
  const allPosts = use(posts) // Reads the promise
  return (
    <ul>
      {allPosts.map((post) => (
        <li key={post.id}>{post.title}</li>
      ))}
    </ul>
  )
}
```

### Using SWR / React Query

```tsx
'use client'
import useSWR from 'swr'

const fetcher = (url: string) => fetch(url).then(r => r.json())

export default function BlogPage() {
  const { data, error, isLoading } = useSWR(
    'https://api.vercel.app/blog',
    fetcher
  )

  if (isLoading) return <div>Loading...</div>
  if (error) return <div>Error: {error.message}</div>

  return (
    <ul>
      {data.map((post: { id: string; title: string }) => (
        <li key={post.id}>{post.title}</li>
      ))}
    </ul>
  )
}
```

**When to use SWR/React Query:** Client-side data that depends on Web APIs (geolocation, File API), frequently polled data, or real-time updates.

---

## Gotchas

1. **Don't fetch from Route Handlers in Server Components** — call your data source (database, external API) directly. Route Handlers add an unnecessary HTTP roundtrip.
2. **Identical fetch requests are memoized** — Next.js deduplicates identical `fetch()` calls within the same render tree automatically.
3. **`fetch()` is not cached by default** — use `cache: 'force-cache'` or the `use cache` directive. Without caching, the page is dynamic.
4. **`params` is always a Promise** — `await` it before using in data fetches
5. **`React.cache` deduplicates within a request** — not across requests; each user gets their own cache scope
6. **Don't pass raw database records to Client Components** — create DTOs in a DAL (see `skills/auth.md`) to filter sensitive fields
7. **Prefetch data before blocking operations** — use `preload()` utility to start data fetching before `await` calls

---

## Prerequisites

- Next.js Core — see `skills/core.md`
- Routing basics — see `skills/routing.md`

## Next Steps

- **Streaming + Suspense:** See `skills/streaming.md` — wrap slow data in Suspense boundaries
- **Caching with Cache Components:** See `skills/caching.md` — `use cache`, `cacheLife`, `cacheTag`
- **Forms + mutations:** See `skills/mutations.md` — Server Actions for data mutations
- **Auth + database access:** See `skills/auth.md` — DAL, DTOs, secure data access
