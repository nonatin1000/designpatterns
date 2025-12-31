"""
Padrão State - Sistema de Pedidos E-commerce

O padrão State permite que um objeto altere seu comportamento quando
seu estado interno muda. O objeto parecerá ter mudado de classe.
"""

from .state_interface import State
from .estados import AguardandoPagamentoState, PagoState, CanceladoState, EnviadoState
from .pedido import Pedido

__all__ = [
    "State",
    "AguardandoPagamentoState",
    "PagoState",
    "CanceladoState",
    "EnviadoState",
    "Pedido",
]
