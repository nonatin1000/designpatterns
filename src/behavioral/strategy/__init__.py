"""Strategy Pattern - E-commerce Freight Calculation System.

The Strategy pattern defines a family of algorithms, encapsulates each one,
and makes them interchangeable. Strategy lets the algorithm vary independently
from clients that use it.

This implementation demonstrates freight calculation strategies for different
order types in an e-commerce system.
"""

from .freight_strategy import FreightStrategy, CommonFreight, ExpressFreight
from .order import Order, ElectronicsOrder, FurnitureOrder

__all__ = [
    "FreightStrategy",
    "CommonFreight",
    "ExpressFreight",
    "Order",
    "ElectronicsOrder",
    "FurnitureOrder",
]
