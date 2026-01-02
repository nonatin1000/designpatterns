"""Order class (Context) for the State pattern.

This module defines the Order class which serves as the context in the
State pattern. The order can be in different states and delegates behavior
to the current state object.

The State pattern allows an object to alter its behavior when its internal
state changes. The object will appear to have changed its class.
"""

from .state import State, PendingPaymentState, PaidState, CancelledState, ShippedState
from typing import List, Dict
from datetime import datetime


class Order:
    """Context class that can have multiple internal states.

    The Order class serves as the context in the State pattern. It maintains
    references to all possible state objects and delegates requests to the
    current state object. The behavior of the Order changes according to its
    internal state, making it appear as if the Order changed its class.

    The State pattern encapsulates state-specific behavior and makes state
    transitions explicit, preventing invalid transitions at the state level.

    Attributes:
        order_id: Unique identifier for the order (auto-incremented).
        items: List of item names in the order.
        total_amount: Total value of the order in BRL.
        created_at: Timestamp when the order was created.
        state_history: History of state transitions with timestamps.
    """

    _id_counter: int = 0  # Class-level counter for unique order IDs

    def __init__(self, items: List[str] = None, total_amount: float = 0.0) -> None:
        """Initialize order with all possible states.

        Creates a new order and initializes all possible state objects.
        The order starts in the PendingPayment state, which is the initial
        state for all new orders.

        Args:
            items: List of item names in the order. Defaults to empty list.
            total_amount: Total value of the order in BRL. Must be >= 0.

        Raises:
            ValueError: If total_amount is negative.

        Example:
            >>> order = Order(items=["Notebook", "Mouse"], total_amount=2500.00)
            >>> order.get_state_name()
            'Pending Payment'
        """
        if total_amount < 0:
            raise ValueError("Total amount cannot be negative")

        # Generate unique ID
        Order._id_counter += 1
        self.order_id: int = Order._id_counter

        # Order data
        self.items: List[str] = items or []
        self.total_amount: float = total_amount
        self.created_at: datetime = datetime.now()
        self.state_history: List[str] = []

        # Create all possible state instances
        self._pending_payment: State = PendingPaymentState(self)
        self._paid: State = PaidState(self)
        self._cancelled: State = CancelledState(self)
        self._shipped: State = ShippedState(self)

        # Set initial state
        self._current_state: State = self._pending_payment
        self._record_state_change("Pending Payment")

        print(f"[ORDER] New order #{self.order_id} created - State: {self.get_state_name()}")

    def pay(self) -> None:
        """Process payment for the order.

        Delegates the payment transition to the current state object.
        The behavior depends on which state the order is currently in.
        Valid states: PendingPayment -> Paid.

        Raises:
            ValueError: If payment is not allowed in the current state.

        Example:
            >>> order = Order(items=["Item"], total_amount=100.0)
            >>> order.pay()  # Valid: PendingPayment -> Paid
            >>> order.pay()  # Invalid: raises ValueError
        """
        try:
            self._current_state.pay()
        except ValueError as e:
            print(f"[ERROR] {str(e)}")
            raise

    def cancel(self) -> None:
        """Cancel the order.

        Delegates the cancellation transition to the current state object.
        The behavior depends on which state the order is currently in.
        Valid states: PendingPayment -> Cancelled, Paid -> Cancelled.

        Raises:
            ValueError: If cancellation is not allowed in the current state.

        Example:
            >>> order = Order(items=["Item"], total_amount=100.0)
            >>> order.cancel()  # Valid: PendingPayment -> Cancelled
            >>> order.cancel()  # Invalid: raises ValueError
        """
        try:
            self._current_state.cancel()
        except ValueError as e:
            print(f"[ERROR] {str(e)}")
            raise

    def ship(self) -> None:
        """Ship the order.

        Delegates the shipping transition to the current state object.
        The behavior depends on which state the order is currently in.
        Valid states: Paid -> Shipped.

        Raises:
            ValueError: If shipping is not allowed in the current state.

        Example:
            >>> order = Order(items=["Item"], total_amount=100.0)
            >>> order.pay()
            >>> order.ship()  # Valid: Paid -> Shipped
            >>> order.ship()  # Invalid: raises ValueError
        """
        try:
            self._current_state.ship()
        except ValueError as e:
            print(f"[ERROR] {str(e)}")
            raise

    # State getters (allow concrete states to perform transitions)

    def get_pending_payment_state(self) -> State:
        """Get the PendingPayment state instance.

        This method is used by state objects to transition back to the
        pending payment state. It returns the same state instance that
        was created during order initialization.

        Returns:
            The PendingPaymentState instance for this order.
        """
        return self._pending_payment

    def get_paid_state(self) -> State:
        """Get the Paid state instance.

        This method is used by state objects to transition to the paid
        state. It returns the same state instance that was created during
        order initialization.

        Returns:
            The PaidState instance for this order.
        """
        return self._paid

    def get_cancelled_state(self) -> State:
        """Get the Cancelled state instance.

        This method is used by state objects to transition to the cancelled
        state. It returns the same state instance that was created during
        order initialization.

        Returns:
            The CancelledState instance for this order.
        """
        return self._cancelled

    def get_shipped_state(self) -> State:
        """Get the Shipped state instance.

        This method is used by state objects to transition to the shipped
        state. It returns the same state instance that was created during
        order initialization.

        Returns:
            The ShippedState instance for this order.
        """
        return self._shipped

    # State management

    def set_state(self, state: State) -> None:
        """Change the current state of the order.

        This method is called by state objects to transition to a new state.
        It updates the current state and records the transition in the history.

        Args:
            state: The new state object to transition to.

        Note:
            This method is typically called by state objects themselves,
            not directly by external code.
        """
        self._current_state = state
        self._record_state_change(state.get_name())

    def get_current_state(self) -> State:
        """Get the current state object.

        Returns:
            The current State instance that defines the order's behavior.
        """
        return self._current_state

    def get_state_name(self) -> str:
        """Get the name of the current state.

        Returns:
            The current state name as a string (e.g., "Pending Payment", "Paid").
        """
        return self._current_state.get_name()

    def _record_state_change(self, state_name: str) -> None:
        """Record state change in history.

        This private method is called whenever the order transitions to a
        new state. It appends a timestamped entry to the state history.

        Args:
            state_name: Name of the state being transitioned to.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.state_history.append(f"{timestamp} - {state_name}")

    def get_history(self) -> List[str]:
        """Get the complete state transition history.

        Returns a copy of the state history to prevent external modification.

        Returns:
            A copy of the state history list, containing timestamped state
            transition records.
        """
        return self.state_history.copy()

    def get_info(self) -> Dict[str, any]:
        """Get complete order information as a dictionary.

        Returns all order details in a structured format suitable for
        API responses or serialization.

        Returns:
            A dictionary containing:
            - order_id: Order ID (int)
            - items: List of item names (List[str])
            - total_amount: Total value in BRL (float)
            - state: Current state name (str)
            - created_at: Creation timestamp (str)
            - state_history: State transition history (List[str])
        """
        return {
            "order_id": self.order_id,
            "items": self.items,
            "total_amount": self.total_amount,
            "state": self.get_state_name(),
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "state_history": self.state_history
        }

    def __str__(self) -> str:
        """String representation of the order.

        Returns:
            A human-readable string with order ID, current state, and total amount.
        """
        return (
            f"Order #{self.order_id} - "
            f"State: {self.get_state_name()} - "
            f"Total: R$ {self.total_amount:.2f}"
        )

    def __repr__(self) -> str:
        """Detailed string representation of the order for debugging.

        Returns:
            A detailed string representation suitable for debugging and logging.
        """
        return (
            f"Order(id={self.order_id}, "
            f"items={self.items}, "
            f"total={self.total_amount}, "
            f"state={self.get_state_name()})"
        )
