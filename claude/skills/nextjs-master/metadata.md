# Next.js Metadata — Metadata API, OG Images, Sitemap, Robots, and JSON-LD

## Overview

Next.js provides a Metadata API for managing `<head>` elements — titles, descriptions, Open Graph images, favicons, and more — without manually managing `<head>` tags. Metadata can be static (exported as an object) or dynamic (generated from data with `generateMetadata`).

**Key patterns:**
- **Static metadata** — export a `Metadata` object from any page/layout
- **Dynamic metadata** — export `generateMetadata()` function
- **Streaming metadata** — metadata streams separately from UI
- **OG images** — `ImageResponse` generates dynamic Open Graph images with JSX
- **File conventions** — `favicon.ico`, `icon.tsx`, `opengraph-image.tsx`
- **Sitemap** — `app/sitemap.ts` for dynamic sitemap
- **Robots** — `app/robots.ts` for robots.txt
- **JSON-LD** — structured data via `<script type="application/ld+json">`

**Related skills:** core, routing, images-fonts, isr

---

## Static Metadata

Export a `Metadata` object from any layout or page:

```tsx
// app/layout.tsx
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: {
    default: 'My App',              // Default title
    template: '%s | My App',        // Template: "Page Title | My App"
  },
  description: 'The best Next.js app ever',
  keywords: ['nextjs', 'react', 'web'],
  authors: [{ name: 'John Doe', url: 'https://example.com' }],
  creator: 'John Doe',
  openGraph: {
    type: 'website',
    locale: 'en_US',
    url: 'https://myapp.com',
    siteName: 'My App',
  },
  twitter: {
    card: 'summary_large_image',
    creator: '@johndoe',
  },
  robots: {
    index: true,
    follow: true,
  },
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
```

---

## Dynamic Metadata (generateMetadata)

Generate metadata from data — ideal for dynamic routes like blog posts:

```tsx
// app/blog/[slug]/page.tsx
import type { Metadata, ResolvingMetadata } from 'next'
import { notFound } from 'next/navigation'

type Props = {
  params: Promise<{ slug: string }>
  searchParams: Promise<{ [key: string]: string | string[] | undefined }>
}

export async function generateMetadata(
  { params, searchParams }: Props,
  parent: ResolvingMetadata
): Promise<Metadata> {
  const { slug } = await params

  const post = await fetch(`https://api.example.com/posts/${slug}`).then(r => r.json())

  if (!post) return { title: 'Post Not Found' }

  return {
    title: post.title,
    description: post.description,
    openGraph: {
      title: post.title,
      description: post.description,
      images: [{ url: post.ogImage, width: 1200, height: 630 }],
    },
    twitter: {
      card: 'summary_large_image',
      title: post.title,
      description: post.description,
      images: [post.ogImage],
    },
  }
}

export default async function Page({ params }: { params: Props['params'] }) {
  const { slug } = await params
  const post = await fetch(`https://api.example.com/posts/${slug}`).then(r => r.json())
  if (!post) notFound()
  return <article>{post.content}</article>
}
```

---

## Deduplicating Metadata Fetches

Use `React.cache` to avoid fetching the same data twice (for metadata + page):

```tsx
// app/lib/data.ts
import { cache } from 'react'

export const getPost = cache(async (slug: string) => {
  return db.query.posts.findFirst({ where: eq(posts.slug, slug) })
})
```

```tsx
// app/blog/[slug]/page.tsx
import { getPost } from '@/lib/data'

export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params
  const post = await getPost(slug) // Single fetch
  return { title: post.title, description: post.description }
}

export default async function Page({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params
  const post = await getPost(slug) // Deduplicated — same fetch as metadata
  return <article>{post.content}</article>
}
```

---

## Streaming Metadata

For dynamically rendered pages, metadata streams separately from the UI — visual content renders first while metadata loads:

```tsx
// app/blog/[slug]/page.tsx
export async function generateMetadata(
  { params }: { params: Promise<{ slug: string }> }
) {
  const { slug } = await params
  const post = await fetchSlowMetadata(slug) // Streams separately
  return {
    title: post.title,
    description: post.description,
    openGraph: { images: [post.ogImage] },
  }
}
```

**Bot handling:** Search engine bots (Twitterbot, Slackbot) that need metadata in `<head>` at crawl time will receive metadata synchronously. Configure with `htmlLimitedBots` in `next.config.ts` to customize this behavior.

---

## Dynamic OG Images (ImageResponse)

Generate dynamic Open Graph images with JSX and CSS:

```tsx
// app/blog/[slug]/opengraph-image.tsx
import { ImageResponse } from 'next/og'
import { getPost } from '@/lib/data'

export const size = { width: 1200, height: 630 }
export const contentType = 'image/png'

export default async function Image({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params
  const post = await getPost(slug)

  return new ImageResponse(
    (
      <div
        style={{
          fontSize: 48,
          background: 'white',
          width: '100%',
          height: '100%',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
          padding: 48,
        }}
      >
        <div style={{ display: 'flex', fontSize: 72, fontWeight: 'bold' }}>
          {post.title}
        </div>
        <div style={{ display: 'flex', fontSize: 32, color: '#666', marginTop: 24 }}>
          {post.author} — {post.date}
        </div>
      </div>
    ),
    { ...size }
  )
}
```

**CSS support:** flexbox, absolute positioning, custom fonts, text wrapping, centering. Grid is NOT supported.

---

## Favicon and App Icons

### Static Favicon

Place `favicon.ico` in the root `app/` directory:

```
app/
└── favicon.ico
```

### Generated Icon with JSX

```tsx
// app/icon.tsx
import { ImageResponse } from 'next/og'

export const size = { width: 48, height: 48 }
export const contentType = 'image/png'

export default function Icon() {
  return new ImageResponse(
    (
      <div
        style={{
          width: '100%',
          height: '100%',
          background: '#0070f3',
          borderRadius: 8,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          color: 'white',
          fontSize: 32,
          fontWeight: 'bold',
        }}
      >
        N
      </div>
    )
  )
}
```

### Apple Touch Icon

```tsx
// app/apple-icon.tsx
export const size = { width: 180, height: 180 }
export const contentType = 'image/png'

export default function AppleIcon() {
  return new ImageResponse(
    (
      <div style={{ width: '100%', height: '100%', background: '#fff' }}>
        <div style={{ fontSize: 100, textAlign: 'center', paddingTop: 40 }}>N</div>
      </div>
    ),
    { ...size }
  )
}
```

---

## Sitemap

### Static Sitemap

```ts
// app/sitemap.ts
import { MetadataRoute } from 'next'

export default function sitemap(): MetadataRoute.Sitemap {
  return [
    { url: 'https://myapp.com', lastModified: new Date(), changeFrequency: 'daily', priority: 1 },
    { url: 'https://myapp.com/blog', lastModified: new Date(), changeFrequency: 'weekly', priority: 0.8 },
  ]
}
```

### Dynamic Sitemap

```ts
// app/sitemap.ts
import { MetadataRoute } from 'next'

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const posts = await db.query.posts.findMany({
    columns: { slug: true, updatedAt: true },
    orderBy: desc(posts.updatedAt),
  })

  return posts.map((post) => ({
    url: `https://myapp.com/blog/${post.slug}`,
    lastModified: post.updatedAt,
    changeFrequency: 'weekly',
    priority: 0.7,
  }))
}
```

---

## Robots.txt

```ts
// app/robots.ts
import { MetadataRoute } from 'next'

export default function robots(): MetadataRoute.Robots {
  return {
    rules: [
      {
        userAgent: '*',
        allow: '/',
        disallow: ['/private/', '/admin/'],
      },
      {
        userAgent: 'Googlebot',
        allow: '/',
      },
    ],
    sitemap: 'https://myapp.com/sitemap.xml',
  }
}
```

---

## JSON-LD Structured Data

```tsx
// app/products/[id]/page.tsx
export default async function Page({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params
  const product = await getProduct(id)

  const jsonLd = {
    '@context': 'https://schema.org',
    '@type': 'Product',
    name: product.name,
    image: product.image,
    description: product.description,
    offers: {
      '@type': 'Offer',
      price: product.price,
      priceCurrency: 'USD',
    },
  }

  return (
    <section>
      {/* Sanitize to prevent XSS */}
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify(jsonLd).replace(/</g, '\\u003c'),
        }}
      />
      {/* ... */}
    </section>
  )
}
```

---

## Metadata API Reference

### Title Templates

```ts
// app/layout.tsx
export const metadata: Metadata = {
  title: {
    default: 'My App',           // Applied to all pages
    template: '%s | My App',     // "Page | My App"
  },
}

// app/about/page.tsx
export const metadata: Metadata = {
  title: 'About Us', // Renders as "About Us | My App"
}
```

### Metadata Fields

| Field | Type | Description |
|-------|------|-------------|
| `title` | `string \| { default, template, absolute }` | Page title |
| `description` | `string` | Meta description |
| `keywords` | `string[]` | Meta keywords |
| `authors` | `Author[]` | Article authors |
| `openGraph` | `OpenGraph` | Open Graph tags |
| `twitter` | `Twitter` | Twitter card tags |
| `robots` | `Robot` | Crawling directives |
| `viewport` | `string` | Viewport meta (auto-added) |
| `alternates` | `Alternates` | Canonical, hreflang |
| `icons` | `Icon` | Favicon, app icon |
| `manifest` | `string` | PWA manifest |

---

## Gotchas

1. **Metadata only in Server Components** — `metadata` and `generateMetadata` are not supported in Client Components
2. **`params` is always a Promise** — always `await` before using
3. **Use `React.cache` to deduplicate** — fetch data once for both metadata and page content
4. **JSON.stringify doesn't sanitize** — always replace `<` with `\u003c` to prevent XSS in JSON-LD
5. **`generateMetadata` streams independently** — bots that need full HTML get synchronous metadata; configure with `htmlLimitedBots`
6. **`ImageResponse` supports limited CSS** — flexbox and absolute positioning work; grid and complex layouts don't
7. **Sitemap URLs must be absolute** — always use full URLs like `https://myapp.com/blog`

---

## Prerequisites

- Next.js Core — see `skills/core.md`
- Routing for dynamic routes — see `skills/routing.md`

## Next Steps

- **Dynamic OG images with data:** See above — `getPost()` + ImageResponse
- **Image optimization:** See `skills/images-fonts.md` — next/image for all product images
- **ISR with metadata:** See `skills/isr.md` — generateStaticParams + metadata
- **Metadata security:** See `skills/security.md` — sanitizing JSON-LD
