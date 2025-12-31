"""Gateway interface (Target) for payment processing.

This is the target interface that the client (Billing) expects to work with.
All payment gateways must be adapted to this interface.
"""

from abc import ABC, abstractmethod


class Gateway(ABC):
    """Abstract payment gateway interface.

    This interface defines the standard contract for all payment gateways.
    Third-party payment services will be adapted to this interface.
    """

    @abstractmethod
    def set_amount(self, amount: float) -> None:
        """Set the payment amount.

        Args:
            amount: The total payment amount in Brazilian Reais (BRL)
        """
        pass

    @abstractmethod
    def set_installments(self, installments: int) -> None:
        """Set the number of installments for the payment.

        Args:
            installments: Number of monthly installments (1 for cash payment)
        """
        pass

    @abstractmethod
    def process(self) -> bool:
        """Process the payment transaction.

        Returns:
            True if payment was processed successfully, False otherwise
        """
        pass

    @abstractmethod
    def get_total_with_fees(self) -> float:
        """Calculate total amount including all fees.

        Returns:
            Total amount with processing fees and interest
        """
        pass
