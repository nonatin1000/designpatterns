"""Adapter Pattern - Payment Gateway Integration System.

The Adapter pattern allows incompatible interfaces to work together by
creating adapters that translate between different interfaces.

This implementation demonstrates adapting two third-party payment gateways
(PagFacil and TopPagamentos) with incompatible interfaces to work with a
common Gateway interface.

Pattern Structure:
- Target (Gateway): Standard interface expected by the client
- Adaptees (PagFacil, TopPagamentos): Existing classes with incompatible interfaces
- Adapters (PagFacilAdapter, TopPagamentosAdapter): Bridge between Target and Adaptees
- Client (Billing): Uses objects through the Target interface
"""

from .gateway_interface import Gateway
from .payment_gateways import PagFacil, TopPagamentos
from .adapters import PagFacilAdapter, TopPagamentosAdapter
from .billing import Billing

__all__ = [
    # Target interface
    "Gateway",
    # Adaptees (third-party classes)
    "PagFacil",
    "TopPagamentos",
    # Adapters
    "PagFacilAdapter",
    "TopPagamentosAdapter",
    # Client
    "Billing",
]
