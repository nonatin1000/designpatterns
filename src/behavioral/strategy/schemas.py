"""Pydantic schemas for request/response validation in the Strategy pattern API."""

from pydantic import BaseModel, Field
from enum import Enum


class OrderCategory(str, Enum):
    """Enumeration of available order categories."""
    ELECTRONICS = "electronics"
    FURNITURE = "furniture"


class FreightType(str, Enum):
    """Enumeration of available freight types."""
    COMMON = "common"
    EXPRESS = "express"


class OrderRequest(BaseModel):
    """Schema for order creation request."""

    category: OrderCategory = Field(
        ...,
        description="Order category (electronics or furniture)",
        example=OrderCategory.ELECTRONICS
    )
    amount: float = Field(
        ...,
        gt=0,
        description="Order amount in Brazilian Reais (BRL)",
        example=250.00
    )
    freight_type: FreightType = Field(
        ...,
        description="Freight type (common or express)",
        example=FreightType.COMMON
    )

    class Config:
        json_schema_extra = {
            "example": {
                "category": "electronics",
                "amount": 250.00,
                "freight_type": "common"
            }
        }


class OrderResponse(BaseModel):
    """Schema for order response."""

    category: str = Field(
        ...,
        description="Order category"
    )
    amount: float = Field(
        ...,
        description="Order amount in BRL"
    )
    freight_type: str = Field(
        ...,
        description="Freight type used"
    )
    freight_cost: float = Field(
        ...,
        description="Calculated freight cost"
    )
    total: float = Field(
        ...,
        description="Total amount (order + freight)"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "category": "Electronics",
                "amount": 250.00,
                "freight_type": "Common Freight",
                "freight_cost": 12.50,
                "total": 262.50
            }
        }


class FreightComparisonRequest(BaseModel):
    """Schema for comparing freight options."""

    category: OrderCategory = Field(
        ...,
        description="Order category",
        example=OrderCategory.ELECTRONICS
    )
    amount: float = Field(
        ...,
        gt=0,
        description="Order amount in BRL",
        example=250.00
    )


class FreightOption(BaseModel):
    """Schema for a single freight option."""

    type: str = Field(..., description="Freight type name")
    cost: float = Field(..., description="Freight cost")
    percentage: float = Field(..., description="Percentage of order amount")
    total: float = Field(..., description="Total (order + freight)")


class FreightComparisonResponse(BaseModel):
    """Schema for freight comparison response."""

    category: str = Field(..., description="Order category")
    amount: float = Field(..., description="Order amount")
    common_freight: FreightOption = Field(..., description="Common freight option")
    express_freight: FreightOption = Field(..., description="Express freight option")
    savings: float = Field(..., description="Savings by choosing common freight")

    class Config:
        json_schema_extra = {
            "example": {
                "category": "Electronics",
                "amount": 250.00,
                "common_freight": {
                    "type": "Common Freight",
                    "cost": 12.50,
                    "percentage": 5.0,
                    "total": 262.50
                },
                "express_freight": {
                    "type": "Express Freight",
                    "cost": 25.00,
                    "percentage": 10.0,
                    "total": 275.00
                },
                "savings": 12.50
            }
        }
