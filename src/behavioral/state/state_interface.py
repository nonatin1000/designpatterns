from abc import ABC, abstractmethod


class State(ABC):
    """
    Interface State: Define interface comum para todos os estados concretos.

    Cada estado implementa seu próprio comportamento para as transições,
    permitindo que o objeto de contexto (Pedido) delegue o processamento
    das solicitações para o estado atual.
    """

    @abstractmethod
    def sucesso_ao_pagar(self) -> None:
        """
        Transição: Sucesso ao Pagar
        Processa pagamento bem-sucedido do pedido
        """
        pass

    @abstractmethod
    def cancelar_pedido(self) -> None:
        """
        Transição: Cancelar Pedido
        Processa cancelamento do pedido
        """
        pass

    @abstractmethod
    def despachar_pedido(self) -> None:
        """
        Transição: Despachar Pedido
        Processa envio do pedido
        """
        pass

    @abstractmethod
    def get_nome_estado(self) -> str:
        """Retorna o nome do estado atual"""
        pass
