# Next.js Performance — Lazy Loading, Bundle Optimization, Turbopack, and next/dynamic

## Overview

Next.js provides several tools to optimize performance: lazy loading components, reducing bundle size, optimizing imports, and using Turbopack for faster builds. This skill covers everything from `next/dynamic` for component lazy loading to `optimizePackageImports` for reducing bundle size.

**Key patterns:**
- **`next/dynamic`** — lazy load Client Components
- **`ssr: false`** — skip SSR for client-only components
- **Named exports** — import specific exports instead of entire libraries
- **`optimizePackageImports`** — auto-optimize known libraries
- **Tailwind content config** — prevent scanning `node_modules`
- **Barrel file avoidance** — import from specific files
- **Turbopack vs Webpack** — choosing the right bundler

**Related skills:** core, streaming, deployment

---

## `next/dynamic` — Lazy Load Components

`next/dynamic` is a wrapper around `React.lazy()` and `Suspense` for lazy-loading Client Components:

```tsx
// app/page.tsx
'use client'
import { useState } from 'react'
import dynamic from 'next/dynamic'

// Lazy load — only loads when showMore is true
const HeavyComponent = dynamic(() => import('../components/HeavyComponent'))

// Lazy load with loading fallback
const Dashboard = dynamic(
  () => import('../components/Dashboard'),
  {
    loading: () => <div>Loading...</div>,
  }
)

// Skip SSR — client-only (uses window/document)
const Map = dynamic(() => import('../components/Map'), { ssr: false })

export default function Page() {
  const [showMore, setShowMore] = useState(false)

  return (
    <div>
      <Dashboard />
      {showMore && <HeavyComponent />}
      <button onClick={() => setShowMore(true)}>Show more</button>
      <Map />
    </div>
  )
}
```

---

## `ssr: false` — Client-Only Components

Components that use browser APIs (`window`, `document`, `localStorage`) should skip SSR:

```tsx
// ✅ CORRECT
const Map = dynamic(() => import('./Map'), { ssr: false })

// ❌ WRONG — ssr:false on a Server Component
// next/dynamic only works with Client Components
```

```tsx
// components/Map.tsx
'use client' // Must be a Client Component
import { useEffect, useState } from 'react'

export function Map() {
  const [map, setMap] = useState(null)

  useEffect(() => {
    // window is available here
    const L = require('leaflet')
    const instance = L.map('map').setView([51.505, -0.09], 13)
    setMap(instance)
  }, [])

  return <div id="map" />
}
```

---

## Dynamic Imports — Named Exports

Import specific named exports to reduce bundle size:

```tsx
// ❌ WRONG — imports entire library
import { TriangleIcon } from '@phosphor-icons/react'

// ✅ CORRECT — imports only TriangleIcon
import { TriangleIcon } from '@phosphor-icons/react/dist/csr/Triangle'
```

Check the library's documentation for the correct import path.

---

## External Libraries with Dynamic Import

```tsx
// app/search/page.tsx
'use client'
import { useState } from 'react'

export default function SearchPage() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState([])

  async function handleSearch(e: React.ChangeEvent<HTMLInputElement>) {
    const { value } = e.target
    setQuery(value)

    if (value.length < 2) return

    // Dynamically load fuse.js only when needed
    const Fuse = (await import('fuse.js')).default
    const fuse = new Fuse(items)
    setResults(fuse.search(value))
  }

  return (
    <div>
      <input value={query} onChange={handleSearch} placeholder="Search..." />
      {results.map(r => <div key={r.item.id}>{r.item.name}</div>)}
    </div>
  )
}
```

---

## `optimizePackageImports` — Auto-Optimize Libraries

Configure known libraries with barrel exports to auto-optimize imports:

```ts
// next.config.ts
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  experimental: {
    optimizePackageImports: [
      '@phosphor-icons/react',
      'react-icons',
      '@mantine/core',
      '@mui/material',
      'lodash',
      'date-fns',
    ],
  },
}

export default nextConfig
```

**Turbopack:** Turbopack automatically optimizes imports — no config needed.

---

## Tailwind CSS — Content Array Optimization

Be specific about which files Tailwind scans:

```js
// ✅ CORRECT — specific path, won't scan node_modules
content: ['./src/**/*.{js,ts,jsx,tsx}']

// ❌ WRONG — too broad, scans everything including node_modules
content: ['./**/*.{js,ts,jsx,tsx}']
```

For monorepos:

```js
content: [
  './apps/web/src/**/*.{js,ts,jsx,tsx}',
  '../../../packages/ui/src/**/*.{js,ts,jsx,tsx}',
]
```

---

## Barrel File Avoidance

Barrel files (`index.ts` that re-exports from many modules) slow down builds because bundlers must parse them to find side effects:

```ts
// ❌ AVOID — index.ts re-exports everything
// components/index.ts
export { Button } from './button'
export { Input } from './input'
export { Modal } from './modal'
// ...
```

```tsx
// ✅ BETTER — import directly
import { Button } from '@/components/button'
import { Modal } from '@/components/modal'
```

---

## Turbopack vs Webpack

Turbopack is the default bundler for development and provides significantly faster builds:

```bash
# Turbopack (default, faster)
npm run dev

# Webpack (if needed)
npm run dev -- --webpack
npm run build -- --webpack
```

### When to Use Webpack

- Custom webpack loaders that Turbopack doesn't support
- Legacy webpack plugins
- Specific webpack configuration needs

---

## Bundle Analysis

### Turbopack Bundle Analyzer

Generate a trace for Turbopack performance analysis:

```bash
NEXT_TURBOPACK_TRACING=1 npm run dev
# Navigate around the app
# Stop the server
# Trace file is at .next/dev/trace-turbopack

# View the trace
npx next internal trace .next/dev/trace-turbopack
```

### Webpack Bundle Analyzer

```bash
pnpm add -D @next/bundle-analyzer
```

```js
// next.config.js
const withBundleAnalyzer = require('@next/bundle-analyzer')({
  enabled: process.env.ANALYZE === 'true',
})

module.exports = withBundleAnalyzer({})
```

```bash
ANALYZE=true npm run build
```

---

## Prefetching

Next.js prefetches linked pages automatically when they enter the viewport (`<Link>`):

```tsx
import Link from 'next/link'

// ✅ Prefetches /dashboard when this link enters viewport
<Link href="/dashboard">Dashboard</Link>

// ❌ Skips prefetch (useful for rarely visited pages)
<Link href="/admin" prefetch={false}>Admin</Link>

// Prefetch with specific loading
<Link href="/heavy-page" prefetchOnInteraction>Heavy Page</Link>
```

---

## Memory Optimization

For large applications, increase Node.js memory:

```bash
# Increase memory limit
NODE_OPTIONS="--max-old-space-size=4096" npm run build
```

---

## Performance Checklist

```markdown
## Performance Audit Checklist

### Bundle Size
- [ ] Icon imports use specific paths, not barrel files
- [ ] Heavy libraries (charts, maps) are lazy-loaded
- [ ] `optimizePackageImports` configured for known barrel-export libraries
- [ ] Bundle analyzer run — no unexpected large dependencies

### Images
- [ ] All images use `next/image`
- [ ] `priority` on above-the-fold images
- [ ] `sizes` prop on responsive images
- [ ] Remote images have `remotePatterns` configured

### Fonts
- [ ] Using `next/font` instead of Google Fonts `<link>` tags
- [ ] Variable fonts preferred over multiple weights

### Code Splitting
- [ ] Components lazy-loaded with `next/dynamic`
- [ ] `ssr: false` for client-only components
- [ ] No barrel `index.ts` files that pull in entire libraries

### CSS
- [ ] Tailwind content array is specific
- [ ] No unused CSS (PurgeCSS handles this)
```

---

## Gotchas

1. **`ssr: false` requires the component to be a Client Component** — `useEffect`, `window`, `document` are only available in Client Components
2. **`optimizePackageImports` is for known barrel-export libraries** — Turbopack doesn't need it (auto-optimizes)
3. **Turbopack is for development only** — production builds still use Webpack (or can use Turbopack with `next build --turbo`)
4. **Dynamic imports must use `import()` (promise syntax)** — `import('./component')` as a promise, not `import('./component').default`
5. **Bundle analyzer adds build time** — only run with `ANALYZE=true` when needed
6. **`--webpack` flag on `next build`** — enables webpack for production builds when needed
7. **Barrel files in `node_modules`** — `optimizePackageImports` handles known problematic libraries

---

## Prerequisites

- Next.js Core — see `skills/core.md`
- Streaming — see `skills/streaming.md`

## Next Steps

- **Deployment:** See `skills/deployment.md` — CI caching for faster builds
- **Lazy loading advanced:** See `skills/streaming.md` — `next/dynamic` + Suspense
- **Bundle analysis:** See above — Turbopack tracing + webpack bundle analyzer
