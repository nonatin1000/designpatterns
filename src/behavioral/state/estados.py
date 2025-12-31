from state_interface import State
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pedido import Pedido


class AguardandoPagamentoState(State):
    """ConcreteState: Estado inicial do pedido aguardando pagamento"""

    def __init__(self, pedido: 'Pedido'):
        self.pedido = pedido

    def sucesso_ao_pagar(self) -> None:
        """Transição válida: Aguardando Pagamento -> Pago"""
        print(f"[TRANSICAO] Pagamento confirmado! Pedido #{self.pedido.id_pedido} está PAGO")
        self.pedido.set_estado_atual(self.pedido.get_pago())

    def cancelar_pedido(self) -> None:
        """Transição válida: Aguardando Pagamento -> Cancelado"""
        print(f"[TRANSICAO] Cancelando pedido #{self.pedido.id_pedido} antes do pagamento")
        self.pedido.set_estado_atual(self.pedido.get_cancelado())

    def despachar_pedido(self) -> None:
        """Transição inválida neste estado"""
        raise Exception("Operacao nao suportada: o pedido ainda nao foi pago.")

    def get_nome_estado(self) -> str:
        return "Aguardando Pagamento"


class PagoState(State):
    """ConcreteState: Pedido foi pago"""

    def __init__(self, pedido: 'Pedido'):
        self.pedido = pedido

    def sucesso_ao_pagar(self) -> None:
        """Transição inválida neste estado"""
        raise Exception("Operacao nao suportada: o pedido ja foi pago.")

    def cancelar_pedido(self) -> None:
        """Transição válida: Pago -> Cancelado"""
        print(f"[TRANSICAO] Cancelando pedido #{self.pedido.id_pedido} apos pagamento")
        self.pedido.set_estado_atual(self.pedido.get_cancelado())

    def despachar_pedido(self) -> None:
        """Transição válida: Pago -> Enviado"""
        print(f"[TRANSICAO] Despachando pedido #{self.pedido.id_pedido} para envio")
        self.pedido.set_estado_atual(self.pedido.get_enviado())

    def get_nome_estado(self) -> str:
        return "Pago"


class CanceladoState(State):
    """ConcreteState: Pedido foi cancelado (estado final)"""

    def __init__(self, pedido: 'Pedido'):
        self.pedido = pedido

    def sucesso_ao_pagar(self) -> None:
        """Transição inválida neste estado"""
        raise Exception("Operacao nao suportada: o pedido se encontra cancelado.")

    def cancelar_pedido(self) -> None:
        """Transição inválida neste estado"""
        raise Exception("Operacao nao suportada: pedido ja cancelado.")

    def despachar_pedido(self) -> None:
        """Transição inválida neste estado"""
        raise Exception("Operacao nao suportada: o pedido se encontra cancelado.")

    def get_nome_estado(self) -> str:
        return "Cancelado"


class EnviadoState(State):
    """ConcreteState: Pedido foi enviado (estado final)"""

    def __init__(self, pedido: 'Pedido'):
        self.pedido = pedido

    def sucesso_ao_pagar(self) -> None:
        """Transição inválida neste estado"""
        raise Exception("Operacao nao suportada: o pedido ja foi pago e enviado.")

    def cancelar_pedido(self) -> None:
        """Transição inválida neste estado"""
        raise Exception("Operacao nao suportada: o pedido ja foi enviado.")

    def despachar_pedido(self) -> None:
        """Transição inválida neste estado"""
        raise Exception("Operacao nao suportada: o pedido ja foi enviado.")

    def get_nome_estado(self) -> str:
        return "Enviado"
