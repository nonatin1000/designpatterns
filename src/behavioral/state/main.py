from fastapi import FastAPI, HTTPException
from pedido import Pedido
from schemas import PedidoCreate, PedidoResponse, TransicaoResponse
from typing import Dict

app = FastAPI(
    title="E-commerce - Padrão State",
    description="API de pedidos implementando o padrão de projeto State",
    version="1.0.0"
)

# Armazena pedidos em memória
pedidos: Dict[int, Pedido] = {}


@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "E-commerce - Padrão State",
        "pattern": "State",
        "description": "Permite objeto alterar comportamento quando estado interno muda",
        "endpoints": {
            "criar_pedido": "/pedidos (POST)",
            "ver_pedido": "/pedidos/{id} (GET)",
            "pagar": "/pedidos/{id}/pagar (POST)",
            "cancelar": "/pedidos/{id}/cancelar (POST)",
            "despachar": "/pedidos/{id}/despachar (POST)"
        }
    }


@app.post("/pedidos", response_model=PedidoResponse, tags=["Pedidos"])
async def criar_pedido(pedido_data: PedidoCreate):
    """Cria novo pedido no estado inicial (Aguardando Pagamento)"""
    pedido = Pedido(itens=pedido_data.itens, valor_total=pedido_data.valor_total)
    pedidos[pedido.id_pedido] = pedido
    return pedido.get_info()


@app.get("/pedidos/{pedido_id}", response_model=PedidoResponse, tags=["Pedidos"])
async def obter_pedido(pedido_id: int):
    """Obtém informações de um pedido"""
    if pedido_id not in pedidos:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return pedidos[pedido_id].get_info()


@app.post("/pedidos/{pedido_id}/pagar", response_model=TransicaoResponse, tags=["Transições"])
async def pagar_pedido(pedido_id: int):
    """
    Transição: Sucesso ao Pagar

    Válido apenas se pedido está em "Aguardando Pagamento"
    Muda estado para "Pago"
    """
    if pedido_id not in pedidos:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    pedido = pedidos[pedido_id]
    estado_anterior = pedido.get_estado_nome()

    try:
        pedido.sucesso_ao_pagar()
        return TransicaoResponse(
            sucesso=True,
            mensagem="Pagamento processado com sucesso",
            estado_anterior=estado_anterior,
            estado_novo=pedido.get_estado_nome(),
            pedido_id=pedido_id
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/pedidos/{pedido_id}/cancelar", response_model=TransicaoResponse, tags=["Transições"])
async def cancelar_pedido(pedido_id: int):
    """
    Transição: Cancelar Pedido

    Válido se pedido está em "Aguardando Pagamento" ou "Pago"
    Muda estado para "Cancelado"
    """
    if pedido_id not in pedidos:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    pedido = pedidos[pedido_id]
    estado_anterior = pedido.get_estado_nome()

    try:
        pedido.cancelar_pedido()
        return TransicaoResponse(
            sucesso=True,
            mensagem="Pedido cancelado com sucesso",
            estado_anterior=estado_anterior,
            estado_novo=pedido.get_estado_nome(),
            pedido_id=pedido_id
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/pedidos/{pedido_id}/despachar", response_model=TransicaoResponse, tags=["Transições"])
async def despachar_pedido(pedido_id: int):
    """
    Transição: Despachar Pedido

    Válido apenas se pedido está "Pago"
    Muda estado para "Enviado"
    """
    if pedido_id not in pedidos:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    pedido = pedidos[pedido_id]
    estado_anterior = pedido.get_estado_nome()

    try:
        pedido.despachar_pedido()
        return TransicaoResponse(
            sucesso=True,
            mensagem="Pedido despachado para envio",
            estado_anterior=estado_anterior,
            estado_novo=pedido.get_estado_nome(),
            pedido_id=pedido_id
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/pedidos", tags=["Pedidos"])
async def listar_pedidos():
    """Lista todos os pedidos"""
    return {
        "total": len(pedidos),
        "pedidos": [p.get_info() for p in pedidos.values()]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
