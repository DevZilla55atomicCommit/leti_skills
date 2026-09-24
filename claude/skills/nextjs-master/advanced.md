# Next.js Advanced — Custom Server, Instrumentation, Draft Mode, PWA, Multi-Tenant, and Debugging

## Overview

This skill covers advanced Next.js patterns that go beyond standard App Router usage: custom servers for non-standard routing, OpenTelemetry instrumentation, Draft Mode for CMS preview, Progressive Web App (PWA) setup, multi-tenant architectures, multi-zones for micro-frontends, and debugging with VS Code and browser DevTools.

**Related skills:** deployment, proxy, security, data-fetching

---

## Custom Server

Use a custom server when you need non-standard routing (e.g., Express, Hono, custom HTTP handling):

```ts
// server.ts
import { createServer } from 'http'
import next from 'next'

const dev = process.env.NODE_ENV !== 'production'
const port = parseInt(process.env.PORT || '3000', 10)
const app = next({ dev })
const handle = app.getRequestHandler()

app.prepare().then(() => {
  createServer((req, res) => {
    // Custom routing logic here
    if (req.url === '/health') {
      res.writeHead(200, { 'Content-Type': 'application/json' })
      res.end(JSON.stringify({ status: 'ok' }))
      return
    }
    handle(req, res)
  }).listen(port, () => {
    console.log(`> Ready on http://localhost:${port}`)
  })
})
```

```json
{
  "scripts": {
    "dev": "node server.ts",
    "build": "next build",
    "start": "NODE_ENV=production node server.ts"
  }
}
```

**Note:** Custom servers remove Automatic Static Optimization. For most cases, use the built-in server instead.

---

## Instrumentation (`instrumentation.ts`)

Run code at server startup — for OpenTelemetry, database pool initialization, feature flag loading:

```ts
// instrumentation.ts
import { registerOTel } from '@vercel/otel'

export function register() {
  registerOTel('my-nextjs-app')
}
```

### Conditional Imports by Runtime

```ts
// instrumentation.ts
export async function register() {
  if (process.env.NEXT_RUNTIME === 'nodejs') {
    await import('./instrumentation-node')
  }
  if (process.env.NEXT_RUNTIME === 'edge') {
    await import('./instrumentation-edge')
  }
}
```

**Rules:**
- File must be at the project root (or inside `src/` if using `src/`)
- `register()` is called once per server instance startup
- Import inside `register()` to avoid global side effects

---

## OpenTelemetry

### With Vercel

```bash
pnpm add @vercel/otel
```

```ts
// instrumentation.ts
import { registerOTel } from '@vercel/otel'

export function register() {
  registerOTel('my-nextjs-app')
}
```

### Manual OpenTelemetry

```bash
pnpm add @opentelemetry/sdk-node @opentelemetry/auto-instrumentations-node @opentelemetry/exporter-trace-otlp-http
```

```ts
// instrumentation.ts
import { NodeSDK } from '@opentelemetry/sdk-node'
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-http'
import { getNodeAutoInstrumentations } from '@opentelemetry/auto-instrumentations-node'

const sdk = new NodeSDK({
  traceExporter: new OTLPTraceExporter({
    url: process.env.OTEL_EXPORTER_OTLP_ENDPOINT,
  }),
  instrumentations: [getNodeAutoInstrumentations()],
})

sdk.start()

process.on('SIGTERM', () => sdk.shutdown())
```

---

## Draft Mode (CMS Preview)

Enable Draft Mode to preview draft content from a headless CMS without rebuilding:

### 1. Create Draft Route Handler

```ts
// app/api/draft/route.ts
import { draftMode } from 'next/headers'
import { redirect } from 'next/navigation'

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url)
  const token = searchParams.get('token')
  const slug = searchParams.get('slug')

  if (token !== process.env.DRAFT_SECRET_TOKEN || !slug) {
    return new Response('Invalid token', { status: 401 })
  }

  const post = await getDraftPost(slug)
  if (!post) return new Response('Invalid slug', { status: 404 })

  const draft = await draftMode()
  draft.enable()
  redirect(post.slug)
}
```

### 2. Use Draft Data in Pages

```tsx
// app/blog/[slug]/page.tsx
import { draftMode } from 'next/headers'

export default async function Page({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params
  const { isEnabled } = await draftMode()

  const url = isEnabled
    ? `https://cms.example.com/drafts/${slug}`
    : `https://cms.example.com/posts/${slug}`

  const post = await fetch(url).then(r => r.json())

  return (
    <article>
      <h1>{post.title}</h1>
      {isEnabled && (
        <div className="bg-yellow-200 p-4">
          Draft Mode — Changes are not published
        </div>
      )}
      <div>{post.content}</div>
    </article>
  )
}
```

---

## Progressive Web App (PWA)

### Using `next-pwa`

```bash
pnpm add next-pwa
```

```js
// next.config.js
const withPWA = require('next-pwa')({
  dest: 'public',
  register: true,
  skipWaiting: true,
  disable: process.env.NODE_ENV === 'development',
})

module.exports = withPWA({
  // Next.js config
})
```

### Service Worker Registration

```ts
// app/service-worker.ts
/// <reference lib="webworker" />

declare const self: ServiceWorkerGlobalScope

self.addEventListener('fetch', (event) => {
  if (event.request.method !== 'GET') return

  event.respondWith(
    caches.match(event.request).then((cached) => {
      return cached || fetch(event.request).then((response) => {
        if (response.ok) {
          const clone = response.clone()
          caches.open('v1').then((cache) => cache.put(event.request, clone))
        }
        return response
      })
    })
  )
})

export {}
```

---

## Multi-Tenant Architecture

Serve multiple customers from a single Next.js app:

### Subdomain Routing

```ts
// proxy.ts
export async function proxy(request: NextRequest) {
  const hostname = request.headers.get('host') ?? ''
  const segments = hostname.split('.')

  // Extract tenant from subdomain: tenant.myapp.com
  if (segments.length >= 3) {
    const tenant = segments[0] // 'tenant'
    const url = request.nextUrl
    url.pathname = `/tenant/${tenant}${url.pathname}`
    return NextResponse.rewrite(url)
  }

  return NextNextResponse.next()
}
```

### Tenant Context

```tsx
// app/tenant/[tenant]/layout.tsx
import { notFound } from 'next/navigation'

export default async function TenantLayout({
  children,
  params,
}: {
  children: React.ReactNode
  params: Promise<{ tenant: string }>
}) {
  const { tenant } = await params
  const tenantData = await getTenant(tenant)

  if (!tenantData) notFound()

  return (
    <TenantProvider tenant={tenantData}>
      {children}
    </TenantProvider>
  )
}
```

---

## Multi-Zones (Micro-Frontends)

Deploy multiple Next.js apps under a single domain:

```ts
// next.config.js
module.exports = {
  async rewrites() {
    return [
      {
        source: '/shop/:path*',
        destination: 'https://shop.myapp.com/:path*',
      },
      {
        source: '/blog/:path*',
        destination: 'https://blog.myapp.com/:path*',
      },
    ]
  },
}
```

---

## Debugging — VS Code

### Launch Configuration

```json
// .vscode/launch.json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Next.js: Debug Server",
      "type": "node-terminal",
      "request": "launch",
      "command": "npm run dev -- --inspect"
    },
    {
      "name": "Next.js: Debug Client",
      "type": "chrome",
      "request": "launch",
      "url": "http://localhost:3000"
    },
    {
      "name": "Next.js: Debug Full Stack",
      "type": "node",
      "request": "launch",
      "program": "${workspaceFolder}/node_modules/next/dist/bin/next",
      "runtimeArgs": ["--inspect"],
      "skipFiles": ["<node_internals>/**"],
      "serverReadyAction": {
        "action": "debugWithEdge",
        "pattern": "- Local: .+(https?://.+)",
        "uriFormat": "%s",
        "webRoot": "${workspaceFolder}"
      }
    }
  ]
}
```

### Chrome DevTools for Server

```bash
npm run dev -- --inspect
# Open chrome://inspect → Remote Target → Next.js server
```

### Turbopack Tracing

```bash
NEXT_TURBOPACK_TRACING=1 npm run dev
# Trace file at .next/dev/trace-turbopack
npx next internal trace .next/dev/trace-turbopack
# Open https://trace.nextjs.org/ to visualize
```

---

## Debugging — Common Issues

```tsx
// Inspect Server Component errors
// proxy.ts — click the Node.js icon on the error overlay to open DevTools

// Inspect Client Component errors
// Use React DevTools browser extension
```

---

## Gotchas

1. **Custom server removes Automatic Static Optimization** — consider if you really need it
2. **`instrumentation.ts` runs once per server instance** — don't use for per-request logic
3. **Draft Mode sets a cookie** — it works only in browsers, not in server-side code
4. **PWA service workers only work in production** (`next start`) or HTTPS
5. **Multi-tenant subdomain detection** — `request.headers.get('host')` may include port; split carefully
6. **`--inspect` enables Node.js debugging** — use for server-side breakpoints
7. **Turbopack tracing is for development only** — performance issues, not production bugs

---

## Prerequisites

- Next.js Core — see `skills/core.md`
- Deployment — see `skills/deployment.md`

## Next Steps

- **OpenTelemetry:** See above — registerOTel for Vercel, manual SDK for self-hosted
- **Draft Mode:** See above — CMS preview pattern
- **Debugging:** See above — VS Code launch.json and Chrome DevTools
- **Performance:** See `skills/performance.md` — Turbopack tracing
