"""Adapter classes to make third-party gateways compatible with our Gateway interface.

These adapters implement the Object Adapter pattern, wrapping the adaptees
and translating calls to match our standard Gateway interface.
"""

from gateway_interface import Gateway
from payment_gateways import PagFacil, TopPagamentos


class PagFacilAdapter(Gateway):
    """Adapter for PagFacil payment gateway.

    Adapts the PagFacil interface (Portuguese method names) to our
    standard Gateway interface (English method names).
    """

    def __init__(self):
        """Initialize the adapter with a PagFacil instance."""
        self._adaptee = PagFacil()

    def set_amount(self, amount: float) -> None:
        """Set the payment amount.

        Args:
            amount: The total payment amount in BRL
        """
        self._adaptee.define_valor(amount)

    def set_installments(self, installments: int) -> None:
        """Set the number of installments.

        Args:
            installments: Number of monthly installments
        """
        self._adaptee.define_parcelas(installments)

    def process(self) -> bool:
        """Process the payment transaction.

        Returns:
            True if payment was processed successfully
        """
        return self._adaptee.processar_pagamento()

    def get_total_with_fees(self) -> float:
        """Calculate total amount including all fees.

        Returns:
            Total amount with PagFacil's fees (R$ 0.40 + 5% interest)
        """
        return self._adaptee.calcular_total_com_taxas()


class TopPagamentosAdapter(Gateway):
    """Adapter for TopPagamentos payment gateway.

    Adapts the TopPagamentos interface (different English method names) to our
    standard Gateway interface.
    """

    def __init__(self):
        """Initialize the adapter with a TopPagamentos instance."""
        self._adaptee = TopPagamentos()

    def set_amount(self, amount: float) -> None:
        """Set the payment amount.

        Args:
            amount: The total payment amount in BRL
        """
        self._adaptee.set_value(amount)

    def set_installments(self, installments: int) -> None:
        """Set the number of installments.

        Args:
            installments: Number of monthly installments
        """
        self._adaptee.set_installment_count(installments)

    def process(self) -> bool:
        """Process the payment transaction.

        Returns:
            True if transaction was executed successfully
        """
        return self._adaptee.execute_transaction()

    def get_total_with_fees(self) -> float:
        """Calculate total amount including all fees.

        Returns:
            Total amount with TopPagamentos's fees (R$ 5.00 + 1% interest)
        """
        return self._adaptee.calculate_final_amount()
