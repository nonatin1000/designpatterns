"""Observer Pattern - Newsletter System.

The Observer is a behavioral pattern that defines a one-to-many dependency
between objects, so that when one object changes state, all its dependents
are notified and updated automatically.
"""

from .observer import (
    Observer,
    BaseSubscriber,
    ClientSubscriber,
    EmployeeSubscriber,
    PartnerSubscriber,
    SupplierSubscriber
)
from .subject import Subject, Newsletter

__all__ = [
    "Observer",
    "Subject",
    "Newsletter",
    "BaseSubscriber",
    "ClientSubscriber",
    "EmployeeSubscriber",
    "PartnerSubscriber",
    "SupplierSubscriber",
]
