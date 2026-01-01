"""Customer entity for the sales subsystem.

This module contains the Customer class which represents a customer
in the e-commerce system. This is part of the subsystem that the
Facade pattern simplifies access to.
"""


class Customer:
    """Represents a customer with personal information.

    Attributes:
        name: Full name of the customer
        tax_id: Tax identification number (CPF in Brazil)
        email: Email address for communication
    """

    def __init__(self, name: str, tax_id: str, email: str):
        """Initialize a new customer.

        Args:
            name: Full name of the customer
            tax_id: Tax identification number (e.g., CPF)
            email: Valid email address

        Raises:
            ValueError: If any parameter is empty or invalid
        """
        if not name or not name.strip():
            raise ValueError("Customer name cannot be empty")
        if not tax_id or not tax_id.strip():
            raise ValueError("Tax ID cannot be empty")
        if not email or "@" not in email:
            raise ValueError("Invalid email address")

        self._name = name.strip()
        self._tax_id = tax_id.strip()
        self._email = email.strip()

    @property
    def name(self) -> str:
        """Get the customer's name.

        Returns:
            Customer's full name
        """
        return self._name

    @property
    def tax_id(self) -> str:
        """Get the customer's tax ID.

        Returns:
            Tax identification number
        """
        return self._tax_id

    @property
    def email(self) -> str:
        """Get the customer's email.

        Returns:
            Email address
        """
        return self._email

    def __repr__(self) -> str:
        """String representation of the customer.

        Returns:
            String with customer details
        """
        return f"Customer(name='{self._name}', tax_id='{self._tax_id}', email='{self._email}')"

    def __str__(self) -> str:
        """Human-readable string representation.

        Returns:
            Customer name and email
        """
        return f"{self._name} <{self._email}>"
