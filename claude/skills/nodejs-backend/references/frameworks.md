# Express & Fastify Patterns

> Load when: API setup, routing, middleware, validation.

## Fastify (Recommended)

```typescript
import Fastify from 'fastify';
import { TypeBoxTypeProvider } from '@fastify/type-provider-typebox';
import { Type } from '@sinclair/typebox';

const app = Fastify({ logger: true }).withTypeProvider<TypeBoxTypeProvider>();

// Schema validation + serialization
const UserSchema = Type.Object({
  id: Type.String(),
  name: Type.String({ minLength: 1 }),
  email: Type.String({ format: 'email' }),
});

app.get('/users/:id', {
  schema: {
    params: Type.Object({ id: Type.String() }),
    response: { 200: UserSchema },
  },
}, async (request) => {
  const user = await db.users.findById(request.params.id);
  if (!user) throw app.httpErrors.notFound('User not found');
  return user;
});

// Plugins for encapsulation
import fp from 'fastify-plugin';
const dbPlugin = fp(async (fastify) => {
  const pool = new Pool({ connectionString: process.env.DATABASE_URL });
  fastify.decorate('db', pool);
  fastify.addHook('onClose', () => pool.end());
});
app.register(dbPlugin);
```

## Express (When Required)

```typescript
import express from 'express';
import helmet from 'helmet';
import cors from 'cors';

const app = express();
app.use(helmet());
app.use(cors({ origin: process.env.ALLOWED_ORIGINS?.split(',') }));
app.use(express.json({ limit: '10mb' }));

// Async error wrapper
const asyncHandler = (fn: Function) => (req: Request, res: Response, next: NextFunction) =>
  Promise.resolve(fn(req, res, next)).catch(next);

app.get('/users/:id', asyncHandler(async (req, res) => {
  const user = await userService.findById(req.params.id);
  if (!user) return res.status(404).json({ error: 'Not found' });
  res.json(user);
}));

// Error middleware (MUST have 4 params)
app.use((err: Error, req: Request, res: Response, next: NextFunction) => {
  logger.error({ err, requestId: req.id }, 'Request failed');
  res.status(500).json({ error: 'Internal server error' });
});
```
