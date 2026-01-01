"""Order classes (Context in Strategy pattern).

This module defines the Order base class (Context) and concrete order types
for different product categories (Electronics, Furniture).
"""

from abc import ABC, abstractmethod
from typing import Optional
from .freight_strategy import FreightStrategy


class Order(ABC):
    """Abstract base class for orders (Context in Strategy pattern).

    This class maintains a reference to a FreightStrategy object and
    delegates freight calculation to it. The strategy can be changed
    at runtime, allowing different freight calculation algorithms.

    Attributes:
        amount: Order value in Brazilian Reais (BRL)
        freight_strategy: Current freight calculation strategy
    """

    def __init__(self):
        """Initialize a new order with no amount and no freight strategy."""
        self._amount: float = 0.0
        self._freight_strategy: Optional[FreightStrategy] = None

    @property
    def amount(self) -> float:
        """Get the order amount.

        Returns:
            Order value in BRL
        """
        return self._amount

    @amount.setter
    def amount(self, value: float) -> None:
        """Set the order amount.

        Args:
            value: Order value in BRL

        Raises:
            ValueError: If amount is negative
        """
        if value < 0:
            raise ValueError("Order amount cannot be negative")
        self._amount = value

    def set_freight_strategy(self, strategy: FreightStrategy) -> None:
        """Set the freight calculation strategy.

        This method allows changing the freight calculation algorithm
        at runtime (Strategy pattern).

        Args:
            strategy: FreightStrategy implementation to use

        Raises:
            ValueError: If strategy is None
        """
        if strategy is None:
            raise ValueError("Freight strategy cannot be None")
        self._freight_strategy = strategy

    def calculate_freight(self) -> float:
        """Calculate freight cost using the current strategy.

        Returns:
            Calculated freight cost

        Raises:
            ValueError: If no freight strategy has been set
        """
        if self._freight_strategy is None:
            raise ValueError("Freight strategy must be set before calculating")
        return self._freight_strategy.calculate(self._amount)

    @property
    @abstractmethod
    def category(self) -> str:
        """Get the order category name.

        Returns:
            Category name (e.g., 'Electronics', 'Furniture')
        """
        pass

    def __repr__(self) -> str:
        """String representation of the order.

        Returns:
            String with order details
        """
        strategy_name = (
            self._freight_strategy.__class__.__name__
            if self._freight_strategy
            else "None"
        )
        return (
            f"{self.__class__.__name__}("
            f"category='{self.category}', "
            f"amount=R$ {self._amount:.2f}, "
            f"strategy={strategy_name})"
        )


class ElectronicsOrder(Order):
    """Order for electronics products.

    Electronics orders support both common and express freight options.
    Examples: Laptops, smartphones, tablets, cameras, etc.
    """

    @property
    def category(self) -> str:
        """Get the category name.

        Returns:
            'Electronics'
        """
        return "Electronics"


class FurnitureOrder(Order):
    """Order for furniture products.

    Furniture orders typically only support common freight due to
    size and weight restrictions in certain regions.
    Examples: Tables, chairs, sofas, beds, wardrobes, etc.
    """

    @property
    def category(self) -> str:
        """Get the category name.

        Returns:
            'Furniture'
        """
        return "Furniture"
