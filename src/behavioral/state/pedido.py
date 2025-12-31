from state_interface import State
from estados import AguardandoPagamentoState, PagoState, CanceladoState, EnviadoState
from typing import List
from datetime import datetime


class Pedido:
    """
    Context: Classe que pode ter vários estados internos diferentes.

    Mantém referência aos objetos de estado e delega as solicitações
    para o estado atual. O comportamento muda conforme o estado interno.
    """

    _contador_id = 0  # Contador estático para IDs únicos

    def __init__(self, itens: List[str] = None, valor_total: float = 0.0):
        """
        Inicializa o pedido com todos os estados possíveis
        e define o estado inicial como AguardandoPagamento
        """
        # Gera ID único
        Pedido._contador_id += 1
        self.id_pedido = Pedido._contador_id

        # Dados do pedido
        self.itens = itens or []
        self.valor_total = valor_total
        self.data_criacao = datetime.now()
        self.historico_estados: List[str] = []

        # Criação de todos os estados possíveis
        self._aguardando_pagamento = AguardandoPagamentoState(self)
        self._pago = PagoState(self)
        self._cancelado = CanceladoState(self)
        self._enviado = EnviadoState(self)

        # Define estado inicial
        self._estado_atual = self._aguardando_pagamento
        self._registrar_mudanca_estado("Aguardando Pagamento")

        print(f"[PEDIDO] Novo pedido #{self.id_pedido} criado - Estado: {self.get_estado_nome()}")

    def sucesso_ao_pagar(self) -> None:
        """
        Delega a transição de pagamento para o estado atual.
        O comportamento depende do estado em que o pedido se encontra.
        """
        try:
            self._estado_atual.sucesso_ao_pagar()
        except Exception as e:
            print(f"[ERRO] {str(e)}")
            raise

    def cancelar_pedido(self) -> None:
        """
        Delega o cancelamento para o estado atual.
        O comportamento depende do estado em que o pedido se encontra.
        """
        try:
            self._estado_atual.cancelar_pedido()
        except Exception as e:
            print(f"[ERRO] {str(e)}")
            raise

    def despachar_pedido(self) -> None:
        """
        Delega o despacho para o estado atual.
        O comportamento depende do estado em que o pedido se encontra.
        """
        try:
            self._estado_atual.despachar_pedido()
        except Exception as e:
            print(f"[ERRO] {str(e)}")
            raise

    # Getters para os estados (permitem que estados concretos façam transições)

    def get_aguardando_pagamento(self) -> State:
        return self._aguardando_pagamento

    def get_pago(self) -> State:
        return self._pago

    def get_cancelado(self) -> State:
        return self._cancelado

    def get_enviado(self) -> State:
        return self._enviado

    # Setter para mudança de estado

    def set_estado_atual(self, estado: State) -> None:
        """Muda o estado atual do pedido"""
        self._estado_atual = estado
        self._registrar_mudanca_estado(estado.get_nome_estado())

    def get_estado_atual(self) -> State:
        """Retorna o estado atual"""
        return self._estado_atual

    def get_estado_nome(self) -> str:
        """Retorna o nome do estado atual"""
        return self._estado_atual.get_nome_estado()

    def _registrar_mudanca_estado(self, nome_estado: str) -> None:
        """Registra mudança de estado no histórico"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.historico_estados.append(f"{timestamp} - {nome_estado}")

    def get_historico(self) -> List[str]:
        """Retorna histórico de mudanças de estado"""
        return self.historico_estados.copy()

    def get_info(self) -> dict:
        """Retorna informações completas do pedido"""
        return {
            "id": self.id_pedido,
            "itens": self.itens,
            "valor_total": self.valor_total,
            "estado_atual": self.get_estado_nome(),
            "data_criacao": self.data_criacao.strftime("%Y-%m-%d %H:%M:%S"),
            "historico": self.historico_estados
        }

    def __str__(self) -> str:
        return f"Pedido #{self.id_pedido} - Estado: {self.get_estado_nome()} - Valor: R$ {self.valor_total:.2f}"
