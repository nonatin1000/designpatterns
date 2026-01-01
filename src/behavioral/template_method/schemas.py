"""Pydantic schemas for request/response validation in the Template Method pattern API."""

from pydantic import BaseModel, Field
from enum import Enum


class PaymentType(str, Enum):
    """Enumeration of available payment types."""

    CREDIT = "credit"
    DEBIT = "debit"
    CASH = "cash"


class PaymentRequest(BaseModel):
    """Schema for payment creation request."""

    amount: float = Field(
        ...,
        gt=0,
        description="Payment amount in Brazilian Reais (BRL)",
        example=1000.00
    )
    payment_type: PaymentType = Field(
        ...,
        description="Payment type (credit, debit, or cash)",
        example=PaymentType.CREDIT
    )

    class Config:
        json_schema_extra = {
            "example": {
                "amount": 1000.00,
                "payment_type": "credit"
            }
        }


class PaymentResponse(BaseModel):
    """Schema for payment response."""

    payment_type: str = Field(
        ...,
        description="Type of payment processed"
    )
    amount: float = Field(
        ...,
        description="Original payment amount in BRL"
    )
    tax: float = Field(
        ...,
        description="Gateway tax charged"
    )
    discount: float = Field(
        ...,
        description="Discount applied"
    )
    final_amount: float = Field(
        ...,
        description="Final amount charged (amount + tax - discount)"
    )
    success: bool = Field(
        ...,
        description="Whether payment was successful"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "payment_type": "Credit Card",
                "amount": 1000.00,
                "tax": 50.00,
                "discount": 20.00,
                "final_amount": 1030.00,
                "success": True
            }
        }


class PaymentComparisonRequest(BaseModel):
    """Schema for comparing payment methods."""

    amount: float = Field(
        ...,
        gt=0,
        description="Payment amount in BRL to compare",
        example=1000.00
    )


class PaymentMethodDetails(BaseModel):
    """Schema for individual payment method details."""

    method: str = Field(..., description="Payment method name")
    tax: float = Field(..., description="Gateway tax")
    discount: float = Field(..., description="Discount applied")
    final_amount: float = Field(..., description="Final amount to pay")


class PaymentComparisonResponse(BaseModel):
    """Schema for payment comparison response."""

    amount: float = Field(..., description="Original amount")
    credit: PaymentMethodDetails = Field(..., description="Credit card details")
    debit: PaymentMethodDetails = Field(..., description="Debit card details")
    cash: PaymentMethodDetails = Field(..., description="Cash payment details")
    best_option: str = Field(..., description="Best payment method (lowest final amount)")

    class Config:
        json_schema_extra = {
            "example": {
                "amount": 1000.00,
                "credit": {
                    "method": "Credit Card",
                    "tax": 50.00,
                    "discount": 20.00,
                    "final_amount": 1030.00
                },
                "debit": {
                    "method": "Debit Card",
                    "tax": 4.00,
                    "discount": 50.00,
                    "final_amount": 954.00
                },
                "cash": {
                    "method": "Cash",
                    "tax": 0.00,
                    "discount": 100.00,
                    "final_amount": 900.00
                },
                "best_option": "Cash"
            }
        }
