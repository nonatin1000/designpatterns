from pydantic import BaseModel, Field
from typing import List
from enum import Enum


class TipoPizza(str, Enum):
    """Enum com os tipos de pizza disponíveis"""
    FRANGO = "frango"
    CALABRESA = "calabresa"
    QUEIJO = "queijo"


class TipoAcrescimo(str, Enum):
    """Enum com os tipos de acréscimos disponíveis"""
    BORDA_REQUEIJAO = "borda_requeijao"
    MASSA_INTEGRAL = "massa_integral"


class PedidoPizzaRequest(BaseModel):
    """Schema para o request de criação de pizza"""
    tipo_pizza: TipoPizza = Field(
        ...,
        description="Tipo da pizza base",
        example=TipoPizza.QUEIJO
    )
    acrescimos: List[TipoAcrescimo] = Field(
        default=[],
        description="Lista de acréscimos desejados",
        example=[TipoAcrescimo.BORDA_REQUEIJAO, TipoAcrescimo.MASSA_INTEGRAL]
    )

    class Config:
        json_schema_extra = {
            "example": {
                "tipo_pizza": "queijo",
                "acrescimos": ["borda_requeijao", "massa_integral"]
            }
        }


class PizzaResponse(BaseModel):
    """Schema para a response com os dados da pizza"""
    descricao: str = Field(
        ...,
        description="Descrição completa da pizza com acréscimos"
    )
    preco: float = Field(
        ...,
        description="Preço total da pizza com acréscimos",
        ge=0
    )

    class Config:
        json_schema_extra = {
            "example": {
                "descricao": "Deliciosa pizza de queijo + Borda recheada de requeijão + Massa integral",
                "preco": 35.50
            }
        }


class CardapioItem(BaseModel):
    """Item do cardápio"""
    nome: str
    preco: float
    tipo: str


class CardapioResponse(BaseModel):
    """Response com o cardápio completo"""
    pizzas: List[CardapioItem]
    acrescimos: List[CardapioItem]
