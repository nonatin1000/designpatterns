"""FastAPI application implementing the Template Method pattern for payment processing.

This API demonstrates how the Template Method pattern allows defining the skeleton
of an algorithm (payment processing) while letting subclasses customize certain steps.
"""

from fastapi import APIRouter, FastAPI, HTTPException
from .payment import Payment, CreditPayment, DebitPayment, CashPayment
from .gateway import Gateway
from .schemas import (
    PaymentRequest,
    PaymentResponse,
    PaymentComparisonRequest,
    PaymentComparisonResponse,
    PaymentMethodDetails,
    PaymentType
)


# Helper functions shared by both router and app
def _process_payment_logic(payment_request: PaymentRequest) -> PaymentResponse:
    """Business logic for processing a payment."""
    try:
        gateway = Gateway()

        # Select payment type (Context selection)
        if payment_request.payment_type == PaymentType.CREDIT:
            payment: Payment = CreditPayment(payment_request.amount, gateway)
            payment_name = "Credit Card"
        elif payment_request.payment_type == PaymentType.DEBIT:
            payment = DebitPayment(payment_request.amount, gateway)
            payment_name = "Debit Card"
        elif payment_request.payment_type == PaymentType.CASH:
            payment = CashPayment(payment_request.amount, gateway)
            payment_name = "Cash"
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid payment type: {payment_request.payment_type}"
            )

        # Calculate values
        tax = payment.calculate_tax()
        discount = payment.calculate_discount()

        # Process payment (Template Method)
        success, final_amount = payment.process_payment()

        return PaymentResponse(
            payment_type=payment_name,
            amount=payment.amount,
            tax=round(tax, 2),
            discount=round(discount, 2),
            final_amount=round(final_amount, 2),
            success=success
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing payment: {str(e)}"
        )


def _compare_payments_logic(request: PaymentComparisonRequest) -> PaymentComparisonResponse:
    """Business logic for comparing payment methods."""
    try:
        gateway = Gateway()
        amount = request.amount

        # Calculate for Credit Card
        credit = CreditPayment(amount, gateway)
        credit_tax = credit.calculate_tax()
        credit_discount = credit.calculate_discount()
        credit_final = amount + credit_tax - credit_discount

        # Calculate for Debit Card
        debit = DebitPayment(amount, gateway)
        debit_tax = debit.calculate_tax()
        debit_discount = debit.calculate_discount()
        debit_final = amount + debit_tax - debit_discount

        # Calculate for Cash
        cash = CashPayment(amount, gateway)
        cash_tax = cash.calculate_tax()
        cash_discount = cash.calculate_discount()
        cash_final = amount + cash_tax - cash_discount

        # Determine best option (lowest final amount)
        options = {
            "Credit Card": credit_final,
            "Debit Card": debit_final,
            "Cash": cash_final
        }
        best_option = min(options, key=options.get)

        return PaymentComparisonResponse(
            amount=amount,
            credit=PaymentMethodDetails(
                method="Credit Card",
                tax=round(credit_tax, 2),
                discount=round(credit_discount, 2),
                final_amount=round(credit_final, 2)
            ),
            debit=PaymentMethodDetails(
                method="Debit Card",
                tax=round(debit_tax, 2),
                discount=round(debit_discount, 2),
                final_amount=round(debit_final, 2)
            ),
            cash=PaymentMethodDetails(
                method="Cash",
                tax=round(cash_tax, 2),
                discount=round(cash_discount, 2),
                final_amount=round(cash_final, 2)
            ),
            best_option=best_option
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error comparing payments: {str(e)}"
        )


# Create router for inclusion in main app
router = APIRouter(prefix="/template-method", tags=["Template Method Pattern"])


@router.get("/")
async def router_root():
    """Get API information and available endpoints."""
    return {
        "message": "Payment Processing System - Template Method Pattern",
        "pattern": "Template Method",
        "description": "Defines algorithm skeleton, deferring steps to subclasses",
        "payment_types": {
            "credit": "Credit card - 5% tax, 2% discount (if > R$ 300)",
            "debit": "Debit card - R$ 4 fixed tax, 5% discount",
            "cash": "Cash - No tax, 10% discount (best option!)"
        },
        "endpoints": {
            "process_payment": "/template-method/payments (POST)",
            "compare_methods": "/template-method/payments/compare (POST)"
        }
    }


@router.post("/payments", response_model=PaymentResponse, status_code=201)
async def router_process_payment(payment_request: PaymentRequest):
    """Process a payment with the specified method."""
    return _process_payment_logic(payment_request)


@router.post("/payments/compare", response_model=PaymentComparisonResponse)
async def router_compare_payments(request: PaymentComparisonRequest):
    """Compare all payment methods for a given amount."""
    return _compare_payments_logic(request)


# Also create standalone app for independent use
app = FastAPI(
    title="Payment Processing - Template Method Pattern",
    description="API demonstrating the Template Method pattern for payment processing",
    version="1.0.0"
)


@app.get("/", tags=["Root"])
async def root():
    """Get API information and available endpoints."""
    return {
        "message": "Payment Processing System - Template Method Pattern",
        "pattern": "Template Method",
        "description": "Defines algorithm skeleton, deferring steps to subclasses",
        "payment_types": {
            "credit": "Credit card - 5% tax, 2% discount (if > R$ 300)",
            "debit": "Debit card - R$ 4 fixed tax, 5% discount",
            "cash": "Cash - No tax, 10% discount (best option!)"
        },
        "algorithm_steps": {
            "1": "Calculate tax (hook - can be overridden)",
            "2": "Calculate discount (abstract - must be implemented)",
            "3": "Compute final amount (amount + tax - discount)",
            "4": "Process charge through gateway"
        },
        "endpoints": {
            "process_payment": "/payments (POST)",
            "compare_methods": "/payments/compare (POST)"
        }
    }


@app.post("/payments", response_model=PaymentResponse, status_code=201, tags=["Payments"])
async def process_payment(payment_request: PaymentRequest):
    """Process a payment with the specified method.

    The Template Method pattern ensures all payments follow the same algorithm:
    1. Calculate tax (varies by payment type)
    2. Calculate discount (varies by payment type)
    3. Compute final amount
    4. Process through gateway
    """
    return _process_payment_logic(payment_request)


@app.post("/payments/compare", response_model=PaymentComparisonResponse, tags=["Payments"])
async def compare_payments(request: PaymentComparisonRequest):
    """Compare all payment methods for a given amount.

    This endpoint demonstrates how different concrete implementations
    (CreditPayment, DebitPayment, CashPayment) customize the algorithm
    steps while following the same template.
    """
    return _compare_payments_logic(request)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
