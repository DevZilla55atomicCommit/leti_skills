# Unit Testing Patterns

> Load when: Mocking strategies, test structure, assertion patterns.

## Test Structure (AAA)

```typescript
describe('CartService', () => {
  describe('addItem', () => {
    it('adds item and updates total', () => {
      // Arrange
      const cart = new CartService();
      const item = { id: '1', name: 'Widget', price: 9.99, quantity: 2 };

      // Act
      cart.addItem(item);

      // Assert
      expect(cart.items).toHaveLength(1);
      expect(cart.total).toBe(19.98);
    });

    it('increments quantity for existing item', () => {
      const cart = new CartService();
      cart.addItem({ id: '1', name: 'Widget', price: 9.99, quantity: 1 });
      cart.addItem({ id: '1', name: 'Widget', price: 9.99, quantity: 2 });

      expect(cart.items).toHaveLength(1);
      expect(cart.items[0].quantity).toBe(3);
    });
  });
});
```

## Mocking Strategies

```typescript
// Dependency injection — test without mocking framework
interface EmailService {
  send(to: string, subject: string, body: string): Promise<void>;
}

class UserService {
  constructor(private email: EmailService) {}

  async register(email: string) {
    const user = await this.createUser(email);
    await this.email.send(email, 'Welcome!', 'Thanks for joining');
    return user;
  }
}

// In test — simple mock
const mockEmail: EmailService = {
  send: vi.fn().mockResolvedValue(undefined),
};

const service = new UserService(mockEmail);
await service.register('test@example.com');
expect(mockEmail.send).toHaveBeenCalledWith(
  'test@example.com', 'Welcome!', expect.any(String)
);
```