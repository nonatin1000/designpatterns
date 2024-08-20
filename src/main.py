from fastapi import FastAPI
from behavioral.strategy.main import router as order_router

app = FastAPI(
    title="API Design Patterns",
    description="Esta é a documentação da API de estudos de design patterns do curso Rabiscando Padrões de Projeto.",
    version="1.0.0",
)


app.include_router(order_router)


@app.get("/", tags=["Health"])
def health_check():
    return {"status": "Ok!"}
