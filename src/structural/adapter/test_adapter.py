"""Comprehensive tests for Adapter pattern implementation."""

import sys
from pathlib import Path
from io import StringIO
from contextlib import redirect_stdout

# Add src directory to path for standalone execution
if __name__ == "__main__":
    src_dir = Path(__file__).parent.parent.parent
    sys.path.insert(0, str(src_dir))

try:
    # Try relative imports first (when used as module)
    from .gateway_interface import Gateway
    from .adapters import PagFacilAdapter, TopPagamentosAdapter
    from .payment_gateways import PagFacil, TopPagamentos
    from .billing import Billing
except ImportError:
    # Fall back to direct module imports
    import importlib.util
    import types
    test_dir = Path(__file__).parent
    
    # Create module structure
    structural = types.ModuleType("structural")
    structural_adapter = types.ModuleType("structural.adapter")
    sys.modules["structural"] = structural
    sys.modules["structural.adapter"] = structural_adapter
    
    # Load modules
    gateway_interface_spec = importlib.util.spec_from_file_location(
        "structural.adapter.gateway_interface",
        test_dir / "gateway_interface.py"
    )
    gateway_interface_module = importlib.util.module_from_spec(gateway_interface_spec)
    sys.modules["structural.adapter.gateway_interface"] = gateway_interface_module
    structural_adapter.gateway_interface = gateway_interface_module
    gateway_interface_spec.loader.exec_module(gateway_interface_module)
    
    payment_gateways_spec = importlib.util.spec_from_file_location(
        "structural.adapter.payment_gateways",
        test_dir / "payment_gateways.py"
    )
    payment_gateways_module = importlib.util.module_from_spec(payment_gateways_spec)
    sys.modules["structural.adapter.payment_gateways"] = payment_gateways_module
    structural_adapter.payment_gateways = payment_gateways_module
    payment_gateways_spec.loader.exec_module(payment_gateways_module)
    
    adapters_spec = importlib.util.spec_from_file_location(
        "structural.adapter.adapters",
        test_dir / "adapters.py"
    )
    adapters_module = importlib.util.module_from_spec(adapters_spec)
    sys.modules["structural.adapter.adapters"] = adapters_module
    structural_adapter.adapters = adapters_module
    adapters_spec.loader.exec_module(adapters_module)
    
    billing_spec = importlib.util.spec_from_file_location(
        "structural.adapter.billing",
        test_dir / "billing.py"
    )
    billing_module = importlib.util.module_from_spec(billing_spec)
    sys.modules["structural.adapter.billing"] = billing_module
    structural_adapter.billing = billing_module
    billing_spec.loader.exec_module(billing_module)
    
    # Extract classes
    Gateway = gateway_interface_module.Gateway
    PagFacilAdapter = adapters_module.PagFacilAdapter
    TopPagamentosAdapter = adapters_module.TopPagamentosAdapter
    PagFacil = payment_gateways_module.PagFacil
    TopPagamentos = payment_gateways_module.TopPagamentos
    Billing = billing_module.Billing


def test_pagfacil_adapter_set_amount():
    """Test PagFacilAdapter set_amount method."""
    adapter = PagFacilAdapter()
    adapter.set_amount(100.0)
    
    # Verify through get_total_with_fees
    total = adapter.get_total_with_fees()
    assert total > 100.0  # Should include fees
    
    print("[OK] Test PagFacilAdapter Set Amount: PASSED")


def test_pagfacil_adapter_set_installments():
    """Test PagFacilAdapter set_installments method."""
    adapter = PagFacilAdapter()
    adapter.set_amount(100.0)
    adapter.set_installments(3)
    
    total = adapter.get_total_with_fees()
    assert total > 100.0
    
    print("[OK] Test PagFacilAdapter Set Installments: PASSED")


def test_pagfacil_adapter_process():
    """Test PagFacilAdapter process method."""
    adapter = PagFacilAdapter()
    adapter.set_amount(100.0)
    adapter.set_installments(1)
    
    f = StringIO()
    with redirect_stdout(f):
        result = adapter.process()
    
    assert result is True
    output = f.getvalue()
    assert "PagFacil" in output or "Processing" in output
    
    print("[OK] Test PagFacilAdapter Process: PASSED")


def test_pagfacil_adapter_get_total_with_fees():
    """Test PagFacilAdapter fee calculation."""
    adapter = PagFacilAdapter()
    adapter.set_amount(100.0)
    adapter.set_installments(1)
    
    # 1 installment: 100 + 0.40 (fixed) + 100 * 0.05 * 1 (interest) = 105.40
    total = adapter.get_total_with_fees()
    expected = 100.0 + 0.40 + (100.0 * 0.05 * 1)
    assert abs(total - expected) < 0.01
    
    print("[OK] Test PagFacilAdapter Get Total With Fees: PASSED")


def test_pagfacil_adapter_multiple_installments():
    """Test PagFacilAdapter with multiple installments."""
    adapter = PagFacilAdapter()
    adapter.set_amount(100.0)
    adapter.set_installments(3)
    
    # 3 installments: 100 + 0.40 + 100 * 0.05 * 3 = 115.40
    total = adapter.get_total_with_fees()
    expected = 100.0 + 0.40 + (100.0 * 0.05 * 3)
    assert abs(total - expected) < 0.01
    
    print("[OK] Test PagFacilAdapter Multiple Installments: PASSED")


def test_toppagamentos_adapter_set_amount():
    """Test TopPagamentosAdapter set_amount method."""
    adapter = TopPagamentosAdapter()
    adapter.set_amount(100.0)
    
    total = adapter.get_total_with_fees()
    assert total > 100.0
    
    print("[OK] Test TopPagamentosAdapter Set Amount: PASSED")


def test_toppagamentos_adapter_set_installments():
    """Test TopPagamentosAdapter set_installments method."""
    adapter = TopPagamentosAdapter()
    adapter.set_amount(100.0)
    adapter.set_installments(3)
    
    total = adapter.get_total_with_fees()
    assert total > 100.0
    
    print("[OK] Test TopPagamentosAdapter Set Installments: PASSED")


def test_toppagamentos_adapter_process():
    """Test TopPagamentosAdapter process method."""
    adapter = TopPagamentosAdapter()
    adapter.set_amount(100.0)
    adapter.set_installments(1)
    
    f = StringIO()
    with redirect_stdout(f):
        result = adapter.process()
    
    assert result is True
    output = f.getvalue()
    assert "TopPagamentos" in output or "Executing" in output
    
    print("[OK] Test TopPagamentosAdapter Process: PASSED")


def test_toppagamentos_adapter_get_total_with_fees():
    """Test TopPagamentosAdapter fee calculation."""
    adapter = TopPagamentosAdapter()
    adapter.set_amount(100.0)
    adapter.set_installments(1)
    
    # 1 installment: 100 + 5.00 (fixed) + 100 * 0.01 * 1 (interest) = 106.00
    total = adapter.get_total_with_fees()
    expected = 100.0 + 5.00 + (100.0 * 0.01 * 1)
    assert abs(total - expected) < 0.01
    
    print("[OK] Test TopPagamentosAdapter Get Total With Fees: PASSED")


def test_toppagamentos_adapter_multiple_installments():
    """Test TopPagamentosAdapter with multiple installments."""
    adapter = TopPagamentosAdapter()
    adapter.set_amount(100.0)
    adapter.set_installments(6)
    
    # 6 installments: 100 + 5.00 + 100 * 0.01 * 6 = 111.00
    total = adapter.get_total_with_fees()
    expected = 100.0 + 5.00 + (100.0 * 0.01 * 6)
    assert abs(total - expected) < 0.01
    
    print("[OK] Test TopPagamentosAdapter Multiple Installments: PASSED")


def test_adapter_implements_gateway_interface():
    """Test that adapters implement Gateway interface."""
    pagfacil = PagFacilAdapter()
    toppagamentos = TopPagamentosAdapter()
    
    assert isinstance(pagfacil, Gateway)
    assert isinstance(toppagamentos, Gateway)
    
    print("[OK] Test Adapter Implements Gateway Interface: PASSED")


def test_billing_process_payment_single_installment():
    """Test Billing with single installment (uses PagFacil)."""
    billing = Billing()
    
    f = StringIO()
    with redirect_stdout(f):
        result = billing.process_payment(100.0, 1)
    
    assert result["gateway"] == "PagFacil"
    assert result["amount"] == 100.0
    assert result["installments"] == 1
    assert result["success"] is True
    assert result["total_with_fees"] > 100.0
    
    print("[OK] Test Billing Process Payment Single Installment: PASSED")


def test_billing_process_payment_multiple_installments():
    """Test Billing with multiple installments (uses TopPagamentos)."""
    billing = Billing()
    
    f = StringIO()
    with redirect_stdout(f):
        result = billing.process_payment(100.0, 6)
    
    assert result["gateway"] == "TopPagamentos"
    assert result["amount"] == 100.0
    assert result["installments"] == 6
    assert result["success"] is True
    assert result["total_with_fees"] > 100.0
    
    print("[OK] Test Billing Process Payment Multiple Installments: PASSED")


def test_billing_negative_amount_validation():
    """Test Billing validates negative amounts."""
    billing = Billing()
    
    try:
        billing.process_payment(-100.0, 1)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "greater than zero" in str(e).lower()
    
    print("[OK] Test Billing Negative Amount Validation: PASSED")


def test_billing_invalid_installments_validation():
    """Test Billing validates invalid installments."""
    billing = Billing()
    
    try:
        billing.process_payment(100.0, 0)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "at least 1" in str(e).lower()
    
    print("[OK] Test Billing Invalid Installments Validation: PASSED")


def test_billing_zero_amount_validation():
    """Test Billing validates zero amount."""
    billing = Billing()
    
    try:
        billing.process_payment(0.0, 1)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "greater than zero" in str(e).lower()
    
    print("[OK] Test Billing Zero Amount Validation: PASSED")


def test_billing_payment_history():
    """Test Billing payment history tracking."""
    billing = Billing()
    
    billing.process_payment(100.0, 1)
    billing.process_payment(200.0, 3)
    
    history = billing.get_payment_history()
    assert len(history) == 2
    assert history[0]["amount"] == 100.0
    assert history[1]["amount"] == 200.0
    
    print("[OK] Test Billing Payment History: PASSED")


def test_billing_get_payment_history_returns_copy():
    """Test that get_payment_history returns a copy."""
    billing = Billing()
    billing.process_payment(100.0, 1)
    
    history1 = billing.get_payment_history()
    history2 = billing.get_payment_history()
    
    assert history1 is not history2
    assert history1 == history2
    
    history1.append({"fake": "data"})
    assert len(billing.get_payment_history()) == 1
    
    print("[OK] Test Billing Get Payment History Returns Copy: PASSED")


def test_billing_calculate_total_fees():
    """Test Billing calculate_total_fees method."""
    billing = Billing()
    billing.process_payment(100.0, 1)
    billing.process_payment(200.0, 3)
    
    total_fees = billing.calculate_total_fees()
    assert total_fees > 0
    
    # Verify it's sum of fees
    history = billing.get_payment_history()
    expected_fees = sum(p["fees"] for p in history)
    assert abs(total_fees - expected_fees) < 0.01
    
    print("[OK] Test Billing Calculate Total Fees: PASSED")


def test_billing_get_statistics():
    """Test Billing get_statistics method."""
    billing = Billing()
    billing.process_payment(100.0, 1)
    billing.process_payment(200.0, 3)
    
    stats = billing.get_statistics()
    assert stats["total_payments"] == 2
    assert stats["total_amount"] == 300.0
    assert stats["total_fees"] > 0
    assert stats["avg_fee_percentage"] > 0
    
    print("[OK] Test Billing Get Statistics: PASSED")


def test_billing_statistics_empty():
    """Test Billing statistics with no payments."""
    billing = Billing()
    
    stats = billing.get_statistics()
    assert stats["total_payments"] == 0
    assert stats["total_amount"] == 0.0
    assert stats["total_fees"] == 0.0
    assert stats["avg_fee_percentage"] == 0.0
    
    print("[OK] Test Billing Statistics Empty: PASSED")


def test_pagfacil_zero_amount_fails():
    """Test PagFacil adapter with zero amount fails."""
    adapter = PagFacilAdapter()
    adapter.set_amount(0.0)
    adapter.set_installments(1)
    
    result = adapter.process()
    assert result is False
    
    print("[OK] Test PagFacil Zero Amount Fails: PASSED")


def test_toppagamentos_zero_amount_fails():
    """Test TopPagamentos adapter with zero amount fails."""
    adapter = TopPagamentosAdapter()
    adapter.set_amount(0.0)
    adapter.set_installments(1)
    
    result = adapter.process()
    assert result is False
    
    print("[OK] Test TopPagamentos Zero Amount Fails: PASSED")


def test_gateway_selection_strategy():
    """Test that Billing selects correct gateway based on installments."""
    billing = Billing()
    
    # 1 installment -> PagFacil
    result1 = billing.process_payment(100.0, 1)
    assert result1["gateway"] == "PagFacil"
    
    # 2+ installments -> TopPagamentos
    result2 = billing.process_payment(100.0, 2)
    assert result2["gateway"] == "TopPagamentos"
    
    result3 = billing.process_payment(100.0, 12)
    assert result3["gateway"] == "TopPagamentos"
    
    print("[OK] Test Gateway Selection Strategy: PASSED")


def test_adapter_fee_comparison():
    """Test fee comparison between adapters."""
    pagfacil = PagFacilAdapter()
    toppagamentos = TopPagamentosAdapter()
    
    amount = 100.0
    
    # Single installment - PagFacil should be cheaper
    pagfacil.set_amount(amount)
    pagfacil.set_installments(1)
    pagfacil_total = pagfacil.get_total_with_fees()
    
    toppagamentos.set_amount(amount)
    toppagamentos.set_installments(1)
    toppagamentos_total = toppagamentos.get_total_with_fees()
    
    assert pagfacil_total < toppagamentos_total
    
    # Multiple installments - TopPagamentos should be cheaper
    pagfacil.set_installments(6)
    pagfacil_total = pagfacil.get_total_with_fees()
    
    toppagamentos.set_installments(6)
    toppagamentos_total = toppagamentos.get_total_with_fees()
    
    assert toppagamentos_total < pagfacil_total
    
    print("[OK] Test Adapter Fee Comparison: PASSED")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("RUNNING ADAPTER PATTERN TESTS")
    print("=" * 60 + "\n")

    try:
        test_pagfacil_adapter_set_amount()
        test_pagfacil_adapter_set_installments()
        test_pagfacil_adapter_process()
        test_pagfacil_adapter_get_total_with_fees()
        test_pagfacil_adapter_multiple_installments()
        test_toppagamentos_adapter_set_amount()
        test_toppagamentos_adapter_set_installments()
        test_toppagamentos_adapter_process()
        test_toppagamentos_adapter_get_total_with_fees()
        test_toppagamentos_adapter_multiple_installments()
        test_adapter_implements_gateway_interface()
        test_billing_process_payment_single_installment()
        test_billing_process_payment_multiple_installments()
        test_billing_negative_amount_validation()
        test_billing_invalid_installments_validation()
        test_billing_zero_amount_validation()
        test_billing_payment_history()
        test_billing_get_payment_history_returns_copy()
        test_billing_calculate_total_fees()
        test_billing_get_statistics()
        test_billing_statistics_empty()
        test_pagfacil_zero_amount_fails()
        test_toppagamentos_zero_amount_fails()
        test_gateway_selection_strategy()
        test_adapter_fee_comparison()

        print("\n" + "=" * 60)
        print("ALL TESTS PASSED! [OK]")
        print("=" * 60 + "\n")

    except AssertionError as e:
        print(f"\n[ERROR] TEST FAILED: {e}\n")
        import traceback
        traceback.print_exc()
    except Exception as e:
        print(f"\n[ERROR] ERROR: {e}\n")
        import traceback
        traceback.print_exc()

