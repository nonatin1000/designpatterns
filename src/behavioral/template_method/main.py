from fastapi import APIRouter
from behavioral.template_method.model.payment_request import PaymentRequest
from behavioral.template_method.model.payment_response import PaymentResponse
from behavioral.template_method.service.payment_credit import PaymentCredit
from behavioral.template_method.service.gateway import Gateway
from behavioral.template_method.service.payment_cash import PaymentCash
from behavioral.template_method.service.payment_debit import PaymentDebit
from behavioral.template_method.enum import PaymentType

router = APIRouter(
    tags=["Pagamentos"],  # Alterar o nome do grupo
)


@router.post(
    "/payments",
    summary="Cria um pagamento com os tipos: credit, debit ou cash",
    description="Esse endpoint permite a criação de pagamentos.",
    response_model=PaymentResponse,
)
def create_payment(payment: PaymentRequest):
    """
    Cria um pagamento com base nas especificações fornecidas.

    - **amount**: O valor do pagamento.
    - **type_payment**: O tipo de pagamento ('credit', 'debit' ou 'cash').
    """
    gateway = Gateway()

    match payment.type_payment:
        case PaymentType.CREDIT:
            payment_exec = PaymentCredit(payment.amount, gateway)
        case PaymentType.DEBIT:
            payment_exec = PaymentDebit(payment.amount, gateway)
        case PaymentType.CASH:
            payment_exec = PaymentCash(payment.amount, gateway)
        case _:
            raise HTTPException(status_code=400, detail="Invalid payment type")

    is_pay, amount = payment_exec.execute_charge()
    return PaymentResponse(
        amount=amount,
        tax=payment_exec.calculate_tax(),
        discount=payment_exec.calculate_discount(),
        payment_type=payment.type_payment,
        is_pay=is_pay,
    )
