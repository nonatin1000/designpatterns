"""FastAPI application implementing the State pattern for order management.

This API demonstrates how the State pattern allows an object to alter its
behavior when its internal state changes. The order can transition between
different states (Pending Payment, Paid, Cancelled, Shipped) with each
state defining valid and invalid transitions.
"""

from fastapi import APIRouter, FastAPI, HTTPException
from typing import Dict, Any
from .order import Order
from .schemas import (
    OrderCreate,
    OrderResponse,
    TransitionResponse
)

# In-memory storage for orders (in production, use a database)
_orders: Dict[int, Order] = {}


# Helper functions for business logic
def _create_order_logic(order_data: OrderCreate) -> OrderResponse:
    """Business logic for creating a new order.

    Args:
        order_data: Validated order creation data.

    Returns:
        OrderResponse with complete order information.

    Raises:
        HTTPException: If order creation fails.
    """
    try:
        order = Order(
            items=order_data.items,
            total_amount=order_data.total_amount
        )
        _orders[order.order_id] = order
        return OrderResponse(**order.get_info())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error creating order: {str(e)}"
        )


def _get_order_logic(order_id: int) -> OrderResponse:
    """Business logic for retrieving an order.

    Args:
        order_id: ID of the order to retrieve.

    Returns:
        OrderResponse with complete order information.

    Raises:
        HTTPException: If order is not found.
    """
    if order_id not in _orders:
        raise HTTPException(
            status_code=404,
            detail=f"Order {order_id} not found"
        )
    return OrderResponse(**_orders[order_id].get_info())


def _transition_order_logic(
    order_id: int,
    transition_func: str,
    success_message: str
) -> TransitionResponse:
    """Business logic for state transitions.

    Args:
        order_id: ID of the order to transition.
        transition_func: Name of the transition method to call.
        success_message: Message to return on successful transition.

    Returns:
        TransitionResponse with transition details.

    Raises:
        HTTPException: If order is not found or transition fails.
    """
    if order_id not in _orders:
        raise HTTPException(
            status_code=404,
            detail=f"Order {order_id} not found"
        )

    order = _orders[order_id]
    previous_state = order.get_state_name()

    try:
        # Call the appropriate transition method
        if transition_func == "pay":
            order.pay()
        elif transition_func == "cancel":
            order.cancel()
        elif transition_func == "ship":
            order.ship()
        else:
            raise ValueError(f"Unknown transition: {transition_func}")

        new_state = order.get_state_name()

        return TransitionResponse(
            success=True,
            message=success_message,
            previous_state=previous_state,
            new_state=new_state,
            order_id=order_id
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error during transition: {str(e)}"
        )


# Create router for inclusion in main app
router = APIRouter(prefix="/state", tags=["State Pattern"])


@router.get("/")
async def router_root():
    """Get API information and available endpoints.

    Returns:
        Dictionary with API information, pattern description, and endpoints.
    """
    return {
        "message": "E-commerce Order System - State Pattern",
        "pattern": "State",
        "description": (
            "Allows an object to alter its behavior when its internal state changes. "
            "The object will appear to have changed its class."
        ),
        "states": {
            "pending_payment": "Initial state - order created, awaiting payment",
            "paid": "Order has been paid - can be shipped or cancelled",
            "cancelled": "Terminal state - order has been cancelled",
            "shipped": "Terminal state - order has been shipped"
        },
        "valid_transitions": {
            "pending_payment": ["pay", "cancel"],
            "paid": ["ship", "cancel"],
            "cancelled": [],
            "shipped": []
        },
        "endpoints": {
            "create_order": "/state/orders (POST)",
            "get_order": "/state/orders/{order_id} (GET)",
            "list_orders": "/state/orders (GET)",
            "pay_order": "/state/orders/{order_id}/pay (POST)",
            "cancel_order": "/state/orders/{order_id}/cancel (POST)",
            "ship_order": "/state/orders/{order_id}/ship (POST)"
        }
    }


@router.post("/orders", response_model=OrderResponse, status_code=201)
async def router_create_order(order_data: OrderCreate):
    """Create a new order in the initial 'Pending Payment' state.

    The order will be created with the provided items and total amount,
    and will start in the Pending Payment state.

    Args:
        order_data: Order creation data (items and total amount).

    Returns:
        OrderResponse with complete order information.

    Raises:
        HTTPException: If order creation fails.
    """
    return _create_order_logic(order_data)


@router.get("/orders/{order_id}", response_model=OrderResponse)
async def router_get_order(order_id: int):
    """Get order information by ID.

    Args:
        order_id: ID of the order to retrieve.

    Returns:
        OrderResponse with complete order information.

    Raises:
        HTTPException: If order is not found.
    """
    return _get_order_logic(order_id)


@router.get("/orders", response_model=Dict[str, Any])
async def router_list_orders():
    """List all orders.

    Returns:
        Dictionary with total count and list of all orders.
    """
    return {
        "total": len(_orders),
        "orders": [OrderResponse(**order.get_info()) for order in _orders.values()]
    }


@router.post("/orders/{order_id}/pay", response_model=TransitionResponse)
async def router_pay_order(order_id: int):
    """Process payment for an order.

    Valid transition: Pending Payment -> Paid

    This transition is only valid if the order is in the Pending Payment state.
    If the order is already paid, cancelled, or shipped, this will fail.

    Args:
        order_id: ID of the order to pay.

    Returns:
        TransitionResponse with transition details.

    Raises:
        HTTPException: If order is not found or transition is invalid.
    """
    return _transition_order_logic(
        order_id=order_id,
        transition_func="pay",
        success_message="Payment processed successfully"
    )


@router.post("/orders/{order_id}/cancel", response_model=TransitionResponse)
async def router_cancel_order(order_id: int):
    """Cancel an order.

    Valid transitions:
    - Pending Payment -> Cancelled
    - Paid -> Cancelled

    This transition is valid if the order is in Pending Payment or Paid state.
    If the order is already cancelled or shipped, this will fail.

    Args:
        order_id: ID of the order to cancel.

    Returns:
        TransitionResponse with transition details.

    Raises:
        HTTPException: If order is not found or transition is invalid.
    """
    return _transition_order_logic(
        order_id=order_id,
        transition_func="cancel",
        success_message="Order cancelled successfully"
    )


@router.post("/orders/{order_id}/ship", response_model=TransitionResponse)
async def router_ship_order(order_id: int):
    """Ship an order.

    Valid transition: Paid -> Shipped

    This transition is only valid if the order is in the Paid state.
    If the order is not paid, already shipped, or cancelled, this will fail.

    Args:
        order_id: ID of the order to ship.

    Returns:
        TransitionResponse with transition details.

    Raises:
        HTTPException: If order is not found or transition is invalid.
    """
    return _transition_order_logic(
        order_id=order_id,
        transition_func="ship",
        success_message="Order shipped successfully"
    )


# Also create standalone app for independent use
app = FastAPI(
    title="E-commerce Order System - State Pattern",
    description=(
        "API demonstrating the State pattern for order management. "
        "The State pattern allows an object to alter its behavior when "
        "its internal state changes."
    ),
    version="1.0.0"
)


@app.get("/", tags=["Root"])
async def root():
    """Get API information and available endpoints.

    Returns:
        Dictionary with API information, pattern description, and endpoints.
    """
    return {
        "message": "E-commerce Order System - State Pattern",
        "pattern": "State",
        "description": (
            "Allows an object to alter its behavior when its internal state changes. "
            "The object will appear to have changed its class."
        ),
        "states": {
            "pending_payment": "Initial state - order created, awaiting payment",
            "paid": "Order has been paid - can be shipped or cancelled",
            "cancelled": "Terminal state - order has been cancelled",
            "shipped": "Terminal state - order has been shipped"
        },
        "valid_transitions": {
            "pending_payment": ["pay", "cancel"],
            "paid": ["ship", "cancel"],
            "cancelled": [],
            "shipped": []
        },
        "endpoints": {
            "create_order": "/orders (POST)",
            "get_order": "/orders/{order_id} (GET)",
            "list_orders": "/orders (GET)",
            "pay_order": "/orders/{order_id}/pay (POST)",
            "cancel_order": "/orders/{order_id}/cancel (POST)",
            "ship_order": "/orders/{order_id}/ship (POST)"
        }
    }


@app.post("/orders", response_model=OrderResponse, status_code=201, tags=["Orders"])
async def create_order(order_data: OrderCreate):
    """Create a new order in the initial 'Pending Payment' state.

    The order will be created with the provided items and total amount,
    and will start in the Pending Payment state.

    Args:
        order_data: Order creation data (items and total amount).

    Returns:
        OrderResponse with complete order information.

    Raises:
        HTTPException: If order creation fails.
    """
    return _create_order_logic(order_data)


@app.get("/orders/{order_id}", response_model=OrderResponse, tags=["Orders"])
async def get_order(order_id: int):
    """Get order information by ID.

    Args:
        order_id: ID of the order to retrieve.

    Returns:
        OrderResponse with complete order information.

    Raises:
        HTTPException: If order is not found.
    """
    return _get_order_logic(order_id)


@app.get("/orders", response_model=Dict[str, Any], tags=["Orders"])
async def list_orders():
    """List all orders.

    Returns:
        Dictionary with total count and list of all orders.
    """
    return {
        "total": len(_orders),
        "orders": [OrderResponse(**order.get_info()) for order in _orders.values()]
    }


@app.post("/orders/{order_id}/pay", response_model=TransitionResponse, tags=["Transitions"])
async def pay_order(order_id: int):
    """Process payment for an order.

    Valid transition: Pending Payment -> Paid

    This transition is only valid if the order is in the Pending Payment state.
    If the order is already paid, cancelled, or shipped, this will fail.

    Args:
        order_id: ID of the order to pay.

    Returns:
        TransitionResponse with transition details.

    Raises:
        HTTPException: If order is not found or transition is invalid.
    """
    return _transition_order_logic(
        order_id=order_id,
        transition_func="pay",
        success_message="Payment processed successfully"
    )


@app.post("/orders/{order_id}/cancel", response_model=TransitionResponse, tags=["Transitions"])
async def cancel_order(order_id: int):
    """Cancel an order.

    Valid transitions:
    - Pending Payment -> Cancelled
    - Paid -> Cancelled

    This transition is valid if the order is in Pending Payment or Paid state.
    If the order is already cancelled or shipped, this will fail.

    Args:
        order_id: ID of the order to cancel.

    Returns:
        TransitionResponse with transition details.

    Raises:
        HTTPException: If order is not found or transition is invalid.
    """
    return _transition_order_logic(
        order_id=order_id,
        transition_func="cancel",
        success_message="Order cancelled successfully"
    )


@app.post("/orders/{order_id}/ship", response_model=TransitionResponse, tags=["Transitions"])
async def ship_order(order_id: int):
    """Ship an order.

    Valid transition: Paid -> Shipped

    This transition is only valid if the order is in the Paid state.
    If the order is not paid, already shipped, or cancelled, this will fail.

    Args:
        order_id: ID of the order to ship.

    Returns:
        TransitionResponse with transition details.

    Raises:
        HTTPException: If order is not found or transition is invalid.
    """
    return _transition_order_logic(
        order_id=order_id,
        transition_func="ship",
        success_message="Order shipped successfully"
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
