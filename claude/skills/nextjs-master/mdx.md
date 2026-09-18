# Next.js MDX — Markdown and MDX Setup with @next/mdx

## Overview

MDX is Markdown with JSX support — you can write Markdown and import React components directly inside it. Next.js supports MDX through `@next/mdx`, allowing MDX files to act as pages, routes, or imported modules.

**Key patterns:**
- **`@next/mdx`** — official Next.js MDX integration
- **`mdx-components.tsx`** — global MDX component overrides
- **File-based MDX pages** — MDX as route pages
- **Imported MDX** — import MDX files as components
- **Dynamic MDX imports** — load MDX based on route params

**Related skills:** core, routing, metadata, deployment

---

## Installation

```bash
pnpm add @next/mdx @mdx-js/loader @mdx-js/react @types/mdx
```

---

## Next.js Configuration

```js
// next.config.mjs
import createMDX from '@next/mdx'

const withMDX = createMDX({
  options: {
    remarkPlugins: [],
    rehypePlugins: [],
  },
})

/** @type {import('next').NextConfig} */
const nextConfig = {
  pageExtensions: ['js', 'jsx', 'md', 'mdx', 'ts', 'tsx'],
}

export default withMDX(nextConfig)
```

---

## `mdx-components.tsx` — Required for App Router

Create this file in the project root (same level as `app/` or `pages/`):

```tsx
// mdx-components.tsx
import type { MDXComponents } from 'mdx/types'

export function useMDXComponents(components: MDXComponents): MDXComponents {
  return {
    ...components,
  }
}
```

---

## MDX as File-Based Pages

Create MDX files directly in the app directory:

```
app/
├── mdx-page/
│   └── page.mdx
└── mdx-components.tsx
```

```mdx
---
title: Welcome to My Blog
date: 2024-01-15
---

import { Callout } from '@/components/callout'

# Welcome to My Blog

This is a **markdown** post with React components!

<Callout type="info">
  You can use any React component inside MDX!
</Callout>
```

---

## Imported MDX Components

Import MDX files as React components:

```
app/
├── blog/
│   └── page.tsx
├── content/
│   ├── welcome.mdx
│   └── getting-started.mdx
└── mdx-components.tsx
```

```tsx
// app/blog/page.tsx
import Welcome from '@/content/welcome.mdx'
import GettingStarted from '@/content/getting-started.mdx'

export default function BlogIndex() {
  return (
    <div>
      <Welcome />
      <hr />
      <GettingStarted />
    </div>
  )
}
```

---

## Dynamic MDX Routes

Load MDX files based on URL parameters:

```tsx
// app/blog/[slug]/page.tsx
export default async function Page({
  params,
}: {
  params: Promise<{ slug: string }>
}) {
  const { slug } = await params
  const { default: Content } = await import(`@/content/${slug}.mdx`)
  return <Content />
}

export async function generateStaticParams() {
  return [
    { slug: 'welcome' },
    { slug: 'getting-started' },
    { slug: 'advanced-features' },
  ]
}

export const dynamicParams = false // Only allow pre-generated slugs
```

---

## Custom MDX Components

Override default HTML elements or add custom components:

```tsx
// mdx-components.tsx
import type { MDXComponents } from 'mdx/types'
import { CustomCode } from '@/components/custom-code'
import { Callout } from '@/components/callout'

export function useMDXComponents(components: MDXComponents): MDXComponents {
  return {
    ...components,
    // Override default HTML elements
    h1: (props) => <h1 className="text-3xl font-bold" {...props} />,
    h2: (props) => <h2 className="text-2xl font-semibold" {...props} />,
    pre: (props) => <CustomCode {...props} />,
    // Add custom components available in all MDX files
    Callout,
    Video,
    InfoBox,
  }
}
```

---

## MDX with Frontmatter

Use `remark-frontmatter` to parse YAML frontmatter:

```bash
pnpm add remark-frontmatter gray-matter
```

```js
// next.config.mjs
import remarkFrontmatter from 'remark-frontmatter'

const withMDX = createMDX({
  options: {
    remarkPlugins: [remarkFrontmatter],
  },
})
```

```mdx
---
title: My Post
author: John Doe
tags: [nextjs, react, mdx]
---

# {frontmatter.title}

Written by {frontmatter.author}
```

---

## Custom Styles for MDX

### Using Tailwind Typography Plugin

```bash
pnpm add -D @tailwindcss/typography
```

```js
// tailwind.config.js
module.exports = {
  plugins: [
    require('@tailwindcss/typography'),
  ],
}
```

```tsx
// app/blog/[slug]/page.tsx
export default async function BlogPost({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params
  const { default: Content, frontmatter } = await import(`@/content/${slug}.mdx`)

  return (
    <article className="prose prose-lg prose-slate max-w-none">
      <h1>{frontmatter.title}</h1>
      <Content />
    </article>
  )
}
```

---

## Gotchas

1. **`mdx-components.tsx` is required in App Router** — without it, `@next/mdx` won't work
2. **Dynamic imports require file extension** — `import(\`@/content/${slug}.mdx\`)` must include `.mdx`
3. **`remarkPlugins`/`rehypePlugins` run during build** — plugins are configured in `next.config.mjs`
4. **MDX files are Server Components by default** — you can use async data in MDX
5. **Frontmatter needs a plugin** — MDX doesn't natively support frontmatter; add `remark-frontmatter`
6. **Component overrides must be in `useMDXComponents`** — return them from this function, don't mix with JSX imports

---

## Prerequisites

- Next.js Core — see `skills/core.md`
- Routing — see `skills/routing.md`

## Next Steps

- **MDX + metadata:** See `skills/metadata.md` — generate metadata from MDX frontmatter
- **MDX + ISR:** See `skills/isr.md` — `generateStaticParams` for all MDX blog posts
- **MDX + deployment:** See `skills/deployment.md` — static export for MDX-heavy sites
