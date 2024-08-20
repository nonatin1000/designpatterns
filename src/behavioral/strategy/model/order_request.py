from typing import Literal
from pydantic import BaseModel


class OrderRequest(BaseModel):
    """
    Representa a requisição para criar um pedido.

    Attributes:
        name: O tipo do pedido, pode ser 'electronic' ou 'shower'.
        amount: O valor do pedido.
        type_freight: O tipo de frete, pode ser 'common' ou 'express'.
    """

    name: Literal["electronic", "shower"]
    amount: float
    type_freight: Literal["common", "express"]
