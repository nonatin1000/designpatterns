"""Facade Pattern - E-commerce Sales System.

The Facade pattern provides a unified interface to a set of interfaces in a subsystem.
Facade defines a higher-level interface that makes the subsystem easier to use.

This implementation demonstrates how a SalesFacade simplifies interaction with
a complex sales subsystem consisting of Order, Payment, and Email services.
"""

from .customer import Customer
from .product import Product
from .order import Order
from .payment import Payment, CreditCardPayment, BankSlipPayment
from .email_service import OrderEmail
from .sales_facade import SalesFacade

__all__ = [
    "Customer",
    "Product",
    "Order",
    "Payment",
    "CreditCardPayment",
    "BankSlipPayment",
    "OrderEmail",
    "SalesFacade",
]
