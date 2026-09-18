# Data Fetching & Caching

> Load when: Fetch strategies, revalidation, cache layers, performance.

## The Four Cache Layers

1. **Request Memoization** — Same fetch URL in the same render is deduped automatically
2. **Data Cache** — Persists across requests. Controlled by `revalidate` and `cache` options.
3. **Full Route Cache** — Static pages cached at build time on the server
4. **Router Cache** — Client-side cache of visited routes (30s for dynamic, 5min for static)

## Fetching in Server Components

```tsx
// Cached indefinitely (default)
const data = await fetch('https://api.example.com/data');

// Revalidate every 60 seconds (ISR)
const data = await fetch('https://api.example.com/data', {
  next: { revalidate: 60 }
});

// No cache — fresh on every request (SSR)
const data = await fetch('https://api.example.com/data', {
  cache: 'no-store'
});

// Revalidate by tag
const data = await fetch('https://api.example.com/posts', {
  next: { tags: ['posts'] }
});
// Then in a Server Action:
import { revalidateTag } from 'next/cache';
revalidateTag('posts');
```

## Non-fetch Caching with `unstable_cache`

For database queries or other non-fetch data:

```tsx
import { unstable_cache } from 'next/cache';

const getCachedUser = unstable_cache(
  async (userId: string) => await db.users.findUnique({ where: { id: userId } }),
  ['user'],            // Cache key prefix
  { revalidate: 300, tags: ['user'] }  // 5 min TTL
);
```

## Parallel Data Loading

```tsx
// ❌ Waterfall — each awaits before the next starts
const user = await getUser(id);
const posts = await getPosts(id);
const analytics = await getAnalytics(id);

// ✅ Parallel — all start simultaneously
const [user, posts, analytics] = await Promise.all([
  getUser(id),
  getPosts(id),
  getAnalytics(id),
]);
```

## Route Segment Config

```tsx
// Force dynamic rendering for entire route
export const dynamic = 'force-dynamic';

// Set revalidation for entire route
export const revalidate = 60;

// Force static (error if dynamic data used)
export const dynamic = 'force-static';
```
