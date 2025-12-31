# Facade Pattern - E-commerce Sales System

## Description

Implementation of the **Facade Pattern** using FastAPI. This structural pattern provides a unified interface to a set of interfaces in a subsystem, making it easier to use.

## Concept

The Facade pattern simplifies interaction with complex subsystems by providing a single, high-level interface. This reduces coupling between clients and subsystem components, making the system easier to understand and maintain.

## Business Scenario

An **e-commerce sales system** with three complex subsystems:

### Subsystems

1. **Order Management**
   - Customer tracking
   - Product management
   - Order totals calculation

2. **Payment Processing**
   - Credit card payments
   - Bank slip (boleto) generation
   - Payment validation

3. **Email Notifications**
   - Order confirmations
   - Payment success/failure notifications
   - Customer communication

### The Problem

Without a facade, clients must interact directly with all three subsystems:
- Create Order
- Set customer and products
- Create Payment (CreditCard or BankSlip)
- Process payment
- Create Email service
- Send appropriate email

**This creates tight coupling and complex client code!**

### The Solution

The `SalesFacade` provides a simplified interface:
```python
facade = SalesFacade(customer)
facade.add_product(product)
facade.process_credit_card_order()  # Handles everything!
```

## Pattern Structure

```
┌─────────┐
│ Client  │ ---uses---> ┌──────────────┐
└─────────┘             │ SalesFacade  │
                        └──────┬───────┘
                               |
                ┌──────────────┼──────────────┐
                |              |              |
          ┌─────▼─────┐  ┌────▼────┐  ┌─────▼─────┐
          │   Order   │  │ Payment │  │   Email   │
          └─────┬─────┘  └────┬────┘  └───────────┘
                |              |
        ┌───────┼───────┐      |
        |       |       |      |
   ┌────▼───┐ ┌▼────┐  |  ┌───▼────────┐
   │Customer│ │Prod │  |  │CreditCard  │
   └────────┘ └─────┘  |  │PaymentImpl │
                        |  └────────────┘
                        |
                    ┌───▼────────┐
                    │ BankSlip   │
                    │PaymentImpl │
                    └────────────┘
```

### Components

- **Facade (SalesFacade)**: Provides simplified interface, knows which subsystem classes handle requests
- **Subsystems (Order, Payment, Email)**: Implement functionality, handle requests from Facade
- **Client**: Uses only the Facade, doesn't need to know subsystem details

## File Structure

```
facade/
├── customer.py           # Customer entity
├── product.py            # Product entity
├── order.py              # Order management subsystem
├── payment.py            # Payment processing subsystem (abstract + concrete)
├── email_service.py      # Email notification subsystem
├── sales_facade.py       # FACADE - Simplified interface
├── schemas.py            # Pydantic models
├── main.py               # FastAPI application
├── exemplo.py            # Usage examples
├── test_facade.py        # Unit tests
└── README.md             # This documentation
```

## How to Run

### 1. Examples (no dependencies)

```bash
cd src/structural/facade
python exemplo.py
```

### 2. Tests

```bash
cd src/structural/facade
python test_facade.py
```

### 3. FastAPI Application

```bash
cd designpatterns
pip install -r requirements.txt
cd src/structural/facade
python main.py
```

Access: http://localhost:8000/docs

## API Endpoints

### POST `/orders`
Create a new order (automatically creates Order, Email via Facade)

**Request:**
```json
{
  "customer": {
    "name": "Luiz da Silva",
    "tax_id": "12345678910",
    "email": "luiz@email.com"
  },
  "products": [
    {
      "name": "Pink Blouse",
      "description": "Women's pink blouse",
      "price": 80.99
    }
  ]
}
```

### GET `/orders/{order_id}`
Get order details

### GET `/orders`
List all orders

### POST `/orders/{order_id}/products`
Add product to existing order

### POST `/orders/payment`
Process payment (automatically handles Payment + Email)

**Request:**
```json
{
  "order_id": 1,
  "payment_method": "credit_card"
}
```

### DELETE `/orders/{order_id}`
Delete an order

## Pattern Advantages

1. **Simplified Interface**: Single entry point for complex operations
2. **Reduced Coupling**: Client doesn't depend on subsystem classes
3. **Ease of Use**: Less code required from client
4. **Flexibility**: Client can still access subsystem directly if needed
5. **Maintainability**: Changes in subsystem don't affect client

## When to Use

- Need to provide a simple interface to a complex subsystem
- Many dependencies between clients and implementation classes
- Want to layer subsystems (facade defines entry point for each layer)
- Need to decouple subsystems from clients and other subsystems

## Code Comparison

### WITHOUT Facade (Complex - 10+ lines)

```python
from order import Order
from payment import CreditCardPayment
from email_service import OrderEmail

# Client must know about all subsystem classes
order = Order(customer)
order.add_product(product1)
order.add_product(product2)

payment = CreditCardPayment(order)
email = OrderEmail(order)

if payment.process_payment():
    email.send_payment_success_email("Credit Card")
else:
    email.send_payment_failure_email("Credit Card")
```

### WITH Facade (Simple - 3 lines)

```python
from sales_facade import SalesFacade

# Client only knows about Facade
facade = SalesFacade(customer)
facade.add_product(product1)
facade.add_product(product2)
facade.process_credit_card_order()  # Handles everything!
```

## Pattern Consequences

### Benefits

- **Shields clients from subsystem complexity**
- **Promotes weak coupling** between subsystem and clients
- **Easier to use** for common tasks
- **Doesn't prevent access** to subsystem if needed

### Trade-offs

- Facade can become a **"god object"** coupled to all subsystem classes
- May need **multiple facades** for different client needs
- Doesn't enforce **encapsulation** - clients can still bypass facade

## Real-World Examples

1. **Database Access Layers**: Single interface for complex DB operations
2. **API Clients**: Simplified interface to external APIs
3. **Framework Libraries**: High-level API over low-level components
4. **Compiler Front-ends**: Simple interface to lexer, parser, code generator

## Testing

Run all tests:
```bash
python test_facade.py
```

Tests cover:
- ✓ Subsystem classes (Customer, Product, Order)
- ✓ Payment processing (CreditCard, BankSlip)
- ✓ Email notifications
- ✓ Facade simplification
- ✓ Error handling

## Reference

Based on "Rabiscando Padrões de Projeto" - Facade Pattern

## Key Takeaway

**The Facade pattern doesn't add new functionality - it makes existing functionality easier to use by providing a simplified, unified interface to a complex subsystem.**
