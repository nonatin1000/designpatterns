"""Comprehensive tests for Template Method pattern implementation."""

import sys
from pathlib import Path
import importlib.util

# Add src directory to path for standalone execution
if __name__ == "__main__":
    src_dir = Path(__file__).parent.parent.parent
    sys.path.insert(0, str(src_dir))

try:
    # Try relative imports first (when used as module)
    from .payment import (
        Payment,
        CreditPayment,
        DebitPayment,
        CashPayment
    )
    from .gateway import Gateway
except ImportError:
    # Fall back to direct module imports (bypassing __init__.py)
    # This avoids importing schemas.py which requires pydantic
    test_dir = Path(__file__).parent
    
    # Load payment module directly
    payment_spec = importlib.util.spec_from_file_location(
        "payment",
        test_dir / "payment.py"
    )
    payment_module = importlib.util.module_from_spec(payment_spec)
    payment_spec.loader.exec_module(payment_module)
    
    # Load gateway module directly
    gateway_spec = importlib.util.spec_from_file_location(
        "gateway",
        test_dir / "gateway.py"
    )
    gateway_module = importlib.util.module_from_spec(gateway_spec)
    gateway_spec.loader.exec_module(gateway_module)
    
    # Extract classes
    Payment = payment_module.Payment
    CreditPayment = payment_module.CreditPayment
    DebitPayment = payment_module.DebitPayment
    CashPayment = payment_module.CashPayment
    Gateway = gateway_module.Gateway


def test_credit_payment_tax():
    """Test credit payment tax calculation."""
    gateway = Gateway()
    payment = CreditPayment(amount=1000.0, gateway=gateway)
    tax = payment.calculate_tax()
    assert tax == 50.0, f"Expected 50.0, got {tax}"
    print("[OK] Test Credit Payment Tax: PASSED")


def test_credit_payment_discount_above_threshold():
    """Test credit payment discount for amounts > R$ 300."""
    gateway = Gateway()
    payment = CreditPayment(amount=1000.0, gateway=gateway)
    discount = payment.calculate_discount()
    assert discount == 20.0, f"Expected 20.0, got {discount}"
    print("[OK] Test Credit Payment Discount (> R$ 300): PASSED")


def test_credit_payment_discount_below_threshold():
    """Test credit payment discount for amounts <= R$ 300."""
    gateway = Gateway()
    payment = CreditPayment(amount=250.0, gateway=gateway)
    discount = payment.calculate_discount()
    assert discount == 0.0, f"Expected 0.0, got {discount}"
    print("[OK] Test Credit Payment Discount (<= R$ 300): PASSED")


def test_debit_payment_tax():
    """Test debit payment fixed tax."""
    gateway = Gateway()
    payment = DebitPayment(amount=1000.0, gateway=gateway)
    tax = payment.calculate_tax()
    assert tax == 4.0, f"Expected 4.0, got {tax}"
    print("[OK] Test Debit Payment Tax: PASSED")


def test_debit_payment_discount():
    """Test debit payment discount calculation."""
    gateway = Gateway()
    payment = DebitPayment(amount=1000.0, gateway=gateway)
    discount = payment.calculate_discount()
    assert discount == 50.0, f"Expected 50.0, got {discount}"
    print("[OK] Test Debit Payment Discount: PASSED")


def test_cash_payment_tax():
    """Test cash payment has no tax (uses hook default)."""
    gateway = Gateway()
    payment = CashPayment(amount=1000.0, gateway=gateway)
    tax = payment.calculate_tax()
    assert tax == 0.0, f"Expected 0.0, got {tax}"
    print("[OK] Test Cash Payment Tax (Hook): PASSED")


def test_cash_payment_discount():
    """Test cash payment discount calculation."""
    gateway = Gateway()
    payment = CashPayment(amount=1000.0, gateway=gateway)
    discount = payment.calculate_discount()
    assert discount == 100.0, f"Expected 100.0, got {discount}"
    print("[OK] Test Cash Payment Discount: PASSED")


def test_process_payment_template_method():
    """Test the template method process_payment."""
    gateway = Gateway()
    payment = CreditPayment(amount=1000.0, gateway=gateway)

    success, final_amount = payment.process_payment()

    # final_amount should be: 1000 + 50 (tax) - 20 (discount) = 1030
    assert final_amount == 1030.0, f"Expected 1030.0, got {final_amount}"
    assert isinstance(success, bool), "Success should be boolean"
    print("[OK] Test Process Payment Template Method: PASSED")


def test_negative_amount_validation():
    """Test that negative amounts raise ValueError."""
    gateway = Gateway()

    try:
        payment = CreditPayment(amount=-100.0, gateway=gateway)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "cannot be negative" in str(e)
        print("[OK] Test Negative Amount Validation: PASSED")


def test_amount_property_getter():
    """Test amount property getter."""
    gateway = Gateway()
    payment = CreditPayment(amount=500.0, gateway=gateway)

    assert payment.amount == 500.0
    print("[OK] Test Amount Property Getter: PASSED")


def test_amount_property_setter():
    """Test amount property setter."""
    gateway = Gateway()
    payment = CreditPayment(amount=500.0, gateway=gateway)

    payment.amount = 750.0
    assert payment.amount == 750.0
    print("[OK] Test Amount Property Setter: PASSED")


def test_amount_setter_validation():
    """Test that setting negative amount raises ValueError."""
    gateway = Gateway()
    payment = CreditPayment(amount=500.0, gateway=gateway)

    try:
        payment.amount = -200.0
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "cannot be negative" in str(e)
        print("[OK] Test Amount Setter Validation: PASSED")


def test_payment_repr():
    """Test payment string representation."""
    gateway = Gateway()
    payment = CreditPayment(amount=1000.0, gateway=gateway)

    repr_str = repr(payment)
    assert "CreditPayment" in repr_str
    assert "1000.00" in repr_str
    assert "Gateway" in repr_str
    print("[OK] Test Payment Representation: PASSED")


def test_different_amounts_credit():
    """Test credit payment with various amounts."""
    gateway = Gateway()

    test_cases = [
        (100.0, 5.0, 0.0),    # Below threshold: no discount
        (300.0, 15.0, 0.0),   # At threshold: no discount
        (500.0, 25.0, 10.0),  # Above threshold: 2% discount
        (1000.0, 50.0, 20.0), # Above threshold: 2% discount
    ]

    for amount, expected_tax, expected_discount in test_cases:
        payment = CreditPayment(amount=amount, gateway=gateway)
        assert payment.calculate_tax() == expected_tax
        assert payment.calculate_discount() == expected_discount

    print("[OK] Test Different Amounts Credit: PASSED")


def test_payment_constants():
    """Test that payment classes use correct constants."""
    # Credit constants
    assert CreditPayment.TAX_RATE == 0.05
    assert CreditPayment.DISCOUNT_RATE == 0.02
    assert CreditPayment.DISCOUNT_THRESHOLD == 300.0

    # Debit constants
    assert DebitPayment.TAX_AMOUNT == 4.0
    assert DebitPayment.DISCOUNT_RATE == 0.05

    # Cash constants
    assert CashPayment.DISCOUNT_RATE == 0.10

    print("[OK] Test Payment Constants: PASSED")


def test_best_payment_option():
    """Test which payment option is best for different amounts."""
    gateway = Gateway()
    amount = 1000.0

    # Calculate final amounts
    credit = CreditPayment(amount, gateway)
    _, credit_final = credit.process_payment()

    debit = DebitPayment(amount, gateway)
    _, debit_final = debit.process_payment()

    cash = CashPayment(amount, gateway)
    _, cash_final = cash.process_payment()

    # Cash should be the best option (lowest final amount)
    assert cash_final < credit_final
    assert cash_final < debit_final

    print("[OK] Test Best Payment Option: PASSED")


def test_gateway_charge_returns_boolean():
    """Test that gateway charge returns boolean."""
    gateway = Gateway()
    result = gateway.charge(100.0)

    assert isinstance(result, bool), "Gateway charge should return boolean"
    print("[OK] Test Gateway Charge Returns Boolean: PASSED")


def test_gateway_repr():
    """Test gateway string representation."""
    gateway = Gateway()
    repr_str = repr(gateway)
    assert "Gateway" in repr_str
    print("[OK] Test Gateway Repr: PASSED")


def test_zero_amount_payment():
    """Test payment with zero amount."""
    gateway = Gateway()
    
    credit = CreditPayment(amount=0.0, gateway=gateway)
    assert credit.amount == 0.0
    assert credit.calculate_tax() == 0.0
    assert credit.calculate_discount() == 0.0
    
    debit = DebitPayment(amount=0.0, gateway=gateway)
    assert debit.calculate_tax() == 4.0  # Fixed tax
    assert debit.calculate_discount() == 0.0
    
    cash = CashPayment(amount=0.0, gateway=gateway)
    assert cash.calculate_tax() == 0.0
    assert cash.calculate_discount() == 0.0
    
    print("[OK] Test Zero Amount Payment: PASSED")


def test_different_amounts_debit():
    """Test debit payment with various amounts."""
    gateway = Gateway()
    
    test_cases = [
        (100.0, 4.0, 5.0),    # Fixed tax R$ 4, 5% discount
        (500.0, 4.0, 25.0),   # Fixed tax R$ 4, 5% discount
        (1000.0, 4.0, 50.0),  # Fixed tax R$ 4, 5% discount
    ]
    
    for amount, expected_tax, expected_discount in test_cases:
        payment = DebitPayment(amount=amount, gateway=gateway)
        assert payment.calculate_tax() == expected_tax
        assert payment.calculate_discount() == expected_discount
    
    print("[OK] Test Different Amounts Debit: PASSED")


def test_different_amounts_cash():
    """Test cash payment with various amounts."""
    gateway = Gateway()
    
    test_cases = [
        (100.0, 0.0, 10.0),   # No tax, 10% discount
        (500.0, 0.0, 50.0),   # No tax, 10% discount
        (1000.0, 0.0, 100.0), # No tax, 10% discount
    ]
    
    for amount, expected_tax, expected_discount in test_cases:
        payment = CashPayment(amount=amount, gateway=gateway)
        assert payment.calculate_tax() == expected_tax
        assert payment.calculate_discount() == expected_discount
    
    print("[OK] Test Different Amounts Cash: PASSED")


def test_large_amount_payment():
    """Test payment with very large amount."""
    gateway = Gateway()
    large_amount = 1000000.0  # 1 million
    
    credit = CreditPayment(amount=large_amount, gateway=gateway)
    tax = credit.calculate_tax()
    discount = credit.calculate_discount()
    
    assert tax == 50000.0  # 5% of 1 million
    assert discount == 20000.0  # 2% of 1 million
    
    success, final = credit.process_payment()
    assert isinstance(success, bool)
    assert final == 1030000.0  # 1M + 50K - 20K
    
    print("[OK] Test Large Amount Payment: PASSED")


def test_credit_payment_at_threshold():
    """Test credit payment exactly at discount threshold."""
    gateway = Gateway()
    
    # Exactly at threshold (R$ 300) - should NOT get discount
    payment = CreditPayment(amount=300.0, gateway=gateway)
    assert payment.calculate_discount() == 0.0
    
    # Just above threshold (R$ 300.01) - should get discount
    payment2 = CreditPayment(amount=300.01, gateway=gateway)
    assert payment2.calculate_discount() > 0.0
    
    print("[OK] Test Credit Payment At Threshold: PASSED")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("RUNNING TEMPLATE METHOD PATTERN TESTS")
    print("=" * 60 + "\n")

    try:
        test_credit_payment_tax()
        test_credit_payment_discount_above_threshold()
        test_credit_payment_discount_below_threshold()
        test_debit_payment_tax()
        test_debit_payment_discount()
        test_cash_payment_tax()
        test_cash_payment_discount()
        test_process_payment_template_method()
        test_negative_amount_validation()
        test_amount_property_getter()
        test_amount_property_setter()
        test_amount_setter_validation()
        test_payment_repr()
        test_different_amounts_credit()
        test_payment_constants()
        test_best_payment_option()
        test_gateway_charge_returns_boolean()
        test_gateway_repr()
        test_zero_amount_payment()
        test_different_amounts_debit()
        test_different_amounts_cash()
        test_large_amount_payment()
        test_credit_payment_at_threshold()

        print("\n" + "=" * 60)
        print("ALL TESTS PASSED! [OK]")
        print("=" * 60 + "\n")

    except AssertionError as e:
        print(f"\n[ERROR] TEST FAILED: {e}\n")
    except Exception as e:
        print(f"\n[ERROR] ERROR: {e}\n")
        import traceback
        traceback.print_exc()
