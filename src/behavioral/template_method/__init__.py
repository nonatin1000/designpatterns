"""Template Method Pattern - Payment Processing System.

This module implements the Template Method design pattern for payment processing.
The pattern defines the skeleton of the payment algorithm while letting subclasses
customize certain steps.

Components:
- Payment: Abstract class defining the template method
- CreditPayment: Concrete implementation for credit cards
- DebitPayment: Concrete implementation for debit cards
- CashPayment: Concrete implementation for cash payments
- Gateway: Payment gateway simulator

Example:
    >>> from template_method import CreditPayment, Gateway
    >>> gateway = Gateway()
    >>> payment = CreditPayment(amount=1000.0, gateway=gateway)
    >>> success, final_amount = payment.process_payment()
    >>> print(f"Payment: R$ {final_amount:.2f} - {'Success' if success else 'Failed'}")
"""

from .payment import Payment, CreditPayment, DebitPayment, CashPayment
from .gateway import Gateway
from .schemas import (
    PaymentType,
    PaymentRequest,
    PaymentResponse,
    PaymentComparisonRequest,
    PaymentComparisonResponse,
    PaymentMethodDetails
)

__all__ = [
    # Core classes
    "Payment",
    "CreditPayment",
    "DebitPayment",
    "CashPayment",
    "Gateway",
    # Schemas
    "PaymentType",
    "PaymentRequest",
    "PaymentResponse",
    "PaymentComparisonRequest",
    "PaymentComparisonResponse",
    "PaymentMethodDetails",
]
