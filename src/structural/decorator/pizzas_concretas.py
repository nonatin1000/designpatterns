"""Concrete pizza components for the Decorator pattern.

This module defines the concrete pizza implementations (ConcreteComponents)
that can be decorated with toppings. Each pizza has a base price and description.
"""

from .pizza import Pizza


class ChickenPizza(Pizza):
    """ConcreteComponent: Chicken pizza implementation.

    This is a concrete component that can be decorated with toppings.
    It represents a base chicken pizza with a fixed price.

    Price: R$ 19.00
    """

    def __init__(self) -> None:
        """Initialize chicken pizza with description and price."""
        super().__init__()
        self.description = "Delicious chicken pizza"
        self.price = 19.00

    def get_description(self) -> str:
        """Get the description of the chicken pizza.

        Returns:
            The base description of the chicken pizza.
        """
        return self.description

    def get_price(self) -> float:
        """Get the base price of the chicken pizza.

        Returns:
            The base price in BRL (R$ 19.00).
        """
        return self.price


class PepperoniPizza(Pizza):
    """ConcreteComponent: Pepperoni pizza implementation.

    This is a concrete component that can be decorated with toppings.
    It represents a base pepperoni pizza with a fixed price.

    Price: R$ 25.00
    """

    def __init__(self) -> None:
        """Initialize pepperoni pizza with description and price."""
        super().__init__()
        self.description = "Delicious pepperoni pizza"
        self.price = 25.00

    def get_description(self) -> str:
        """Get the description of the pepperoni pizza.

        Returns:
            The base description of the pepperoni pizza.
        """
        return self.description

    def get_price(self) -> float:
        """Get the base price of the pepperoni pizza.

        Returns:
            The base price in BRL (R$ 25.00).
        """
        return self.price


class CheesePizza(Pizza):
    """ConcreteComponent: Cheese pizza implementation.

    This is a concrete component that can be decorated with toppings.
    It represents a base cheese pizza with a fixed price.

    Price: R$ 22.00
    """

    def __init__(self) -> None:
        """Initialize cheese pizza with description and price."""
        super().__init__()
        self.description = "Delicious cheese pizza"
        self.price = 22.00

    def get_description(self) -> str:
        """Get the description of the cheese pizza.

        Returns:
            The base description of the cheese pizza.
        """
        return self.description

    def get_price(self) -> float:
        """Get the base price of the cheese pizza.

        Returns:
            The base price in BRL (R$ 22.00).
        """
        return self.price
