# Authentication Security

> Load when: Password hashing, JWT security, session management.

## Password Hashing

```typescript
import bcrypt from 'bcrypt';

// Hash (cost factor 12 — good balance of security and speed)
const hash = await bcrypt.hash(password, 12);

// Verify
const isValid = await bcrypt.compare(password, hash);
```

```python
# Python — use argon2
from argon2 import PasswordHasher
ph = PasswordHasher()
hash = ph.hash(password)
ph.verify(hash, password)  # Raises on mismatch
```

## JWT Best Practices

```typescript
import jwt from 'jsonwebtoken';

// Short-lived access token + long-lived refresh token
const accessToken = jwt.sign(
  { sub: user.id, role: user.role },
  process.env.JWT_SECRET,
  { expiresIn: '15m', algorithm: 'HS256' }
);

const refreshToken = jwt.sign(
  { sub: user.id, jti: crypto.randomUUID() },
  process.env.REFRESH_SECRET,
  { expiresIn: '7d' }
);
```

Rules:
- Access tokens: 15 min max lifetime
- Refresh tokens: store in httpOnly secure cookie, not localStorage
- Always verify `exp`, `iss`, `aud` claims
- Use RS256 (asymmetric) for distributed systems
- Rotate signing keys periodically
