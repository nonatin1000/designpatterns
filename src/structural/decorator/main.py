from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pizzas_concretas import PizzaFrango, PizzaCalabresa, PizzaQueijo
from decorators_concretos import BordaRequeijao, MassaIntegral
from schemas import (
    PedidoPizzaRequest,
    PizzaResponse,
    TipoPizza,
    TipoAcrescimo,
    CardapioResponse,
    CardapioItem
)
from pizza import Pizza

app = FastAPI(
    title="Pizzaria - Padrão Decorator",
    description="API de pizzaria implementando o padrão de projeto Decorator",
    version="1.0.0"
)


def criar_pizza_base(tipo: TipoPizza) -> Pizza:
    """Factory method para criar a pizza base"""
    pizzas = {
        TipoPizza.FRANGO: PizzaFrango,
        TipoPizza.CALABRESA: PizzaCalabresa,
        TipoPizza.QUEIJO: PizzaQueijo,
    }
    return pizzas[tipo]()


def aplicar_acrescimos(pizza: Pizza, acrescimos: list[TipoAcrescimo]) -> Pizza:
    """
    Aplica os decorators (acréscimos) à pizza.
    Cada acréscimo envolve a pizza anterior, criando uma cadeia de decorators.
    """
    decorators = {
        TipoAcrescimo.BORDA_REQUEIJAO: BordaRequeijao,
        TipoAcrescimo.MASSA_INTEGRAL: MassaIntegral,
    }

    pizza_decorada = pizza
    for acrescimo in acrescimos:
        decorator_class = decorators.get(acrescimo)
        if decorator_class:
            pizza_decorada = decorator_class(pizza_decorada)

    return pizza_decorada


@app.get("/", tags=["Root"])
async def root():
    """Endpoint raiz com informações da API"""
    return {
        "message": "Bem-vindo à Pizzaria - Padrão Decorator",
        "endpoints": {
            "cardapio": "/cardapio",
            "criar_pizza": "/pizza (POST)",
            "docs": "/docs"
        }
    }


@app.get("/cardapio", response_model=CardapioResponse, tags=["Cardápio"])
async def get_cardapio():
    """
    Retorna o cardápio completo da pizzaria.
    Lista todas as pizzas disponíveis e seus acréscimos.
    """
    return CardapioResponse(
        pizzas=[
            CardapioItem(nome="Pizza de Frango", preco=19.00, tipo="frango"),
            CardapioItem(nome="Pizza de Calabresa", preco=25.00, tipo="calabresa"),
            CardapioItem(nome="Pizza de Queijo", preco=22.00, tipo="queijo"),
        ],
        acrescimos=[
            CardapioItem(
                nome="Borda recheada com requeijão",
                preco=8.50,
                tipo="borda_requeijao"
            ),
            CardapioItem(
                nome="Massa Integral",
                preco=5.00,
                tipo="massa_integral"
            ),
        ]
    )


@app.post("/pizza", response_model=PizzaResponse, tags=["Pizzas"])
async def criar_pizza(pedido: PedidoPizzaRequest):
    """
    Cria uma pizza customizada aplicando o padrão Decorator.

    O padrão Decorator permite adicionar responsabilidades a um objeto
    dinamicamente. Aqui, cada acréscimo (decorator) envolve a pizza base,
    adicionando funcionalidade (descrição e preço) sem modificar a classe original.

    Exemplo de fluxo:
    1. Cria-se uma PizzaQueijo (R$ 22,00)
    2. Envolve-se com BordaRequeijao (+ R$ 8,50)
    3. Envolve-se com MassaIntegral (+ R$ 5,00)
    4. Total: R$ 35,50
    """
    try:
        # Cria a pizza base (Component)
        pizza = criar_pizza_base(pedido.tipo_pizza)

        # Aplica os decorators (acréscimos)
        pizza_final = aplicar_acrescimos(pizza, pedido.acrescimos)

        # Retorna a pizza decorada com descrição e preço totais
        return PizzaResponse(
            descricao=pizza_final.get_descricao(),
            preco=pizza_final.get_preco()
        )
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Erro ao criar pizza: {str(e)}"
        )


@app.get("/pizza/exemplo/{tipo}", response_model=PizzaResponse, tags=["Pizzas"])
async def exemplo_pizza_completa(tipo: TipoPizza):
    """
    Retorna um exemplo de pizza com todos os acréscimos disponíveis.
    Demonstra o padrão Decorator aplicando todos os decorators.
    """
    pizza = criar_pizza_base(tipo)
    pizza_completa = aplicar_acrescimos(
        pizza,
        [TipoAcrescimo.BORDA_REQUEIJAO, TipoAcrescimo.MASSA_INTEGRAL]
    )

    return PizzaResponse(
        descricao=pizza_completa.get_descricao(),
        preco=pizza_completa.get_preco()
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
