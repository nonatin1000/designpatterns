"""FastAPI application implementing the Adapter pattern for payment processing.

This API demonstrates how the Adapter pattern allows incompatible payment gateway
interfaces to work together through a common Gateway interface.
"""

from fastapi import FastAPI, HTTPException
from billing import Billing
from adapters import PagFacilAdapter, TopPagamentosAdapter
from schemas import (
    PaymentRequest,
    PaymentResponse,
    PaymentHistoryResponse,
    StatisticsResponse,
    GatewayComparisonRequest,
    GatewayComparisonResponse,
    GatewayOption
)

app = FastAPI(
    title="Payment Gateway - Adapter Pattern",
    description="API demonstrating the Adapter pattern with multiple payment gateways",
    version="1.0.0"
)

# Single billing instance to maintain payment history
billing = Billing()


@app.get("/", tags=["Root"])
async def root():
    """Get API information and available endpoints."""
    return {
        "message": "Payment Gateway - Adapter Pattern",
        "pattern": "Adapter",
        "description": "Allows incompatible interfaces to work together",
        "gateways": {
            "PagFacil": {
                "fixed_fee": "R$ 0.40",
                "interest_rate": "5% per month",
                "best_for": "Cash payments (1 installment)"
            },
            "TopPagamentos": {
                "fixed_fee": "R$ 5.00",
                "interest_rate": "1% per month",
                "best_for": "Installment payments (2+)"
            }
        },
        "endpoints": {
            "process_payment": "/payments (POST)",
            "compare_gateways": "/payments/compare (POST)",
            "payment_history": "/payments/history (GET)",
            "statistics": "/payments/statistics (GET)"
        }
    }


@app.post("/payments", response_model=PaymentResponse, tags=["Payments"])
async def process_payment(payment: PaymentRequest):
    """Process a payment using the most cost-effective gateway.

    The system automatically selects the best gateway:
    - 1 installment: PagFacil (R$ 0.40 + 5% interest)
    - 2+ installments: TopPagamentos (R$ 5.00 + 1% interest)

    Args:
        payment: Payment details (amount and installments)

    Returns:
        Payment confirmation with fees and gateway used

    Raises:
        HTTPException: If payment processing fails
    """
    try:
        result = billing.process_payment(
            amount=payment.amount,
            installments=payment.installments
        )
        return PaymentResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Payment processing error: {str(e)}")


@app.post("/payments/compare", response_model=GatewayComparisonResponse, tags=["Payments"])
async def compare_gateways(request: GatewayComparisonRequest):
    """Compare costs between PagFacil and TopPagamentos for a given payment.

    This endpoint helps users understand which gateway offers better rates
    for their specific payment scenario.

    Args:
        request: Amount and installments to compare

    Returns:
        Detailed comparison of both gateways with recommendation
    """
    try:
        # Calculate with PagFacil
        pag_facil = PagFacilAdapter()
        pag_facil.set_amount(request.amount)
        pag_facil.set_installments(request.installments)
        pag_facil_total = pag_facil.get_total_with_fees()
        pag_facil_fees = pag_facil_total - request.amount

        # Calculate with TopPagamentos
        top_pagamentos = TopPagamentosAdapter()
        top_pagamentos.set_amount(request.amount)
        top_pagamentos.set_installments(request.installments)
        top_total = top_pagamentos.get_total_with_fees()
        top_fees = top_total - request.amount

        # Determine best option
        if pag_facil_total < top_total:
            recommended = "PagFacil"
            savings = top_total - pag_facil_total
        else:
            recommended = "TopPagamentos"
            savings = pag_facil_total - top_total

        return GatewayComparisonResponse(
            amount=request.amount,
            installments=request.installments,
            pag_facil=GatewayOption(
                gateway="PagFacil",
                total_with_fees=round(pag_facil_total, 2),
                fees=round(pag_facil_fees, 2),
                fee_breakdown={
                    "fixed_fee": 0.40,
                    "interest": round(pag_facil_fees - 0.40, 2)
                }
            ),
            top_pagamentos=GatewayOption(
                gateway="TopPagamentos",
                total_with_fees=round(top_total, 2),
                fees=round(top_fees, 2),
                fee_breakdown={
                    "fixed_fee": 5.00,
                    "interest": round(top_fees - 5.00, 2)
                }
            ),
            recommended=recommended,
            savings=round(savings, 2)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Comparison error: {str(e)}")


@app.get("/payments/history", response_model=PaymentHistoryResponse, tags=["Payments"])
async def get_payment_history():
    """Get complete payment history.

    Returns:
        List of all processed payments with details
    """
    history = billing.get_payment_history()
    return PaymentHistoryResponse(
        total_payments=len(history),
        payments=history
    )


@app.get("/payments/statistics", response_model=StatisticsResponse, tags=["Statistics"])
async def get_statistics():
    """Get billing statistics including total fees and averages.

    Returns:
        Aggregated statistics about all processed payments
    """
    stats = billing.get_statistics()
    return StatisticsResponse(**stats)


@app.delete("/payments/history", tags=["Payments"])
async def clear_payment_history():
    """Clear all payment history (useful for testing).

    Returns:
        Confirmation message
    """
    global billing
    billing = Billing()
    return {
        "message": "Payment history cleared successfully",
        "total_payments": 0
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
