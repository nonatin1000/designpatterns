"""Third-party payment gateway implementations (Adaptees).

These are external payment services with their own interfaces that cannot
be modified. They need to be adapted to work with our Gateway interface
using adapter classes.

The Adapter pattern allows these incompatible interfaces to work together
by creating adapter classes that translate between the adaptee's interface
and our target Gateway interface.
"""


class PagFacil:
    """PagFacil payment gateway (Adaptee).

    This is a third-party payment service with a Portuguese interface.
    It cannot be modified, so it must be adapted using PagFacilAdapter.

    Pricing model:
    - Fixed fee: R$ 0.40 per transaction
    - Interest rate: 5% per month per installment

    Best for: Cash payments (1 installment) due to low fixed fee.

    Note:
        This class uses Portuguese method names (define_valor, define_parcelas,
        etc.) which are incompatible with our Gateway interface. The adapter
        translates these calls to the standard interface.
    """

    def __init__(self) -> None:
        """Initialize PagFacil gateway with default pricing."""
        self._amount: float = 0.0
        self._installments: int = 1
        self._fixed_fee: float = 0.40
        self._monthly_interest_rate: float = 0.05  # 5%

    def define_valor(self, amount: float) -> None:
        """Set the payment amount (Portuguese naming - original interface).

        Args:
            amount: Payment amount in BRL
        """
        self._amount = amount

    def define_parcelas(self, installments: int) -> None:
        """Set the number of installments (Portuguese naming - original interface).

        Args:
            installments: Number of monthly installments
        """
        self._installments = installments

    def processar_pagamento(self) -> bool:
        """Process the payment (Portuguese naming - original interface).

        Returns:
            True if payment was successfully processed
        """
        if self._amount <= 0:
            return False
        print(f"[PagFacil] Processing payment: R$ {self._amount:.2f} "
              f"in {self._installments}x installments")
        return True

    def calcular_total_com_taxas(self) -> float:
        """Calculate total with fees (Portuguese naming - original interface).

        Returns:
            Total amount including fixed fee and interest
        """
        total_interest = self._amount * self._monthly_interest_rate * self._installments
        return self._amount + self._fixed_fee + total_interest


class TopPagamentos:
    """TopPagamentos payment gateway (Adaptee).

    This is a third-party payment service with a different English interface.
    It cannot be modified, so it must be adapted using TopPagamentosAdapter.

    Pricing model:
    - Fixed fee: R$ 5.00 per transaction
    - Interest rate: 1% per month per installment

    Best for: Installment payments (2+ installments) due to low interest rate.

    Note:
        This class uses different method names (set_value, set_installment_count,
        etc.) which are incompatible with our Gateway interface. The adapter
        translates these calls to the standard interface.
    """

    def __init__(self) -> None:
        """Initialize TopPagamentos gateway with default pricing."""
        self._payment_value: float = 0.0
        self._number_of_installments: int = 1
        self._transaction_fee: float = 5.00
        self._interest_per_installment: float = 0.01  # 1%

    def set_value(self, value: float) -> None:
        """Set the payment value (English naming - different interface).

        Args:
            value: Payment value in BRL
        """
        self._payment_value = value

    def set_installment_count(self, count: int) -> None:
        """Set the installment count (English naming - different interface).

        Args:
            count: Number of monthly installments
        """
        self._number_of_installments = count

    def execute_transaction(self) -> bool:
        """Execute the payment transaction (different method name).

        Returns:
            True if transaction was executed successfully
        """
        if self._payment_value <= 0:
            return False
        print(f"[TopPagamentos] Executing transaction: R$ {self._payment_value:.2f} "
              f"in {self._number_of_installments}x installments")
        return True

    def calculate_final_amount(self) -> float:
        """Calculate final amount including all charges (different method name).

        Returns:
            Final amount with transaction fee and interest
        """
        total_interest = (self._payment_value * self._interest_per_installment
                         * self._number_of_installments)
        return self._payment_value + self._transaction_fee + total_interest
