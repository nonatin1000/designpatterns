from pydantic import BaseModel, Field
from typing import List
from datetime import datetime


class PedidoCreate(BaseModel):
    """Schema para criação de pedido"""
    itens: List[str] = Field(..., min_items=1, description="Lista de itens do pedido")
    valor_total: float = Field(..., gt=0, description="Valor total do pedido")

    class Config:
        json_schema_extra = {
            "example": {
                "itens": ["Notebook", "Mouse"],
                "valor_total": 2500.00
            }
        }


class PedidoResponse(BaseModel):
    """Schema para response de pedido"""
    id: int
    itens: List[str]
    valor_total: float
    estado_atual: str
    data_criacao: str
    historico: List[str]


class TransicaoResponse(BaseModel):
    """Schema para response de transição de estado"""
    sucesso: bool
    mensagem: str
    estado_anterior: str
    estado_novo: str
    pedido_id: int
