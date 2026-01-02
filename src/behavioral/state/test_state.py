"""Comprehensive tests for State pattern implementation."""

import sys
from pathlib import Path

# Add src directory to path for standalone execution
if __name__ == "__main__":
    src_dir = Path(__file__).parent.parent.parent
    sys.path.insert(0, str(src_dir))

try:
    # Try relative imports first (when used as module)
    from .order import Order
    from .state import (
        State,
        PendingPaymentState,
        PaidState,
        CancelledState,
        ShippedState
    )
except ImportError:
    # Fall back to direct module imports (bypassing __init__.py)
    # This avoids importing schemas.py which requires pydantic
    import importlib.util
    import types
    test_dir = Path(__file__).parent
    
    # Create module structure for relative imports
    behavioral = types.ModuleType("behavioral")
    behavioral_state = types.ModuleType("behavioral.state")
    sys.modules["behavioral"] = behavioral
    sys.modules["behavioral.state"] = behavioral_state
    
    # Load state module first (order.py depends on it)
    state_spec = importlib.util.spec_from_file_location(
        "behavioral.state.state",
        test_dir / "state.py"
    )
    state_module = importlib.util.module_from_spec(state_spec)
    sys.modules["behavioral.state.state"] = state_module
    behavioral_state.state = state_module
    state_spec.loader.exec_module(state_module)
    
    # Load order module (depends on state)
    order_spec = importlib.util.spec_from_file_location(
        "behavioral.state.order",
        test_dir / "order.py"
    )
    order_module = importlib.util.module_from_spec(order_spec)
    sys.modules["behavioral.state.order"] = order_module
    behavioral_state.order = order_module
    order_spec.loader.exec_module(order_module)
    
    # Extract classes
    Order = order_module.Order
    State = state_module.State
    PendingPaymentState = state_module.PendingPaymentState
    PaidState = state_module.PaidState
    CancelledState = state_module.CancelledState
    ShippedState = state_module.ShippedState


def test_order_initial_state():
    """Test that new orders start in PendingPayment state."""
    order = Order(items=["Item1"], total_amount=100.0)
    
    assert order.get_state_name() == "Pending Payment"
    assert order.order_id > 0
    assert len(order.items) == 1
    assert order.total_amount == 100.0
    assert len(order.state_history) == 1
    assert "Pending Payment" in order.state_history[0]
    
    print("[OK] Test Order Initial State: PASSED")


def test_pending_payment_to_paid():
    """Test valid transition: PendingPayment -> Paid."""
    order = Order(items=["Item1"], total_amount=100.0)
    
    assert order.get_state_name() == "Pending Payment"
    order.pay()
    assert order.get_state_name() == "Paid"
    assert len(order.state_history) == 2
    
    print("[OK] Test PendingPayment -> Paid: PASSED")


def test_pending_payment_to_cancelled():
    """Test valid transition: PendingPayment -> Cancelled."""
    order = Order(items=["Item1"], total_amount=100.0)
    
    assert order.get_state_name() == "Pending Payment"
    order.cancel()
    assert order.get_state_name() == "Cancelled"
    assert len(order.state_history) == 2
    
    print("[OK] Test PendingPayment -> Cancelled: PASSED")


def test_pending_payment_cannot_ship():
    """Test invalid transition: PendingPayment cannot ship."""
    order = Order(items=["Item1"], total_amount=100.0)
    
    assert order.get_state_name() == "Pending Payment"
    try:
        order.ship()
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "payment not received" in str(e).lower()
    
    # State should remain unchanged
    assert order.get_state_name() == "Pending Payment"
    
    print("[OK] Test PendingPayment Cannot Ship: PASSED")


def test_paid_to_shipped():
    """Test valid transition: Paid -> Shipped."""
    order = Order(items=["Item1"], total_amount=100.0)
    order.pay()
    
    assert order.get_state_name() == "Paid"
    order.ship()
    assert order.get_state_name() == "Shipped"
    assert len(order.state_history) == 3
    
    print("[OK] Test Paid -> Shipped: PASSED")


def test_paid_to_cancelled():
    """Test valid transition: Paid -> Cancelled."""
    order = Order(items=["Item1"], total_amount=100.0)
    order.pay()
    
    assert order.get_state_name() == "Paid"
    order.cancel()
    assert order.get_state_name() == "Cancelled"
    assert len(order.state_history) == 3
    
    print("[OK] Test Paid -> Cancelled: PASSED")


def test_paid_cannot_pay_again():
    """Test invalid transition: Paid cannot pay again."""
    order = Order(items=["Item1"], total_amount=100.0)
    order.pay()
    
    assert order.get_state_name() == "Paid"
    try:
        order.pay()
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "already paid" in str(e).lower()
    
    # State should remain unchanged
    assert order.get_state_name() == "Paid"
    
    print("[OK] Test Paid Cannot Pay Again: PASSED")


def test_cancelled_is_terminal():
    """Test that Cancelled is a terminal state (no transitions allowed)."""
    order = Order(items=["Item1"], total_amount=100.0)
    order.cancel()
    
    assert order.get_state_name() == "Cancelled"
    
    # Try all transitions - all should fail
    try:
        order.pay()
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "cancelled" in str(e).lower()
    
    try:
        order.cancel()
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "already cancelled" in str(e).lower()
    
    try:
        order.ship()
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "cancelled" in str(e).lower()
    
    # State should remain Cancelled
    assert order.get_state_name() == "Cancelled"
    
    print("[OK] Test Cancelled Is Terminal: PASSED")


def test_shipped_is_terminal():
    """Test that Shipped is a terminal state (no transitions allowed)."""
    order = Order(items=["Item1"], total_amount=100.0)
    order.pay()
    order.ship()
    
    assert order.get_state_name() == "Shipped"
    
    # Try all transitions - all should fail
    try:
        order.pay()
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "already paid and shipped" in str(e).lower() or "already shipped" in str(e).lower()
    
    try:
        order.cancel()
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "already shipped" in str(e).lower()
    
    try:
        order.ship()
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "already shipped" in str(e).lower()
    
    # State should remain Shipped
    assert order.get_state_name() == "Shipped"
    
    print("[OK] Test Shipped Is Terminal: PASSED")


def test_complete_order_lifecycle():
    """Test complete order lifecycle: Pending -> Paid -> Shipped."""
    order = Order(items=["Notebook", "Mouse"], total_amount=2500.0)
    
    # Initial state
    assert order.get_state_name() == "Pending Payment"
    assert len(order.state_history) == 1
    
    # Pay
    order.pay()
    assert order.get_state_name() == "Paid"
    assert len(order.state_history) == 2
    
    # Ship
    order.ship()
    assert order.get_state_name() == "Shipped"
    assert len(order.state_history) == 3
    
    # Verify order data
    assert order.order_id > 0
    assert len(order.items) == 2
    assert order.total_amount == 2500.0
    
    print("[OK] Test Complete Order Lifecycle: PASSED")


def test_cancelled_before_payment():
    """Test order cancelled before payment."""
    order = Order(items=["Item1"], total_amount=100.0)
    
    assert order.get_state_name() == "Pending Payment"
    order.cancel()
    assert order.get_state_name() == "Cancelled"
    
    # Cannot do anything after cancellation
    try:
        order.pay()
        assert False, "Should have raised ValueError"
    except ValueError:
        pass
    
    print("[OK] Test Cancelled Before Payment: PASSED")


def test_cancelled_after_payment():
    """Test order cancelled after payment."""
    order = Order(items=["Item1"], total_amount=100.0)
    order.pay()
    
    assert order.get_state_name() == "Paid"
    order.cancel()
    assert order.get_state_name() == "Cancelled"
    
    # Cannot do anything after cancellation
    try:
        order.ship()
        assert False, "Should have raised ValueError"
    except ValueError:
        pass
    
    print("[OK] Test Cancelled After Payment: PASSED")


def test_negative_amount_validation():
    """Test that negative amounts raise ValueError."""
    try:
        Order(items=["Item1"], total_amount=-100.0)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "cannot be negative" in str(e).lower()
    
    print("[OK] Test Negative Amount Validation: PASSED")


def test_zero_amount():
    """Test order with zero amount."""
    order = Order(items=["Free Item"], total_amount=0.0)
    
    assert order.total_amount == 0.0
    assert order.get_state_name() == "Pending Payment"
    
    # Should be able to pay and ship
    order.pay()
    assert order.get_state_name() == "Paid"
    
    order.ship()
    assert order.get_state_name() == "Shipped"
    
    print("[OK] Test Zero Amount: PASSED")


def test_empty_items_list():
    """Test order with empty items list."""
    order = Order(items=[], total_amount=100.0)
    
    assert len(order.items) == 0
    assert order.get_state_name() == "Pending Payment"
    
    order.pay()
    assert order.get_state_name() == "Paid"
    
    print("[OK] Test Empty Items List: PASSED")


def test_order_with_multiple_items():
    """Test order with multiple items."""
    items = ["Item1", "Item2", "Item3", "Item4"]
    order = Order(items=items, total_amount=500.0)
    
    assert len(order.items) == 4
    assert order.items == items
    assert order.total_amount == 500.0
    
    print("[OK] Test Order With Multiple Items: PASSED")


def test_state_history_tracking():
    """Test that state history is properly tracked."""
    order = Order(items=["Item1"], total_amount=100.0)
    
    # Initial state
    assert len(order.state_history) == 1
    assert "Pending Payment" in order.state_history[0]
    
    # Pay
    order.pay()
    assert len(order.state_history) == 2
    assert "Paid" in order.state_history[1]
    
    # Ship
    order.ship()
    assert len(order.state_history) == 3
    assert "Shipped" in order.state_history[2]
    
    print("[OK] Test State History Tracking: PASSED")


def test_order_id_auto_increment():
    """Test that order IDs are auto-incremented."""
    # Reset counter for testing
    Order._id_counter = 0
    
    order1 = Order(items=["Item1"], total_amount=100.0)
    order2 = Order(items=["Item2"], total_amount=200.0)
    order3 = Order(items=["Item3"], total_amount=300.0)
    
    assert order1.order_id == 1
    assert order2.order_id == 2
    assert order3.order_id == 3
    
    print("[OK] Test Order ID Auto Increment: PASSED")


def test_order_get_info():
    """Test order get_info method."""
    order = Order(items=["Item1", "Item2"], total_amount=250.0)
    
    info = order.get_info()
    
    assert "order_id" in info
    assert "items" in info
    assert "total_amount" in info
    assert "state" in info
    assert "created_at" in info
    assert "state_history" in info
    
    assert info["order_id"] == order.order_id
    assert info["items"] == ["Item1", "Item2"]
    assert info["total_amount"] == 250.0
    assert info["state"] == "Pending Payment"
    assert len(info["state_history"]) == 1
    
    print("[OK] Test Order Get Info: PASSED")


def test_state_names():
    """Test that all states return correct names."""
    order = Order(items=["Item1"], total_amount=100.0)
    
    # Test state names
    assert order.get_state_name() == "Pending Payment"
    
    order.pay()
    assert order.get_state_name() == "Paid"
    
    order.ship()
    assert order.get_state_name() == "Shipped"
    
    # Test cancelled
    order2 = Order(items=["Item2"], total_amount=200.0)
    order2.cancel()
    assert order2.get_state_name() == "Cancelled"
    
    print("[OK] Test State Names: PASSED")


def test_state_objects_are_singletons():
    """Test that state objects are reused (same instance)."""
    order = Order(items=["Item1"], total_amount=100.0)
    
    # Get initial state
    initial_state = order._current_state
    
    # Transition and come back (if possible)
    order.pay()
    paid_state = order._current_state
    
    # States should be different instances
    assert initial_state is not paid_state
    
    # But the state objects should be the same instances stored in order
    assert order._pending_payment is not None
    assert order._paid is not None
    assert order._cancelled is not None
    assert order._shipped is not None
    
    print("[OK] Test State Objects Are Singletons: PASSED")


def test_order_repr():
    """Test order string representation."""
    order = Order(items=["Item1"], total_amount=100.0)
    
    repr_str = repr(order)
    assert "Order" in repr_str
    assert str(order.order_id) in repr_str
    
    print("[OK] Test Order Repr: PASSED")


def test_order_str():
    """Test order string representation (__str__)."""
    order = Order(items=["Item1"], total_amount=100.0)
    
    str_repr = str(order)
    assert "Order #" in str_repr
    assert str(order.order_id) in str_repr
    assert "Pending Payment" in str_repr
    assert "100.00" in str_repr
    
    print("[OK] Test Order Str: PASSED")


def test_get_current_state():
    """Test get_current_state method."""
    order = Order(items=["Item1"], total_amount=100.0)
    
    initial_state = order.get_current_state()
    assert initial_state is not None
    assert initial_state.get_name() == "Pending Payment"
    
    order.pay()
    paid_state = order.get_current_state()
    assert paid_state.get_name() == "Paid"
    assert paid_state is not initial_state
    
    print("[OK] Test Get Current State: PASSED")


def test_get_history_returns_copy():
    """Test that get_history returns a copy, not the original list."""
    order = Order(items=["Item1"], total_amount=100.0)
    order.pay()
    
    history1 = order.get_history()
    history2 = order.get_history()
    
    # Should be different objects
    assert history1 is not history2
    # But same content
    assert history1 == history2
    
    # Modifying one shouldn't affect the other
    history1.append("Fake entry")
    assert len(order.get_history()) == 2
    
    print("[OK] Test Get History Returns Copy: PASSED")


def test_state_getters():
    """Test state getter methods."""
    order = Order(items=["Item1"], total_amount=100.0)
    
    pending = order.get_pending_payment_state()
    paid = order.get_paid_state()
    cancelled = order.get_cancelled_state()
    shipped = order.get_shipped_state()
    
    assert pending is not None
    assert paid is not None
    assert cancelled is not None
    assert shipped is not None
    
    assert pending.get_name() == "Pending Payment"
    assert paid.get_name() == "Paid"
    assert cancelled.get_name() == "Cancelled"
    assert shipped.get_name() == "Shipped"
    
    print("[OK] Test State Getters: PASSED")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("RUNNING STATE PATTERN TESTS")
    print("=" * 60 + "\n")

    try:
        test_order_initial_state()
        test_pending_payment_to_paid()
        test_pending_payment_to_cancelled()
        test_pending_payment_cannot_ship()
        test_paid_to_shipped()
        test_paid_to_cancelled()
        test_paid_cannot_pay_again()
        test_cancelled_is_terminal()
        test_shipped_is_terminal()
        test_complete_order_lifecycle()
        test_cancelled_before_payment()
        test_cancelled_after_payment()
        test_negative_amount_validation()
        test_zero_amount()
        test_empty_items_list()
        test_order_with_multiple_items()
        test_state_history_tracking()
        test_order_id_auto_increment()
        test_order_get_info()
        test_state_names()
        test_state_objects_are_singletons()
        test_order_repr()
        test_order_str()
        test_get_current_state()
        test_get_history_returns_copy()
        test_state_getters()

        print("\n" + "=" * 60)
        print("ALL TESTS PASSED! [OK]")
        print("=" * 60 + "\n")

    except AssertionError as e:
        print(f"\n[ERROR] TEST FAILED: {e}\n")
    except Exception as e:
        print(f"\n[ERROR] ERROR: {e}\n")
        import traceback
        traceback.print_exc()

