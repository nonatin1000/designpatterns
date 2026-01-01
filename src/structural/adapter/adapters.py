"""Adapter classes to make third-party gateways compatible with Gateway interface.

These adapters implement the Object Adapter pattern, wrapping the adaptees
and translating calls to match our standard Gateway interface.

The Adapter pattern allows incompatible interfaces to work together by
creating a wrapper that translates between the adaptee's interface and
the target interface expected by the client.
"""

from .gateway_interface import Gateway
from .payment_gateways import PagFacil, TopPagamentos


class PagFacilAdapter(Gateway):
    """Adapter for PagFacil payment gateway (Object Adapter).

    This adapter wraps a PagFacil instance and translates calls from our
    standard Gateway interface to PagFacil's Portuguese interface.

    The adapter implements the Object Adapter pattern by composition,
    maintaining a reference to the adaptee (PagFacil) and delegating
    calls with appropriate translations.

    Translation mapping:
    - set_amount() -> define_valor()
    - set_installments() -> define_parcelas()
    - process() -> processar_pagamento()
    - get_total_with_fees() -> calcular_total_com_taxas()
    """

    def __init__(self) -> None:
        """Initialize the adapter with a PagFacil instance.

        Creates a new PagFacil adaptee instance that will be wrapped
        by this adapter.
        """
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
    """Adapter for TopPagamentos payment gateway (Object Adapter).

    This adapter wraps a TopPagamentos instance and translates calls from our
    standard Gateway interface to TopPagamentos's different English interface.

    The adapter implements the Object Adapter pattern by composition,
    maintaining a reference to the adaptee (TopPagamentos) and delegating
    calls with appropriate translations.

    Translation mapping:
    - set_amount() -> set_value()
    - set_installments() -> set_installment_count()
    - process() -> execute_transaction()
    - get_total_with_fees() -> calculate_final_amount()
    """

    def __init__(self) -> None:
        """Initialize the adapter with a TopPagamentos instance.

        Creates a new TopPagamentos adaptee instance that will be wrapped
        by this adapter.
        """
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
