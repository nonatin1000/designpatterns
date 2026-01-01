"""FastAPI application implementing the Strategy pattern for freight calculation.

This API demonstrates how the Strategy pattern allows changing freight
calculation algorithms at runtime without modifying the Order class.
"""

from fastapi import APIRouter, FastAPI, HTTPException
from .order import Order, ElectronicsOrder, FurnitureOrder
from .freight_strategy import CommonFreight, ExpressFreight
from .schemas import (
    OrderRequest,
    OrderResponse,
    FreightComparisonRequest,
    FreightComparisonResponse,
    FreightOption,
    OrderCategory,
    FreightType
)

# Helper functions shared by both router and app
def _create_order_logic(order_data: OrderRequest) -> OrderResponse:
    """Business logic for creating an order."""
    try:
        # Create appropriate order type (Context)
        if order_data.category == OrderCategory.ELECTRONICS:
            order = ElectronicsOrder()
        elif order_data.category == OrderCategory.FURNITURE:
            order = FurnitureOrder()
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid category: {order_data.category}"
            )

        # Set order amount
        order.amount = order_data.amount

        # Select and set freight strategy
        if order_data.freight_type == FreightType.COMMON:
            strategy = CommonFreight()
            freight_name = "Common Freight"
        elif order_data.freight_type == FreightType.EXPRESS:
            strategy = ExpressFreight()
            freight_name = "Express Freight"

            # Business rule: Furniture doesn't support express freight
            if order_data.category == OrderCategory.FURNITURE:
                raise HTTPException(
                    status_code=400,
                    detail="Express freight not available for furniture orders in this region"
                )
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid freight type: {order_data.freight_type}"
            )

        order.set_freight_strategy(strategy)

        # Calculate freight using the selected strategy
        freight_cost = order.calculate_freight()
        total = order.amount + freight_cost

        return OrderResponse(
            category=order.category,
            amount=order.amount,
            freight_type=freight_name,
            freight_cost=round(freight_cost, 2),
            total=round(total, 2)
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error creating order: {str(e)}"
        )


def _compare_freight_logic(request: FreightComparisonRequest) -> FreightComparisonResponse:
    """Business logic for comparing freight options."""
    try:
        # Create order based on category
        if request.category == OrderCategory.ELECTRONICS:
            order = ElectronicsOrder()
        elif request.category == OrderCategory.FURNITURE:
            order = FurnitureOrder()
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid category: {request.category}"
            )

        order.amount = request.amount

        # Calculate with Common Freight strategy
        order.set_freight_strategy(CommonFreight())
        common_cost = order.calculate_freight()
        common_total = order.amount + common_cost

        # Calculate with Express Freight strategy
        order.set_freight_strategy(ExpressFreight())
        express_cost = order.calculate_freight()
        express_total = order.amount + express_cost

        # Calculate savings
        savings = express_cost - common_cost

        return FreightComparisonResponse(
            category=order.category,
            amount=order.amount,
            common_freight=FreightOption(
                type="Common Freight",
                cost=round(common_cost, 2),
                percentage=5.0,
                total=round(common_total, 2)
            ),
            express_freight=FreightOption(
                type="Express Freight",
                cost=round(express_cost, 2),
                percentage=10.0,
                total=round(express_total, 2)
            ),
            savings=round(savings, 2)
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error comparing freight: {str(e)}"
        )


# Create router for inclusion in main app
router = APIRouter(prefix="/strategy", tags=["Strategy Pattern"])


@router.get("/")
async def router_root():
    """Get API information and available endpoints."""
    return {
        "message": "E-commerce Freight System - Strategy Pattern",
        "pattern": "Strategy",
        "description": "Defines a family of algorithms and makes them interchangeable",
        "order_categories": {
            "electronics": "Supports both common and express freight",
            "furniture": "Typically supports only common freight due to size/weight"
        },
        "freight_types": {
            "common": "5% of order value - Standard delivery",
            "express": "10% of order value - Fast delivery"
        },
        "endpoints": {
            "create_order": "/strategy/orders (POST)",
            "compare_freight": "/strategy/orders/compare-freight (POST)"
        }
    }


@router.post("/orders", response_model=OrderResponse, status_code=201)
async def router_create_order(order_data: OrderRequest):
    """Create an order with specified category and freight strategy."""
    return _create_order_logic(order_data)


@router.post("/orders/compare-freight", response_model=FreightComparisonResponse)
async def router_compare_freight(request: FreightComparisonRequest):
    """Compare freight costs between common and express options."""
    return _compare_freight_logic(request)


# Also create standalone app for independent use
app = FastAPI(
    title="E-commerce Freight - Strategy Pattern",
    description="API demonstrating the Strategy pattern for freight calculation",
    version="1.0.0"
)


@app.get("/", tags=["Root"])
async def root():
    """Get API information and available endpoints."""
    return {
        "message": "E-commerce Freight System - Strategy Pattern",
        "pattern": "Strategy",
        "description": "Defines a family of algorithms and makes them interchangeable",
        "order_categories": {
            "electronics": "Supports both common and express freight",
            "furniture": "Typically supports only common freight due to size/weight"
        },
        "freight_types": {
            "common": "5% of order value - Standard delivery",
            "express": "10% of order value - Fast delivery"
        },
        "endpoints": {
            "create_order": "/orders (POST)",
            "compare_freight": "/orders/compare-freight (POST)"
        }
    }


@app.post("/orders", response_model=OrderResponse, status_code=201, tags=["Orders"])
async def create_order(order_data: OrderRequest):
    """Create an order with specified category and freight strategy.

    The Strategy pattern allows the freight calculation algorithm to be
    selected at runtime. Different categories can use different strategies.
    """
    return _create_order_logic(order_data)


@app.post("/orders/compare-freight", response_model=FreightComparisonResponse, tags=["Orders"])
async def compare_freight_options(request: FreightComparisonRequest):
    """Compare freight costs between common and express options.

    This endpoint demonstrates the Strategy pattern by calculating
    the same order with different strategies and comparing results.
    """
    return _compare_freight_logic(request)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
