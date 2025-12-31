from abc import ABC, abstractmethod


class Observer(ABC):
    """
    Interface Observer: Define uma interface de atualização para objetos
    que devem ser notificados sobre alterações em um Subject.

    Todos os observadores devem implementar o método update() para
    receber notificações do Subject.
    """

    @abstractmethod
    def update(self, mensagem: str) -> None:
        """
        Método chamado pelo Subject para notificar o Observer
        sobre uma mudança de estado.

        Args:
            mensagem: Mensagem/notificação enviada pelo Subject
        """
        pass

    @abstractmethod
    def get_nome(self) -> str:
        """Retorna o nome do observador"""
        pass

    @abstractmethod
    def get_email(self) -> str:
        """Retorna o email do observador"""
        pass
