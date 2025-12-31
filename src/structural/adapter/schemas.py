"""Pydantic schemas for request/response validation in the Adapter pattern API."""

from pydantic import BaseModel, Field
from typing import List, Dict


class PaymentRequest(BaseModel):
    """Schema for payment processing request."""

    amount: float = Field(
        ...,
        gt=0,
        description="Payment amount in Brazilian Reais (BRL)",
        example=100.00
    )
    installments: int = Field(
        default=1,
        ge=1,
        le=12,
        description="Number of monthly installments (1-12)",
        example=1
    )


class PaymentResponse(BaseModel):
    """Schema for payment processing response."""

    success: bool = Field(
        ...,
        description="Whether the payment was processed successfully"
    )
    amount: float = Field(
        ...,
        description="Original payment amount"
    )
    installments: int = Field(
        ...,
        description="Number of installments"
    )
    gateway: str = Field(
        ...,
        description="Payment gateway used (PagFacil or TopPagamentos)"
    )
    total_with_fees: float = Field(
        ...,
        description="Total amount including processing fees"
    )
    fees: float = Field(
        ...,
        description="Total fees charged (fixed fee + interest)"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "amount": 100.00,
                "installments": 1,
                "gateway": "PagFacil",
                "total_with_fees": 105.40,
                "fees": 5.40
            }
        }


class PaymentHistoryResponse(BaseModel):
    """Schema for payment history response."""

    total_payments: int = Field(
        ...,
        description="Total number of payments processed"
    )
    payments: List[Dict] = Field(
        ...,
        description="List of all payment records"
    )


class StatisticsResponse(BaseModel):
    """Schema for billing statistics response."""

    total_payments: int = Field(
        ...,
        description="Total number of payments processed"
    )
    total_amount: float = Field(
        ...,
        description="Sum of all payment amounts"
    )
    total_fees: float = Field(
        ...,
        description="Sum of all fees charged"
    )
    avg_fee_percentage: float = Field(
        ...,
        description="Average fee percentage across all payments"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "total_payments": 10,
                "total_amount": 1500.00,
                "total_fees": 75.50,
                "avg_fee_percentage": 5.03
            }
        }


class GatewayComparisonRequest(BaseModel):
    """Schema for comparing payment gateways."""

    amount: float = Field(
        ...,
        gt=0,
        description="Payment amount to compare",
        example=100.00
    )
    installments: int = Field(
        ...,
        ge=1,
        le=12,
        description="Number of installments",
        example=3
    )


class GatewayOption(BaseModel):
    """Schema for a single gateway option in comparison."""

    gateway: str = Field(
        ...,
        description="Gateway name"
    )
    total_with_fees: float = Field(
        ...,
        description="Total cost with this gateway"
    )
    fees: float = Field(
        ...,
        description="Fees charged by this gateway"
    )
    fee_breakdown: Dict[str, float] = Field(
        ...,
        description="Breakdown of fees (fixed + interest)"
    )


class GatewayComparisonResponse(BaseModel):
    """Schema for gateway comparison response."""

    amount: float = Field(
        ...,
        description="Original amount"
    )
    installments: int = Field(
        ...,
        description="Number of installments"
    )
    pag_facil: GatewayOption = Field(
        ...,
        description="PagFacil option details"
    )
    top_pagamentos: GatewayOption = Field(
        ...,
        description="TopPagamentos option details"
    )
    recommended: str = Field(
        ...,
        description="Recommended gateway (lowest cost)"
    )
    savings: float = Field(
        ...,
        description="Amount saved by choosing recommended gateway"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "amount": 100.00,
                "installments": 3,
                "pag_facil": {
                    "gateway": "PagFacil",
                    "total_with_fees": 115.40,
                    "fees": 15.40,
                    "fee_breakdown": {
                        "fixed_fee": 0.40,
                        "interest": 15.00
                    }
                },
                "top_pagamentos": {
                    "gateway": "TopPagamentos",
                    "total_with_fees": 108.00,
                    "fees": 8.00,
                    "fee_breakdown": {
                        "fixed_fee": 5.00,
                        "interest": 3.00
                    }
                },
                "recommended": "TopPagamentos",
                "savings": 7.40
            }
        }
