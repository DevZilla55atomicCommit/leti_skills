# Next.js Route Handlers — API Routes, NextRequest, NextResponse, and Webhooks

## Overview

Route Handlers are the App Router equivalent of API Routes. They let you create custom HTTP endpoints using the Web Request/Response APIs. Route Handlers live inside the `app` directory and are the bridge between your frontend and any external services.

**Key APIs:**
- `GET`, `POST`, `PUT`, `PATCH`, `DELETE`, `HEAD`, `OPTIONS` — HTTP methods
- `NextRequest` — extended Request with parsed URL, cookies, headers
- `NextResponse` — helpers: `json()`, `redirect()`, `rewrite()`
- `cookies()` from `next/headers` — read/write cookies
- `RouteContext` — TypeScript helper for typed `params`
- `revalidateTag()` — revalidate cache from external webhooks

**Related skills:** mutations, proxy, auth, caching, security

---

## Basic Route Handler

```ts
// app/api/route.ts
export async function GET(request: Request) {
  return Response.json({ message: 'Hello, world!' })
}
```

**Route Handler vs Page:** A route at `/api` can have both `page.tsx` (UI) and `route.ts` (API) because `page.tsx` only handles GET via the UI and `route.ts` handles HTTP verbs. However, you cannot have `route.ts` and `page.tsx` at the same level.

---

## HTTP Methods

```ts
// app/api/items/route.ts
export async function GET(request: Request) {
  const items = await db.query.items.findMany()
  return Response.json({ items })
}

export async function POST(request: Request) {
  const body = await request.json()
  const item = await db.item.create({ data: body })
  return Response.json({ item }, { status: 201 })
}

export async function PUT(request: Request) {
  const body = await request.json()
  const item = await db.item.update({ where: { id: body.id }, data: body })
  return Response.json({ item })
}

export async function DELETE(request: Request) {
  const { searchParams } = new URL(request.url)
  const id = searchParams.get('id')
  await db.item.delete({ where: { id } })
  return new Response(null, { status: 204 })
}
```

---

## NextRequest and NextResponse

```ts
import { type NextRequest, NextResponse } from 'next/server'

export async function GET(request: NextRequest) {
  // nextUrl — parsed URL with searchParams
  const { pathname, searchParams } = request.nextUrl
  const page = searchParams.get('page') ?? '1'

  // Read cookies
  const token = request.cookies.get('session')?.value

  // Check headers
  const auth = request.headers.get('authorization')

  // redirect()
  if (!token) {
    return NextResponse.redirect(new URL('/login', request.url))
  }

  // rewrite()
  return NextResponse.rewrite(new URL('/api-proxy', request.url))

  // json() shortcut
  return NextResponse.json({ page }, { status: 200 })
}
```

---

## Reading Request Bodies

```ts
// JSON
export async function POST(request: Request) {
  const data = await request.json()
  return Response.json({ received: data })
}

// FormData
export async function POST(request: Request) {
  const formData = await request.formData()
  const email = formData.get('email')
  return Response.json({ email })
}

// Read body only once — clone if needed twice
export async function POST(request: Request) {
  try {
    const clone = request.clone()
    await request.json()     // First read
    await clone.json()      // Second read from clone
    return Response.json({ ok: true })
  } catch {
    return Response.json({ ok: false }, { status: 400 })
  }
}
```

---

## Setting Cookies

```ts
import { NextResponse } from 'next/server'

export async function POST(request: Request) {
  const response = NextResponse.json({ success: true })

  // Set cookie
  response.cookies.set('session', 'abc123', {
    httpOnly: true,  // JavaScript can't read it
    secure: true,    // HTTPS only
    sameSite: 'lax', // CSRF protection
    maxAge: 60 * 60 * 24 * 7, // 7 days
    path: '/',
  })

  return response
}
```

### Using `cookies()` from `next/headers`

```ts
import { cookies } from 'next/headers'

export async function GET(request: Request) {
  const cookieStore = await cookies()
  const session = cookieStore.get('session')?.value

  // Set (in Server Actions — in Route Handlers use NextResponse.cookies)
  cookieStore.set('theme', 'dark')

  // Delete
  cookieStore.delete('session')

  return Response.json({ session })
}
```

---

## Caching Route Handler Responses

Route Handlers are **not cached by default**. Opt in with `export const dynamic = 'force-static'`:

```ts
// app/api/static-data/route.ts
export const dynamic = 'force-static'

export async function GET() {
  // This response is cached
  return Response.json({
    data: [1, 2, 3],
    generatedAt: new Date().toISOString(), // Won't update in cache
  })
}
```

**With Cache Components:** Route Handlers follow the same prerendering model as pages:
- **Static** — doesn't access runtime data → prerendered at build
- **Dynamic** — accesses `headers()`, `cookies()` → rendered at request time
- **Cached** — uses `use cache` → prerendered with revalidation

---

## Webhook Receiver

```ts
// app/api/webhook/route.ts
import { type NextRequest, NextResponse } from 'next/server'
import { revalidateTag } from 'next/cache'

export async function POST(request: NextRequest) {
  // Verify webhook signature
  const token = request.nextUrl.searchParams.get('token')
  if (token !== process.env.REVALIDATE_SECRET_TOKEN) {
    return NextResponse.json({ success: false }, { status: 401 })
  }

  // Read the webhook payload
  const payload = await request.json()

  // Trigger content revalidation when CMS updates
  if (payload.event === 'post.published') {
    revalidateTag('posts')
  }

  return NextResponse.json({ success: true })
}
```

---

## Route Handler for Static Files (sitemap, robots)

```ts
// app/sitemap.ts
import { MetadataRoute } from 'next'

export default function sitemap(): MetadataRoute.Sitemap {
  return [
    {
      url: 'https://example.com',
      lastModified: new Date(),
      changeFrequency: 'yearly',
      priority: 1,
    },
    {
      url: 'https://example.com/blog',
      lastModified: new Date(),
      changeFrequency: 'weekly',
      priority: 0.8,
    },
  ]
}
```

```ts
// app/robots.ts
import { MetadataRoute } from 'next'

export default function robots(): MetadataRoute.Robots {
  return {
    rules: {
      userAgent: '*',
      allow: '/',
      disallow: '/private/',
    },
    sitemap: 'https://example.com/sitemap.xml',
  }
}
```

---

## TypeScript — `RouteContext` Helper

```ts
// app/users/[id]/route.ts
import type { NextRequest } from 'next/server'

export async function GET(
  _req: NextRequest,
  ctx: RouteContext<'/users/[id]'>
) {
  const { id } = await ctx.params
  return Response.json({ id })
}
```

Types are generated during `next dev`, `next build`, or `next typegen`.

---

## Content Negotiation (Serve Different Formats)

```ts
// app/docs/md/[...slug]/route.ts
export async function GET(
  request: Request,
  { params }: { params: Promise<{ slug: string[] }> }
) {
  const { slug } = await params
  const doc = await getDocsMd(slug)

  // Check Accept header
  const accept = request.headers.get('accept') ?? ''
  const wantsMarkdown = accept.includes('text/markdown')

  if (wantsMarkdown) {
    return new Response(doc, {
      headers: {
        'Content-Type': 'text/markdown; charset=utf-8',
        'Vary': 'Accept',
      },
    })
  }

  // Serve HTML
  return new Response(renderToHTML(doc), {
    headers: { 'Vary': 'Accept' },
  })
}
```

**Tip:** Always include `Vary: Accept` when content depends on request headers.

---

## Proxy Pattern — Rewrite to External API

```ts
// app/api/proxy/route.ts
import { NextResponse } from 'next/server'

export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams
  const targetUrl = `https://api.example.com/data?${searchParams.toString()}`

  const response = await fetch(targetUrl, {
    headers: {
      Authorization: `Bearer ${process.env.API_SECRET}`,
    },
  })

  const data = await response.json()
  return NextResponse.json(data)
}
```

---

## Gotchas

1. **Route Handlers are not cached by default** — use `export const dynamic = 'force-static'` for static responses
2. **`params` is always a Promise** — `await ctx.params` before using
3. **Route Handlers cannot share data** — each invocation is stateless
4. **File size limits** — avoid returning very large payloads; use streaming for files
5. **No WebSockets in Route Handlers** — connection closes after response
6. **Don't call Route Handlers from Server Components** — fetch directly from the data source instead
7. **`revalidateTag()` works in Route Handlers** — useful for webhook-triggered cache invalidation

---

## Prerequisites

- Next.js Core — see `skills/core.md`
- Server Actions — see `skills/mutations.md`

## Next Steps

- **Proxy/Middleware:** See `skills/proxy.md` — global request/response manipulation
- **Auth in Route Handlers:** See `skills/auth.md` — JWT verification, session checks
- **Webhook security:** See `skills/security.md` — signature verification, payload validation
- **Caching from webhooks:** See `skills/caching.md` — `revalidateTag` in Route Handlers
