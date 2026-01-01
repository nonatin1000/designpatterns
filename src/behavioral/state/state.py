"""State interface and concrete state implementations.

This module defines the State pattern components - the state interface
and concrete state classes for order processing.

The State pattern allows an object to alter its behavior when its internal
state changes. The object will appear to have changed its class.
"""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .order import Order


class State(ABC):
    """Abstract state interface for all concrete states.

    Each concrete state implements its own behavior for state transitions,
    allowing the context object (Order) to delegate request processing to
    the current state object. This encapsulation makes state-specific
    behavior explicit and easier to maintain.

    The State pattern encapsulates state-specific behavior and makes state
    transitions explicit, preventing invalid transitions at the state level.
    """

    @abstractmethod
    def pay(self) -> None:
        """Process payment for the order.

        This method handles the payment transition. The behavior depends
        on the current state - some states allow payment, others raise
        exceptions.

        Raises:
            ValueError: If payment is not allowed in the current state.
        """
        ...

    @abstractmethod
    def cancel(self) -> None:
        """Cancel the order.

        This method handles the cancellation transition. The behavior
        depends on the current state - some states allow cancellation,
        others raise exceptions.

        Raises:
            ValueError: If cancellation is not allowed in the current state.
        """
        ...

    @abstractmethod
    def ship(self) -> None:
        """Ship the order.

        This method handles the shipping transition. The behavior depends
        on the current state - some states allow shipping, others raise
        exceptions.

        Raises:
            ValueError: If shipping is not allowed in the current state.
        """
        ...

    @abstractmethod
    def get_name(self) -> str:
        """Get the name of the current state.

        Returns:
            The state name as a string (e.g., "Pending Payment", "Paid").
        """
        ...


class PendingPaymentState(State):
    """Concrete state: Order is pending payment (initial state).

    This is the initial state when an order is created. The order must be
    paid before it can be shipped.

    Valid transitions:
        - pay() -> transitions to PaidState
        - cancel() -> transitions to CancelledState

    Invalid transitions:
        - ship() -> raises ValueError (order not paid yet)
    """

    def __init__(self, order: "Order") -> None:
        """Initialize pending payment state.

        Args:
            order: Reference to the context (Order) object that owns
                this state.
        """
        self._order = order

    def pay(self) -> None:
        """Process payment successfully.

        Transitions the order from Pending Payment to Paid state.
        This is a valid transition and will succeed.

        Raises:
            ValueError: Never raised in this state (payment is valid).
        """
        order_id = self._order.order_id
        print(f"[TRANSITION] Payment confirmed! Order #{order_id} is PAID")
        self._order.set_state(self._order.get_paid_state())

    def cancel(self) -> None:
        """Cancel order before payment.

        Transitions the order from Pending Payment to Cancelled state.
        This is a valid transition and will succeed.

        Raises:
            ValueError: Never raised in this state (cancellation is valid).
        """
        order_id = self._order.order_id
        msg = f"[TRANSITION] Cancelling order #{order_id} before payment"
        print(msg)
        self._order.set_state(self._order.get_cancelled_state())

    def ship(self) -> None:
        """Attempt to ship unpaid order.

        This is an invalid transition - orders cannot be shipped before
        payment.

        Raises:
            ValueError: Always raised, as shipping is not allowed in
                this state.
        """
        raise ValueError("Cannot ship order: payment not received yet")

    def get_name(self) -> str:
        """Get the name of this state.

        Returns:
            The state name: "Pending Payment".
        """
        return "Pending Payment"


class PaidState(State):
    """Concrete state: Order has been paid.

    The order has successfully received payment and can now be shipped or
    cancelled. This is an intermediate state between payment and shipping.

    Valid transitions:
        - ship() -> transitions to ShippedState
        - cancel() -> transitions to CancelledState

    Invalid transitions:
        - pay() -> raises ValueError (already paid)
    """

    def __init__(self, order: "Order") -> None:
        """Initialize paid state.

        Args:
            order: Reference to the context (Order) object that owns
                this state.
        """
        self._order = order

    def pay(self) -> None:
        """Attempt to pay again.

        This is an invalid transition - the order is already paid.

        Raises:
            ValueError: Always raised, as payment is not allowed in
                this state.
        """
        raise ValueError("Cannot process payment: order already paid")

    def cancel(self) -> None:
        """Cancel order after payment.

        Transitions the order from Paid to Cancelled state.
        This is a valid transition and will succeed.

        Raises:
            ValueError: Never raised in this state (cancellation is valid).
        """
        order_id = self._order.order_id
        msg = f"[TRANSITION] Cancelling order #{order_id} after payment"
        print(msg)
        self._order.set_state(self._order.get_cancelled_state())

    def ship(self) -> None:
        """Ship the paid order.

        Transitions the order from Paid to Shipped state.
        This is a valid transition and will succeed.

        Raises:
            ValueError: Never raised in this state (shipping is valid).
        """
        order_id = self._order.order_id
        print(f"[TRANSITION] Shipping order #{order_id}")
        self._order.set_state(self._order.get_shipped_state())

    def get_name(self) -> str:
        """Get the name of this state.

        Returns:
            The state name: "Paid".
        """
        return "Paid"


class CancelledState(State):
    """Concrete state: Order has been cancelled (terminal state).

    This is a terminal state - once an order is cancelled, no further
    transitions are allowed. The order lifecycle ends here.

    Invalid transitions:
        - pay() -> raises ValueError (order cancelled)
        - cancel() -> raises ValueError (already cancelled)
        - ship() -> raises ValueError (order cancelled)
    """

    def __init__(self, order: "Order") -> None:
        """Initialize cancelled state.

        Args:
            order: Reference to the context (Order) object that owns
                this state.
        """
        self._order = order

    def pay(self) -> None:
        """Attempt to pay cancelled order.

        This is an invalid transition - cancelled orders cannot be paid.

        Raises:
            ValueError: Always raised, as payment is not allowed in
                this state.
        """
        raise ValueError("Cannot process payment: order is cancelled")

    def cancel(self) -> None:
        """Attempt to cancel again.

        This is an invalid transition - the order is already cancelled.

        Raises:
            ValueError: Always raised, as cancellation is not allowed
                in this state.
        """
        raise ValueError("Cannot cancel: order already cancelled")

    def ship(self) -> None:
        """Attempt to ship cancelled order.

        This is an invalid transition - cancelled orders cannot be shipped.

        Raises:
            ValueError: Always raised, as shipping is not allowed in
                this state.
        """
        raise ValueError("Cannot ship: order is cancelled")

    def get_name(self) -> str:
        """Get the name of this state.

        Returns:
            The state name: "Cancelled".
        """
        return "Cancelled"


class ShippedState(State):
    """Concrete state: Order has been shipped (terminal state).

    This is a terminal state - once an order is shipped, no further
    transitions are allowed. The order lifecycle ends here successfully.

    Invalid transitions:
        - pay() -> raises ValueError (already paid and shipped)
        - cancel() -> raises ValueError (already shipped)
        - ship() -> raises ValueError (already shipped)
    """

    def __init__(self, order: "Order") -> None:
        """Initialize shipped state.

        Args:
            order: Reference to the context (Order) object that owns
                this state.
        """
        self._order = order

    def pay(self) -> None:
        """Attempt to pay shipped order.

        This is an invalid transition - shipped orders are already paid.

        Raises:
            ValueError: Always raised, as payment is not allowed in
                this state.
        """
        msg = "Cannot process payment: order already paid and shipped"
        raise ValueError(msg)

    def cancel(self) -> None:
        """Attempt to cancel shipped order.

        This is an invalid transition - shipped orders cannot be cancelled.

        Raises:
            ValueError: Always raised, as cancellation is not allowed
                in this state.
        """
        raise ValueError("Cannot cancel: order already shipped")

    def ship(self) -> None:
        """Attempt to ship again.

        This is an invalid transition - the order is already shipped.

        Raises:
            ValueError: Always raised, as shipping is not allowed in
                this state.
        """
        raise ValueError("Cannot ship: order already shipped")

    def get_name(self) -> str:
        """Get the name of this state.

        Returns:
            The state name: "Shipped".
        """
        return "Shipped"
