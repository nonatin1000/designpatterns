"""Decorator Pattern - Pizzeria System.

The Decorator pattern attaches additional responsibilities to objects dynamically.
Decorators provide a flexible alternative to subclassing for extending functionality.

This implementation demonstrates the Decorator pattern using a pizzeria system
where pizzas can be decorated with toppings at runtime without modifying the
original pizza classes.

Pattern Structure:
- Component (Pizza): Base interface for pizzas and decorators
- ConcreteComponent (ChickenPizza, PepperoniPizza, CheesePizza): Base pizzas
- Decorator (ToppingDecorator): Abstract base for all toppings
- ConcreteDecorator (StuffedCrust, WholeWheatCrust): Specific toppings
"""

from .pizza import Pizza
from .pizzas_concretas import ChickenPizza, PepperoniPizza, CheesePizza
from .topping_decorator import ToppingDecorator
from .concrete_toppings import StuffedCrust, WholeWheatCrust

__all__ = [
    # Component interface
    "Pizza",
    # Concrete components (base pizzas)
    "ChickenPizza",
    "PepperoniPizza",
    "CheesePizza",
    # Decorator base
    "ToppingDecorator",
    # Concrete decorators (toppings)
    "StuffedCrust",
    "WholeWheatCrust",
]
