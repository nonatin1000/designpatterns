"""Order management for the sales subsystem.

This module contains the Order class which manages customer orders
and their associated products.
"""

from typing import List
from customer import Customer
from product import Product


class Order:
    """Represents a customer order containing products.

    An order is associated with a customer and contains a list of products.
    It calculates the total amount based on the products added.

    Attributes:
        customer: The customer who placed the order
        products: List of products in the order
    """

    def __init__(self, customer: Customer):
        """Initialize a new order for a customer.

        Args:
            customer: The customer placing the order

        Raises:
            ValueError: If customer is None
        """
        if customer is None:
            raise ValueError("Customer cannot be None")

        self._customer = customer
        self._products: List[Product] = []

    @property
    def customer(self) -> Customer:
        """Get the customer associated with this order.

        Returns:
            Customer object
        """
        return self._customer

    @customer.setter
    def customer(self, customer: Customer) -> None:
        """Set the customer for this order.

        Args:
            customer: Customer object

        Raises:
            ValueError: If customer is None
        """
        if customer is None:
            raise ValueError("Customer cannot be None")
        self._customer = customer

    @property
    def products(self) -> List[Product]:
        """Get the list of products in this order.

        Returns:
            List of Product objects (copy to prevent external modification)
        """
        return self._products.copy()

    def add_product(self, product: Product) -> None:
        """Add a product to the order.

        Args:
            product: Product to be added

        Raises:
            ValueError: If product is None
        """
        if product is None:
            raise ValueError("Product cannot be None")
        self._products.append(product)

    def remove_product(self, product: Product) -> bool:
        """Remove a product from the order.

        Args:
            product: Product to be removed

        Returns:
            True if product was removed, False if not found
        """
        try:
            self._products.remove(product)
            return True
        except ValueError:
            return False

    def get_total(self) -> float:
        """Calculate the total amount of the order.

        Returns:
            Sum of all product prices
        """
        return sum(product.price for product in self._products)

    def get_product_count(self) -> int:
        """Get the number of products in the order.

        Returns:
            Number of products
        """
        return len(self._products)

    def clear_products(self) -> None:
        """Remove all products from the order."""
        self._products.clear()

    def __repr__(self) -> str:
        """String representation of the order.

        Returns:
            String with order details
        """
        return (f"Order(customer={self._customer.name}, "
                f"products={len(self._products)}, "
                f"total=R$ {self.get_total():.2f})")

    def __str__(self) -> str:
        """Human-readable string representation.

        Returns:
            Order summary with customer and total
        """
        return (f"Order for {self._customer.name}: "
                f"{len(self._products)} items - "
                f"R$ {self.get_total():.2f}")
