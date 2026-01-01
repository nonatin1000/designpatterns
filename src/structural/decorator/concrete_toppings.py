"""Concrete topping decorators for the Decorator pattern.

This module defines concrete decorator implementations that add specific
toppings to pizzas. Each decorator wraps a pizza and adds its own price
and description.
"""

from .topping_decorator import ToppingDecorator
from .pizza import Pizza


class StuffedCrust(ToppingDecorator):
    """ConcreteDecorator: Stuffed crust with cream cheese topping.

    This decorator adds a stuffed crust with cream cheese to any pizza.
    It wraps the pizza and adds R$ 8.50 to the total price.

    Price: R$ 8.50
    """

    def __init__(self, pizza: Pizza) -> None:
        """Initialize stuffed crust decorator.

        Args:
            pizza: The Pizza component to decorate.
        """
        super().__init__(pizza)

    def get_description(self) -> str:
        """Get description with stuffed crust added.

        Returns:
            The pizza description concatenated with " + Stuffed crust
            with cream cheese".
        """
        return f"{self.pizza.get_description()} + Stuffed crust with cream cheese"

    def get_price(self) -> float:
        """Get total price including stuffed crust.

        Returns:
            The wrapped pizza's price plus R$ 8.50 for the stuffed crust.
        """
        return self.pizza.get_price() + 8.50


class WholeWheatCrust(ToppingDecorator):
    """ConcreteDecorator: Whole wheat crust topping.

    This decorator adds a whole wheat crust option to any pizza.
    It wraps the pizza and adds R$ 5.00 to the total price.

    Price: R$ 5.00
    """

    def __init__(self, pizza: Pizza) -> None:
        """Initialize whole wheat crust decorator.

        Args:
            pizza: The Pizza component to decorate.
        """
        super().__init__(pizza)

    def get_description(self) -> str:
        """Get description with whole wheat crust added.

        Returns:
            The pizza description concatenated with " + Whole wheat crust".
        """
        return f"{self.pizza.get_description()} + Whole wheat crust"

    def get_price(self) -> float:
        """Get total price including whole wheat crust.

        Returns:
            The wrapped pizza's price plus R$ 5.00 for the whole wheat crust.
        """
        return self.pizza.get_price() + 5.00

