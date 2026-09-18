# Next.js Images & Fonts — next/image and next/font

## Overview

Next.js provides optimized components for images (`next/image`) and fonts (`next/font`). These components automatically handle performance optimizations — responsive sizing, lazy loading, format conversion (WebP/AVIF), and font subsetting — with zero configuration.

**Key patterns:**
- **next/image** — responsive, optimized images with blur placeholders
- **next/font** — self-hosted Google Fonts with zero layout shift
- **Remote images** — configure `remotePatterns` for external sources
- **`fill` prop** — parent-controlled sizing for cover/contain layouts

**Related skills:** core, styling, metadata

---

## next/image — Local Images

### Static Import (Recommended)

```tsx
import Image from 'next/image'
import profile from './profile.png' // Static import

export default function Page() {
  return (
    <Image
      src={profile}
      alt="Profile photo"
      // width and height auto-detected from static import
      priority // Load above-the-fold images immediately
    />
  )
}
```

### Explicit Dimensions

```tsx
import Image from 'next/image'

export default function Page() {
  return (
    <Image
      src="/profile.png"
      alt="Profile photo"
      width={500}
      height={500}
    />
  )
}
```

**Rule:** Always provide `width` and `height` OR use `fill` to prevent layout shift.

---

## next/image — Remote Images

Configure `remotePatterns` to allow external image sources:

```ts
// next.config.ts
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 's3.amazonaws.com',
        port: '',
        pathname: '/my-bucket/**',
      },
      {
        protocol: 'https',
        hostname: '**.example.com',
      },
    ],
  },
}

export default nextConfig
```

```tsx
import Image from 'next/image'

export default function Page() {
  return (
    <Image
      src="https://s3.amazonaws.com/my-bucket/profile.png"
      alt="Remote profile"
      width={500}
      height={500}
    />
  )
}
```

---

## `fill` Prop — Full-Width/Height Images

Use `fill` when the image should fill its parent container:

```tsx
// Full-bleed hero image
export default function Hero() {
  return (
    <div style={{ position: 'relative', width: '100vw', height: '400px' }}>
      <Image
        src="/hero.jpg"
        alt="Hero"
        fill
        style={{ objectFit: 'cover' }} // Equivalent to background-size: cover
        priority
      />
    </div>
  )
}
```

---

## Blur Placeholder

```tsx
import Image from 'next/image'
import profile from './profile.png' // Static import → auto-generates blurDataURL

export default function Page() {
  return (
    <Image
      src={profile}
      alt="Profile"
      placeholder="blur" // Automatically uses blurDataURL from static import
      blurDataURL="data:image/jpeg;base64,..." // Or provide manually
    />
  )
}
```

For remote images, generate a blur placeholder URL on the server:

```tsx
import Image from 'next/image'

export default async function Page() {
  const { blurDataURL } = await getImageData('https://example.com/photo.jpg')

  return (
    <Image
      src="https://example.com/photo.jpg"
      alt="Photo"
      width={800}
      height={600}
      placeholder="blur"
      blurDataURL={blurDataURL}
    />
  )
}
```

---

## next/font — Google Fonts

next/font automatically self-hosts Google Fonts — no external requests to Google.

### Variable Fonts (Recommended)

```tsx
import { Geist } from 'next/font/google'

const geist = Geist({
  subsets: ['latin'],
  variable: '--font-geist', // CSS variable name
  display: 'swap',
})

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={geist.className}>
      <body>{children}</body>
    </html>
  )
}
```

```css
/* Using the CSS variable */
body {
  font-family: var(--font-geist), sans-serif;
}

h1 {
  font-family: var(--font-geist-sans), serif;
}
```

### Specific Weights (Non-Variable Fonts)

```tsx
import { Roboto } from 'next/font/google'

const roboto = Roboto({
  weight: ['400', '700'],
  subsets: ['latin'],
  variable: '--font-roboto',
  display: 'swap',
})
```

---

## next/font — Local Fonts

```tsx
import localFont from 'next/font/local'

const myFont = localFont({
  src: [
    {
      path: './fonts/Roboto-Regular.woff2',
      weight: '400',
      style: 'normal',
    },
    {
      path: './fonts/Roboto-Bold.woff2',
      weight: '700',
      style: 'normal',
    },
    {
      path: './fonts/Roboto-Italic.woff2',
      weight: '400',
      style: 'italic',
    },
  ],
  variable: '--font-my-local',
  display: 'swap',
})

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={myFont.className}>
      <body>{children}</body>
    </html>
  )
}
```

---

## Multiple Fonts

```tsx
import { Geist, Inter } from 'next/font/google'

const geist = Geist({ subsets: ['latin'], variable: '--font-geist' })
const inter = Inter({
  subsets: ['latin'],
  variable: '--font-inter',
  display: 'swap',
})

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={`${geist.variable} ${inter.variable}`}>
      <body>{children}</body>
    </html>
  )
}
```

---

## Responsive Images with `sizes`

Help Next.js serve the right image size for the viewport:

```tsx
import Image from 'next/image'

export default function ResponsiveImage() {
  return (
    <Image
      src="/hero.jpg"
      alt="Hero"
      width={1200}
      height={600}
      sizes="
        (max-width: 640px) 100vw,
        (max-width: 1024px) 50vw,
        33vw
      "
    />
  )
}
```

**Why `sizes` matters:** Without `sizes`, Next.js serves the same image size regardless of viewport. With `sizes`, Next.js generates multiple sizes and serves the smallest one that fills the container.

---

## Image Component Props Reference

| Prop | Type | Description |
|------|------|-------------|
| `src` | `string \| StaticImport` | Image source |
| `alt` | `string` | Required for accessibility |
| `width` | `number` | Intrinsic width (with `fill`, omit) |
| `height` | `number` | Intrinsic height (with `fill`, omit) |
| `fill` | `boolean` | Fill parent container |
| `placeholder` | `'blur' \| 'empty'` | Show blur placeholder |
| `blurDataURL` | `string` | Base64 blur placeholder URL |
| `priority` | `boolean` | Preload above-the-fold image |
| `sizes` | `string` | Responsive size hint |
| `style` | `CSSProperties` | Inline styles |
| `quality` | `number` | 1-100, default 75 |
| `loader` | `function` | Custom image loader |
| `onLoad` | `function` | Image loaded callback |
| `onError` | `function` | Image error callback |

---

## Gotchas

1. **Always provide `width`/`height` or use `fill`** — otherwise Next.js doesn't know the aspect ratio, causing layout shift
2. **Remote images need `remotePatterns`** — Next.js needs explicit allowlist for external images
3. **Static imports auto-detect dimensions** — use static imports when possible for blur placeholder support
4. **`priority` on above-the-fold images** — LCP images should use `priority` to preload
5. **`next/font` self-hosts Google Fonts** — the browser never contacts Google; fonts are served from your domain
6. **Variable fonts are smaller** — prefer variable fonts for better performance
7. **`fill` images need positioned parent** — the parent must have `position: relative` (or similar)

---

## Prerequisites

- Next.js Core — see `skills/core.md`

## Next Steps

- **OG images with next/image:** See `skills/metadata.md` — ImageResponse for dynamic OG images
- **Styling images with Tailwind:** See `skills/styling.md` — `object-fit`, responsive image layouts
- **Metadata:** See `skills/metadata.md` — favicon, sitemap, robots.txt
