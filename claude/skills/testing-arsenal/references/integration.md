# Integration & E2E Testing

> Load when: API testing, database testing, Playwright.

## API Integration Testing

```typescript
import { describe, it, expect, beforeAll, afterAll } from 'vitest';
import { app } from '../src/app';

describe('POST /api/users', () => {
  let server: any;
  beforeAll(async () => { server = await app.listen(0); });
  afterAll(async () => { await server.close(); });

  it('creates user with valid data', async () => {
    const response = await fetch(`http://localhost:${server.address().port}/api/users`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name: 'Alice', email: 'alice@test.com' }),
    });

    expect(response.status).toBe(201);
    const user = await response.json();
    expect(user).toMatchObject({ name: 'Alice', email: 'alice@test.com' });
    expect(user.id).toBeDefined();
  });

  it('returns 400 for invalid email', async () => {
    const response = await fetch(`http://localhost:${server.address().port}/api/users`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name: 'Bob', email: 'not-an-email' }),
    });
    expect(response.status).toBe(400);
  });
});
```

## Playwright E2E

```typescript
import { test, expect } from '@playwright/test';

test('user can complete checkout', async ({ page }) => {
  await page.goto('/products');
  await page.getByRole('button', { name: 'Add to cart' }).first().click();
  await page.getByRole('link', { name: 'Cart' }).click();
  await page.getByRole('button', { name: 'Checkout' }).click();

  // Fill checkout form
  await page.getByLabel('Email').fill('test@example.com');
  await page.getByLabel('Card number').fill('4242424242424242');
  await page.getByRole('button', { name: 'Pay' }).click();

  await expect(page.getByText('Order confirmed')).toBeVisible();
});
```