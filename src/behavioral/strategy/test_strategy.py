"""Comprehensive tests for Strategy pattern implementation."""

import sys
from pathlib import Path

# Add src directory to path for standalone execution
if __name__ == "__main__":
    src_dir = Path(__file__).parent.parent.parent
    sys.path.insert(0, str(src_dir))

try:
    # Try relative imports first (when used as module)
    from .freight_strategy import (
        CommonFreight,
        ExpressFreight
    )
    from .order import ElectronicsOrder, FurnitureOrder
except ImportError:
    # Fall back to absolute imports (when run as script)
    from behavioral.strategy.freight_strategy import (
        CommonFreight,
        ExpressFreight
    )
    from behavioral.strategy.order import (
        ElectronicsOrder,
        FurnitureOrder
    )


def test_common_freight_calculation():
    """Test common freight strategy calculation."""
    strategy = CommonFreight()
    cost = strategy.calculate(100.0)
    assert cost == 5.0, f"Expected 5.0, got {cost}"
    print("[OK] Test Common Freight Calculation: PASSED")


def test_express_freight_calculation():
    """Test express freight strategy calculation."""
    strategy = ExpressFreight()
    cost = strategy.calculate(100.0)
    assert cost == 10.0, f"Expected 10.0, got {cost}"
    print("[OK] Test Express Freight Calculation: PASSED")


def test_electronics_order_with_common_freight():
    """Test electronics order with common freight."""
    order = ElectronicsOrder()
    order.amount = 250.0
    order.set_freight_strategy(CommonFreight())

    assert order.category == "Electronics"
    assert order.amount == 250.0

    freight = order.calculate_freight()
    assert freight == 12.5, f"Expected 12.5, got {freight}"
    print("[OK] Test Electronics Order + Common Freight: PASSED")


def test_electronics_order_with_express_freight():
    """Test electronics order with express freight."""
    order = ElectronicsOrder()
    order.amount = 250.0
    order.set_freight_strategy(ExpressFreight())

    freight = order.calculate_freight()
    assert freight == 25.0, f"Expected 25.0, got {freight}"
    print("[OK] Test Electronics Order + Express Freight: PASSED")


def test_furniture_order_with_common_freight():
    """Test furniture order with common freight."""
    order = FurnitureOrder()
    order.amount = 500.0
    order.set_freight_strategy(CommonFreight())

    assert order.category == "Furniture"
    freight = order.calculate_freight()
    assert freight == 25.0, f"Expected 25.0, got {freight}"
    print("[OK] Test Furniture Order + Common Freight: PASSED")


def test_strategy_change_at_runtime():
    """Test changing strategy at runtime."""
    order = ElectronicsOrder()
    order.amount = 100.0

    # Start with common freight
    order.set_freight_strategy(CommonFreight())
    freight1 = order.calculate_freight()
    assert freight1 == 5.0

    # Change to express freight
    order.set_freight_strategy(ExpressFreight())
    freight2 = order.calculate_freight()
    assert freight2 == 10.0

    assert freight2 != freight1, "Strategies should produce different results"
    print("[OK] Test Runtime Strategy Change: PASSED")


def test_negative_amount_validation():
    """Test that negative amounts raise ValueError."""
    order = ElectronicsOrder()

    try:
        order.amount = -100.0
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "cannot be negative" in str(e)
        print("[OK] Test Negative Amount Validation: PASSED")


def test_missing_strategy_error():
    """Test that calculating without strategy raises error."""
    order = ElectronicsOrder()
    order.amount = 100.0

    try:
        order.calculate_freight()
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "must be set" in str(e)
        print("[OK] Test Missing Strategy Error: PASSED")


def test_none_strategy_error():
    """Test that setting None strategy raises error."""
    order = ElectronicsOrder()

    try:
        order.set_freight_strategy(None)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "cannot be None" in str(e)
        print("[OK] Test None Strategy Error: PASSED")


def test_different_amounts():
    """Test freight calculation with various amounts."""
    strategy = CommonFreight()

    test_cases = [
        (100.0, 5.0),
        (250.0, 12.5),
        (500.0, 25.0),
        (1000.0, 50.0),
    ]

    for amount, expected in test_cases:
        result = strategy.calculate(amount)
        assert result == expected, (
            f"For {amount}, expected {expected}, got {result}"
        )

    print("[OK] Test Different Amounts: PASSED")


def test_order_repr():
    """Test order string representation."""
    order = ElectronicsOrder()
    order.amount = 100.0
    order.set_freight_strategy(CommonFreight())

    repr_str = repr(order)
    assert "ElectronicsOrder" in repr_str
    assert "Electronics" in repr_str
    assert "100.00" in repr_str
    assert "CommonFreight" in repr_str

    print("[OK] Test Order Representation: PASSED")


def test_freight_rate_constants():
    """Test that freight strategies use correct rate constants."""
    common = CommonFreight()
    express = ExpressFreight()

    assert common.RATE == 0.05, "Common freight should be 5%"
    assert express.RATE == 0.10, "Express freight should be 10%"

    print("[OK] Test Freight Rate Constants: PASSED")


def test_zero_amount():
    """Test freight calculation with zero amount."""
    strategy = CommonFreight()
    cost = strategy.calculate(0.0)
    assert cost == 0.0, f"Expected 0.0, got {cost}"

    strategy = ExpressFreight()
    cost = strategy.calculate(0.0)
    assert cost == 0.0, f"Expected 0.0, got {cost}"

    print("[OK] Test Zero Amount: PASSED")


def test_express_freight_different_amounts():
    """Test express freight calculation with various amounts."""
    strategy = ExpressFreight()

    test_cases = [
        (100.0, 10.0),
        (250.0, 25.0),
        (500.0, 50.0),
        (1000.0, 100.0),
    ]

    for amount, expected in test_cases:
        result = strategy.calculate(amount)
        assert result == expected, (
            f"For {amount}, expected {expected}, got {result}"
        )

    print("[OK] Test Express Freight Different Amounts: PASSED")


def test_furniture_order_repr():
    """Test furniture order string representation."""
    order = FurnitureOrder()
    order.amount = 500.0
    order.set_freight_strategy(CommonFreight())

    repr_str = repr(order)
    assert "FurnitureOrder" in repr_str
    assert "Furniture" in repr_str
    assert "500.00" in repr_str
    assert "CommonFreight" in repr_str

    print("[OK] Test Furniture Order Representation: PASSED")


def test_multiple_strategy_changes():
    """Test multiple strategy changes on the same order."""
    order = ElectronicsOrder()
    order.amount = 100.0

    # Change strategy multiple times
    order.set_freight_strategy(CommonFreight())
    cost1 = order.calculate_freight()
    assert cost1 == 5.0

    order.set_freight_strategy(ExpressFreight())
    cost2 = order.calculate_freight()
    assert cost2 == 10.0

    order.set_freight_strategy(CommonFreight())
    cost3 = order.calculate_freight()
    assert cost3 == 5.0

    assert cost1 == cost3, "Should be able to revert to previous strategy"
    assert cost2 != cost1, "Strategies should produce different results"

    print("[OK] Test Multiple Strategy Changes: PASSED")


def test_decimal_precision():
    """Test freight calculation with decimal amounts."""
    strategy = CommonFreight()

    # Test with various decimal precisions
    test_cases = [
        (99.99, 4.9995),  # Should handle rounding
        (123.45, 6.1725),
        (0.01, 0.0005),
    ]

    for amount, expected in test_cases:
        result = strategy.calculate(amount)
        # Allow small floating point differences
        assert abs(result - expected) < 0.0001, (
            f"For {amount}, expected ~{expected}, got {result}"
        )

    print("[OK] Test Decimal Precision: PASSED")


def test_large_amounts():
    """Test freight calculation with large amounts."""
    strategy = CommonFreight()
    large_amount = 1000000.0  # 1 million
    cost = strategy.calculate(large_amount)
    assert cost == 50000.0, f"Expected 50000.0, got {cost}"

    strategy = ExpressFreight()
    cost = strategy.calculate(large_amount)
    assert cost == 100000.0, f"Expected 100000.0, got {cost}"

    print("[OK] Test Large Amounts: PASSED")


def test_furniture_order_with_express_technically_possible():
    """Test that FurnitureOrder can technically use ExpressFreight.

    Note: The business rule preventing this is enforced at the API level,
    not at the Order class level. This test verifies that the Order class
    itself doesn't prevent it (separation of concerns).
    """
    order = FurnitureOrder()
    order.amount = 500.0
    order.set_freight_strategy(ExpressFreight())

    # Technically possible, but business rule should prevent in API
    freight = order.calculate_freight()
    assert freight == 50.0, "Express freight should work technically"

    print("[OK] Test Furniture + Express (Technical): PASSED")


def test_order_initial_state():
    """Test order initial state (no amount, no strategy)."""
    order = ElectronicsOrder()

    assert order.amount == 0.0, "Initial amount should be 0.0"
    assert order.category == "Electronics", "Category should be set"

    try:
        order.calculate_freight()
        assert False, "Should raise error when strategy not set"
    except ValueError as e:
        assert "must be set" in str(e)

    print("[OK] Test Order Initial State: PASSED")


def test_furniture_order_category():
    """Test furniture order category."""
    order = FurnitureOrder()
    assert order.category == "Furniture"
    print("[OK] Test Furniture Order Category: PASSED")


def test_electronics_order_category():
    """Test electronics order category."""
    order = ElectronicsOrder()
    assert order.category == "Electronics"
    print("[OK] Test Electronics Order Category: PASSED")


def test_strategy_repr():
    """Test strategy string representation."""
    common = CommonFreight()
    express = ExpressFreight()
    
    assert "CommonFreight" in repr(common) or "Common" in repr(common)
    assert "ExpressFreight" in repr(express) or "Express" in repr(express)
    
    print("[OK] Test Strategy Repr: PASSED")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("RUNNING STRATEGY PATTERN TESTS")
    print("=" * 60 + "\n")

    try:
        test_common_freight_calculation()
        test_express_freight_calculation()
        test_electronics_order_with_common_freight()
        test_electronics_order_with_express_freight()
        test_furniture_order_with_common_freight()
        test_strategy_change_at_runtime()
        test_negative_amount_validation()
        test_missing_strategy_error()
        test_none_strategy_error()
        test_different_amounts()
        test_order_repr()
        test_freight_rate_constants()
        test_zero_amount()
        test_express_freight_different_amounts()
        test_furniture_order_repr()
        test_multiple_strategy_changes()
        test_decimal_precision()
        test_large_amounts()
        test_furniture_order_with_express_technically_possible()
        test_order_initial_state()
        test_furniture_order_category()
        test_electronics_order_category()
        test_strategy_repr()

        print("\n" + "=" * 60)
        print("ALL TESTS PASSED! [OK]")
        print("=" * 60 + "\n")

    except AssertionError as e:
        print(f"\n[ERROR] TEST FAILED: {e}\n")
    except Exception as e:
        print(f"\n[ERROR] ERROR: {e}\n")
        import traceback
        traceback.print_exc()
