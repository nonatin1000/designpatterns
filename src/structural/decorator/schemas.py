"""Pydantic schemas for request/response validation in the Decorator pattern API.

This module defines all Pydantic models used for request validation and
response serialization in the Decorator pattern FastAPI endpoints.
"""

from pydantic import BaseModel, Field
from typing import List
from enum import Enum


class PizzaType(str, Enum):
    """Enum with available pizza types."""

    CHICKEN = "chicken"
    PEPPERONI = "pepperoni"
    CHEESE = "cheese"


class ToppingType(str, Enum):
    """Enum with available topping types."""

    STUFFED_CRUST = "stuffed_crust"
    WHOLE_WHEAT_CRUST = "whole_wheat_crust"


class PizzaOrderRequest(BaseModel):
    """Schema for pizza order request.

    This schema validates the input data when creating a custom pizza.
    The Decorator pattern will be applied to add toppings to the base pizza.

    Attributes:
        pizza_type: Type of base pizza to create.
        toppings: List of toppings to add (decorators to apply).

    Example:
        {
            "pizza_type": "cheese",
            "toppings": ["stuffed_crust", "whole_wheat_crust"]
        }
    """

    pizza_type: PizzaType = Field(
        ...,
        description="Type of base pizza",
        example=PizzaType.CHEESE
    )
    toppings: List[ToppingType] = Field(
        default=[],
        description="List of toppings to add to the pizza",
        example=[ToppingType.STUFFED_CRUST, ToppingType.WHOLE_WHEAT_CRUST]
    )

    class Config:
        """Pydantic configuration for this model."""
        json_schema_extra = {
            "example": {
                "pizza_type": "cheese",
                "toppings": ["stuffed_crust", "whole_wheat_crust"]
            }
        }


class PizzaResponse(BaseModel):
    """Schema for pizza response.

    This schema represents the complete pizza information after applying
    all decorators (toppings). It includes the full description and total price.

    Attributes:
        description: Complete description of the pizza with all toppings.
        price: Total price including base pizza and all toppings.
    """

    description: str = Field(
        ...,
        description="Complete description of the pizza with all toppings"
    )
    price: float = Field(
        ...,
        description="Total price of the pizza including all toppings",
        ge=0
    )

    class Config:
        """Pydantic configuration for this model."""
        json_schema_extra = {
            "example": {
                "description": (
                    "Delicious cheese pizza + Stuffed crust with cream cheese "
                    "+ Whole wheat crust"
                ),
                "price": 35.50
            }
        }


class MenuItem(BaseModel):
    """Schema for a menu item (pizza or topping)."""

    name: str = Field(..., description="Name of the item")
    price: float = Field(..., description="Price in BRL", ge=0)
    type: str = Field(..., description="Type identifier")


class MenuResponse(BaseModel):
    """Schema for complete menu response.

    This schema represents the full menu with all available pizzas and toppings.

    Attributes:
        pizzas: List of available base pizzas.
        toppings: List of available toppings (decorators).
    """

    pizzas: List[MenuItem] = Field(..., description="List of available pizzas")
    toppings: List[MenuItem] = Field(..., description="List of available toppings")
