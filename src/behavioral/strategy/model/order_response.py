from pydantic import BaseModel


class OrderResponse(BaseModel):
    name: str
    amount: float
    freight_type: str
    calculated_freight: str
