# Next.js Deployment — Docker, Node.js, Static Export, Vercel, Adapters, and CI

## Overview

Next.js can be deployed to any platform. This skill covers Node.js server deployments, Docker containers, static exports, platform-specific adapters (Vercel, Fly.io, Render, Netlify, Cloudflare), and CI/CD build caching for GitHub Actions, CircleCI, GitLab, and more.

**Deployment options:**

| Option | Features | Best For |
|--------|---------|---------|
| **Node.js server** | All features | Self-hosted, any VPS |
| **Docker** | All features, portable | Kubernetes, cloud containers |
| **Static export** | Static only | CDN, S3, Nginx |
| **Vercel** | All features, zero-config | Recommended, easiest |
| **Adapters** | Platform-specific | Fly.io, Render, Netlify, Cloudflare |

**Related skills:** isr, caching, advanced

---

## Node.js Server

### Package Scripts

```json
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start"
  }
}
```

```bash
npm run build
npm start
```

### `next start` Options

```bash
# Start on specific port
PORT=8080 npm start

# Start on specific host
HOST=0.0.0.0 npm start
```

---

## Docker

### Dockerfile (Standalone Output — Recommended)

The `standalone` output mode produces a minimal image with only the runtime files:

```dockerfile
# Dockerfile
FROM node:20-alpine AS base

# Install dependencies
FROM base AS deps
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm ci

# Build
FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

# Production
FROM base AS runner
WORKDIR /app
ENV NODE_ENV=production

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs
EXPOSE 3000
ENV PORT=3000

CMD ["node", "server.js"]
```

### Docker Compose

```yaml
version: '3.8'
services:
  nextjs:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - DATABASE_URL=postgres://db:5432/myapp
    depends_on:
      - db
```

### Dockerfile (Static Export)

```dockerfile
FROM nginx:alpine
COPY .next/static /usr/share/nginx/html/_next/static
COPY out /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

---

## Static Export (`output: 'export'`)

Generate static HTML/CSS/JS with no server required:

```ts
// next.config.ts
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  output: 'export',
  images: {
    unoptimized: true, // Required for static export
  },
}

export default nextConfig
```

```bash
npm run build
# Output in /out directory
```

**Limitations:** No server-side features (ISR, Route Handlers, Server Actions require a server).

---

## Platform Adapters

### Vercel (Recommended)

Zero configuration — Next.js detects the framework automatically.

```bash
# Install Vercel CLI
npm i -g vercel
vercel
```

Vercel supports all Next.js features including ISR, Image Optimization, and Edge Functions.

### Fly.io

```bash
# Install Fly CLI
fly launch
fly deploy
```

### Render

Connect your GitHub repository and use:
- **Build Command:** `npm run build`
- **Start Command:** `npm start`

### Netlify

Use `@netlify/plugin-nextjs` or connect via Git integration with:
- **Build Command:** `npm run build`
- **Publish Directory:** `.next`

### Cloudflare

```bash
npm install @next/mdx @cloudflare/next-on-pages
```

---

## CI/CD Build Caching

### GitHub Actions

```yaml
name: Next.js CI

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Build
        run: npm run build

      - uses: actions/cache@v4
        with:
          path: |
            ~/.npm
            ${{ github.workspace }}/.next/cache
          key: ${{ runner.os }}-nextjs-${{ hashFiles('**/package-lock.json') }}-${{ hashFiles('**/*.tsx') }}
          restore-keys: |
            ${{ runner.os }}-nextjs-${{ hashFiles('**/package-lock.json') }}-
```

### CircleCI

```yaml
steps:
  - save_cache:
      key: dependency-cache-{{ checksum "yarn.lock" }}
      paths:
        - ./node_modules
        - ./.next/cache
```

### GitLab CI

```yaml
cache:
  key: ${CI_COMMIT_REF_SLUG}
  paths:
    - node_modules/
    - .next/cache/
```

### Netlify

Use `@netlify/plugin-nextjs` — it handles caching automatically.

---

## Environment Variables in Deployment

### Build-Time Variables

Variables without `NEXT_PUBLIC_` are server-side only:

```bash
# Build-time (used during npm run build)
DATABASE_URL=postgres://...
API_SECRET=...
SESSION_SECRET=...
```

### Runtime Variables

For runtime-only variables (injected at startup):

```bash
# Docker
docker run -e NEXT_PUBLIC_ANALYTICS_ID=xxx myapp

# Docker Compose
environment:
  - NODE_ENV=production
  - DATABASE_URL=postgres://db:5432/myapp
```

### Vercel

Set environment variables in the Vercel Dashboard or via CLI:

```bash
vercel env add DATABASE_URL
vercel env add NEXT_PUBLIC_ANALYTICS_ID
```

---

## Health Check Endpoint

```ts
// app/api/health/route.ts
export async function GET() {
  return Response.json({
    status: 'ok',
    timestamp: new Date().toISOString(),
    uptime: process.uptime(),
  })
}
```

---

## Health Check with Database

```ts
// app/api/health/route.ts
export async function GET() {
  try {
    await db.execute(sql`SELECT 1`)
    return Response.json({
      status: 'ok',
      database: 'connected',
      timestamp: new Date().toISOString(),
    })
  } catch {
    return Response.json(
      { status: 'error', database: 'disconnected' },
      { status: 503 }
    )
  }
}
```

---

## Upgrading Next.js

```bash
# Use the upgrade command (Next.js 16.1.0+)
npx next upgrade

# For older versions
npx @next/codemod@canary upgrade latest

# Or manually
npm install next@latest react@latest react-dom@latest eslint-config-next@latest
```

---

## Gotchas

1. **`standalone` output is minimal** — no `node_modules`, just the server. For `node_modules`, copy from the `builder` stage or use `node_modules`
2. **`output: 'export'` disables ISR** — no server features work; use for truly static sites
3. **`NEXT_PUBLIC_` variables are inlined at build time** — changing them requires rebuild. Use a server-side API for runtime-config values
4. **Docker on Mac/Windows is slow for dev** — use local `npm run dev` instead of Docker for development
5. **`npm run lint` no longer runs during build** (Next.js 16) — add it to your CI pipeline explicitly
6. **CI caching key must include source files** — `package-lock.json` alone won't catch code changes
7. **`unoptimized: true` is required for static export with images** — image optimization requires a server

---

## Prerequisites

- Next.js Core — see `skills/core.md`
- ISR — see `skills/isr.md`

## Next Steps

- **Docker in production:** See above — standalone output Dockerfile
- **CI caching:** See above — GitHub Actions, CircleCI, GitLab configs
- **Custom server:** See `skills/advanced.md` — Express/custom server for complex routing
