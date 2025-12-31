"""Product entity for the sales subsystem.

This module contains the Product class which represents an item
that can be sold in the e-commerce system.
"""


class Product:
    """Represents a product available for purchase.

    Attributes:
        name: Product name
        description: Detailed product description
        price: Product price in Brazilian Reais (BRL)
    """

    def __init__(self, name: str, description: str, price: float):
        """Initialize a new product.

        Args:
            name: Product name
            description: Product description
            price: Product price (must be positive)

        Raises:
            ValueError: If name/description is empty or price is invalid
        """
        if not name or not name.strip():
            raise ValueError("Product name cannot be empty")
        if not description or not description.strip():
            raise ValueError("Product description cannot be empty")
        if price <= 0:
            raise ValueError("Product price must be greater than zero")

        self._name = name.strip()
        self._description = description.strip()
        self._price = price

    @property
    def name(self) -> str:
        """Get the product name.

        Returns:
            Product name
        """
        return self._name

    @property
    def description(self) -> str:
        """Get the product description.

        Returns:
            Product description
        """
        return self._description

    @property
    def price(self) -> float:
        """Get the product price.

        Returns:
            Product price in BRL
        """
        return self._price

    def __repr__(self) -> str:
        """String representation of the product.

        Returns:
            String with product details
        """
        return (f"Product(name='{self._name}', "
                f"description='{self._description}', "
                f"price={self._price:.2f})")

    def __str__(self) -> str:
        """Human-readable string representation.

        Returns:
            Product name and price
        """
        return f"{self._name} - R$ {self._price:.2f}"
