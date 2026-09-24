# Next.js Security — CSP, Taint APIs, Server-Only, and Auditing

## Overview

Security in Next.js involves multiple layers: server-side data protection (DAL, DTOs), runtime protection (CSP, nonces), and build-time safeguards (taint APIs, server-only). This skill covers the complete security stack for production Next.js applications.

**Key patterns:**
- **CSP (Content Security Policy)** — prevent XSS with nonce-based script allowlisting
- **Taint APIs** — prevent accidental exposure of sensitive data to the client
- **`server-only`** — enforce server-only execution at build time
- **Environment variable security** — NEXT_PUBLIC_ prefix, secrets in DAL only
- **XSS prevention** — sanitize data, avoid dangerouslySetInnerHTML
- **IDOR prevention** — verify resource ownership in the DAL
- **CSRF prevention** — Server Actions use POST, SameSite cookies

**Related skills:** auth, proxy, mutations, route-handlers

---

## Environment Variables — Security First

```bash
# .env — NEVER commit this
DB_PASSWORD=super_secret_password
API_SECRET=internal_api_key

# NEXT_PUBLIC_ prefix exposes to client bundle — only use for PUBLIC values
NEXT_PUBLIC_ANALYTICS_ID=abc123
NEXT_PUBLIC_APP_URL=https://myapp.com
```

### Access Environment Variables

```ts
// ✅ CORRECT — access secrets only in server-side code
// app/lib/db.ts
import 'server-only'

const connectionString = process.env.DATABASE_URL
// connectionString is NEVER sent to the client

// ✅ CORRECT — public values available anywhere
// app/page.tsx
const appUrl = process.env.NEXT_PUBLIC_APP_URL // Inlined at build time
```

```tsx
// ❌ WRONG — never expose private env vars to the client
// app/page.tsx
const secret = process.env.DB_PASSWORD // EXPOSED in client bundle!
```

**Rule:** Only `NEXT_PUBLIC_` prefixed variables are exposed to the client. All others stay server-side. But never store truly sensitive values even in `NEXT_PUBLIC_`.

---

## `server-only` — Prevent Server Code in Client Bundle

Mark modules that must never be imported in Client Components:

```bash
pnpm add server-only
```

```ts
// app/lib/db.ts
import 'server-only'

// Any import of this file from a Client Component → BUILD ERROR
export async function getSecretData() {
  return db.query.privateData.findMany()
}
```

```tsx
// app/ui/client-component.tsx
'use client'
import { getSecretData } from '@/lib/db' // ❌ BUILD ERROR
// Error: Module 'server-only' cannot be imported from a Client Component
```

---

## Taint APIs — Prevent Accidental Data Exposure

Enable experimental taint to prevent passing sensitive objects directly to Client Components:

```ts
// next.config.ts
const nextConfig = {
  experimental: {
    taint: true,
  },
}
```

### `experimental_taintObjectReference`

Mark entire objects as tainted — they cannot be passed to Client Components:

```ts
// app/lib/data.ts
import { experimental_taintObjectReference } from 'react'

export async function getPrivateUserData(userId: string) {
  const user = await db.query.users.findFirst({
    where: eq(users.id, userId),
  })

  // Taint the entire user object
  experimental_taintObjectReference(
    'Sensitive user data cannot be passed to the client',
    user
  )

  return user // Return object but it cannot be passed as a prop to Client Components
}
```

```tsx
// app/profile/page.tsx — Server Component
import { getPrivateUserData } from '@/lib/data'

export default async function Page({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params
  const user = await getPrivateUserData(id)

  // ❌ TypeScript/Next.js error at build time
  return <ClientUserCard user={user} />
}
```

### `experimental_taintUniqueValue`

Mark specific sensitive values as tainted:

```ts
import { experimental_taintUniqueValue } from 'react'

export async function getPaymentToken(userId: string) {
  const token = await generatePaymentToken(userId)

  experimental_taintUniqueValue(
    'Payment token cannot be passed to the client',
    process,
    token
  )

  return token // Cannot be passed to Client Components
}
```

**Important:** Taint is an additional layer. Always filter data with DTOs in your DAL — don't rely on taint alone.

---

## Content Security Policy (CSP)

CSP prevents XSS by controlling which resources can be loaded. Use **nonce-based CSP** for maximum security.

### Enabling CSP via Proxy

```ts
// proxy.ts
import { NextRequest, NextResponse } from 'next/server'

export function proxy(request: NextRequest) {
  const nonce = Buffer.from(crypto.randomUUID()).toString('base64')
  const isDev = process.env.NODE_ENV === 'development'

  const cspHeader = `
    default-src 'self';
    script-src 'self' 'nonce-${nonce}' 'strict-dynamic'${isDev ? " 'unsafe-eval'" : ''};
    style-src 'self' 'nonce-${nonce}';
    img-src 'self' blob: data: https:;
    font-src 'self';
    object-src 'none';
    base-uri 'self';
    form-action 'self';
    frame-ancestors 'none';
    upgrade-insecure-requests;
  `.replace(/\s{2,}/g, ' ').trim()

  const requestHeaders = new Headers(request.headers)
  requestHeaders.set('x-nonce', nonce)

  const response = NextResponse.next({ request: { headers: requestHeaders } })
  response.headers.set('Content-Security-Policy', cspHeader)

  return response
}

export const config = {
  matcher: [
    {
      source: '/((?!api|_next/static|_next/image|favicon.ico).*)',
      missing: [
        { type: 'header', key: 'next-router-prefetch' },
        { type: 'header', key: 'purpose', value: 'prefetch' },
      ],
    },
  ],
}
```

### CSP + Third-Party Scripts

```tsx
// app/layout.tsx
import { GoogleTagManager } from '@next/third-parties/google'
import { headers } from 'next/headers'

export default async function RootLayout({ children }: { children: React.ReactNode }) {
  const nonce = (await headers()).get('x-nonce')

  return (
    <html lang="en">
      <body>
        {children}
        <GoogleTagManager
          gtmId="GTM-XYZ"
          nonce={nonce ?? undefined}
        />
      </body>
    </html>
  )
}
```

### CSP with Subresource Integrity (SRI)

For static exports, SRI is an alternative to nonces — hashes are generated at build time:

```ts
// next.config.ts
const nextConfig = {
  experimental: {
    sri: { algorithm: 'sha256' },
  },
}
```

---

## XSS Prevention

### Avoid `dangerouslySetInnerHTML`

```tsx
// ❌ DANGEROUS — userInput could contain malicious scripts
<div dangerouslySetInnerHTML={{ __html: userInput }} />

// ✅ SAFE — sanitize before rendering
import sanitizeHtml from 'sanitize-html'

<div dangerouslySetInnerHTML={{
  __html: sanitizeHtml(userInput, {
    allowedTags: ['b', 'i', 'em', 'strong', 'p', 'br'],
    allowedAttributes: {},
  })
}} />
```

### JSON-LD XSS Prevention

```tsx
// JSON.stringify doesn't sanitize — replace < characters
<script
  type="application/ld+json"
  dangerouslySetInnerHTML={{
    __html: JSON.stringify(jsonLd).replace(/</g, '\\u003c'),
  }}
/>
```

---

## CSRF Prevention

Server Actions automatically include CSRF protection:

1. Server Actions use **POST only** — GET cannot trigger them
2. Next.js compares the **Origin header** to the **Host header** — mismatched origins are rejected
3. **SameSite cookies** prevent cross-site cookie sending

For additional allowed origins (reverse proxies):

```ts
// next.config.ts
const nextConfig = {
  experimental: {
    serverActions: {
      allowedOrigins: ['my-proxy.com', '*.my-proxy.com'],
    },
  },
}
```

---

## IDOR Prevention (Insecure Direct Object Reference)

Always verify ownership in the DAL, not just at the page level:

```ts
// ❌ WRONG — page-level check is insufficient
export default async function DeleteButton({ postId }: { postId: string }) {
  const session = await auth()
  if (session?.user.role !== 'admin') return null

  return <button formAction={deletePost}>Delete</button> // User could forge this!
}

// ✅ CORRECT — verify inside the action
export async function deletePost(postId: string) {
  const session = await auth()
  if (!session?.user) throw new Error('Unauthorized')

  const post = await db.post.findUnique({ where: { id: postId } })
  if (post.authorId !== session.user.id) throw new Error('Forbidden')

  await db.post.delete({ where: { id: postId } })
}
```

---

## Security Headers (via Proxy)

```ts
// proxy.ts
export function proxy(request: NextRequest) {
  const response = NextResponse.next()

  response.headers.set('Strict-Transport-Security', 'max-age=63072000; includeSubDomains; preload')
  response.headers.set('X-Content-Type-Options', 'nosniff')
  response.headers.set('X-Frame-Options', 'DENY')
  response.headers.set('Referrer-Policy', 'strict-origin-when-cross-origin')
  response.headers.set('Permissions-Policy', 'camera=(), microphone=(), geolocation=()')

  return response
}
```

---

## Security Auditing Checklist

When auditing a Next.js project:

```markdown
## Security Audit Checklist

### Data Access Layer
- [ ] Is there a dedicated DAL module?
- [ ] Are database packages imported only in server-side code?
- [ ] Are env vars accessed only in the DAL?

### Client Components
- [ ] Are component props type-safe and minimal?
- [ ] Are there any raw DB records passed as props?

### Server Actions
- [ ] Is every action verified with auth inside the action?
- [ ] Is resource ownership checked (IDOR prevention)?
- [ ] Are DTOs returned, not raw DB records?
- [ ] Is input validated with Zod?

### Params and URLs
- [ ] Are URL params validated before use?
- [ ] Is `searchParams` re-verified server-side?

### Proxy and Route Handlers
- [ ] Does proxy verify auth before redirects?
- [ ] Are Route Handlers accessible without auth checks?
- [ ] Is sensitive data in error messages exposed?

### Dependencies
- [ ] Are dependencies up to date?
- [ ] Are there known CVEs in dependencies?
```

---

## Gotchas

1. **`NEXT_PUBLIC_` exposes to the bundle** — only use for truly public values; never secrets
2. **`server-only` causes build errors** — not runtime errors; catches accidental imports at build time
3. **Taint is experimental** — verify before using in production; always prefer DTO filtering
4. **CSP nonces require dynamic rendering** — static pages can't use nonces; pages with nonces cannot use ISR
5. **Sanitize before `dangerouslySetInnerHTML`** — `JSON.stringify` doesn't protect against XSS
6. **SameSite cookies are critical** — always set `sameSite: 'lax'` or `'strict'`
7. **Verify auth in every entry point** — Proxy guards are optimistic; Server Actions and Route Handlers need their own checks

---

## Prerequisites

- Next.js Core — see `skills/core.md`
- Auth — see `skills/auth.md`

## Next Steps

- **Proxy CSP setup:** See `skills/proxy.md` — nonce generation in proxy
- **Server Actions security:** See `skills/mutations.md` — verifying auth in actions
- **Route Handler security:** See `skills/route-handlers.md` — webhook verification
- **Full auth stack:** See `skills/auth.md` — DAL, DTOs, session management
