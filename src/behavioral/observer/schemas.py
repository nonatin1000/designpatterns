from pydantic import BaseModel, Field, EmailStr
from typing import List
from enum import Enum


class TipoAssinante(str, Enum):
    """Enum com os tipos de assinantes disponíveis"""
    CLIENTE = "cliente"
    FUNCIONARIO = "funcionario"
    PARCEIRO = "parceiro"
    FORNECEDOR = "fornecedor"


class AssinanteCreate(BaseModel):
    """Schema para criação de um novo assinante"""
    nome: str = Field(..., min_length=3, max_length=100, description="Nome do assinante")
    email: EmailStr = Field(..., description="Email do assinante")
    tipo: TipoAssinante = Field(..., description="Tipo de assinante")

    class Config:
        json_schema_extra = {
            "example": {
                "nome": "João Silva",
                "email": "joao.silva@email.com",
                "tipo": "cliente"
            }
        }


class AssinanteResponse(BaseModel):
    """Schema para response com dados do assinante"""
    nome: str
    email: str
    tipo: str

    class Config:
        json_schema_extra = {
            "example": {
                "nome": "João Silva",
                "email": "joao.silva@email.com",
                "tipo": "cliente"
            }
        }


class MensagemCreate(BaseModel):
    """Schema para criação de uma nova mensagem"""
    conteudo: str = Field(
        ...,
        min_length=10,
        max_length=1000,
        description="Conteúdo da mensagem a ser enviada"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "conteudo": "Novidade! Confira nossos novos produtos em promoção!"
            }
        }


class MensagemResponse(BaseModel):
    """Schema para response de mensagem enviada"""
    mensagem: str
    total_notificados: int
    assinantes_notificados: List[str]

    class Config:
        json_schema_extra = {
            "example": {
                "mensagem": "Novidade! Confira nossos novos produtos em promoção!",
                "total_notificados": 3,
                "assinantes_notificados": ["João Silva", "Maria Santos", "Tech Corp"]
            }
        }


class NewsletterStatus(BaseModel):
    """Schema para status da newsletter"""
    total_assinantes: int
    total_mensagens: int
    assinantes: List[dict]

    class Config:
        json_schema_extra = {
            "example": {
                "total_assinantes": 5,
                "total_mensagens": 3,
                "assinantes": [
                    {"nome": "João Silva", "email": "joao.silva@email.com"},
                    {"nome": "Maria Santos", "email": "maria.santos@email.com"}
                ]
            }
        }


class CancelarInscricaoRequest(BaseModel):
    """Schema para cancelamento de inscrição"""
    email: EmailStr = Field(..., description="Email do assinante a ser removido")

    class Config:
        json_schema_extra = {
            "example": {
                "email": "joao.silva@email.com"
            }
        }


class OperacaoResponse(BaseModel):
    """Schema genérico para responses de operações"""
    sucesso: bool
    mensagem: str

    class Config:
        json_schema_extra = {
            "example": {
                "sucesso": True,
                "mensagem": "Operação realizada com sucesso"
            }
        }
