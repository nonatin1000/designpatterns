"""Adapter Pattern - Payment Gateway Integration System.

The Adapter pattern allows incompatible interfaces to work together.
It acts as a bridge between two incompatible interfaces by wrapping
an object and exposing a different interface.

This implementation demonstrates adapting two third-party payment gateways
(PagFacil and TopPagamentos) to work with a common Gateway interface.
"""

from .gateway_interface import Gateway
from .payment_gateways import PagFacil, TopPagamentos
from .adapters import PagFacilAdapter, TopPagamentosAdapter
from .billing import Billing

__all__ = [
    "Gateway",
    "PagFacil",
    "TopPagamentos",
    "PagFacilAdapter",
    "TopPagamentosAdapter",
    "Billing",
]
