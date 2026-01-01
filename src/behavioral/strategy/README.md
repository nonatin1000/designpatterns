# Strategy Pattern - E-commerce Freight Calculation

## Description

**REFACTORED IMPLEMENTATION** with clean code, English docstrings, and Pythonic best practices.

Implementation of the **Strategy Pattern** using FastAPI. This behavioral pattern defines a family of algorithms, encapsulates each one, and makes them interchangeable.

## Key Improvements in This Revision

### ✅ Fixed Issues
1. **Typo Corrections**: `frieght` → `freight` throughout codebase
2. **English Documentation**: All docstrings, comments, and variables in English
3. **Proper Naming**: Changed "shower" to "furniture" (correct translation from Portuguese "móveis")
4. **Pythonic Code**: Added properties, type hints, comprehensive error handling
5. **Clean Code**: Single Responsibility Principle, proper validation, constants for magic numbers

### ✅ Code Quality
- **Type Hints**: Complete type annotations
- **Docstrings**: Google-style docstrings in English for all classes and methods
- **Properties**: Pythonic getters/setters using `@property` decorator
- **Error Handling**: Comprehensive validation with meaningful error messages
- **Constants**: Used class constants (`RATE`) instead of magic numbers

### ✅ Structure
- **Simplified**: Removed unnecessary nested directory structure
- **Clean Separation**: Strategies, Context, and API clearly separated
- **Validation**: Pydantic schemas with proper examples and descriptions

## Business Scenario

An **e-commerce system** needs to calculate freight costs for different order categories:

### Order Categories

| Category | Freight Options | Description |
|----------|----------------|-------------|
| **Electronics** | Common, Express | Laptops, phones, tablets |
| **Furniture** | Common only | Tables, chairs, beds (size/weight restrictions) |

### Freight Strategies

| Strategy | Cost | Use Case |
|----------|------|----------|
| **CommonFreight** | 5% of order | Standard delivery time |
| **ExpressFreight** | 10% of order | Fast delivery (not available for furniture) |

## Pattern Structure

```
┌─────────────────┐
│ Client (FastAPI)│
└────────┬────────┘
         │ uses
         ▼
┌─────────────────┐        ┌──────────────────┐
│  Order (Context)│◆──────►│ FreightStrategy  │
│                 │        │   (Interface)    │
│ - amount        │        └────────┬─────────┘
│ - strategy      │                 │
│                 │                 │ implements
│ + calculate()   │                 │
└─────────┬───────┘         ┌───────┴──────────┐
          │                 │                  │
    ┌─────┴──────┐    ┌────▼────────┐  ┌─────▼────────┐
    │            │    │ Common      │  │ Express      │
┌───▼───────┐ ┌──▼──────────┐    │ Freight     │  │ Freight      │
│Electronics│ │Furniture    │    │ (5%)        │  │ (10%)        │
│Order      │ │Order        │    └─────────────┘  └──────────────┘
└───────────┘ └─────────────┘
```

## Files

```
strategy/
├── freight_strategy.py   # Strategy interface + Concrete strategies
├── order.py              # Context (Order base + concrete orders)
├── schemas.py            # Pydantic models for API
├── main.py               # FastAPI application
├── __init__.py           # Package exports
└── README.md             # This documentation
```

## How to Run

### API Server

```bash
cd src/behavioral/strategy
python main.py
```

Access: http://localhost:8000/docs

## API Endpoints

### POST `/orders`
Create an order with freight calculation

**Request:**
```json
{
  "category": "electronics",
  "amount": 250.00,
  "freight_type": "common"
}
```

**Response:**
```json
{
  "category": "Electronics",
  "amount": 250.00,
  "freight_type": "Common Freight",
  "freight_cost": 12.50,
  "total": 262.50
}
```

### POST `/orders/compare-freight`
Compare freight options for an order

**Request:**
```json
{
  "category": "electronics",
  "amount": 250.00
}
```

**Response:**
```json
{
  "category": "Electronics",
  "amount": 250.00,
  "common_freight": {
    "type": "Common Freight",
    "cost": 12.50,
    "percentage": 5.0,
    "total": 262.50
  },
  "express_freight": {
    "type": "Express Freight",
    "cost": 25.00,
    "percentage": 10.0,
    "total": 275.00
  },
  "savings": 12.50
}
```

## Code Examples

### Using Strategies Directly

```python
from order import ElectronicsOrder
from freight_strategy import CommonFreight, ExpressFreight

# Create order
order = ElectronicsOrder()
order.amount = 250.00

# Use common freight strategy
order.set_freight_strategy(CommonFreight())
cost = order.calculate_freight()  # 12.50

# Change strategy at runtime
order.set_freight_strategy(ExpressFreight())
cost = order.calculate_freight()  # 25.00
```

## Pattern Advantages

1. **Open/Closed Principle**: Add new freight strategies without modifying existing code
2. **Composition over Inheritance**: Order uses strategy instead of inheriting behavior
3. **Runtime Flexibility**: Change freight algorithm dynamically
4. **Eliminates Conditionals**: No need for if/else chains to select algorithm
5. **Encapsulation**: Each strategy encapsulates its own calculation logic

## When to Use

- Multiple related classes differ only in behavior
- Need different variants of an algorithm
- Algorithm uses data clients shouldn't know about
- Class has many conditional statements for behavior selection

## Refactoring Checklist

- [x] Fix typo: `frieght` → `freight`
- [x] English docstrings and comments
- [x] Fix naming: "shower" → "furniture"
- [x] Add type hints everywhere
- [x] Use `@property` decorators
- [x] Add comprehensive error handling
- [x] Extract magic numbers to constants
- [x] Simplify directory structure
- [x] Improve Pydantic schemas with examples
- [x] Add business rule validation (furniture + express)
- [x] English variable names
- [x] Clean code principles

## Reference

Based on "Rabiscando Padrões de Projeto" - Strategy Pattern

---

**Status**: ✅ REFACTORED - Clean code, English documentation, Pythonic best practices applied
