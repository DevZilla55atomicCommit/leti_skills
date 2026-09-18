# Next.js ISR — Incremental Static Regeneration

## Overview

ISR enables pages to be statically generated at build time while still being updated after deployment — without rebuilding the entire site. It's the best of both worlds: static performance with dynamic freshness.

**Key patterns:**
- **`revalidate`** — set time-based revalidation in seconds
- **`generateStaticParams`** — prerender dynamic routes at build time
- **`dynamicParams`** — control 404 behavior for unknown dynamic routes
- **On-demand revalidation** — revalidate via `revalidatePath()` or `revalidateTag()`

**Related skills:** core, routing, caching, metadata, mutations

---

## How ISR Works

```
1. Build: Next.js generates static HTML for all known pages
2. Request: Cached HTML is served instantly
3. After N seconds (revalidate): Next.js serves stale page immediately
4. Background: Next.js regenerates fresh HTML for next visitor
5. Next request: Fresh page is cached and served
```

---

## Basic ISR — `revalidate`

```tsx
// app/blog/[id]/page.tsx
interface Post {
  id: string
  title: string
  content: string
}

export const revalidate = 60 // Revalidate at most once per 60 seconds

export async function generateStaticParams() {
  const posts: Post[] = await fetch('https://api.example.com/blog').then(r => r.json())
  return posts.map((post) => ({ id: String(post.id) }))
}

export default async function Page({
  params,
}: {
  params: Promise<{ id: string }>
}) {
  const { id } = await params
  const post: Post = await fetch(`https://api.example.com/blog/${id}`).then(r => r.json())

  return (
    <main>
      <h1>{post.title}</h1>
      <p>{post.content}</p>
    </main>
  )
}
```

---

## `generateStaticParams` — Prerendering Dynamic Routes

Generate static HTML for known dynamic routes at build time:

```tsx
// app/products/[category]/[slug]/page.tsx

export async function generateStaticParams() {
  const categories = await db.query.categories.findMany()
  const params: { category: string; slug: string }[] = []

  for (const category of categories) {
    const products = await db.query.products.findMany({
      where: eq(products.categoryId, category.id),
      columns: { slug: true },
    })
    for (const product of products) {
      params.push({ category: category.slug, slug: product.slug })
    }
  }

  return params
}

export const revalidate = 3600 // Revalidate every hour

export default async function Page({
  params,
}: {
  params: Promise<{ category: string; slug: string }>
}) {
  const { category, slug } = await params
  const product = await getProduct(category, slug)
  return <ProductPage product={product} />
}
```

---

## `dynamicParams` — Control Unknown Routes

By default, Next.js generates unknown dynamic routes on-demand (returns 404 only if the route truly doesn't exist). Set `dynamicParams = false` to return 404 for routes not in `generateStaticParams`:

```tsx
// app/blog/[slug]/page.tsx
export async function generateStaticParams() {
  // Only prerender these 5 posts at build time
  const featuredPosts = await getFeaturedPosts()
  return featuredPosts.map((post) => ({ slug: post.slug }))
}

export const dynamicParams = false // Only allow pre-generated slugs

export default async function Page({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params
  const post = await getPost(slug)
  if (!post) notFound()
  return <Article post={post} />
}
```

---

## On-Demand Revalidation

When content changes (e.g., CMS update), trigger revalidation immediately:

### From a Server Action

```ts
// app/actions.ts
'use server'
import { revalidatePath, revalidateTag } from 'next/cache'

export async function publishPost(postId: string) {
  await db.post.update({ where: { id: postId }, data: { published: true } })
  // Invalidate the specific post page
  revalidatePath(`/posts/${postId}`)
  // Or invalidate all posts
  revalidateTag('posts')
}
```

### From a Webhook (Route Handler)

```ts
// app/api/revalidate/route.ts
import { type NextRequest, NextResponse } from 'next/server'
import { revalidateTag } from 'next/cache'

export async function POST(request: NextRequest) {
  const token = request.nextUrl.searchParams.get('token')
  if (token !== process.env.REVALIDATE_SECRET_TOKEN) {
    return NextResponse.json({ success: false }, { status: 401 })
  }

  const payload = await request.json()
  if (payload.type === 'post.updated') {
    revalidateTag('posts')
  }

  return NextResponse.json({ revalidated: true })
}
```

---

## ISR with Database Queries

```tsx
// app/blog/[slug]/page.tsx
import { db, posts } from '@/lib/db'
import { eq } from 'drizzle-orm'

export const revalidate = 300 // 5 minutes

export async function generateStaticParams() {
  const allPosts = await db.select().from(posts)
  return allPosts.map((post) => ({ slug: post.slug }))
}

export default async function Page({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params
  const [post] = await db.select().from(posts).where(eq(posts.slug, slug))
  if (!post) notFound()
  return <article>{post.content}</article>
}
```

---

## Time-Based Revalidation Reference

| `revalidate` | Behavior |
|-------------|---------|
| `0` | Always dynamic (never cached) |
| `false` (default) | Cached indefinitely until revalidated |
| `60` | Revalidate at most every 60 seconds |
| `3600` | Revalidate at most every hour |
| `86400` | Revalidate at most once per day |

**Tip:** Set high revalidation times (hours, not seconds). Use on-demand revalidation for precise control.

---

## ISR + CI Build Caching

CI environments can reuse the `.next/cache` directory to speed up builds. Configure for each CI provider:

### GitHub Actions

```yaml
- uses: actions/cache@v4
  with:
    path: |
      ~/.npm
      ${{ github.workspace }}/.next/cache
    key: ${{ runner.os }}-nextjs-${{ hashFiles('**/package-lock.json') }}-${{ hashFiles('**/*.tsx') }}
    restore-keys: |
      ${{ runner.os }}-nextjs-${{ hashFiles('**/package-lock.json') }}-
```

---

## ISR Caveats

1. **ISR requires Node.js runtime** — not supported with static export (`output: 'export'`)
2. **Multiple fetch requests with different revalidate times** — the lowest time wins for the whole route segment
3. **`revalidate = 0` forces dynamic rendering** — if any fetch has `cache: 'no-store'` or revalidate 0, the whole route is dynamic
4. **Proxy doesn't run for on-demand ISR requests** — revalidate the exact path, not a rewritten one
5. **`generateStaticParams` is for known paths** — unknown paths are generated on-demand if `dynamicParams` defaults to true
6. **Revalidation happens on next request** — after the revalidate period, the first visitor gets stale content while the page regenerates
7. **Cookie-based content cannot be ISR'd** — if a page reads `cookies()`, it's dynamic regardless of `revalidate`

---

## Gotchas

1. **`revalidate` is a route segment config** — export it from `page.tsx`, `layout.tsx`, or both
2. **Route segment revalidation** — child pages are revalidated at least as frequently as parent layouts
3. **`generateStaticParams` runs at build time** — no runtime API calls available
4. **Revalidation errors** — if regeneration fails, the last successfully generated page continues to be served
5. **`revalidatePath` invalidates cache entries** — regeneration happens on the next request, not immediately
6. **Vercel automatically configures ISR** — no additional setup needed on Vercel

---

## Prerequisites

- Next.js Core — see `skills/core.md`
- Routing — see `skills/routing.md`

## Next Steps

- **Cache Components (new model):** See `skills/caching.md` — `use cache` + Partial Prerendering
- **Server Actions + revalidation:** See `skills/mutations.md` — `updateTag` for immediate expiry
- **Metadata + ISR:** See `skills/metadata.md` — `generateMetadata` with ISR pages
- **Deployment:** See `skills/deployment.md` — ISR on self-hosted Node.js
