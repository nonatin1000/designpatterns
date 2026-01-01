"""Billing system (Client) that uses payment gateways through Gateway interface.

The Billing class demonstrates the Adapter pattern in action. It doesn't know
about specific payment gateway implementations - it only works with the
Gateway interface, allowing any adapted gateway to be used transparently.

This is the Client in the Adapter pattern - it depends on the Target interface
(Gateway) and doesn't need to know about the Adaptees (PagFacil, TopPagamentos)
or the Adapters that bridge them.
"""

from .gateway_interface import Gateway
from .adapters import PagFacilAdapter, TopPagamentosAdapter
from typing import List, Dict, Any


class Billing:
    """Billing system (Client) that processes payments using different gateways.

    This class demonstrates the Adapter pattern in action. It works exclusively
    with the Gateway interface, not knowing about specific gateway implementations.
    The adapters handle the translation between the Gateway interface and the
    actual gateway services.

    Gateway Selection Strategy:
    - 1 installment (cash): Uses PagFacil (R$ 0.40 fixed fee, 5% interest)
    - 2+ installments: Uses TopPagamentos (R$ 5.00 fixed fee, 1% interest)

    The selection is based on cost-effectiveness - PagFacil is better for cash
    payments due to low fixed fee, while TopPagamentos is better for installments
    due to low interest rate.
    """

    def __init__(self) -> None:
        """Initialize the billing system.

        Creates a new billing instance with an empty payment history.
        """
        self._payment_history: List[Dict[str, Any]] = []

    def process_payment(
        self, amount: float, installments: int = 1
    ) -> Dict[str, Any]:
        """Process a payment using the most cost-effective gateway.

        This method automatically selects the best gateway based on the number
        of installments, configures it, processes the payment, and records
        the transaction in the payment history.

        Args:
            amount: Payment amount in BRL. Must be greater than zero.
            installments: Number of monthly installments. Default is 1 (cash).
                Must be at least 1.

        Returns:
            Dictionary containing:
            - amount: Original payment amount
            - installments: Number of installments
            - gateway: Name of gateway used (PagFacil or TopPagamentos)
            - total_with_fees: Total amount including all fees
            - fees: Total fees charged (fixed fee + interest)
            - success: Whether payment was processed successfully

        Raises:
            ValueError: If amount is invalid (<= 0) or installments is
                invalid (< 1), or if payment processing fails.

        Example:
            >>> billing = Billing()
            >>> result = billing.process_payment(100.00, 1)
            >>> result['gateway']
            'PagFacil'
            >>> result = billing.process_payment(100.00, 6)
            >>> result['gateway']
            'TopPagamentos'
        """
        if amount <= 0:
            raise ValueError("Payment amount must be greater than zero")

        if installments < 1:
            raise ValueError("Number of installments must be at least 1")

        # Select best gateway based on installments
        gateway = self._select_best_gateway(installments)
        gateway_name = gateway.__class__.__name__.replace("Adapter", "")

        # Configure and process payment
        gateway.set_amount(amount)
        gateway.set_installments(installments)

        success = gateway.process()

        if not success:
            raise ValueError("Payment processing failed")

        total_with_fees = gateway.get_total_with_fees()

        # Record payment in history
        payment_record = {
            "amount": amount,
            "installments": installments,
            "gateway": gateway_name,
            "total_with_fees": total_with_fees,
            "fees": total_with_fees - amount,
            "success": success
        }

        self._payment_history.append(payment_record)

        return payment_record

    def _select_best_gateway(self, installments: int) -> Gateway:
        """Select the most cost-effective payment gateway.

        This private method implements the gateway selection strategy based
        on the number of installments. The strategy optimizes for lowest
        total cost (fixed fee + interest).

        Strategy:
        - 1 installment: PagFacil (R$ 0.40 fixed fee, 5% interest/month)
          Best for cash payments due to low fixed fee.
        - 2+ installments: TopPagamentos (R$ 5.00 fixed fee, 1% interest/month)
          Best for installments due to low interest rate.

        Args:
            installments: Number of monthly installments.

        Returns:
            A Gateway adapter instance (PagFacilAdapter or TopPagamentosAdapter).

        Note:
            This method creates a new adapter instance for each payment.
            In a production system, you might want to reuse adapter instances
            or use a factory pattern.
        """
        if installments == 1:
            return PagFacilAdapter()
        else:
            return TopPagamentosAdapter()

    def get_payment_history(self) -> List[Dict[str, Any]]:
        """Get the complete payment history.

        Returns a copy of the payment history to prevent external modification.

        Returns:
            List of all processed payment records. Each record contains:
            - amount: Original payment amount
            - installments: Number of installments
            - gateway: Gateway used
            - total_with_fees: Total amount with fees
            - fees: Fees charged
            - success: Payment success status
        """
        return self._payment_history.copy()

    def calculate_total_fees(self) -> float:
        """Calculate total fees paid across all transactions.

        Returns:
            Sum of all processing fees (fixed fees + interest) from all
            processed payments in BRL.
        """
        return sum(payment["fees"] for payment in self._payment_history)

    def get_statistics(self) -> Dict[str, Any]:
        """Get billing statistics and aggregated metrics.

        Calculates aggregate statistics from all processed payments including
        totals, averages, and counts.

        Returns:
            Dictionary containing:
            - total_payments: Total number of payments processed
            - total_amount: Sum of all payment amounts (without fees)
            - total_fees: Sum of all fees charged
            - avg_fee_percentage: Average fee percentage across all payments

        Note:
            Returns zeros for all metrics if no payments have been processed.
        """
        total_payments = len(self._payment_history)

        if total_payments == 0:
            return {
                "total_payments": 0,
                "total_amount": 0.0,
                "total_fees": 0.0,
                "avg_fee_percentage": 0.0
            }

        total_amount = sum(p["amount"] for p in self._payment_history)
        total_fees = self.calculate_total_fees()
        avg_fee_percentage = (total_fees / total_amount * 100) if total_amount > 0 else 0

        return {
            "total_payments": total_payments,
            "total_amount": total_amount,
            "total_fees": total_fees,
            "avg_fee_percentage": round(avg_fee_percentage, 2)
        }
