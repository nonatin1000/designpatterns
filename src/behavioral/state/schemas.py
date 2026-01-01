"""Pydantic schemas for request/response validation in the State pattern API.

This module defines all Pydantic models used for request validation and
response serialization in the State pattern FastAPI endpoints.
"""

from pydantic import BaseModel, Field, field_validator
from typing import List


class OrderCreate(BaseModel):
    """Schema for creating a new order.

    This schema validates the input data when creating a new order.
    The order will be created in the initial "Pending Payment" state.

    Attributes:
        items: List of item names in the order (minimum 1 item required).
        total_amount: Total order value in BRL (must be greater than 0).

    Example:
        {
            "items": ["Notebook", "Mouse"],
            "total_amount": 2500.00
        }
    """

    items: List[str] = Field(
        ...,
        min_length=1,
        description="List of items in the order (at least one item required)"
    )
    total_amount: float = Field(
        ...,
        gt=0,
        description="Total order value in BRL (must be greater than 0)"
    )

    @field_validator("items")
    @classmethod
    def validate_items_not_empty(cls, v: List[str]) -> List[str]:
        """Validate that items list is not empty and contains non-empty strings."""
        if not v:
            raise ValueError("Items list cannot be empty")
        if any(not item.strip() for item in v):
            raise ValueError("Items cannot be empty strings")
        return v

    class Config:
        """Pydantic configuration for this model."""
        json_schema_extra = {
            "example": {
                "items": ["Notebook", "Mouse"],
                "total_amount": 2500.00
            }
        }


class OrderResponse(BaseModel):
    """Schema for order response.

    This schema represents the complete order information returned by
    the API, including current state and transition history.

    Attributes:
        id: Unique order identifier.
        items: List of items in the order.
        total_amount: Total order value in BRL.
        current_state: Current state name (e.g., "Pending Payment", "Paid").
        created_at: Order creation timestamp in format "YYYY-MM-DD HH:MM:SS".
        history: List of state transitions with timestamps.
    """

    id: int = Field(..., description="Unique order identifier", ge=1)
    items: List[str] = Field(..., description="List of items in the order")
    total_amount: float = Field(..., description="Total order value in BRL", ge=0)
    current_state: str = Field(..., description="Current order state name")
    created_at: str = Field(..., description="Order creation timestamp")
    history: List[str] = Field(..., description="State transition history with timestamps")

    class Config:
        """Pydantic configuration for this model."""
        json_schema_extra = {
            "example": {
                "id": 1,
                "items": ["Notebook", "Mouse"],
                "total_amount": 2500.00,
                "current_state": "Pending Payment",
                "created_at": "2024-01-15 10:30:00",
                "history": [
                    "2024-01-15 10:30:00 - Pending Payment"
                ]
            }
        }


class TransitionResponse(BaseModel):
    """Schema for state transition response.

    This schema represents the result of a state transition operation
    (pay, cancel, or ship). It includes information about the transition
    success and the state change.

    Attributes:
        success: Whether the transition was successful.
        message: Human-readable message describing the transition result.
        previous_state: State name before the transition.
        new_state: State name after the transition.
        order_id: ID of the order that was transitioned.
    """

    success: bool = Field(..., description="Whether the transition was successful")
    message: str = Field(..., description="Human-readable transition result message")
    previous_state: str = Field(..., description="State name before the transition")
    new_state: str = Field(..., description="State name after the transition")
    order_id: int = Field(..., description="ID of the order that was transitioned", ge=1)

    class Config:
        """Pydantic configuration for this model."""
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Payment processed successfully",
                "previous_state": "Pending Payment",
                "new_state": "Paid",
                "order_id": 1
            }
        }
