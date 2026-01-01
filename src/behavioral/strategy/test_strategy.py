"""Comprehensive tests for Strategy pattern implementation."""

from .freight_strategy import CommonFreight, ExpressFreight
from .order import ElectronicsOrder, FurnitureOrder


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
        assert result == expected, f"For {amount}, expected {expected}, got {result}"

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

        print("\n" + "=" * 60)
        print("ALL TESTS PASSED! [OK]")
        print("=" * 60 + "\n")

    except AssertionError as e:
        print(f"\n[ERROR] TEST FAILED: {e}\n")
    except Exception as e:
        print(f"\n[ERROR] ERROR: {e}\n")
        import traceback
        traceback.print_exc()
