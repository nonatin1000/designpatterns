"""Freight calculation strategies (Strategy pattern implementation).

This module defines the Strategy interface and concrete implementations
for different freight calculation algorithms.
"""

from abc import ABC, abstractmethod


class FreightStrategy(ABC):
    """Abstract base class for freight calculation strategies.

    This is the Strategy interface that defines the contract for all
    concrete freight calculation implementations.
    """

    @abstractmethod
    def calculate(self, order_amount: float) -> float:
        """Calculate freight cost based on order amount.

        Args:
            order_amount: The total order value in BRL

        Returns:
            The calculated freight cost
        """
        pass


class CommonFreight(FreightStrategy):
    """Concrete strategy for common (standard) freight calculation.

    Common freight costs 5% of the order value.
    Best for: Regular deliveries with standard delivery time.
    """

    RATE = 0.05  # 5% of order value

    def calculate(self, order_amount: float) -> float:
        """Calculate common freight cost.

        Args:
            order_amount: The total order value in BRL

        Returns:
            Freight cost (5% of order amount)
        """
        return order_amount * self.RATE


class ExpressFreight(FreightStrategy):
    """Concrete strategy for express (fast) freight calculation.

    Express freight costs 10% of the order value.
    Best for: Urgent deliveries with faster delivery time.
    """

    RATE = 0.10  # 10% of order value

    def calculate(self, order_amount: float) -> float:
        """Calculate express freight cost.

        Args:
            order_amount: The total order value in BRL

        Returns:
            Freight cost (10% of order amount)
        """
        return order_amount * self.RATE
