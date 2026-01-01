"""Topping decorator base class for the Decorator pattern.

This module defines the abstract Decorator class that serves as the base
for all concrete decorators (toppings). Decorators wrap components and
add functionality dynamically.
"""

from abc import abstractmethod
from .pizza import Pizza


class ToppingDecorator(Pizza):
    """Decorator: Abstract base class for all topping decorators.

    This is the Decorator class in the Decorator pattern. It maintains a
    reference to a Component (Pizza) and defines an interface that conforms
    to the Component's interface.

    Decorators wrap components and add responsibilities dynamically. Each
    decorator can add its own behavior before or after delegating to the
    wrapped component.

    The Decorator pattern allows:
    - Adding responsibilities to objects dynamically
    - Mixing and matching behaviors
    - Avoiding class explosion from subclassing

    Attributes:
        pizza: Reference to the wrapped Pizza component.
    """

    def __init__(self, pizza: Pizza) -> None:
        """Initialize decorator with a pizza to wrap.

        Args:
            pizza: The Pizza component to decorate. This can be either a
            concrete pizza or another decorator (allowing chaining).
        """
        super().__init__()
        self.pizza = pizza

    @abstractmethod
    def get_description(self) -> str:
        """Get the description including this topping.

        Each decorator must implement this method to concatenate its
        description with the wrapped component's description.

        Returns:
            A string describing the pizza with this topping added.
            Format: "{component_description} + {topping_description}"

        Note:
            This method should call self.pizza.get_description() and
            append the topping's description.
        """
        ...

    @abstractmethod
    def get_price(self) -> float:
        """Get the total price including this topping.

        Each decorator must implement this method to add its price to
        the wrapped component's price.

        Returns:
            The total price in BRL, including the wrapped component's
            price plus this topping's price.

        Note:
            This method should call self.pizza.get_price() and add
            the topping's price to it.
        """
        ...

