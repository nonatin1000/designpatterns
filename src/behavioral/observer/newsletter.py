from typing import List
from subject_interface import Subject
from observer_interface import Observer


class Newsletter(Subject):
    """
    ConcreteSubject: Newsletter que notifica observers sobre novas mensagens.

    Implementa a interface Subject, mantendo uma lista de observers
    e notificando-os automaticamente quando uma nova mensagem é adicionada.
    """

    def __init__(self):
        """Inicializa a newsletter com listas vazias de observers e mensagens"""
        self._observers: List[Observer] = []
        self._mensagens: List[str] = []

    def register_observer(self, observer: Observer) -> None:
        """
        Adiciona um observer à lista de objetos a serem notificados.

        Args:
            observer: O observador a ser registrado
        """
        if observer not in self._observers:
            self._observers.append(observer)
            print(f"[NEWSLETTER] {observer.get_nome()} foi inscrito na newsletter")
        else:
            print(f"[NEWSLETTER] {observer.get_nome()} já está inscrito")

    def remove_observer(self, observer: Observer) -> None:
        """
        Remove um observer da lista de objetos a serem notificados.

        Args:
            observer: O observador a ser removido
        """
        if observer in self._observers:
            self._observers.remove(observer)
            print(f"[NEWSLETTER] {observer.get_nome()} cancelou a inscrição")
        else:
            print(f"[NEWSLETTER] {observer.get_nome()} não está inscrito")

    def notify_observers(self) -> None:
        """
        Notifica todos os observers sobre a nova mensagem da newsletter.

        Este método é chamado automaticamente quando uma nova mensagem
        é adicionada à newsletter.
        """
        if not self._mensagens:
            print("[NEWSLETTER] Nenhuma mensagem para notificar")
            return

        ultima_mensagem = self._mensagens[-1]
        print(f"\n[NEWSLETTER] Notificando {len(self._observers)} assinante(s)...")
        print(f"[NEWSLETTER] Mensagem: {ultima_mensagem}\n")

        for observer in self._observers:
            observer.update(ultima_mensagem)

    def add_mensagem(self, mensagem: str) -> None:
        """
        Adiciona uma nova mensagem à newsletter e notifica todos os observers.

        Args:
            mensagem: Conteúdo da mensagem a ser enviada
        """
        print(f"\n{'=' * 80}")
        print(f"[NEWSLETTER] Nova mensagem publicada!")
        print(f"{'=' * 80}")

        self._mensagens.append(mensagem)
        self.notify_observers()

    def get_mensagens(self) -> List[str]:
        """Retorna todas as mensagens publicadas"""
        return self._mensagens.copy()

    def get_total_assinantes(self) -> int:
        """Retorna o número total de assinantes"""
        return len(self._observers)

    def get_assinantes(self) -> List[dict]:
        """
        Retorna informações dos assinantes.

        Returns:
            Lista de dicts com nome e email dos assinantes
        """
        return [
            {
                "nome": obs.get_nome(),
                "email": obs.get_email()
            }
            for obs in self._observers
        ]
