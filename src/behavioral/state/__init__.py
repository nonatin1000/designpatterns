"""State pattern - Order management system.

The State pattern allows an object to alter its behavior when its internal
state changes. The object will appear to have changed its class.

This module implements the State pattern for an e-commerce order management
system, where orders can transition between different states:
- Pending Payment (initial state)
- Paid
- Cancelled (terminal state)
- Shipped (terminal state)
"""

from .state import (
    State,
    PendingPaymentState,
    PaidState,
    CancelledState,
    ShippedState
)
from .order import Order
from .schemas import (
    OrderCreate,
    OrderResponse,
    TransitionResponse
)

__all__ = [
    # State interface and concrete states
    "State",
    "PendingPaymentState",
    "PaidState",
    "CancelledState",
    "ShippedState",
    # Context class
    "Order",
    # Schemas
    "OrderCreate",
    "OrderResponse",
    "TransitionResponse",
]
