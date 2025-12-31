"""
Padrão Decorator - Sistema de Pizzaria

O padrão Decorator anexa responsabilidades adicionais a um objeto dinamicamente.
Os Decorators fornecem uma alternativa flexível ao uso de subclasses para
extensão de funcionalidades.
"""

from .pizza import Pizza
from .pizzas_concretas import PizzaFrango, PizzaCalabresa, PizzaQueijo
from .acrescimo_decorator import AcrescimoDecorator
from .decorators_concretos import BordaRequeijao, MassaIntegral

__all__ = [
    "Pizza",
    "PizzaFrango",
    "PizzaCalabresa",
    "PizzaQueijo",
    "AcrescimoDecorator",
    "BordaRequeijao",
    "MassaIntegral",
]
