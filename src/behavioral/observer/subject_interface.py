from abc import ABC, abstractmethod
from observer_interface import Observer


class Subject(ABC):
    """
    Interface Subject: Define a interface para objetos que podem ser observados.

    Um Subject deve ser capaz de:
    - Adicionar observers à sua lista de objetos a serem notificados
    - Remover observers de sua lista
    - Notificar todos os observers registrados sobre mudanças de estado
    """

    @abstractmethod
    def register_observer(self, observer: Observer) -> None:
        """
        Registra um observer para receber notificações.

        Args:
            observer: O observador a ser registrado
        """
        pass

    @abstractmethod
    def remove_observer(self, observer: Observer) -> None:
        """
        Remove um observer da lista de notificações.

        Args:
            observer: O observador a ser removido
        """
        pass

    @abstractmethod
    def notify_observers(self) -> None:
        """
        Notifica todos os observers registrados sobre uma mudança de estado.
        """
        pass
