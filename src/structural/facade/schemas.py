"""Pydantic schemas for request/response validation in the Facade pattern API."""

from pydantic import BaseModel, Field, EmailStr
from typing import List
from enum import Enum


class PaymentMethod(str, Enum):
    """Enumeration of available payment methods."""
    CREDIT_CARD = "credit_card"
    BANK_SLIP = "bank_slip"


class CustomerCreate(BaseModel):
    """Schema for creating a new customer."""

    name: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="Customer's full name",
        example="Luiz da Silva"
    )
    tax_id: str = Field(
        ...,
        min_length=11,
        max_length=14,
        description="Tax ID (CPF in Brazil)",
        example="12345678910"
    )
    email: EmailStr = Field(
        ...,
        description="Customer's email address",
        example="luiz@email.com"
    )


class ProductCreate(BaseModel):
    """Schema for creating a new product."""

    name: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="Product name",
        example="Pink Blouse"
    )
    description: str = Field(
        ...,
        min_length=5,
        max_length=500,
        description="Product description",
        example="Women's pink blouse"
    )
    price: float = Field(
        ...,
        gt=0,
        description="Product price in BRL",
        example=80.99
    )


class ProductResponse(BaseModel):
    """Schema for product response."""

    name: str = Field(..., description="Product name")
    description: str = Field(..., description="Product description")
    price: float = Field(..., description="Product price")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Pink Blouse",
                "description": "Women's pink blouse",
                "price": 80.99
            }
        }


class CustomerResponse(BaseModel):
    """Schema for customer response."""

    name: str = Field(..., description="Customer name")
    tax_id: str = Field(..., description="Tax ID")
    email: str = Field(..., description="Email address")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Luiz da Silva",
                "tax_id": "12345678910",
                "email": "luiz@email.com"
            }
        }


class OrderCreate(BaseModel):
    """Schema for creating a new order."""

    customer: CustomerCreate = Field(..., description="Customer information")
    products: List[ProductCreate] = Field(
        ...,
        min_length=1,
        description="List of products (at least one required)"
    )


class OrderResponse(BaseModel):
    """Schema for order response."""

    order_id: int = Field(..., description="Unique order identifier")
    customer: CustomerResponse = Field(..., description="Customer details")
    products: List[ProductResponse] = Field(..., description="List of products")
    product_count: int = Field(..., description="Number of products")
    total_amount: float = Field(..., description="Total order amount")

    class Config:
        json_schema_extra = {
            "example": {
                "order_id": 1,
                "customer": {
                    "name": "Luiz da Silva",
                    "tax_id": "12345678910",
                    "email": "luiz@email.com"
                },
                "products": [
                    {
                        "name": "Pink Blouse",
                        "description": "Women's pink blouse",
                        "price": 80.99
                    }
                ],
                "product_count": 3,
                "total_amount": 250.79
            }
        }


class PaymentRequest(BaseModel):
    """Schema for payment processing request."""

    order_id: int = Field(
        ...,
        gt=0,
        description="Order ID to process payment for",
        example=1
    )
    payment_method: PaymentMethod = Field(
        ...,
        description="Payment method to use",
        example=PaymentMethod.CREDIT_CARD
    )


class PaymentResponse(BaseModel):
    """Schema for payment processing response."""

    success: bool = Field(..., description="Whether payment was successful")
    order_id: int = Field(..., description="Order ID")
    payment_method: str = Field(..., description="Payment method used")
    amount: float = Field(..., description="Amount paid")
    message: str = Field(..., description="Status message")

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "order_id": 1,
                "payment_method": "Credit Card",
                "amount": 250.79,
                "message": "Payment processed successfully"
            }
        }


class OrderListResponse(BaseModel):
    """Schema for listing all orders."""

    total_orders: int = Field(..., description="Total number of orders")
    orders: List[OrderResponse] = Field(..., description="List of orders")


class OrderAddProductRequest(BaseModel):
    """Schema for adding products to an existing order."""

    product: ProductCreate = Field(..., description="Product to add to the order")
