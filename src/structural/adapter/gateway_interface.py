"""Gateway interface (Target) for payment processing.

This module defines the target interface that the client (Billing) expects
to work with. All payment gateways must be adapted to this interface.

The Adapter pattern allows incompatible interfaces to work together by
creating adapters that translate between the target interface and the
adaptee's interface.
"""

from abc import ABC, abstractmethod


class Gateway(ABC):
    """Abstract payment gateway interface (Target).

    This interface defines the standard contract for all payment gateways
    in the system. Third-party payment services with incompatible interfaces
    will be adapted to this interface using adapter classes.

    The Adapter pattern enables the system to work with multiple payment
    gateways without modifying the client code (Billing class).
    """

    @abstractmethod
    def set_amount(self, amount: float) -> None:
        """Set the payment amount.

        Args:
            amount: The total payment amount in Brazilian Reais (BRL).
                Must be greater than zero.

        Raises:
            ValueError: If amount is invalid (not implemented in base,
                but adapters may validate).
        """
        ...

    @abstractmethod
    def set_installments(self, installments: int) -> None:
        """Set the number of installments for the payment.

        Args:
            installments: Number of monthly installments. Must be at least 1.
                1 installment represents a cash payment.

        Raises:
            ValueError: If installments is invalid (not implemented in base,
                but adapters may validate).
        """
        ...

    @abstractmethod
    def process(self) -> bool:
        """Process the payment transaction.

        This method initiates the payment processing with the configured
        amount and installments.

        Returns:
            True if payment was processed successfully, False otherwise.

        Note:
            The actual implementation depends on the specific gateway adapter.
        """
        ...

    @abstractmethod
    def get_total_with_fees(self) -> float:
        """Calculate total amount including all fees.

        This method calculates the final amount the customer will pay,
        including fixed processing fees and interest charges.

        Returns:
            Total amount with processing fees and interest in BRL.

        Note:
            The calculation formula depends on the specific gateway:
            - PagFacil: amount + R$ 0.40 + (amount * 5% * installments)
            - TopPagamentos: amount + R$ 5.00 + (amount * 1% * installments)
        """
        ...
