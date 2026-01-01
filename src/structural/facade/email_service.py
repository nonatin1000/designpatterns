"""Email notification service for the sales subsystem.

This module contains the OrderEmail class which handles sending
email notifications to customers about their orders. This is part
of the subsystem that the Facade pattern simplifies access to.
"""

from .order import Order


class OrderEmail:
    """Service for sending order-related email notifications.

    This class handles email communication with customers about
    their order status, payment confirmations, etc.

    Attributes:
        order: The order associated with the email
    """

    def __init__(self, order: Order):
        """Initialize email service with an order.

        Args:
            order: Order to send emails about

        Raises:
            ValueError: If order is None
        """
        if order is None:
            raise ValueError("Order cannot be None")

        self._order = order

    @property
    def order(self) -> Order:
        """Get the order associated with this email service.

        Returns:
            Order object
        """
        return self._order

    def send_email(self, message: str) -> bool:
        """Send an email notification to the customer.

        In a production system, this would integrate with an email service
        like SendGrid, Amazon SES, or SMTP server.

        Args:
            message: Email message content

        Returns:
            True if email was sent successfully

        Raises:
            ValueError: If message is empty
        """
        if not message or not message.strip():
            raise ValueError("Email message cannot be empty")

        customer = self._order.customer
        email_address = customer.email

        # Simulate sending email
        print(f"\n{'=' * 70}")
        print(f"EMAIL SENT")
        print(f"{'=' * 70}")
        print(f"To: {email_address}")
        print(f"Subject: Order Notification - {customer.name}")
        print(f"{'-' * 70}")
        print(f"Dear {customer.name},")
        print(f"\n{message}")
        print(f"\nOrder Details:")
        print(f"  - Products: {self._order.get_product_count()} items")
        print(f"  - Total Amount: R$ {self._order.get_total():.2f}")
        print(f"\nThank you for your purchase!")
        print(f"{'=' * 70}\n")

        # In a real system, this would send actual email via SMTP or API
        # For simulation purposes, we always return True
        return True

    def send_payment_success_email(self, payment_method: str) -> bool:
        """Send payment success notification.

        Args:
            payment_method: Payment method used (e.g., 'Credit Card', 'Bank Slip')

        Returns:
            True if email was sent successfully
        """
        message = (f"Your payment via {payment_method} has been processed successfully!\n"
                   f"Your order is being prepared for shipping.")
        return self.send_email(message)

    def send_payment_failure_email(self, payment_method: str) -> bool:
        """Send payment failure notification.

        Args:
            payment_method: Payment method that failed

        Returns:
            True if email was sent successfully
        """
        message = (f"Unfortunately, your payment via {payment_method} could not be processed.\n"
                   f"Please try again or contact our support team.")
        return self.send_email(message)

    def send_order_confirmation_email(self) -> bool:
        """Send order confirmation notification.

        Returns:
            True if email was sent successfully
        """
        message = (f"Your order has been confirmed!\n"
                   f"We will notify you when payment is processed.")
        return self.send_email(message)
