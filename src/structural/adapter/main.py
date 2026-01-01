"""FastAPI application implementing the Adapter pattern for payment processing.

This API demonstrates how the Adapter pattern allows incompatible payment
gateway interfaces to work together through a common Gateway interface.

The Adapter pattern acts as a bridge between two incompatible interfaces,
allowing the client (Billing) to work with multiple payment gateways
without knowing their specific implementations.
"""

from fastapi import APIRouter, FastAPI, HTTPException
from typing import Dict, Any
from .billing import Billing
from .adapters import PagFacilAdapter, TopPagamentosAdapter
from .schemas import (
    PaymentRequest,
    PaymentResponse,
    PaymentHistoryResponse,
    StatisticsResponse,
    GatewayComparisonRequest,
    GatewayComparisonResponse,
    GatewayOption
)

# In-memory billing instance (in production, use dependency injection)
_billing: Billing = Billing()


# Helper functions for business logic
def _process_payment_logic(payment_data: PaymentRequest) -> PaymentResponse:
    """Business logic for processing a payment.

    Args:
        payment_data: Validated payment request data.

    Returns:
        PaymentResponse with complete payment details.

    Raises:
        HTTPException: If payment processing fails.
    """
    try:
        result = _billing.process_payment(
            amount=payment_data.amount,
            installments=payment_data.installments
        )
        return PaymentResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Payment processing error: {str(e)}"
        )


def _compare_gateways_logic(
    request: GatewayComparisonRequest
) -> GatewayComparisonResponse:
    """Business logic for comparing payment gateways.

    Args:
        request: Amount and installments to compare.

    Returns:
        GatewayComparisonResponse with detailed comparison.

    Raises:
        HTTPException: If comparison calculation fails.
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

        # Calculate fee breakdowns
        pag_facil_interest = pag_facil_fees - 0.40
        top_interest = top_fees - 5.00

        return GatewayComparisonResponse(
            amount=request.amount,
            installments=request.installments,
            pag_facil=GatewayOption(
                gateway="PagFacil",
                total_with_fees=round(pag_facil_total, 2),
                fees=round(pag_facil_fees, 2),
                fee_breakdown={
                    "fixed_fee": 0.40,
                    "interest": round(pag_facil_interest, 2)
                }
            ),
            top_pagamentos=GatewayOption(
                gateway="TopPagamentos",
                total_with_fees=round(top_total, 2),
                fees=round(top_fees, 2),
                fee_breakdown={
                    "fixed_fee": 5.00,
                    "interest": round(top_interest, 2)
                }
            ),
            recommended=recommended,
            savings=round(savings, 2)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Comparison error: {str(e)}"
        )


# Create router for inclusion in main app
router = APIRouter(prefix="/adapter", tags=["Adapter Pattern"])


@router.get("/")
async def router_root():
    """Get API information and available endpoints.

    Returns:
        Dictionary with API information, pattern description, and endpoints.
    """
    return {
        "message": "Payment Gateway System - Adapter Pattern",
        "pattern": "Adapter",
        "description": (
            "Allows incompatible interfaces to work together by creating "
            "adapters that translate between different interfaces."
        ),
        "gateways": {
            "PagFacil": {
                "fixed_fee": "R$ 0.40",
                "interest_rate": "5% per month",
                "best_for": "Cash payments (1 installment)"
            },
            "TopPagamentos": {
                "fixed_fee": "R$ 5.00",
                "interest_rate": "1% per month",
                "best_for": "Installment payments (2+ installments)"
            }
        },
        "selection_strategy": {
            "1_installment": "PagFacil (low fixed fee)",
            "2+_installments": "TopPagamentos (low interest rate)"
        },
        "endpoints": {
            "process_payment": "/adapter/payments (POST)",
            "compare_gateways": "/adapter/payments/compare (POST)",
            "payment_history": "/adapter/payments/history (GET)",
            "statistics": "/adapter/payments/statistics (GET)",
            "clear_history": "/adapter/payments/history (DELETE)"
        }
    }


@router.post("/payments", response_model=PaymentResponse, status_code=201)
async def router_process_payment(payment: PaymentRequest):
    """Process a payment using the most cost-effective gateway.

    The system automatically selects the best gateway based on the number
    of installments:
    - 1 installment: PagFacil (R$ 0.40 + 5% interest)
    - 2+ installments: TopPagamentos (R$ 5.00 + 1% interest)

    Args:
        payment: Payment details (amount and installments).

    Returns:
        Payment confirmation with fees and gateway used.

    Raises:
        HTTPException: If payment processing fails.
    """
    return _process_payment_logic(payment)


@router.post("/payments/compare", response_model=GatewayComparisonResponse)
async def router_compare_gateways(request: GatewayComparisonRequest):
    """Compare costs between PagFacil and TopPagamentos for a given payment.

    This endpoint helps users understand which gateway offers better rates
    for their specific payment scenario.

    Args:
        request: Amount and installments to compare.

    Returns:
        Detailed comparison of both gateways with recommendation.

    Raises:
        HTTPException: If comparison calculation fails.
    """
    return _compare_gateways_logic(request)


@router.get("/payments/history", response_model=PaymentHistoryResponse)
async def router_get_payment_history():
    """Get complete payment history.

    Returns:
        List of all processed payments with details.
    """
    history = _billing.get_payment_history()
    return PaymentHistoryResponse(
        total_payments=len(history),
        payments=history
    )


@router.get("/payments/statistics", response_model=StatisticsResponse)
async def router_get_statistics():
    """Get billing statistics including total fees and averages.

    Returns:
        Aggregated statistics about all processed payments.
    """
    stats = _billing.get_statistics()
    return StatisticsResponse(**stats)


@router.delete("/payments/history")
async def router_clear_payment_history():
    """Clear all payment history (useful for testing).

    Returns:
        Confirmation message with reset statistics.
    """
    global _billing
    _billing = Billing()
    return {
        "message": "Payment history cleared successfully",
        "total_payments": 0
    }


# Also create standalone app for independent use
app = FastAPI(
    title="Payment Gateway System - Adapter Pattern",
    description=(
        "API demonstrating the Adapter pattern with multiple payment gateways. "
        "The Adapter pattern allows incompatible interfaces to work together "
        "by creating adapters that translate between different interfaces."
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
        "message": "Payment Gateway System - Adapter Pattern",
        "pattern": "Adapter",
        "description": (
            "Allows incompatible interfaces to work together by creating "
            "adapters that translate between different interfaces."
        ),
        "gateways": {
            "PagFacil": {
                "fixed_fee": "R$ 0.40",
                "interest_rate": "5% per month",
                "best_for": "Cash payments (1 installment)"
            },
            "TopPagamentos": {
                "fixed_fee": "R$ 5.00",
                "interest_rate": "1% per month",
                "best_for": "Installment payments (2+ installments)"
            }
        },
        "selection_strategy": {
            "1_installment": "PagFacil (low fixed fee)",
            "2+_installments": "TopPagamentos (low interest rate)"
        },
        "endpoints": {
            "process_payment": "/payments (POST)",
            "compare_gateways": "/payments/compare (POST)",
            "payment_history": "/payments/history (GET)",
            "statistics": "/payments/statistics (GET)",
            "clear_history": "/payments/history (DELETE)"
        }
    }


@app.post("/payments", response_model=PaymentResponse, status_code=201, tags=["Payments"])
async def process_payment(payment: PaymentRequest):
    """Process a payment using the most cost-effective gateway.

    The system automatically selects the best gateway based on the number
    of installments:
    - 1 installment: PagFacil (R$ 0.40 + 5% interest)
    - 2+ installments: TopPagamentos (R$ 5.00 + 1% interest)

    Args:
        payment: Payment details (amount and installments).

    Returns:
        Payment confirmation with fees and gateway used.

    Raises:
        HTTPException: If payment processing fails.
    """
    return _process_payment_logic(payment)


@app.post("/payments/compare", response_model=GatewayComparisonResponse, tags=["Payments"])
async def compare_gateways(request: GatewayComparisonRequest):
    """Compare costs between PagFacil and TopPagamentos for a given payment.

    This endpoint helps users understand which gateway offers better rates
    for their specific payment scenario.

    Args:
        request: Amount and installments to compare.

    Returns:
        Detailed comparison of both gateways with recommendation.

    Raises:
        HTTPException: If comparison calculation fails.
    """
    return _compare_gateways_logic(request)


@app.get("/payments/history", response_model=PaymentHistoryResponse, tags=["Payments"])
async def get_payment_history():
    """Get complete payment history.

    Returns:
        List of all processed payments with details.
    """
    history = _billing.get_payment_history()
    return PaymentHistoryResponse(
        total_payments=len(history),
        payments=history
    )


@app.get("/payments/statistics", response_model=StatisticsResponse, tags=["Statistics"])
async def get_statistics():
    """Get billing statistics including total fees and averages.

    Returns:
        Aggregated statistics about all processed payments.
    """
    stats = _billing.get_statistics()
    return StatisticsResponse(**stats)


@app.delete("/payments/history", tags=["Payments"])
async def clear_payment_history():
    """Clear all payment history (useful for testing).

    Returns:
        Confirmation message with reset statistics.
    """
    global _billing
    _billing = Billing()
    return {
        "message": "Payment history cleared successfully",
        "total_payments": 0
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
