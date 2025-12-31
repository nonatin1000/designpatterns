"""Unit tests for the Adapter pattern implementation."""

from billing import Billing
from adapters import PagFacilAdapter, TopPagamentosAdapter
from payment_gateways import PagFacil, TopPagamentos


def test_pag_facil_adapter():
    """Test that PagFacilAdapter correctly adapts PagFacil interface."""
    adapter = PagFacilAdapter()
    adapter.set_amount(100.00)
    adapter.set_installments(1)

    success = adapter.process()
    total = adapter.get_total_with_fees()

    # PagFacil: R$ 100 + R$ 0.40 (fixed) + R$ 5.00 (5% interest on 1x)
    expected_total = 100.00 + 0.40 + (100.00 * 0.05 * 1)
    assert success == True
    assert abs(total - expected_total) < 0.01
    print("[OK] Test PagFacil Adapter: PASSED")


def test_top_pagamentos_adapter():
    """Test that TopPagamentosAdapter correctly adapts TopPagamentos interface."""
    adapter = TopPagamentosAdapter()
    adapter.set_amount(100.00)
    adapter.set_installments(3)

    success = adapter.process()
    total = adapter.get_total_with_fees()

    # TopPagamentos: R$ 100 + R$ 5.00 (fixed) + R$ 3.00 (1% interest on 3x)
    expected_total = 100.00 + 5.00 + (100.00 * 0.01 * 3)
    assert success == True
    assert abs(total - expected_total) < 0.01
    print("[OK] Test TopPagamentos Adapter: PASSED")


def test_billing_selects_pag_facil_for_cash():
    """Test that Billing selects PagFacil for cash payments (1 installment)."""
    billing = Billing()
    result = billing.process_payment(100.00, 1)

    assert result["gateway"] == "PagFacil"
    assert result["installments"] == 1
    assert result["success"] == True
    print("[OK] Test Billing Selects PagFacil for Cash: PASSED")


def test_billing_selects_top_pagamentos_for_installments():
    """Test that Billing selects TopPagamentos for installment payments."""
    billing = Billing()
    result = billing.process_payment(100.00, 6)

    assert result["gateway"] == "TopPagamentos"
    assert result["installments"] == 6
    assert result["success"] == True
    print("[OK] Test Billing Selects TopPagamentos for Installments: PASSED")


def test_billing_calculates_fees_correctly():
    """Test that Billing correctly calculates fees."""
    billing = Billing()

    # Test with PagFacil (1 installment)
    result1 = billing.process_payment(100.00, 1)
    expected_fees1 = 0.40 + (100.00 * 0.05 * 1)  # Fixed + Interest
    assert abs(result1["fees"] - expected_fees1) < 0.01

    # Test with TopPagamentos (3 installments)
    result2 = billing.process_payment(100.00, 3)
    expected_fees2 = 5.00 + (100.00 * 0.01 * 3)  # Fixed + Interest
    assert abs(result2["fees"] - expected_fees2) < 0.01

    print("[OK] Test Billing Calculates Fees Correctly: PASSED")


def test_payment_history_tracking():
    """Test that Billing tracks payment history correctly."""
    billing = Billing()

    billing.process_payment(100.00, 1)
    billing.process_payment(200.00, 3)
    billing.process_payment(300.00, 6)

    history = billing.get_payment_history()

    assert len(history) == 3
    assert history[0]["amount"] == 100.00
    assert history[1]["amount"] == 200.00
    assert history[2]["amount"] == 300.00
    print("[OK] Test Payment History Tracking: PASSED")


def test_billing_statistics():
    """Test that Billing calculates statistics correctly."""
    billing = Billing()

    billing.process_payment(100.00, 1)
    billing.process_payment(200.00, 3)

    stats = billing.get_statistics()

    assert stats["total_payments"] == 2
    assert stats["total_amount"] == 300.00
    assert stats["total_fees"] > 0
    assert stats["avg_fee_percentage"] > 0
    print("[OK] Test Billing Statistics: PASSED")


def test_invalid_payment_amount():
    """Test that Billing rejects invalid payment amounts."""
    billing = Billing()

    try:
        billing.process_payment(0.00, 1)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "greater than zero" in str(e)
        print("[OK] Test Invalid Payment Amount: PASSED")


def test_invalid_installments():
    """Test that Billing rejects invalid installment values."""
    billing = Billing()

    try:
        billing.process_payment(100.00, 0)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "at least 1" in str(e)
        print("[OK] Test Invalid Installments: PASSED")


def test_pag_facil_original_interface():
    """Test that original PagFacil interface still works (Adaptee)."""
    pag_facil = PagFacil()
    pag_facil.define_valor(100.00)
    pag_facil.define_parcelas(1)

    success = pag_facil.processar_pagamento()
    total = pag_facil.calcular_total_com_taxas()

    assert success == True
    assert total > 100.00  # Should include fees
    print("[OK] Test PagFacil Original Interface: PASSED")


def test_top_pagamentos_original_interface():
    """Test that original TopPagamentos interface still works (Adaptee)."""
    top = TopPagamentos()
    top.set_value(100.00)
    top.set_installment_count(3)

    success = top.execute_transaction()
    total = top.calculate_final_amount()

    assert success == True
    assert total > 100.00  # Should include fees
    print("[OK] Test TopPagamentos Original Interface: PASSED")


def test_gateway_cost_comparison():
    """Test cost comparison between gateways for different scenarios."""
    # For 1 installment, PagFacil should be cheaper
    pf1 = PagFacilAdapter()
    pf1.set_amount(100.00)
    pf1.set_installments(1)
    pf1_total = pf1.get_total_with_fees()

    tp1 = TopPagamentosAdapter()
    tp1.set_amount(100.00)
    tp1.set_installments(1)
    tp1_total = tp1.get_total_with_fees()

    assert pf1_total < tp1_total, "PagFacil should be cheaper for cash"

    # For many installments, TopPagamentos should be cheaper
    pf12 = PagFacilAdapter()
    pf12.set_amount(100.00)
    pf12.set_installments(12)
    pf12_total = pf12.get_total_with_fees()

    tp12 = TopPagamentosAdapter()
    tp12.set_amount(100.00)
    tp12.set_installments(12)
    tp12_total = tp12.get_total_with_fees()

    assert tp12_total < pf12_total, "TopPagamentos should be cheaper for installments"
    print("[OK] Test Gateway Cost Comparison: PASSED")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("RUNNING ADAPTER PATTERN TESTS")
    print("=" * 60 + "\n")

    try:
        test_pag_facil_adapter()
        test_top_pagamentos_adapter()
        test_billing_selects_pag_facil_for_cash()
        test_billing_selects_top_pagamentos_for_installments()
        test_billing_calculates_fees_correctly()
        test_payment_history_tracking()
        test_billing_statistics()
        test_invalid_payment_amount()
        test_invalid_installments()
        test_pag_facil_original_interface()
        test_top_pagamentos_original_interface()
        test_gateway_cost_comparison()

        print("\n" + "=" * 60)
        print("ALL TESTS PASSED! [OK]")
        print("=" * 60 + "\n")
    except AssertionError as e:
        print(f"\n[ERROR] TEST FAILED: {e}\n")
    except Exception as e:
        print(f"\n[ERROR] ERROR: {e}\n")
