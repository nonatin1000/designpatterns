from pydantic import BaseModel


class PaymentResponse(BaseModel):
    """
    Representa a resposta de um pagamento.

    Attributes:
        amount: O valor do pagamento.
        tax: O valor do imposto.
        discount: O valor do desconto.
        payment_type: O tipo de pagamento
    """

    amount: float
    tax: float
    discount: float
    payment_type: str
    is_pay: bool
