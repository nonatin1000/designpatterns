"""FastAPI application implementing the Decorator pattern for pizza customization.

This API demonstrates how the Decorator pattern allows attaching additional
responsibilities to objects dynamically. Pizzas can be decorated with toppings
at runtime without modifying the original pizza classes.

The Decorator pattern provides a flexible alternative to subclassing for
extending functionality, avoiding class explosion from creating subclasses
for every possible combination.
"""

from fastapi import APIRouter, FastAPI, HTTPException
from typing import Dict, Any
from .pizza import Pizza
from .pizzas_concretas import ChickenPizza, PepperoniPizza, CheesePizza
from .concrete_toppings import StuffedCrust, WholeWheatCrust
from .schemas import (
    PizzaOrderRequest,
    PizzaResponse,
    PizzaType,
    ToppingType,
    MenuResponse,
    MenuItem
)


# Helper functions for business logic
def _create_base_pizza(pizza_type: PizzaType) -> Pizza:
    """Create a base pizza instance.

    Args:
        pizza_type: Type of pizza to create.

    Returns:
        A Pizza instance (concrete component).

    Raises:
        ValueError: If pizza type is invalid.
    """
    pizzas: Dict[PizzaType, type] = {
        PizzaType.CHICKEN: ChickenPizza,
        PizzaType.PEPPERONI: PepperoniPizza,
        PizzaType.CHEESE: CheesePizza,
    }

    pizza_class = pizzas.get(pizza_type)
    if not pizza_class:
        raise ValueError(f"Invalid pizza type: {pizza_type}")

    return pizza_class()


def _apply_toppings(pizza: Pizza, toppings: list[ToppingType]) -> Pizza:
    """Apply decorators (toppings) to a pizza.

    Each topping wraps the pizza, creating a chain of decorators.
    The order of toppings matters - they are applied in the order provided.

    Args:
        pizza: The base pizza to decorate.
        toppings: List of toppings to apply.

    Returns:
        The decorated pizza with all toppings applied.

    Note:
        This function demonstrates the Decorator pattern in action.
        Each decorator wraps the previous component, allowing dynamic composition.
    """
    decorators: Dict[ToppingType, type] = {
        ToppingType.STUFFED_CRUST: StuffedCrust,
        ToppingType.WHOLE_WHEAT_CRUST: WholeWheatCrust,
    }

    decorated_pizza = pizza
    for topping in toppings:
        decorator_class = decorators.get(topping)
        if decorator_class:
            decorated_pizza = decorator_class(decorated_pizza)

    return decorated_pizza


def _create_pizza_logic(order_data: PizzaOrderRequest) -> PizzaResponse:
    """Business logic for creating a custom pizza.

    Args:
        order_data: Validated pizza order data.

    Returns:
        PizzaResponse with complete pizza information.

    Raises:
        HTTPException: If pizza creation fails.
    """
    try:
        # Create base pizza (Component)
        pizza = _create_base_pizza(order_data.pizza_type)

        # Apply decorators (toppings)
        decorated_pizza = _apply_toppings(pizza, order_data.toppings)

        # Return decorated pizza with description and total price
        return PizzaResponse(
            description=decorated_pizza.get_description(),
            price=decorated_pizza.get_price()
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error creating pizza: {str(e)}"
        )


# Create router for inclusion in main app
router = APIRouter(prefix="/decorator", tags=["Decorator Pattern"])


@router.get("/")
async def router_root():
    """Get API information and available endpoints.

    Returns:
        Dictionary with API information, pattern description, and endpoints.
    """
    return {
        "message": "Pizzeria System - Decorator Pattern",
        "pattern": "Decorator",
        "description": (
            "Attaches additional responsibilities to objects dynamically. "
            "Decorators provide a flexible alternative to subclassing for "
            "extending functionality."
        ),
        "pizzas": {
            "chicken": "R$ 19.00 - Delicious chicken pizza",
            "pepperoni": "R$ 25.00 - Delicious pepperoni pizza",
            "cheese": "R$ 22.00 - Delicious cheese pizza"
        },
        "toppings": {
            "stuffed_crust": "R$ 8.50 - Stuffed crust with cream cheese",
            "whole_wheat_crust": "R$ 5.00 - Whole wheat crust"
        },
        "endpoints": {
            "menu": "/decorator/menu (GET)",
            "create_pizza": "/decorator/pizza (POST)",
            "example_pizza": "/decorator/pizza/example/{pizza_type} (GET)"
        }
    }


@router.get("/menu", response_model=MenuResponse)
async def router_get_menu():
    """Get complete pizzeria menu.

    Returns:
        MenuResponse with all available pizzas and toppings.
    """
    return MenuResponse(
        pizzas=[
            MenuItem(name="Chicken Pizza", price=19.00, type="chicken"),
            MenuItem(name="Pepperoni Pizza", price=25.00, type="pepperoni"),
            MenuItem(name="Cheese Pizza", price=22.00, type="cheese"),
        ],
        toppings=[
            MenuItem(
                name="Stuffed crust with cream cheese",
                price=8.50,
                type="stuffed_crust"
            ),
            MenuItem(
                name="Whole wheat crust",
                price=5.00,
                type="whole_wheat_crust"
            ),
        ]
    )


@router.post("/pizza", response_model=PizzaResponse, status_code=201)
async def router_create_pizza(order: PizzaOrderRequest):
    """Create a custom pizza with toppings using the Decorator pattern.

    The Decorator pattern allows adding responsibilities to objects dynamically.
    Here, each topping (decorator) wraps the pizza, adding functionality
    (description and price) without modifying the original pizza classes.

    Example flow:
    1. Create a CheesePizza (R$ 22.00)
    2. Wrap with StuffedCrust (+ R$ 8.50)
    3. Wrap with WholeWheatCrust (+ R$ 5.00)
    4. Total: R$ 35.50

    Args:
        order: Pizza order details (pizza type and toppings).

    Returns:
        PizzaResponse with complete description and total price.

    Raises:
        HTTPException: If pizza creation fails.
    """
    return _create_pizza_logic(order)


@router.get("/pizza/example/{pizza_type}", response_model=PizzaResponse)
async def router_example_pizza(pizza_type: PizzaType):
    """Get an example pizza with all available toppings.

    This endpoint demonstrates the Decorator pattern by applying all
    available decorators to a base pizza.

    Args:
        pizza_type: Type of base pizza to use.

    Returns:
        PizzaResponse with all toppings applied.

    Raises:
        HTTPException: If pizza creation fails.
    """
    try:
        pizza = _create_base_pizza(pizza_type)
        pizza_with_all_toppings = _apply_toppings(
            pizza,
            [ToppingType.STUFFED_CRUST, ToppingType.WHOLE_WHEAT_CRUST]
        )

        return PizzaResponse(
            description=pizza_with_all_toppings.get_description(),
            price=pizza_with_all_toppings.get_price()
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error creating example pizza: {str(e)}"
        )


# Also create standalone app for independent use
app = FastAPI(
    title="Pizzeria System - Decorator Pattern",
    description=(
        "API demonstrating the Decorator pattern for pizza customization. "
        "The Decorator pattern allows attaching additional responsibilities "
        "to objects dynamically."
    ),
    version="1.0.0"
)


@app.get("/", tags=["Root"])
async def root():
    """Get API information and available endpoints.

    Returns:
        Dictionary with API information, pattern description, and endpoints.
    """
    return {
        "message": "Pizzeria System - Decorator Pattern",
        "pattern": "Decorator",
        "description": (
            "Attaches additional responsibilities to objects dynamically. "
            "Decorators provide a flexible alternative to subclassing for "
            "extending functionality."
        ),
        "pizzas": {
            "chicken": "R$ 19.00 - Delicious chicken pizza",
            "pepperoni": "R$ 25.00 - Delicious pepperoni pizza",
            "cheese": "R$ 22.00 - Delicious cheese pizza"
        },
        "toppings": {
            "stuffed_crust": "R$ 8.50 - Stuffed crust with cream cheese",
            "whole_wheat_crust": "R$ 5.00 - Whole wheat crust"
        },
        "endpoints": {
            "menu": "/menu (GET)",
            "create_pizza": "/pizza (POST)",
            "example_pizza": "/pizza/example/{pizza_type} (GET)"
        }
    }


@app.get("/menu", response_model=MenuResponse, tags=["Menu"])
async def get_menu():
    """Get complete pizzeria menu.

    Returns:
        MenuResponse with all available pizzas and toppings.
    """
    return MenuResponse(
        pizzas=[
            MenuItem(name="Chicken Pizza", price=19.00, type="chicken"),
            MenuItem(name="Pepperoni Pizza", price=25.00, type="pepperoni"),
            MenuItem(name="Cheese Pizza", price=22.00, type="cheese"),
        ],
        toppings=[
            MenuItem(
                name="Stuffed crust with cream cheese",
                price=8.50,
                type="stuffed_crust"
            ),
            MenuItem(
                name="Whole wheat crust",
                price=5.00,
                type="whole_wheat_crust"
            ),
        ]
    )


@app.post("/pizza", response_model=PizzaResponse, status_code=201, tags=["Pizzas"])
async def create_pizza(order: PizzaOrderRequest):
    """Create a custom pizza with toppings using the Decorator pattern.

    The Decorator pattern allows adding responsibilities to objects dynamically.
    Here, each topping (decorator) wraps the pizza, adding functionality
    (description and price) without modifying the original pizza classes.

    Args:
        order: Pizza order details (pizza type and toppings).

    Returns:
        PizzaResponse with complete description and total price.

    Raises:
        HTTPException: If pizza creation fails.
    """
    return _create_pizza_logic(order)


@app.get("/pizza/example/{pizza_type}", response_model=PizzaResponse, tags=["Pizzas"])
async def example_pizza(pizza_type: PizzaType):
    """Get an example pizza with all available toppings.

    This endpoint demonstrates the Decorator pattern by applying all
    available decorators to a base pizza.

    Args:
        pizza_type: Type of base pizza to use.

    Returns:
        PizzaResponse with all toppings applied.

    Raises:
        HTTPException: If pizza creation fails.
    """
    try:
        pizza = _create_base_pizza(pizza_type)
        pizza_with_all_toppings = _apply_toppings(
            pizza,
            [ToppingType.STUFFED_CRUST, ToppingType.WHOLE_WHEAT_CRUST]
        )

        return PizzaResponse(
            description=pizza_with_all_toppings.get_description(),
            price=pizza_with_all_toppings.get_price()
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error creating example pizza: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
