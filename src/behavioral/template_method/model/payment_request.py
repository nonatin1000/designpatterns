from typing import Literal
from pydantic import BaseModel


class PaymentRequest(BaseModel):
    """
    Representa a requisição para criar um pagamento.

    Attributes:
        amount: O valor do pagamento.
        type_payment: O tipo de pagamento, pode ser 'credit', 'debit' ou 'cash'.
    """

    amount: float
    type_payment: Literal["credit", "debit", "cash"]
