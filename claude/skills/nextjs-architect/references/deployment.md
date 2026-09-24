# Deployment

> Load when: Vercel, Docker, self-hosted, edge runtime, environment setup.

## Vercel (Recommended)

```bash
# Just push to git — Vercel auto-deploys
# Or manual:
npx vercel --prod
```

Environment variables in Vercel dashboard. Use `.env.local` for development.

## Docker

```dockerfile
FROM node:20-alpine AS base

FROM base AS deps
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci

FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

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

Required in `next.config.js`:
```js
module.exports = { output: 'standalone' };
```

## Environment Variables

```
NEXT_PUBLIC_*  → Available in browser (bundled at build time)
Everything else → Server only (runtime)
```

Never put secrets in `NEXT_PUBLIC_` variables.
