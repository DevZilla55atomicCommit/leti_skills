# Middleware & Authentication

> Load when: Auth checks, redirects, headers, geo-routing, rate limiting.

## Middleware Basics

```tsx
// middleware.ts (root of project)
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  // Check auth
  const token = request.cookies.get('session')?.value;
  if (!token && request.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  // Add headers
  const response = NextResponse.next();
  response.headers.set('x-request-id', crypto.randomUUID());
  return response;
}

export const config = {
  matcher: ['/dashboard/:path*', '/api/:path*'],
};
```

## Auth Pattern with JWT

```tsx
import { jwtVerify } from 'jose';

export async function middleware(request: NextRequest) {
  const token = request.cookies.get('token')?.value;

  if (request.nextUrl.pathname.startsWith('/api/')) {
    if (!token) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }
    try {
      const { payload } = await jwtVerify(token, new TextEncoder().encode(process.env.JWT_SECRET));
      const headers = new Headers(request.headers);
      headers.set('x-user-id', payload.sub as string);
      return NextResponse.next({ headers });
    } catch {
      return NextResponse.json({ error: 'Invalid token' }, { status: 401 });
    }
  }
}
```

## Geo-routing

```tsx
export function middleware(request: NextRequest) {
  const country = request.geo?.country || 'US';
  if (country === 'TR' && !request.nextUrl.pathname.startsWith('/tr')) {
    return NextResponse.redirect(new URL(`/tr${request.nextUrl.pathname}`, request.url));
  }
}
```

Middleware runs on the Edge Runtime — keep it lightweight. No Node.js APIs, no heavy computation.
