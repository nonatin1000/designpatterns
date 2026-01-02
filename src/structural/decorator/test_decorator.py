"""Comprehensive tests for Decorator pattern implementation."""

import sys
from pathlib import Path

# Add src directory to path for standalone execution
if __name__ == "__main__":
    src_dir = Path(__file__).parent.parent.parent
    sys.path.insert(0, str(src_dir))

try:
    # Try relative imports first
    from .pizza import Pizza
    from .pizzas_concretas import ChickenPizza, PepperoniPizza, CheesePizza
    from .topping_decorator import ToppingDecorator
    from .concrete_toppings import StuffedCrust, WholeWheatCrust
except ImportError:
    # Fall back to direct module imports
    import importlib.util
    import types
    test_dir = Path(__file__).parent
    
    # Create module structure
    structural = types.ModuleType("structural")
    structural_decorator = types.ModuleType("structural.decorator")
    sys.modules["structural"] = structural
    sys.modules["structural.decorator"] = structural_decorator
    
    # Load modules
    pizza_spec = importlib.util.spec_from_file_location(
        "structural.decorator.pizza",
        test_dir / "pizza.py"
    )
    pizza_module = importlib.util.module_from_spec(pizza_spec)
    sys.modules["structural.decorator.pizza"] = pizza_module
    structural_decorator.pizza = pizza_module
    pizza_spec.loader.exec_module(pizza_module)
    
    pizzas_spec = importlib.util.spec_from_file_location(
        "structural.decorator.pizzas_concretas",
        test_dir / "pizzas_concretas.py"
    )
    pizzas_module = importlib.util.module_from_spec(pizzas_spec)
    sys.modules["structural.decorator.pizzas_concretas"] = pizzas_module
    structural_decorator.pizzas_concretas = pizzas_module
    pizzas_spec.loader.exec_module(pizzas_module)
    
    topping_decorator_spec = importlib.util.spec_from_file_location(
        "structural.decorator.topping_decorator",
        test_dir / "topping_decorator.py"
    )
    topping_decorator_module = importlib.util.module_from_spec(topping_decorator_spec)
    sys.modules["structural.decorator.topping_decorator"] = topping_decorator_module
    structural_decorator.topping_decorator = topping_decorator_module
    topping_decorator_spec.loader.exec_module(topping_decorator_module)
    
    concrete_toppings_spec = importlib.util.spec_from_file_location(
        "structural.decorator.concrete_toppings",
        test_dir / "concrete_toppings.py"
    )
    concrete_toppings_module = importlib.util.module_from_spec(concrete_toppings_spec)
    sys.modules["structural.decorator.concrete_toppings"] = concrete_toppings_module
    structural_decorator.concrete_toppings = concrete_toppings_module
    concrete_toppings_spec.loader.exec_module(concrete_toppings_module)
    
    # Extract classes
    Pizza = pizza_module.Pizza
    ChickenPizza = pizzas_module.ChickenPizza
    PepperoniPizza = pizzas_module.PepperoniPizza
    CheesePizza = pizzas_module.CheesePizza
    ToppingDecorator = topping_decorator_module.ToppingDecorator
    StuffedCrust = concrete_toppings_module.StuffedCrust
    WholeWheatCrust = concrete_toppings_module.WholeWheatCrust


def test_chicken_pizza_base():
    """Test base chicken pizza without decorations."""
    pizza = ChickenPizza()
    
    assert pizza.get_price() == 19.00
    assert "chicken" in pizza.get_description().lower()
    
    print("[OK] Test Chicken Pizza Base: PASSED")


def test_pepperoni_pizza_base():
    """Test base pepperoni pizza without decorations."""
    pizza = PepperoniPizza()
    
    assert pizza.get_price() == 25.00
    assert "pepperoni" in pizza.get_description().lower()
    
    print("[OK] Test Pepperoni Pizza Base: PASSED")


def test_cheese_pizza_base():
    """Test base cheese pizza without decorations."""
    pizza = CheesePizza()
    
    assert pizza.get_price() == 22.00
    assert "cheese" in pizza.get_description().lower()
    
    print("[OK] Test Cheese Pizza Base: PASSED")


def test_single_decorator():
    """Test pizza with single decorator."""
    pizza = ChickenPizza()
    decorated = StuffedCrust(pizza)
    
    assert decorated.get_price() == 19.00 + 8.50
    assert "stuffed crust" in decorated.get_description().lower()
    
    print("[OK] Test Single Decorator: PASSED")


def test_multiple_decorators():
    """Test pizza with multiple decorators (chaining)."""
    pizza = PepperoniPizza()
    with_stuffed = StuffedCrust(pizza)
    with_wheat = WholeWheatCrust(with_stuffed)
    
    # Price should be: 25.00 + 8.50 + 5.00 = 38.50
    assert with_wheat.get_price() == 38.50
    assert "pepperoni" in with_wheat.get_description().lower()
    assert "stuffed crust" in with_wheat.get_description().lower()
    assert "whole wheat" in with_wheat.get_description().lower()
    
    print("[OK] Test Multiple Decorators: PASSED")


def test_decorator_order_matters():
    """Test that decorator order affects description but not price."""
    pizza = CheesePizza()
    
    # Order 1: Stuffed then Wheat
    order1 = WholeWheatCrust(StuffedCrust(pizza))
    
    # Order 2: Wheat then Stuffed
    order2 = StuffedCrust(WholeWheatCrust(pizza))
    
    # Price should be the same
    assert order1.get_price() == order2.get_price()
    assert order1.get_price() == 22.00 + 8.50 + 5.00
    
    # But descriptions might differ in order
    assert "stuffed" in order1.get_description().lower()
    assert "whole wheat" in order1.get_description().lower()
    
    print("[OK] Test Decorator Order Matters: PASSED")


def test_stuffed_crust_price():
    """Test StuffedCrust decorator price."""
    pizza = ChickenPizza()
    decorated = StuffedCrust(pizza)
    
    assert decorated.get_price() == 19.00 + 8.50
    
    print("[OK] Test Stuffed Crust Price: PASSED")


def test_whole_wheat_crust_price():
    """Test WholeWheatCrust decorator price."""
    pizza = PepperoniPizza()
    decorated = WholeWheatCrust(pizza)
    
    assert decorated.get_price() == 25.00 + 5.00
    
    print("[OK] Test Whole Wheat Crust Price: PASSED")


def test_decorator_implements_pizza_interface():
    """Test that decorators implement Pizza interface."""
    pizza = ChickenPizza()
    stuffed = StuffedCrust(pizza)
    wheat = WholeWheatCrust(pizza)
    
    assert isinstance(stuffed, Pizza)
    assert isinstance(wheat, Pizza)
    assert isinstance(stuffed, ToppingDecorator)
    assert isinstance(wheat, ToppingDecorator)
    
    print("[OK] Test Decorator Implements Pizza Interface: PASSED")


def test_decorator_wraps_another_decorator():
    """Test that decorators can wrap other decorators."""
    pizza = CheesePizza()
    first_decorator = StuffedCrust(pizza)
    second_decorator = WholeWheatCrust(first_decorator)
    
    assert isinstance(second_decorator.pizza, StuffedCrust)
    assert second_decorator.get_price() == 22.00 + 8.50 + 5.00
    
    print("[OK] Test Decorator Wraps Another Decorator: PASSED")


def test_all_pizza_types_with_decorators():
    """Test all pizza types with decorators."""
    pizzas = [ChickenPizza(), PepperoniPizza(), CheesePizza()]
    
    for pizza in pizzas:
        decorated = StuffedCrust(pizza)
        base_price = pizza.get_price()
        decorated_price = decorated.get_price()
        
        assert decorated_price == base_price + 8.50
        assert "stuffed crust" in decorated.get_description().lower()
    
    print("[OK] Test All Pizza Types With Decorators: PASSED")


def test_decorator_description_format():
    """Test decorator description format."""
    pizza = ChickenPizza()
    decorated = StuffedCrust(pizza)
    
    description = decorated.get_description()
    assert pizza.get_description() in description
    assert "Stuffed crust" in description or "stuffed crust" in description
    
    print("[OK] Test Decorator Description Format: PASSED")


def test_multiple_same_decorator():
    """Test applying same decorator multiple times."""
    pizza = PepperoniPizza()
    first = StuffedCrust(pizza)
    second = StuffedCrust(first)
    
    # Should add price twice
    assert second.get_price() == 25.00 + 8.50 + 8.50
    assert second.get_description().count("stuffed") >= 2 or second.get_description().count("Stuffed") >= 2
    
    print("[OK] Test Multiple Same Decorator: PASSED")


def test_decorator_price_calculation():
    """Test decorator price calculation is additive."""
    pizza = CheesePizza()
    
    # Base price
    base_price = pizza.get_price()
    assert base_price == 22.00
    
    # With one decorator
    with_one = StuffedCrust(pizza)
    assert with_one.get_price() == base_price + 8.50
    
    # With two decorators
    with_two = WholeWheatCrust(StuffedCrust(pizza))
    assert with_two.get_price() == base_price + 8.50 + 5.00
    
    print("[OK] Test Decorator Price Calculation: PASSED")


def test_decorator_chain_length():
    """Test decorator chain of different lengths."""
    pizza = ChickenPizza()
    
    # No decorators
    assert pizza.get_price() == 19.00
    
    # One decorator
    one = StuffedCrust(pizza)
    assert one.get_price() == 27.50
    
    # Two decorators
    two = WholeWheatCrust(StuffedCrust(pizza))
    assert two.get_price() == 32.50
    
    print("[OK] Test Decorator Chain Length: PASSED")


def test_pizza_base_prices():
    """Test that base pizza prices are correct."""
    chicken = ChickenPizza()
    pepperoni = PepperoniPizza()
    cheese = CheesePizza()
    
    assert chicken.get_price() == 19.00
    assert pepperoni.get_price() == 25.00
    assert cheese.get_price() == 22.00
    
    print("[OK] Test Pizza Base Prices: PASSED")


def test_topping_prices():
    """Test that topping prices are correct."""
    pizza = ChickenPizza()
    
    stuffed = StuffedCrust(pizza)
    assert stuffed.get_price() - pizza.get_price() == 8.50
    
    wheat = WholeWheatCrust(pizza)
    assert wheat.get_price() - pizza.get_price() == 5.00
    
    print("[OK] Test Topping Prices: PASSED")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("RUNNING DECORATOR PATTERN TESTS")
    print("=" * 60 + "\n")

    try:
        test_chicken_pizza_base()
        test_pepperoni_pizza_base()
        test_cheese_pizza_base()
        test_single_decorator()
        test_multiple_decorators()
        test_decorator_order_matters()
        test_stuffed_crust_price()
        test_whole_wheat_crust_price()
        test_decorator_implements_pizza_interface()
        test_decorator_wraps_another_decorator()
        test_all_pizza_types_with_decorators()
        test_decorator_description_format()
        test_multiple_same_decorator()
        test_decorator_price_calculation()
        test_decorator_chain_length()
        test_pizza_base_prices()
        test_topping_prices()

        print("\n" + "=" * 60)
        print("ALL TESTS PASSED! [OK]")
        print("=" * 60 + "\n")

    except AssertionError as e:
        print(f"\n[ERROR] TEST FAILED: {e}\n")
        import traceback
        traceback.print_exc()
    except Exception as e:
        print(f"\n[ERROR] ERROR: {e}\n")
        import traceback
        traceback.print_exc()

