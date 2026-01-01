from fastapi import FastAPI
from behavioral.strategy.main import router as strategy_router
from behavioral.template_method.main import router as template_method_router
from behavioral.observer.main import router as observer_router
from behavioral.state.main import router as state_router
from structural.adapter.main import router as adapter_router
from structural.decorator.main import router as decorator_router
from structural.facade.main import router as facade_router

app = FastAPI(
    title="API Design Patterns",
    description=(
        "API documentation for design patterns studies from the course "
        "Rabiscando Padrões de Projeto."
    ),
    version="1.0.0",
)


app.include_router(strategy_router)
app.include_router(template_method_router)
app.include_router(observer_router)
app.include_router(state_router)
app.include_router(adapter_router)
app.include_router(decorator_router)
app.include_router(facade_router)


@app.get("/", tags=["Health"])
def health_check():
    return {"status": "Ok!"}
