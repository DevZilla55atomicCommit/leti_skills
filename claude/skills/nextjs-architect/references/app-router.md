# App Router Patterns

> Load when: Routing, layouts, loading states, error handling, parallel routes.

## File Conventions

```
app/
├── layout.tsx          # Root layout (wraps everything)
├── page.tsx            # Home page (/)
├── loading.tsx         # Loading UI (auto-wrapped in Suspense)
├── error.tsx           # Error boundary
├── not-found.tsx       # 404 page
├── dashboard/
│   ├── layout.tsx      # Dashboard layout (nested, persistent)
│   ├── page.tsx        # /dashboard
│   ├── loading.tsx     # Dashboard loading state
│   └── settings/
│       └── page.tsx    # /dashboard/settings
├── blog/
│   ├── page.tsx        # /blog (list)
│   └── [slug]/
│       └── page.tsx    # /blog/my-post (dynamic)
└── (marketing)/        # Route group — no URL segment
    ├── about/page.tsx  # /about
    └── pricing/page.tsx # /pricing
```

## Dynamic Routes

```tsx
// app/blog/[slug]/page.tsx
export default async function BlogPost({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const post = await getPost(slug);
  if (!post) notFound();
  return <article>{post.content}</article>;
}

// Generate static params for SSG
export async function generateStaticParams() {
  const posts = await getAllPosts();
  return posts.map((post) => ({ slug: post.slug }));
}

// Catch-all: app/docs/[...slug]/page.tsx
// Matches /docs/a, /docs/a/b, /docs/a/b/c
```

## Layouts — Persistent UI

Layouts don't re-render on navigation. Use them for shared UI:

```tsx
// app/dashboard/layout.tsx
export default function DashboardLayout({ children }: { children: ReactNode }) {
  return (
    <div className="flex">
      <Sidebar />           {/* Stays mounted across navigation */}
      <main>{children}</main> {/* Only this part changes */}
    </div>
  );
}
```

## Parallel Routes

Render multiple pages simultaneously in the same layout:

```
app/dashboard/
├── layout.tsx
├── page.tsx
├── @analytics/page.tsx    # Parallel slot
├── @notifications/page.tsx # Parallel slot
└── @analytics/loading.tsx  # Each slot can have its own loading
```

```tsx
// app/dashboard/layout.tsx
export default function Layout({
  children, analytics, notifications
}: {
  children: ReactNode;
  analytics: ReactNode;
  notifications: ReactNode;
}) {
  return (
    <div>
      {children}
      <div className="grid grid-cols-2 gap-4">
        {analytics}
        {notifications}
      </div>
    </div>
  );
}
```

## Error Handling

```tsx
// app/dashboard/error.tsx
'use client'; // Error boundaries must be client components

export default function Error({ error, reset }: { error: Error; reset: () => void }) {
  useEffect(() => { reportError(error); }, [error]);
  return (
    <div>
      <h2>Something went wrong</h2>
      <button onClick={reset}>Try again</button>
    </div>
  );
}
```

## Metadata

```tsx
// Static metadata
export const metadata: Metadata = {
  title: 'My App',
  description: 'Description',
  openGraph: { title: 'My App', images: ['/og.png'] },
};

// Dynamic metadata
export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { slug } = await params;
  const post = await getPost(slug);
  return { title: post.title, description: post.excerpt };
}
```
