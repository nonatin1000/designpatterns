"""Examples demonstrating the Adapter pattern with payment gateways.

These examples show how the Adapter pattern allows different payment gateway
interfaces to work seamlessly through a common interface.
"""

from billing import Billing
from adapters import PagFacilAdapter, TopPagamentosAdapter


def example_cash_payment():
    """Example 1: Cash payment (1 installment) - Uses PagFacil."""
    print("\n" + "=" * 80)
    print("EXAMPLE 1: Cash Payment (1 Installment)")
    print("=" * 80)

    billing = Billing()

    print("\nProcessing R$ 100.00 cash payment...")
    result = billing.process_payment(amount=100.00, installments=1)

    print(f"\n[OK] Payment processed successfully!")
    print(f"Gateway used: {result['gateway']}")
    print(f"Original amount: R$ {result['amount']:.2f}")
    print(f"Total with fees: R$ {result['total_with_fees']:.2f}")
    print(f"Fees charged: R$ {result['fees']:.2f}")
    print()


def example_installment_payment():
    """Example 2: Installment payment (6x) - Uses TopPagamentos."""
    print("\n" + "=" * 80)
    print("EXAMPLE 2: Installment Payment (6 Installments)")
    print("=" * 80)

    billing = Billing()

    print("\nProcessing R$ 600.00 in 6 installments...")
    result = billing.process_payment(amount=600.00, installments=6)

    print(f"\n[OK] Payment processed successfully!")
    print(f"Gateway used: {result['gateway']}")
    print(f"Original amount: R$ {result['amount']:.2f}")
    print(f"Total with fees: R$ {result['total_with_fees']:.2f}")
    print(f"Fees charged: R$ {result['fees']:.2f}")
    print(f"Per installment: R$ {result['total_with_fees'] / result['installments']:.2f}")
    print()


def example_direct_adapter_usage():
    """Example 3: Using adapters directly (bypassing automatic selection)."""
    print("\n" + "=" * 80)
    print("EXAMPLE 3: Direct Adapter Usage")
    print("=" * 80)

    print("\nComparing both gateways for R$ 200.00 in 3 installments:\n")

    # Using PagFacil directly
    print("--- PagFacil Adapter ---")
    pag_facil = PagFacilAdapter()
    pag_facil.set_amount(200.00)
    pag_facil.set_installments(3)
    pag_facil.process()
    pag_facil_total = pag_facil.get_total_with_fees()
    print(f"Total with fees: R$ {pag_facil_total:.2f}")
    print(f"Fees: R$ {pag_facil_total - 200.00:.2f}\n")

    # Using TopPagamentos directly
    print("--- TopPagamentos Adapter ---")
    top = TopPagamentosAdapter()
    top.set_amount(200.00)
    top.set_installments(3)
    top.process()
    top_total = top.get_total_with_fees()
    print(f"Total with fees: R$ {top_total:.2f}")
    print(f"Fees: R$ {top_total - 200.00:.2f}\n")

    # Show best option
    if pag_facil_total < top_total:
        print(f"[OK] Best option: PagFacil (saves R$ {top_total - pag_facil_total:.2f})")
    else:
        print(f"[OK] Best option: TopPagamentos (saves R$ {pag_facil_total - top_total:.2f})")
    print()


def example_multiple_payments():
    """Example 4: Processing multiple payments with automatic gateway selection."""
    print("\n" + "=" * 80)
    print("EXAMPLE 4: Multiple Payments with Statistics")
    print("=" * 80)

    billing = Billing()

    payments = [
        (50.00, 1),    # Cash
        (150.00, 3),   # 3x
        (300.00, 6),   # 6x
        (100.00, 1),   # Cash
        (500.00, 12),  # 12x
    ]

    print("\nProcessing 5 different payments...\n")

    for idx, (amount, installments) in enumerate(payments, 1):
        result = billing.process_payment(amount, installments)
        print(f"{idx}. R$ {amount:.2f} in {installments}x -> "
              f"{result['gateway']} -> Total: R$ {result['total_with_fees']:.2f}")

    # Show statistics
    stats = billing.get_statistics()
    print(f"\n--- Statistics ---")
    print(f"Total payments: {stats['total_payments']}")
    print(f"Total amount: R$ {stats['total_amount']:.2f}")
    print(f"Total fees: R$ {stats['total_fees']:.2f}")
    print(f"Average fee: {stats['avg_fee_percentage']:.2f}%")
    print()


def example_payment_history():
    """Example 5: Viewing payment history."""
    print("\n" + "=" * 80)
    print("EXAMPLE 5: Payment History Tracking")
    print("=" * 80)

    billing = Billing()

    # Process some payments
    billing.process_payment(100.00, 1)
    billing.process_payment(200.00, 4)
    billing.process_payment(300.00, 1)

    print("\nPayment History:\n")
    history = billing.get_payment_history()

    for idx, payment in enumerate(history, 1):
        print(f"Payment #{idx}:")
        print(f"  Amount: R$ {payment['amount']:.2f}")
        print(f"  Installments: {payment['installments']}x")
        print(f"  Gateway: {payment['gateway']}")
        print(f"  Total: R$ {payment['total_with_fees']:.2f}")
        print(f"  Fees: R$ {payment['fees']:.2f}\n")


def example_cost_analysis():
    """Example 6: Cost analysis - when each gateway is better."""
    print("\n" + "=" * 80)
    print("EXAMPLE 6: Cost Analysis - Gateway Comparison")
    print("=" * 80)

    print("\nAnalyzing costs for R$ 100.00 with different installments:\n")
    print("Installments | PagFacil     | TopPagamentos | Best Choice")
    print("-" * 65)

    for installments in [1, 2, 3, 6, 12]:
        # PagFacil calculation
        pf = PagFacilAdapter()
        pf.set_amount(100.00)
        pf.set_installments(installments)
        pf_total = pf.get_total_with_fees()

        # TopPagamentos calculation
        tp = TopPagamentosAdapter()
        tp.set_amount(100.00)
        tp.set_installments(installments)
        tp_total = tp.get_total_with_fees()

        best = "PagFacil" if pf_total < tp_total else "TopPagamentos"
        savings = abs(pf_total - tp_total)

        print(f"{installments:^12} | R$ {pf_total:>8.2f} | R$ {tp_total:>10.2f}  | "
              f"{best} (saves R$ {savings:.2f})")

    print()


if __name__ == "__main__":
    print("\n")
    print("=" * 80)
    print(" " * 25 + "ADAPTER PATTERN - EXAMPLES")
    print(" " * 20 + "Payment Gateway Integration System")
    print("=" * 80)

    example_cash_payment()
    example_installment_payment()
    example_direct_adapter_usage()
    example_multiple_payments()
    example_payment_history()
    example_cost_analysis()

    print("=" * 80)
    print("To test the API: python main.py")
    print("Access: http://localhost:8000/docs")
    print("=" * 80 + "\n")
