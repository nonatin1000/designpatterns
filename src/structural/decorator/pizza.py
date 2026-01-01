"""Pizza component interface for the Decorator pattern.

This module defines the Component interface (Pizza) that serves as the base
for both concrete pizzas and decorators. The Decorator pattern allows
attaching additional responsibilities to objects dynamically.
"""

from abc import ABC, abstractmethod


class Pizza(ABC):
    """Component: Abstract base class for all pizzas and decorators.

    This is the Component interface in the Decorator pattern. It defines the
    common interface for objects that can have responsibilities added to them
    dynamically. Both concrete pizzas and decorators implement this interface.

    The Decorator pattern provides a flexible alternative to subclassing for
    extending functionality. Decorators can wrap pizzas and add features
    (like toppings) without modifying the original pizza classes.

    Attributes:
        description: Default description string (can be overridden).
        price: Default price value (can be overridden).
    """

    def __init__(self) -> None:
        """Initialize pizza with default values."""
        self.description: str = "Description not defined"
        self.price: float = 0.0

    @abstractmethod
    def get_description(self) -> str:
        """Get the description of the pizza.

        Returns:
            A string describing the pizza, including all toppings/decorators
            if any have been applied.

        Note:
            Concrete components return their base description.
            Decorators concatenate their description with the wrapped component's.
        """
        ...

    @abstractmethod
    def get_price(self) -> float:
        """Get the total price of the pizza.

        Returns:
            The total price in BRL, including the base pizza price and
            all applied toppings/decorators.

        Note:
            Concrete components return their base price.
            Decorators add their price to the wrapped component's price.
        """
        ...
