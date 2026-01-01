"""Payment gateway simulator.

This module provides a Gateway class that simulates payment processing.
In a real system, this would integrate with actual payment processors
like Stripe, PayPal, PagSeguro, etc.
"""

import random


class Gateway:
    """Payment gateway simulator.

    This class simulates a payment gateway that processes charges.
    In production, this would be replaced with actual payment gateway
    integration (Stripe, PayPal, Mercado Pago, PagSeguro, etc.).

    The charge() method randomly returns True or False to simulate
    successful and failed payment attempts for testing purposes.

    Examples:
        >>> gateway = Gateway()
        >>> success = gateway.charge(100.50)
        >>> print(f"Payment {'approved' if success else 'rejected'}")
    """

    def charge(self, amount: float) -> bool:
        """Process a payment charge.

        This method simulates sending a charge request to a payment gateway.
        It randomly returns True (success) or False (failure) to simulate
        real-world scenarios where payments can be approved or declined.

        In a production environment, this would:
        1. Connect to actual payment gateway API
        2. Send charge request with amount and payment details
        3. Handle gateway response (approved/declined/error)
        4. Return actual success status

        Args:
            amount: Amount to charge in BRL

        Returns:
            True if payment was successful, False if declined
        """
        # Simulate gateway response (50% success rate)
        return random.choice([True, False])

    def __repr__(self) -> str:
        """String representation of the gateway.

        Returns:
            Gateway class name
        """
        return f"{self.__class__.__name__}()"
