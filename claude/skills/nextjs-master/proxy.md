# Next.js Proxy (Middleware) — Global Request Handling, CSP, and Security Headers

## Overview

The Proxy (formerly called Middleware) runs before a request is completed. It lets you modify the request or response — rewriting URLs, adding headers, checking authentication, and enforcing CSP — on a global or per-route basis. Only ONE `proxy.ts` file runs per project.

**Key capabilities:**
- Rewrite URLs (A/B testing, feature flags)
- Redirect users (auth guards, locale routing)
- Add/modify request and response headers
- Generate CSP nonces for scripts
- Match specific paths with `config.matcher`

**Related skills:** auth, security, caching, routing, route-handlers

---

## Basic Proxy

```ts
// proxy.ts — in the project root (or src/ if using src/)
import { type NextRequest, NextResponse } from 'next/server'

export function proxy(request: NextRequest) {
  // Every request passes through here first
  return NextResponse.next()
}

export const config = {
  // Run proxy only on specific paths
  matcher: ['/about/:path*', '/dashboard/:path*'],
}
```

---

## Proxy Matcher

```ts
export const config = {
  // Match all paths except static files
  matcher: [
    '/((?!api|_next/static|_next/image|favicon.ico).*)',
  ],
}

// Or match specific patterns:
matcher: [
  '/about/:path*',
  '/api/:path*',
  '/((?!private).*)', // Exclude /private
]

// Exclude based on headers:
matcher: [
  {
    source: '/(.*)',
    missing: [
      { type: 'header', key: 'next-router-prefetch' },
      { type: 'header', key: 'purpose', value: 'prefetch' },
    ],
  },
]
```

**Performance tip:** Be specific with matchers. Running proxy on all routes (including `_next/static`) adds latency to every static asset request.

---

## Authentication Guard

Protect routes by checking session cookies and redirecting unauthenticated users:

```ts
// proxy.ts
import { NextRequest, NextResponse } from 'next/server'
import { decrypt } from '@/lib/session'

const protectedRoutes = ['/dashboard', '/profile', '/settings']
const publicRoutes = ['/login', '/signup', '/']

export async function proxy(request: NextRequest) {
  const { pathname } = request.nextUrl

  const isProtectedRoute = protectedRoutes.some((route) =>
    pathname.startsWith(route)
  )
  const isPublicRoute = publicRoutes.includes(pathname)

  // Read session cookie
  const sessionCookie = request.cookies.get('session')?.value
  const session = await decrypt(sessionCookie)

  // Redirect unauthenticated users from protected routes to login
  if (isProtectedRoute && !session?.userId) {
    const loginUrl = new URL('/login', request.url)
    loginUrl.searchParams.set('redirect', pathname)
    return NextResponse.redirect(loginUrl)
  }

  // Redirect authenticated users from public routes to dashboard
  if (isPublicRoute && session?.userId && pathname === '/') {
    return NextResponse.redirect(new URL('/dashboard', request.url))
  }

  return NextResponse.next()
}
```

**Important:** Proxy does optimistic auth checks only — always verify auth inside Server Actions and Route Handlers. See `skills/auth.md` for the full Data Access Layer pattern.

---

## A/B Testing with Rewrites

```ts
// proxy.ts
export async function proxy(request: NextRequest) {
  const { pathname } = request.nextUrl

  // Only for the landing page
  if (pathname === '/') {
    // Check for experiment cookie
    const variant = request.cookies.get('ab-variant')?.value || 'control'

    if (variant === 'experiment') {
      // Rewrite to experiment page (URL stays /)
      const url = request.nextUrl
      url.pathname = '/landing-experiment'
      return NextResponse.rewrite(url)
    }
  }

  return NextResponse.next()
}
```

---

## Locale Detection and Redirection

```ts
// proxy.ts
import { match } from '@formatjs/intl-localematcher'
import Negotiator from 'negotiator'

const locales = ['en-US', 'fr-FR', 'de-DE', 'ja-JP']
const defaultLocale = 'en-US'

function getLocale(request: NextRequest): string {
  const headers = {
    'accept-language': request.headers.get('accept-language') ?? '',
  }
  const languages = new Negotiator({ headers }).languages()
  return match(languages, locales, defaultLocale)
}

export async function proxy(request: NextRequest) {
  const { pathname } = request.nextUrl

  // Check if pathname already has a locale
  const pathnameHasLocale = locales.some(
    (locale) => pathname.startsWith(`/${locale}/`) || pathname === `/${locale}`
  )

  if (pathnameHasLocale) return NextResponse.next()

  // Redirect to localized version
  const locale = getLocale(request)
  const url = request.nextUrl
  url.pathname = `/${locale}${pathname}`
  return NextResponse.redirect(url)
}

export const config = {
  matcher: ['/((?!api|_next/static|_next/image|favicon.ico).*)'],
}
```

---

## CSP Nonce Generation

Generate a cryptographic nonce for every request to allowlist specific inline scripts:

```ts
// proxy.ts
import { NextRequest, NextResponse } from 'next/server'

export function proxy(request: NextRequest) {
  // Generate a unique nonce for this request
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

  // Pass nonce to the app via custom header
  const requestHeaders = new Headers(request.headers)
  requestHeaders.set('x-nonce', nonce)

  const response = NextResponse.next({ request: { headers: requestHeaders } })

  // Set CSP header on the response
  response.headers.set('Content-Security-Policy', cspHeader)

  return response
}
```

**Tip:** In development, `'unsafe-eval'` is required because React uses `eval` for enhanced error debugging. Not needed in production.

---

## CSP Matcher (Exclude Static Files)

```ts
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

---

## Adding Security Headers

```ts
import { NextRequest, NextResponse } from 'next/server'

export function proxy(request: NextRequest) {
  const response = NextResponse.next()

  // Strict-Transport-Security — force HTTPS
  response.headers.set(
    'Strict-Transport-Security',
    'max-age=63072000; includeSubDomains; preload'
  )

  // X-Content-Type-Options — prevent MIME sniffing
  response.headers.set('X-Content-Type-Options', 'nosniff')

  // X-Frame-Options — prevent clickjacking
  response.headers.set('X-Frame-Options', 'DENY')

  // Referrer-Policy
  response.headers.set('Referrer-Policy', 'strict-origin-when-cross-origin')

  // Permissions-Policy
  response.headers.set(
    'Permissions-Policy',
    'camera=(), microphone=(), geolocation=()'
  )

  return response
}
```

---

## Organizing Proxy Logic

Break complex proxy logic into separate modules and import them:

```ts
// proxy.ts — entry point (single file)
import { NextRequest, NextResponse } from 'next/server'
import { handleAuthGuard } from './proxy/auth-guard'
import { handleSecurityHeaders } from './proxy/security-headers'
import { handleLocaleRedirect } from './proxy/locale'

export async function proxy(request: NextRequest) {
  // 1. Auth guard
  const authResponse = await handleAuthGuard(request)
  if (authResponse) return authResponse

  // 2. Locale redirect
  const localeResponse = await handleLocaleRedirect(request)
  if (localeResponse) return localeResponse

  // 3. Security headers
  return handleSecurityHeaders(request)
}

export const config = {
  matcher: ['/((?!api|_next/static|_next/image|favicon.ico).*)'],
}
```

```ts
// proxy/auth-guard.ts
export async function handleAuthGuard(request: NextRequest) {
  const { pathname } = request.nextUrl
  if (!pathname.startsWith('/dashboard')) return null

  const session = request.cookies.get('session')?.value
  if (!session) {
    return NextResponse.redirect(new URL('/login', request.url))
  }
  return null
}
```

---

## Gotchas

1. **Only ONE proxy.ts per project** — break logic into imported modules if complex
2. **Proxy runs on every matched request** — be specific with `matcher` to avoid performance impact
3. **Don't use Proxy for slow operations** — it's on the hot path; keep logic fast
4. **Proxy cannot set `Set-Cookie` for different domains** — CORS restrictions apply
5. **`request.cookies.get()` reads the cookie** — `response.cookies.set()` sets it
6. **`fetch()` options in Proxy don't support caching** — `options.cache` and `options.next.revalidate` have no effect
7. **Proxy does optimistic checks only** — Server Actions and Route Handlers must do their own auth verification

---

## Prerequisites

- Next.js Core — see `skills/core.md`
- Routing — see `skills/routing.md`

## Next Steps

- **Full auth system:** See `skills/auth.md` — JOSE sessions, DAL, DTOs, Proxy guard
- **CSP + nonce:** See `skills/security.md` — detailed CSP configuration, SRI
- **Locale routing:** See `skills/i18n.md` — full i18n setup
- **A/B testing:** See `skills/performance.md` — feature flags + proxy
