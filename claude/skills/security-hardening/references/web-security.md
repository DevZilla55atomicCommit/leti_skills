# Web Security

> Load when: Security headers, CORS, CSP, XSS/CSRF prevention.

## Security Headers

```typescript
// Express with helmet
import helmet from 'helmet';
app.use(helmet());

// Manual headers
app.use((req, res, next) => {
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.setHeader('X-Frame-Options', 'DENY');
  res.setHeader('X-XSS-Protection', '0'); // Disabled — use CSP instead
  res.setHeader('Strict-Transport-Security', 'max-age=31536000; includeSubDomains');
  res.setHeader('Referrer-Policy', 'strict-origin-when-cross-origin');
  res.setHeader('Permissions-Policy', 'camera=(), microphone=(), geolocation=()');
  next();
});
```

## Content Security Policy

```
Content-Security-Policy:
  default-src 'self';
  script-src 'self' 'nonce-{random}';
  style-src 'self' 'unsafe-inline';
  img-src 'self' data: https:;
  connect-src 'self' https://api.example.com;
  font-src 'self';
  frame-ancestors 'none';
```

## SQL Injection Prevention

```typescript
// ❌ NEVER do this
const query = `SELECT * FROM users WHERE id = '${userId}'`;

// ✅ Parameterized query
const result = await db.query('SELECT * FROM users WHERE id = $1', [userId]);

// ✅ ORM
const user = await User.findOne({ where: { id: userId } });
```

## XSS Prevention

```typescript
// ❌ Never insert raw HTML
element.innerHTML = userInput;

// ✅ Use textContent
element.textContent = userInput;

// ✅ Sanitize if HTML is needed
import DOMPurify from 'dompurify';
element.innerHTML = DOMPurify.sanitize(userInput);
```