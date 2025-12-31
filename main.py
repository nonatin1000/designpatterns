"""Main FastAPI application aggregating all design patterns.

This application provides a unified API interface for all implemented
design patterns, making them accessible through a single Swagger UI.
"""

import sys
from pathlib import Path

# Add src directories to Python path
base_path = Path(__file__).parent
sys.path.insert(0, str(base_path / "src" / "structural" / "decorator"))
sys.path.insert(0, str(base_path / "src" / "behavioral" / "observer"))
sys.path.insert(0, str(base_path / "src" / "behavioral" / "state"))
sys.path.insert(0, str(base_path / "src" / "structural" / "adapter"))
sys.path.insert(0, str(base_path / "src" / "structural" / "facade"))

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

app = FastAPI(
    title="Design Patterns - Complete API",
    description="""
## Design Patterns API Collection

This API showcases various design patterns from "Rabiscando Padrões de Projeto".

### 🎯 Behavioral Patterns
- **Decorator** - Add responsibilities dynamically (Pizzeria)
- **Observer** - One-to-many dependency (Newsletter)
- **State** - Behavior changes with state (Order lifecycle)

### 🏗️ Structural Patterns
- **Adapter** - Interface compatibility (Payment gateways)
- **Facade** - Simplified interface (Sales system)

### 📖 How to Use
Each pattern has its own set of endpoints. Click on the sections below to explore!
    """,
    version="1.0.0"
)


@app.get("/", tags=["📚 Home"])
async def root():
    """Welcome endpoint with navigation guide.

    IMPORTANT: Each pattern has its own Swagger documentation!
    Access /decorator/docs, /facade/docs, etc. to see all endpoints.
    """
    return {
        "message": "Design Patterns - Complete API",
        "version": "1.0.0",
        "main_docs": "http://localhost:8000/docs (this page - shows only overview)",
        "important": "Each pattern has its own Swagger UI - see links below!",
        "patterns": {
            "decorator": {
                "name": "🍕 Decorator Pattern",
                "description": "Pizzeria with dynamic toppings",
                "swagger_ui": "http://localhost:8000/decorator/docs",
                "base_url": "/decorator",
                "example_endpoints": [
                    "GET /decorator/cardapio",
                    "POST /decorator/pizza"
                ]
            },
            "observer": {
                "name": "📧 Observer Pattern",
                "description": "Newsletter with subscribers",
                "swagger_ui": "http://localhost:8000/observer/docs",
                "base_url": "/observer",
                "example_endpoints": [
                    "POST /observer/assinantes",
                    "POST /observer/mensagens"
                ]
            },
            "state": {
                "name": "🔄 State Pattern",
                "description": "E-commerce order states",
                "swagger_ui": "http://localhost:8000/state/docs",
                "base_url": "/state",
                "example_endpoints": [
                    "POST /state/pedidos",
                    "POST /state/pedidos/{id}/pagar"
                ]
            },
            "adapter": {
                "name": "🔌 Adapter Pattern",
                "description": "Payment gateway integration",
                "swagger_ui": "http://localhost:8000/adapter/docs",
                "base_url": "/adapter",
                "example_endpoints": [
                    "POST /adapter/payments",
                    "POST /adapter/payments/compare"
                ]
            },
            "facade": {
                "name": "🏢 Facade Pattern",
                "description": "Simplified sales system",
                "swagger_ui": "http://localhost:8000/facade/docs",
                "base_url": "/facade",
                "example_endpoints": [
                    "POST /facade/orders",
                    "POST /facade/orders/payment"
                ]
            }
        },
        "how_to_use": {
            "1": "Main API shows only this overview endpoint",
            "2": "Each pattern has its OWN Swagger documentation",
            "3": "Click on swagger_ui links above to see each pattern's endpoints",
            "4": "Example: http://localhost:8000/facade/docs shows Facade endpoints"
        }
    }


# Import and mount sub-applications
print("\nLoading design patterns...")

# Decorator Pattern
try:
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "decorator_main",
        base_path / "src" / "structural" / "decorator" / "main.py"
    )
    decorator_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(decorator_module)
    app.mount("/decorator", decorator_module.app)
    print("✓ Decorator Pattern loaded")
except Exception as e:
    print(f"✗ Decorator Pattern: {e}")

# Observer Pattern
try:
    spec = importlib.util.spec_from_file_location(
        "observer_main",
        base_path / "src" / "behavioral" / "observer" / "main.py"
    )
    observer_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(observer_module)
    app.mount("/observer", observer_module.app)
    print("✓ Observer Pattern loaded")
except Exception as e:
    print(f"✗ Observer Pattern: {e}")

# State Pattern
try:
    spec = importlib.util.spec_from_file_location(
        "state_main",
        base_path / "src" / "behavioral" / "state" / "main.py"
    )
    state_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(state_module)
    app.mount("/state", state_module.app)
    print("✓ State Pattern loaded")
except Exception as e:
    print(f"✗ State Pattern: {e}")

# Adapter Pattern
try:
    spec = importlib.util.spec_from_file_location(
        "adapter_main",
        base_path / "src" / "structural" / "adapter" / "main.py"
    )
    adapter_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(adapter_module)
    app.mount("/adapter", adapter_module.app)
    print("✓ Adapter Pattern loaded")
except Exception as e:
    print(f"✗ Adapter Pattern: {e}")

# Facade Pattern
try:
    spec = importlib.util.spec_from_file_location(
        "facade_main",
        base_path / "src" / "structural" / "facade" / "main.py"
    )
    facade_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(facade_module)
    app.mount("/facade", facade_module.app)
    print("✓ Facade Pattern loaded")
except Exception as e:
    print(f"✗ Facade Pattern: {e}")


if __name__ == "__main__":
    import uvicorn

    print("\n" + "=" * 70)
    print(" " * 20 + "DESIGN PATTERNS API")
    print("=" * 70)
    print("\n📚 All patterns available at:")
    print("   Swagger UI: http://localhost:8000/docs")
    print("   ReDoc:      http://localhost:8000/redoc")
    print("\n🎯 Individual pattern endpoints:")
    print("   Decorator: http://localhost:8000/decorator/docs")
    print("   Observer:  http://localhost:8000/observer/docs")
    print("   State:     http://localhost:8000/state/docs")
    print("   Adapter:   http://localhost:8000/adapter/docs")
    print("   Facade:    http://localhost:8000/facade/docs")
    print("=" * 70 + "\n")

    uvicorn.run(app, host="0.0.0.0", port=8000)
