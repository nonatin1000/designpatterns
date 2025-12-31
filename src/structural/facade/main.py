"""FastAPI application implementing the Facade pattern for sales system.

This API demonstrates how the Facade pattern simplifies interaction with
a complex subsystem (Order, Payment, Email) through a unified interface.
"""

from fastapi import FastAPI, HTTPException
from typing import Dict
from customer import Customer
from product import Product
from sales_facade import SalesFacade
from schemas import (
    OrderCreate,
    OrderResponse,
    OrderListResponse,
    PaymentRequest,
    PaymentResponse,
    PaymentMethod,
    CustomerResponse,
    ProductResponse,
    OrderAddProductRequest
)

app = FastAPI(
    title="E-commerce Sales - Facade Pattern",
    description="API demonstrating the Facade pattern for simplified sales processing",
    version="1.0.0"
)

# Store for active sales facades (in-memory)
# Key: order_id, Value: SalesFacade instance
sales_facades: Dict[int, SalesFacade] = {}
next_order_id = 1


@app.get("/", tags=["Root"])
async def root():
    """Get API information and available endpoints."""
    return {
        "message": "E-commerce Sales System - Facade Pattern",
        "pattern": "Facade",
        "description": "Provides a simplified interface to a complex subsystem",
        "subsystems": {
            "Order": "Manages customer orders and products",
            "Payment": "Processes credit card and bank slip payments",
            "Email": "Sends order notifications to customers"
        },
        "facade_benefits": [
            "Simplified interface for clients",
            "Reduced coupling between client and subsystems",
            "Easy to use without deep subsystem knowledge"
        ],
        "endpoints": {
            "create_order": "/orders (POST)",
            "get_order": "/orders/{order_id} (GET)",
            "list_orders": "/orders (GET)",
            "add_product": "/orders/{order_id}/products (POST)",
            "process_payment": "/orders/payment (POST)"
        }
    }


@app.post("/orders", response_model=OrderResponse, status_code=201, tags=["Orders"])
async def create_order(order_data: OrderCreate):
    """Create a new order using the SalesFacade.

    The facade simplifies order creation by handling:
    - Customer creation
    - Order initialization
    - Email service setup

    Args:
        order_data: Order information including customer and products

    Returns:
        Created order details
    """
    global next_order_id

    try:
        # Create customer
        customer = Customer(
            name=order_data.customer.name,
            tax_id=order_data.customer.tax_id,
            email=order_data.customer.email
        )

        # Create sales facade (this automatically creates Order and Email)
        facade = SalesFacade(customer)

        # Add products to the order through the facade
        for product_data in order_data.products:
            product = Product(
                name=product_data.name,
                description=product_data.description,
                price=product_data.price
            )
            facade.add_product(product)

        # Store facade with order ID
        order_id = next_order_id
        sales_facades[order_id] = facade
        next_order_id += 1

        # Build response
        return OrderResponse(
            order_id=order_id,
            customer=CustomerResponse(
                name=customer.name,
                tax_id=customer.tax_id,
                email=customer.email
            ),
            products=[
                ProductResponse(
                    name=p.name,
                    description=p.description,
                    price=p.price
                ) for p in facade.order.products
            ],
            product_count=facade.get_product_count(),
            total_amount=facade.get_order_total()
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating order: {str(e)}")


@app.get("/orders/{order_id}", response_model=OrderResponse, tags=["Orders"])
async def get_order(order_id: int):
    """Get order details by ID.

    Args:
        order_id: Order identifier

    Returns:
        Order details

    Raises:
        HTTPException: If order not found
    """
    if order_id not in sales_facades:
        raise HTTPException(status_code=404, detail="Order not found")

    facade = sales_facades[order_id]
    customer = facade.order.customer

    return OrderResponse(
        order_id=order_id,
        customer=CustomerResponse(
            name=customer.name,
            tax_id=customer.tax_id,
            email=customer.email
        ),
        products=[
            ProductResponse(
                name=p.name,
                description=p.description,
                price=p.price
            ) for p in facade.order.products
        ],
        product_count=facade.get_product_count(),
        total_amount=facade.get_order_total()
    )


@app.get("/orders", response_model=OrderListResponse, tags=["Orders"])
async def list_orders():
    """List all orders.

    Returns:
        List of all orders in the system
    """
    orders = []

    for order_id, facade in sales_facades.items():
        customer = facade.order.customer
        orders.append(
            OrderResponse(
                order_id=order_id,
                customer=CustomerResponse(
                    name=customer.name,
                    tax_id=customer.tax_id,
                    email=customer.email
                ),
                products=[
                    ProductResponse(
                        name=p.name,
                        description=p.description,
                        price=p.price
                    ) for p in facade.order.products
                ],
                product_count=facade.get_product_count(),
                total_amount=facade.get_order_total()
            )
        )

    return OrderListResponse(
        total_orders=len(orders),
        orders=orders
    )


@app.post("/orders/{order_id}/products", response_model=OrderResponse, tags=["Orders"])
async def add_product_to_order(order_id: int, request: OrderAddProductRequest):
    """Add a product to an existing order.

    Args:
        order_id: Order identifier
        request: Product to add

    Returns:
        Updated order details

    Raises:
        HTTPException: If order not found
    """
    if order_id not in sales_facades:
        raise HTTPException(status_code=404, detail="Order not found")

    facade = sales_facades[order_id]

    try:
        product = Product(
            name=request.product.name,
            description=request.product.description,
            price=request.product.price
        )
        facade.add_product(product)

        customer = facade.order.customer
        return OrderResponse(
            order_id=order_id,
            customer=CustomerResponse(
                name=customer.name,
                tax_id=customer.tax_id,
                email=customer.email
            ),
            products=[
                ProductResponse(
                    name=p.name,
                    description=p.description,
                    price=p.price
                ) for p in facade.order.products
            ],
            product_count=facade.get_product_count(),
            total_amount=facade.get_order_total()
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/orders/payment", response_model=PaymentResponse, tags=["Payments"])
async def process_payment(payment_data: PaymentRequest):
    """Process payment for an order using the SalesFacade.

    The facade simplifies payment processing by handling:
    - Payment creation (credit card or bank slip)
    - Payment processing
    - Email notification

    All in a single method call!

    Args:
        payment_data: Payment information

    Returns:
        Payment processing result

    Raises:
        HTTPException: If order not found or payment fails
    """
    order_id = payment_data.order_id

    if order_id not in sales_facades:
        raise HTTPException(status_code=404, detail="Order not found")

    facade = sales_facades[order_id]

    try:
        # Process payment through facade (automatically sends email)
        if payment_data.payment_method == PaymentMethod.CREDIT_CARD:
            success = facade.process_credit_card_order()
            payment_method_name = "Credit Card"
        elif payment_data.payment_method == PaymentMethod.BANK_SLIP:
            success = facade.process_bank_slip_order()
            payment_method_name = "Bank Slip"
        else:
            raise HTTPException(status_code=400, detail="Invalid payment method")

        if not success:
            raise HTTPException(status_code=500, detail="Payment processing failed")

        return PaymentResponse(
            success=success,
            order_id=order_id,
            payment_method=payment_method_name,
            amount=facade.get_order_total(),
            message=f"Payment processed successfully via {payment_method_name}"
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Payment error: {str(e)}")


@app.delete("/orders/{order_id}", tags=["Orders"])
async def delete_order(order_id: int):
    """Delete an order.

    Args:
        order_id: Order identifier

    Returns:
        Confirmation message

    Raises:
        HTTPException: If order not found
    """
    if order_id not in sales_facades:
        raise HTTPException(status_code=404, detail="Order not found")

    del sales_facades[order_id]

    return {
        "message": f"Order {order_id} deleted successfully",
        "order_id": order_id
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
