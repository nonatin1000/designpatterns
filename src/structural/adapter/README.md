# Adapter Pattern - Payment Gateway Integration System

## Description

Implementation of the **Adapter Pattern** using FastAPI. This structural pattern allows incompatible interfaces to work together by acting as a bridge between them.

## Concept

The system integrates two third-party payment gateways (PagFacil and TopPagamentos) with different interfaces into a unified payment processing system. The Adapter pattern allows these incompatible interfaces to work seamlessly through a common Gateway interface.

## Business Scenario

**FreteExpress** (a shipping company) needs to process payments using two different gateways:

### Payment Gateways

| Gateway | Fixed Fee | Interest Rate | Best For |
|---------|-----------|---------------|----------|
| **PagFacil** | R$ 0.40 | 5% per month | Cash payments (1x) |
| **TopPagamentos** | R$ 5.00 | 1% per month | Installments (2x+) |

**Strategy**: Automatically select the most cost-effective gateway based on the number of installments.

## Pattern Structure

```
Client (Billing)
     |
     | uses
     v
Target (Gateway Interface)
     ^
     | implements
     |
     +----------------+------------------+
     |                                   |
PagFacilAdapter              TopPagamentosAdapter
     |                                   |
     | wraps                             | wraps
     v                                   v
PagFacil (Adaptee)           TopPagamentos (Adaptee)
(Portuguese Interface)       (Different English Interface)
```

### Components

- **Target (Gateway)**: Standard interface that the client expects
- **Adaptee (PagFacil, TopPagamentos)**: Existing classes with incompatible interfaces
- **Adapter (PagFacilAdapter, TopPagamentosAdapter)**: Bridges between Target and Adaptee
- **Client (Billing)**: Uses objects through the Target interface

## File Structure

```
adapter/
├── gateway_interface.py       # Target interface
├── payment_gateways.py        # Adaptees (PagFacil, TopPagamentos)
├── adapters.py                # Adapters for each gateway
├── billing.py                 # Client that uses adapters
├── schemas.py                 # Pydantic models
├── main.py                    # FastAPI application
├── exemplo.py                 # Usage examples
├── test_adapter.py            # Unit tests
└── README.md                  # This documentation
```

## How to Run

### 1. Examples (no dependencies)

```bash
cd src/structural/adapter
python exemplo.py
```

### 2. Tests

```bash
cd src/structural/adapter
python test_adapter.py
```

### 3. FastAPI Application

```bash
cd designpatterns
pip install -r requirements.txt
cd src/structural/adapter
python main.py
```

Access: http://localhost:8000/docs

## API Endpoints

### POST `/payments`
Process a payment with automatic gateway selection

**Request:**
```json
{
  "amount": 100.00,
  "installments": 1
}
```

**Response:**
```json
{
  "success": true,
  "amount": 100.00,
  "installments": 1,
  "gateway": "PagFacil",
  "total_with_fees": 105.40,
  "fees": 5.40
}
```

### POST `/payments/compare`
Compare costs between both gateways

**Request:**
```json
{
  "amount": 100.00,
  "installments": 3
}
```

**Response:**
```json
{
  "amount": 100.00,
  "installments": 3,
  "pag_facil": {
    "gateway": "PagFacil",
    "total_with_fees": 115.40,
    "fees": 15.40
  },
  "top_pagamentos": {
    "gateway": "TopPagamentos",
    "total_with_fees": 108.00,
    "fees": 8.00
  },
  "recommended": "TopPagamentos",
  "savings": 7.40
}
```

### GET `/payments/history`
Get payment history

### GET `/payments/statistics`
Get billing statistics

### DELETE `/payments/history`
Clear payment history

## Pattern Advantages

1. **Single Responsibility**: Each adapter handles one specific integration
2. **Open/Closed Principle**: Add new gateways without modifying existing code
3. **Interface Compatibility**: Makes incompatible interfaces work together
4. **Flexibility**: Client code works with any adapted gateway

## When to Use

- Need to use existing classes with incompatible interfaces
- Want to create reusable code that works with various interfaces
- Need to integrate third-party libraries with different APIs
- Multiple classes need to be used interchangeably

## Code Examples

### Using Adapters Directly

```python
from adapters import PagFacilAdapter, TopPagamentosAdapter

# PagFacil for cash payment
pag_facil = PagFacilAdapter()
pag_facil.set_amount(100.00)
pag_facil.set_installments(1)
pag_facil.process()
total = pag_facil.get_total_with_fees()  # R$ 105.40
```

### Using Billing (Automatic Selection)

```python
from billing import Billing

billing = Billing()

# Automatically selects PagFacil for cash
result1 = billing.process_payment(100.00, 1)
# Gateway: PagFacil

# Automatically selects TopPagamentos for installments
result2 = billing.process_payment(600.00, 6)
# Gateway: TopPagamentos
```

## Cost Analysis

For a R$ 100.00 payment:

| Installments | PagFacil | TopPagamentos | Best Choice | Savings |
|--------------|----------|---------------|-------------|---------|
| 1x | R$ 105.40 | R$ 106.00 | **PagFacil** | R$ 0.60 |
| 2x | R$ 110.40 | R$ 107.00 | **TopPagamentos** | R$ 3.40 |
| 3x | R$ 115.40 | R$ 108.00 | **TopPagamentos** | R$ 7.40 |
| 6x | R$ 130.40 | R$ 111.00 | **TopPagamentos** | R$ 19.40 |
| 12x | R$ 160.40 | R$ 117.00 | **TopPagamentos** | R$ 43.40 |

## Adapter vs Strategy Pattern

While both patterns are used here:
- **Adapter**: Makes incompatible interfaces compatible
- **Strategy**: Selects the best algorithm (gateway) at runtime

The Adapter enables the Strategy!

## Reference

Based on "Rabiscando Padrões de Projeto" - Adapter Pattern
