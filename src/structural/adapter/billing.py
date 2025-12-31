"""Billing system (Client) that uses payment gateways through the Gateway interface.

The Billing class doesn't know about specific payment gateway implementations.
It only works with the Gateway interface, allowing any adapted gateway to be used.
"""

from gateway_interface import Gateway
from adapters import PagFacilAdapter, TopPagamentosAdapter
from typing import List, Dict


class Billing:
    """Billing system that processes payments using different gateways.

    This class demonstrates the Adapter pattern in action. It selects the most
    cost-effective payment gateway based on the number of installments:
    - 1 installment (cash): Uses PagFacil (low fixed fee)
    - 2+ installments: Uses TopPagamentos (low interest rate)
    """

    def __init__(self):
        """Initialize the billing system."""
        self._payment_history: List[Dict] = []

    def process_payment(self, amount: float, installments: int = 1) -> Dict:
        """Process a payment using the most cost-effective gateway.

        Args:
            amount: Payment amount in BRL
            installments: Number of monthly installments (default: 1 for cash)

        Returns:
            Dictionary with payment details including gateway used and total cost

        Raises:
            ValueError: If amount is invalid or payment processing fails
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

        Strategy:
        - 1 installment: PagFacil (R$ 0.40 fixed, 5% interest)
        - 2+ installments: TopPagamentos (R$ 5.00 fixed, 1% interest)

        Args:
            installments: Number of installments

        Returns:
            The selected Gateway adapter instance
        """
        if installments == 1:
            return PagFacilAdapter()
        else:
            return TopPagamentosAdapter()

    def get_payment_history(self) -> List[Dict]:
        """Get the complete payment history.

        Returns:
            List of all processed payments
        """
        return self._payment_history.copy()

    def calculate_total_fees(self) -> float:
        """Calculate total fees paid across all transactions.

        Returns:
            Sum of all processing fees
        """
        return sum(payment["fees"] for payment in self._payment_history)

    def get_statistics(self) -> Dict:
        """Get billing statistics.

        Returns:
            Dictionary with statistics including total processed, fees, etc.
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
