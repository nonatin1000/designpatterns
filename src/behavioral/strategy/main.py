from fastapi import APIRouter
from behavioral.strategy.service.order_eletronic import OrderElectronic
from behavioral.strategy.service.order_shower import OrderShower
from behavioral.strategy.service.freight_common import FreightCommon
from behavioral.strategy.service.freight_express import FreightExpress
from behavioral.strategy.model.order_request import OrderRequest
from behavioral.strategy.model.order_response import OrderResponse

router = APIRouter(
    tags=["Pedidos"],  # Alterar o nome do grupo
)


@router.post(
    "/orders",
    summary="Cria um pedido com o tipo e frete solicitados",
    description="Esse endpoint permite a criação de pedidos de eletrônicos ou banho, com frete comum ou expresso.",
    response_model=OrderResponse,
)
def create_order(order: OrderRequest):
    """
    Cria um pedido com base nas especificações fornecidas.

    - **name**: O tipo de pedido ('electronic' ou 'shower')
    - **amount**: O valor do pedido.
    - **type_freight**: O tipo de frete ('common' ou 'express').
    O tipo de frete expresso não é permitido para pedidos do tipo 'shower'.
    """

    # Seleciona o tipo de pedido
    if order.name == "electronic":
        order_instance = OrderElectronic()
    elif order.name == "shower":
        order_instance = OrderShower()

    order_instance.amount = order.amount

    # Configura o tipo de frete
    if order.type_freight == "common":
        order_instance.set_type_freight(FreightCommon())
    elif order.type_freight == "express":
        order_instance.set_type_freight(FreightExpress())

    # Calcula o frete
    calculated_freight = order_instance.calculate_freight()

    return OrderResponse(
        name=order.name,
        amount=order.amount,
        freight_type=order.type_freight,
        calculated_freight=f"{calculated_freight:.2f}",
    )
