"""Sales Facade - Simplified interface for the sales subsystem.

This module contains the SalesFacade class which provides a unified
and simplified interface to the complex sales subsystem (Order, Payment, Email).
This is the main implementation of the Facade pattern.
"""

from customer import Customer
from product import Product
from order import Order
from payment import CreditCardPayment, BankSlipPayment
from email_service import OrderEmail


class SalesFacade:
    """Facade for the sales subsystem.

    This class provides a simplified interface for processing sales,
    hiding the complexity of dealing with Order, Payment, and Email classes.

    The facade encapsulates the workflow:
    1. Create order with customer
    2. Add products to order
    3. Process payment (credit card or bank slip)
    4. Send email notification

    Attributes:
        order: The current order being processed
        email: Email service for this order
    """

    def __init__(self, customer: Customer):
        """Initialize the sales facade with a customer.

        This automatically creates an order and email service,
        simplifying the client's interaction with the subsystem.

        Args:
            customer: Customer placing the order

        Raises:
            ValueError: If customer is None
        """
        if customer is None:
            raise ValueError("Customer cannot be None")

        # Create order for the customer
        self._order = Order(customer)

        # Create email service linked to the order
        self._email = OrderEmail(self._order)

    @property
    def order(self) -> Order:
        """Get the current order.

        Returns:
            Order object
        """
        return self._order

    @property
    def email(self) -> OrderEmail:
        """Get the email service.

        Returns:
            OrderEmail object
        """
        return self._email

    def add_product(self, product: Product) -> None:
        """Add a product to the order.

        This method simplifies product addition by delegating to the Order class.

        Args:
            product: Product to add to the order

        Raises:
            ValueError: If product is None
        """
        self._order.add_product(product)

    def process_credit_card_order(self) -> bool:
        """Process the order using credit card payment.

        This method encapsulates the entire workflow:
        1. Create credit card payment
        2. Process the payment
        3. Send appropriate email notification

        Returns:
            True if payment was successful, False otherwise

        Raises:
            ValueError: If order has no products
        """
        if self._order.get_product_count() == 0:
            raise ValueError("Cannot process order without products")

        # Create and process credit card payment
        payment = CreditCardPayment(self._order)
        success = payment.process_payment()

        # Send email based on payment result
        if success:
            self._email.send_payment_success_email("Credit Card")
        else:
            self._email.send_payment_failure_email("Credit Card")

        return success

    def process_bank_slip_order(self) -> bool:
        """Process the order using bank slip payment.

        This method encapsulates the entire workflow:
        1. Create bank slip payment
        2. Process the payment (generate bank slip)
        3. Send appropriate email notification

        Returns:
            True if bank slip was generated successfully, False otherwise

        Raises:
            ValueError: If order has no products
        """
        if self._order.get_product_count() == 0:
            raise ValueError("Cannot process order without products")

        # Create and process bank slip payment
        payment = BankSlipPayment(self._order)
        success = payment.process_payment()

        # Send email based on payment result
        if success:
            self._email.send_payment_success_email("Bank Slip")
        else:
            self._email.send_payment_failure_email("Bank Slip")

        return success

    def get_order_total(self) -> float:
        """Get the total amount of the current order.

        Returns:
            Total order amount
        """
        return self._order.get_total()

    def get_product_count(self) -> int:
        """Get the number of products in the current order.

        Returns:
            Number of products
        """
        return self._order.get_product_count()

    def get_customer_name(self) -> str:
        """Get the customer's name.

        Returns:
            Customer name
        """
        return self._order.customer.name

    def __repr__(self) -> str:
        """String representation of the facade.

        Returns:
            String with facade details
        """
        return (f"SalesFacade(customer='{self.get_customer_name()}', "
                f"products={self.get_product_count()}, "
                f"total=R$ {self.get_order_total():.2f})")

    def __str__(self) -> str:
        """Human-readable string representation.

        Returns:
            Facade summary
        """
        return (f"Sales Facade for {self.get_customer_name()} - "
                f"{self.get_product_count()} items - "
                f"R$ {self.get_order_total():.2f}")
