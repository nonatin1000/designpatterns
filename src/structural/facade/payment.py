"""Payment processing classes for the sales subsystem.

This module contains the abstract Payment class and concrete implementations
for different payment methods (Credit Card and Bank Slip). This is part of
the subsystem that the Facade pattern simplifies access to.
"""

from abc import ABC, abstractmethod
from .order import Order


class Payment(ABC):
    """Abstract base class for payment processing.

    This class defines the interface that all concrete payment
    implementations must follow.

    Attributes:
        order: The order being paid
    """

    def __init__(self, order: Order):
        """Initialize payment with an order.

        Args:
            order: Order to be paid

        Raises:
            ValueError: If order is None or has no products
        """
        if order is None:
            raise ValueError("Order cannot be None")
        if order.get_product_count() == 0:
            raise ValueError("Order must have at least one product")

        self._order = order

    @property
    def order(self) -> Order:
        """Get the order associated with this payment.

        Returns:
            Order object
        """
        return self._order

    @abstractmethod
    def process_payment(self) -> bool:
        """Process the payment transaction.

        This method must be implemented by concrete payment classes.

        Returns:
            True if payment was successful, False otherwise.

        Note:
            In production, this would integrate with payment gateways
            or bank systems to process actual transactions.
        """
        ...

    def get_payment_amount(self) -> float:
        """Get the total amount to be paid.

        Returns:
            Total order amount
        """
        return self._order.get_total()


class CreditCardPayment(Payment):
    """Concrete payment implementation for credit card transactions.

    This class simulates credit card payment processing.
    In a real system, this would integrate with a payment gateway.
    """

    def process_payment(self) -> bool:
        """Process credit card payment.

        Simulates payment processing with a credit card.
        In production, this would call a payment gateway API.

        Returns:
            True if payment was successful
        """
        amount = self.get_payment_amount()
        customer = self._order.customer

        print(f"[CreditCardPayment] Processing credit card payment...")
        print(f"[CreditCardPayment] Customer: {customer.name}")
        print(f"[CreditCardPayment] Amount: R$ {amount:.2f}")
        print(f"[CreditCardPayment] Payment approved!")

        # In a real system, this would make an API call to payment gateway
        # For simulation purposes, we always return True
        return True


class BankSlipPayment(Payment):
    """Concrete payment implementation for bank slip (boleto) transactions.

    This class simulates bank slip payment processing.
    Bank slips are a popular payment method in Brazil.
    """

    def process_payment(self) -> bool:
        """Process bank slip payment.

        Simulates generating a bank slip for payment.
        In production, this would generate an actual bank slip with barcode.

        Returns:
            True if bank slip was generated successfully
        """
        amount = self.get_payment_amount()
        customer = self._order.customer

        print(f"[BankSlipPayment] Generating bank slip...")
        print(f"[BankSlipPayment] Customer: {customer.name}")
        print(f"[BankSlipPayment] Amount: R$ {amount:.2f}")
        print(f"[BankSlipPayment] Bank slip generated successfully!")
        print(f"[BankSlipPayment] Barcode: 23793.38128 60000.123456 78901.234567 1 88880000012345")

        # In a real system, this would generate an actual bank slip
        # For simulation purposes, we always return True
        return True
